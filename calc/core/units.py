# -*- coding: utf-8 -*-
"""
A parser for units. Converts string representation into PySpice unit

Examples of valid notations include:
    1,234.56kΩ
    1k234
    1k234Ω
    1,234.56Ω
    4µA
    4e6A
    4e6nA

Usage example:
    >>> print(normalize_engineer_notation("1µ234 Ω"))
    (1.234e-6, 'Ω')

Based on code published at techoverflow.net.
"""
import math
import itertools
import numpy as np
from PySpice.Unit import *


class Parser(object):
    instance = None
    NUM_CHARACTERS = frozenset("0123456789-e.")
    UNITS = [['F'], ['A'], ['Ω', 'Ohm', 'R'], ['W'], ['H'], ['C'], ['K'],
             ['Hz'], ['V'], ['J'], ['S']]

    PYSPICE_UNIT_MAP = {'F': u_F, 'A': u_A, 'Ω': u_Ohm, 'Ohm': u_Ohm, 'R': u_Ohm,
                        'W': u_W, 'H': u_H, 'C': u_C, 'K': u_K, 'Hz': u_Hz, 'V': u_V,
                        'J': u_J, 'S': u_S}

    UNIT_PREFIXES = "Δ°"
    SUFFICES = [["y"], ["z"], ["a"], ["f"], ["p"], ["n"], ["µ", "u"], ["m"], ['', 'R'],
                ["k"], ["M"], ["G"], ["T"], ["E"], ["Z"], ["Y"]]
    FIRST_SUFFIX_EXP = -24

    def __init__(self):
        # Unit prefixes will only be used in strip, so we can strip spaces in one go.
        self.strippable = Parser.UNIT_PREFIXES + " \t\n"
        # Compute maps
        self.all_suffixes = set(itertools.chain(*Parser.SUFFICES))
        self.all_units = set(itertools.chain(*Parser.UNITS))

        self.exp_suffix_map = {}  # Key: exp // 3, Value: suffix
        self.suffix_exp_map = {}  # Key: suffix, value: exponent
        self.exp_map_min = None
        self.exp_map_max = None

        self._recompute_suffix_maps()

    def _recompute_suffix_maps(self):
        """
        Recompute the exponent -> suffix map and
        the suffix -> exponent map
        """
        # Compute inverse suffix map
        current_exp = Parser.FIRST_SUFFIX_EXP
        # Iterate over first suffices in each list
        for current_suffices in Parser.SUFFICES:
            if not current_suffices:
                self.exp_suffix_map[current_exp // 3] = ""
                current_exp += 3
                continue
            # Compute exponent -> suffix (only first suffix)
            self.exp_suffix_map[current_exp // 3] = current_suffices[0]
            # Compute suffix -> exponent
            for current_suffix in current_suffices:
                self.suffix_exp_map[current_suffix] = current_exp
            current_exp += 3
        # Compute min/max SI value
        self.exp_map_min = min(self.exp_suffix_map.keys())
        self.exp_map_max = max(self.exp_suffix_map.keys())

    def split_input(self, s):
        """
        Separate a string into a 3-tuple (number, suffix, unit).
        returns None if the string could not be parsed.

        The tuple will never contain None but empty strings if some
        element is not present. The number must be present for the string
        to be considered valid.

        Units always need to be a suffix. Instead
        Thousands separators or commata instead of points may be used
        (see _normalize_interpunctation documentation).

        Thousands separators and suffix-as-decimal-separators may NOT
        be mixed. Whitespace is removed automatically.
        """
        # Remove thousands separator & ensure dot is used
        s = Parser._normalize_interpunctation(s).replace(" ", "")

        s, u = self.split_unit(s)

        if not s:
            raise ValueError("Can't split empty string")

        # Try to find SI suffix at the end or in the middle
        if s[-1] in self.all_suffixes:
            s, suffix = s[:-1], s[-1]
        else:  # Try to find unit anywhere
            suffix_list = [ch in self.all_suffixes for ch in s]
            suffix_count = sum(suffix_list)
            
            if suffix_count > 1:
                raise ValueError("More than one SI suffix in the string")
            elif suffix_count == 0:
                suffix = ""
            else:
                # Suffix-as-decimal-separator --> there must be no other decimal separator
                if "." in s:
                    raise ValueError("Suffix as decimal separator, but dot is also in string: {0}".format(s))
                suffix_index = suffix_list.index(True)
                # Suffix must NOT be first character
                if suffix_index == 0:
                    raise ValueError("Suffix in '{0}' must not be the first char".format(s))
                suffix = s[suffix_index]
                s = s.replace(suffix, ".")
        # Handle unit prefix (if any). Not allowable if no unit is present
        s = s.strip(self.strippable)
        # Final check: Is there any number left and is it valid?
        if not all((ch in Parser.NUM_CHARACTERS for ch in s)):
            raise ValueError("Remainder of string is not purely numeric: {0}".format(s))

        # special case for R (R can be suffix, then the unit is implicitly R
        if u == "" and suffix == 'R':
            u = 'R'
        return s, suffix, u

    def split_unit(self, s):
        """
        Split a string into (remainder, unit).
        Only units in the units set are recognized
        unit may be "None" if no unit is recognized
        """
        # Fallback for strings which are too short
        if len(s) <= 1:
            return s, ""
        if s[-3:] in self.all_units:
            s, u = s[:-3], s[-3:]
        elif s[-2:] in self.all_units:
            s, u = s[:-2], s[-2:]
        elif s[-1] in self.all_units:
            s, u = s[:-1], s[-1]
        else:
            s, u = s, ''
        # Remove unit prefix, if any (e.g. degrees symbol, delta symbol)
        s = s.rstrip(self.strippable)
        return s, u

    def normalize(self, s, encoding="utf8"):
        """
        Converts an engineer's input of a wide variety of formats to a numeric
        value.

        Returns a pair (number, unit) or None if the conversion could not be performed.

        See splitSuffixSeparator() for further details on supported formats
        """
        # Scalars get returned directly
        if isinstance(s, (int, float, np.generic)):
            return s, ''
        # Make sure it's a decoded string
        if isinstance(s, bytes):
            s = s.decode(encoding)
        # Handle lists / array
        if isinstance(s, (list, tuple, np.ndarray)):
            return [self.normalize(elem) for elem in s]
        # Perform splitting
        num, suffix, u = self.split_input(s.strip())
        mul = (10 ** self.suffix_exp_map[suffix]) if suffix else 1
        return float(num) * mul, u

    def normalize_pyspice(self, s, encoding='utf8'):
        num, u = self.normalize(s, encoding)
        pyspice_u = Parser.PYSPICE_UNIT_MAP.get(u, None)
        if pyspice_u is None:
            raise ValueError('Cannot find corresponding PySpice unit')

        return num, pyspice_u(num)

    def format(self, v, unit_symbol=""):
        """
        Format v using SI suffices with optional units.
        Produces a string with 3 visible digits.
        """
        # Suffix map is indexed by one third of the decadic logarithm.
        exp = 0 if v == 0. else math.log(abs(v), 10.)
        suffixMapIdx = int(math.floor(exp / 3.))
        # Ensure we're in range
        if not self.exp_map_min < suffixMapIdx < self.exp_map_max:
            raise ValueError("Value out of range: {0}".format(v))
        # Pre-multiply the value
        v = v * (10.0 ** -(suffixMapIdx * 3))
        # Delegate the rest of the task to the helper
        return _formatWithSuffix(v, self.exp_suffix_map[suffixMapIdx] + unit_symbol)

    def auto_suffix_1d(self, arr):
        """
        Takes an array of arbitrary values and determines
        what is the best suffix (e.g. M, m, n, f) to represent
        as many values as possible with as few powers of 10 as possible.

        Returns a tuple (factor, suffix) where the factor is a floating-point
        value to multiply the array with to obtain value with "suffix" suffix.
        """
        # Compute logarithmic magnitudes of data
        arr_log = np.log10(np.abs(arr))
        arr_log[np.isinf(arr_log)] = 0  # log(0) == inf
        log_mean = arr_log.mean()
        # Generate score matrix
        suffix_idx = int(round(log_mean / 3))
        # Ensure we're in range
        suffix_idx = max(self.exp_map_min, suffix_idx)
        suffix_idx = min(self.exp_map_max, suffix_idx)
        # Pre-multiply the value
        multiplier = 10.0 ** -(suffix_idx * 3)
        return multiplier, self.exp_suffix_map[suffix_idx]

    @staticmethod
    def _normalize_interpunctation(s):
        """
        Normalize comma to point for float conversion.
        Correctly handles thousands separators.

        Note that cases like "1,234" will be treated as "1.234".
        """
        comma_idx = s.find(",")
        point_idx = s.find(".")
        found_comma = comma_idx is not None
        found_point = point_idx is not None
        comma_first = comma_idx < point_idx if (found_comma and found_point) else None

        if found_comma and found_point:
            if comma_first:
                # Comma first => comma used as thousands separators
                return s.replace(",", "")
            else:
                # Dot first => dot used as thousands separator
                return s.replace(".", "").replace(",", ".")
        elif found_comma:
            return s.replace(",", ".")
        else:
            return s


# Initialize global instance
Parser.instance = Parser()


def _formatWithSuffix(v, suffix=""):
    """
    Format a given value with a given suffix.
    This helper function formats the value to 3 visible digits.
    v must be pre-multiplied by the factor implied by the suffix
    """
    if v < 10.0:
        res = "{:.2f}".format(v)
    elif v < 100.0:
        res = "{:.1f}".format(v)
    else:  # Should only happen if v < 1000
        res = str(int(round(v)))
    # Avoid appending whitespace if there is no suffix
    return "{0} {1}".format(res, suffix) if suffix else res


def normalize_engineer_notation(s, encoding="utf8"):
    return Parser.instance.normalize(s)


def format_value(v, unit=""):
    return Parser.instance.format(v, unit)


def normalize_engineer_notation_safe(v, unit=""):
    return Parser.instance.safe_normalize(v, unit)


def normalize_numeric(v):
    return Parser.instance.normalize_numeric(v)


def auto_format(v, *args, **kwargs):
    return Parser.instance.auto_format(v, *args, **kwargs)
