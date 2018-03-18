#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from core import units
from core.units import AllUnits as U


def calc_xc(u1, u2):
    cf = u1[0]
    fc = u2[0]
    return 1 / (2 * np.pi * fc * cf), U.R


def calc_f(u1, u2):
    xcc = u1[0]
    cxc = u2[0]
    return 1 / (2 * np.pi * xcc * cxc), U.Hz


def calc_c(u1, u2):
    xcf = u1[0]
    fxc = u2[0]
    return 1 / (2 * np.pi * xcf * fxc), U.F


SELECTOR = {
    (U.F, U.R): calc_f,
    (U.R, U.F): calc_f,
    (U.F, U.Hz): calc_xc,
    (U.Hz, U.F): calc_xc,
    (U.Hz, U.R): calc_c,
    (U.R, U.Hz): calc_c
}


def play(u1, u2):
    u1 = U.convert_to_canonical(u1)
    u2 = U.convert_to_canonical(u2)
    return SELECTOR[(u1[1], u2[1])](u1, u2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = """
Calculate a capacitive reactance using the following formula: Xl= 1 / (2pi*f*C)
    """
    parser.add_argument("arg1", help='It can be any of these three units: Hz, Ω or F')
    parser.add_argument("arg2", help='It can be any of these three units: Hz, Ω or F')
    args = parser.parse_args()

    arg1 = units.parse(args.arg1)
    arg2 = units.parse(args.arg2)

    res = play(arg1, arg2)
    msg = units.format_verbose(res[0], res[1])
    print(msg)
