#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from core import units
from core.units import AllUnits as U


def calc_i(u1, u2):
    if u1[1] == U.V:
        v = u1
        r = u2
    else:
        v = u2
        r = u1
    return v[0] / r[0], U.A


def calc_r(u1, u2):
    if u1[1] == U.V:
        v = u1
        i = u2
    else:
        v = u2
        i = u1
    return v[0] / i[0], U.R


def calc_v(i, r):
    return i[0] * r[0], U.V


SELECTOR = {
    (U.R, U.V): calc_i,
    (U.V, U.R): calc_i,
    (U.V, U.A): calc_r,
    (U.A, U.V): calc_r,
    (U.A, U.R): calc_v,
    (U.R, U.A): calc_v
}


def play(u1, u2):
    u1 = U.convert_to_canonical(u1)
    u2 = U.convert_to_canonical(u2)
    return SELECTOR[(u1[1], u2[1])](u1, u2)


def calc_power(*arg):
    for a in arg:
        if a[1] == U.A:
            i = a[0]
            continue
        if a[1] == U.V:
            u = a[0]
            continue
    return u * i, U.W


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = """
Provide a pair of values of the following units: V, A or Ω and the program will calculate the result according
to the Ohm law: I = V/R. The resistance unit Ω can be omitted.
For example: ohm_law.py 10mA 4k7
    """
    parser.add_argument("arg1", help='It can be any of these three units: V, A or Ω')
    parser.add_argument("arg2", help='It can be any of these three units: V, A or Ω')
    args = parser.parse_args()

    arg1 = units.parse(args.arg1)
    arg2 = units.parse(args.arg2)

    res = play(arg1, arg2)
    msg = units.format_verbose(res[0], res[1])
    print(msg)
    # calc power dissipation
    p = calc_power(arg1, arg2, res)
    msg = units.format_verbose(p[0], p[1])
    print('Power dissipation: {0}'.format(msg))

