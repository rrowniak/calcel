#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from core import units
from core.units import AllUnits as U

def play(v_in, r1, r2):
    v_in = U.convert_to_canonical(v_in)
    r1 = U.convert_to_canonical(r1)
    r2 = U.convert_to_canonical(r2)
    
    if v_in[1] != U.V:
        print('V_in is expected to be [{0}]'.format(U.V))
        os.exit(-1)
        
    if r1[1] != U.R:
        print('R1 is expected to be [{0}]'.format(U.R))
        os.exit(-1)
        
    if r2[1] != U.R:
        print('R2 is expected to be [{0}]'.format(U.R))
        os.exit(-1)
    
    return v_in[0] * r2[0] / (r1[0] + r2[0]), U.V


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = """
Voltage divider. Provide input voltage [V], first resistance [Ω] and second resistance [Ω].
The resulting voltage will be calculated according to the formula:
V_out = V_in * R2 / (R1 + R2)
For example: volt_divider.py 10V 4k7 1k2
    """
    parser.add_argument("arg1", help='Input voltage V_in [V]')
    parser.add_argument("arg2", help='First resistor of the divider R1 [Ω]')
    parser.add_argument("arg3", help='Second resistor of the divider R2 [Ω]')
    args = parser.parse_args()

    arg1 = units.parse(args.arg1)
    arg2 = units.parse(args.arg2)
    arg3 = units.parse(args.arg3)

    res = play(arg1, arg2, arg3)
    msg = units.format_verbose(res[0], res[1])
    print(msg)

