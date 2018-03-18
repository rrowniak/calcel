#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from core import units
from core.units import AllUnits as U


def calc_f(u1, u2):
    lc = u1[0]
    cl = u2[0]
    return 1.0 / (2*np.pi * np.sqrt(lc*cl)), U.Hz


def calc_c(u1, u2):
    if u1[1] == U.Hz:
        f = u1[0]
        l = u2[0]
    else:
        f = u2[0]
        l = u1[0]
    return 1.0 / (np.square(2*np.pi*f) * l), U.F


def calc_l(u1, u2):
    if u1[1] == U.Hz:
        f = u1[0]
        c = u2[0]
    else:
        f = u2[0]
        c = u1[0]
    return 1.0 / (np.square(2*np.pi*f) * c), U.H


SELECTOR = {
    (U.H, U.F): calc_f,
    (U.F, U.H): calc_f,
    (U.H, U.Hz): calc_c,
    (U.Hz, U.H): calc_c,
    (U.Hz, U.F): calc_l,
    (U.F, U.Hz): calc_l
}


def play(u1, u2):
    u1 = U.convert_to_canonical(u1)
    u2 = U.convert_to_canonical(u2)
    return SELECTOR[(u1[1], u2[1])](u1, u2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = """
Calculate a resonant frequency of LC circuit using the following formula: f=1/(2pi*sqrt(LC))
    """
    parser.add_argument("arg1", help='It can be any of these three units: Hz, F or H')
    parser.add_argument("arg2", help='It can be any of these three units: Hz, F or H')
    args = parser.parse_args()

    arg1 = units.parse(args.arg1)
    arg2 = units.parse(args.arg2)

    res = play(arg1, arg2)
    msg = units.format_verbose(res[0], res[1])
    print(msg)
