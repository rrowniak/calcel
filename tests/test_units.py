import unittest
from calc.core import units


class UnitsTestCase(unittest.TestCase):
    def test1_parser_split_input(self):
        p = units.Parser.instance

        s, suffix, u = p.split_input("1kR")
        self.assertEqual('1', s)
        self.assertEqual('k', suffix)
        self.assertEqual('R', u)

        s, suffix, u = p.split_input("1R")
        self.assertEqual('1', s)
        self.assertEqual('', suffix)
        self.assertEqual('R', u)

        s, suffix, u = p.split_input("1R2")
        self.assertEqual('1.2', s)
        self.assertEqual('R', suffix)
        self.assertEqual('R', u)

        s, suffix, u = p.split_input("2mV")
        self.assertEqual('2', s)
        self.assertEqual('m', suffix)
        self.assertEqual('V', u)

    def test2_parser_normalize(self):
        p = units.Parser.instance

        n, u = p.normalize('1kR')
        self.assertEqual(1000.0, n)
        self.assertEqual('R', u)

        n, u = p.normalize('1R')
        self.assertEqual(1.0, n)
        self.assertEqual('R', u)

        n, u = p.normalize('1R2')
        self.assertEqual(1.2, n)
        self.assertEqual('R', u)

        n, u = p.normalize('2mV')
        self.assertEqual(0.002, n)
        self.assertEqual('V', u)

    def test2_parser_normalize_pyspice(self):
        p = units.Parser.instance

        n, pyspice_u = p.normalize_pyspice('1kR')
        self.assertEqual(1000.0, n)
        self.assertEqual('ohm', pyspice_u.unit.unit_name)
        self.assertEqual(1000.0, pyspice_u.value)

        n, pyspice_u = p.normalize_pyspice('1R')
        self.assertEqual(1.0, n)
        self.assertEqual('ohm', pyspice_u.unit.unit_name)
        self.assertEqual(1.0, pyspice_u.value)

        n, pyspice_u = p.normalize_pyspice('1R2')
        self.assertEqual(1.2, n)
        self.assertEqual('ohm', pyspice_u.unit.unit_name)
        self.assertEqual(1.2, pyspice_u.value)

        n, pyspice_u = p.normalize_pyspice('2mV')
        self.assertEqual(0.002, n)
        self.assertEqual('V', pyspice_u.unit.unit_suffix)
        self.assertEqual(0.002, pyspice_u.value)

    def test99_basic_units(self):
        r = units.normalize_engineer_notation('1k')
        self.assertEqual(r[0], 1000)


if __name__ == '__main__':
    unittest.main()
