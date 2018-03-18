#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from core import units
from core.units import AllUnits as U


def calc_xl(u1, u2):
    lf = u1[0]
    fl = u2[0]
    return 2 * np.pi * fl * lf, U.R


def calc_f(u1, u2):
    if u1[1] == U.H:
        l = u1[0]
        xl = u2[0]
    else:
        l = u2[0]
        xl = u1[0]
    return xl / (2 * np.pi * l), U.Hz


def calc_l(u1, u2):
    if u1[1] == U.Hz:
        f = u1[0]
        xl = u2[0]
    else:
        f = u2[0]
        xl = u1[0]
    return xl / (2 * np.pi * f), U.H


SELECTOR = {
    (U.H, U.R): calc_f,
    (U.R, U.H): calc_f,
    (U.H, U.Hz): calc_xl,
    (U.Hz, U.H): calc_xl,
    (U.Hz, U.R): calc_l,
    (U.R, U.Hz): calc_l
}


def play(u1, u2):
    u1 = U.convert_to_canonical(u1)
    u2 = U.convert_to_canonical(u2)
    return SELECTOR[(u1[1], u2[1])](u1, u2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = """
Calculate an inductive reactance using the following formula: Xl=2pi*f*L
    """
    parser.add_argument("arg1", help='It can be any of these three units: Hz, Ω or H')
    parser.add_argument("arg2", help='It can be any of these three units: Hz, Ω or H')
    args = parser.parse_args()

    arg1 = units.parse(args.arg1)
    arg2 = units.parse(args.arg2)

    res = play(arg1, arg2)
    msg = units.format_verbose(res[0], res[1])
    print(msg)
