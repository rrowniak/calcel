#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from core import units
from core.units import AllUnits as U




def play(u1, u2):
    reference = u1[0]
    measured = u2[0]
    power = 10.0 * np.log10(measured / reference)
    amplitude = 20.0 * np.log10(measured / reference)
    return power, amplitude


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = """
Calculate ratio in decibels
    """
    parser.add_argument("arg1", help='Reference numeric value (No units are expected)')
    parser.add_argument("arg2", help='Measured numeric value (No units are expected)')
    args = parser.parse_args()

    arg1 = units.parse(args.arg1)
    arg2 = units.parse(args.arg2)

    res = play(arg1, arg2)
    msg1 = units.format_verbose(res[0], 'dB')
    msg2 = units.format_verbose(res[1], 'dB')

    print('Power ratio    : {0}'.format(msg1))
    print('Amplitude ratio: {0}'.format(msg2))

