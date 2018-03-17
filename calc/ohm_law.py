#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from calc.core import units


def calc_I(r, v):
    return v / r


def calc_R(v, i):
    return v / i


def calc_V(i, r):
    return i * r


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = """
Provide a pair of values of the following units: V, A or Ω and the program will calculate the result according
to the Ohm law: I = V/R. The resistance unit Ω can be omitted.
For example: ohm_law.py 10mA 4k7
    """
    parser.add_argument("arg1", help='It can be any of these three units: V, A or Ω')
    parser.add_argument("arg2", help='It can be any of these three units: V, A or Ω')
    parser.parse_args()
