#!/usr/bin/env python
from __future__ import print_function
import argparse
from progenitor_probability import progenitor_probability

parser = argparse.ArgumentParser()
parser.add_argument('-z', '--redshift', type=float, default=None, help='Redshift')
parser.add_argument('-m', '--mass', type=float, default=None, help='Log10 stellar mass/M_sun')
parser.add_argument('-d', '--density', type=float, default=None, help='Local number density percentile [0,100]')
parser.add_argument('-s', '--SFR', type=float, default=None, help='SFR in M_sun/yr')
args = parser.parse_args()

fit = progenitor_probability(density=args.density, sfr=args.SFR, mass=args.mass, redshift=args.redshift)
print(fit[0])
