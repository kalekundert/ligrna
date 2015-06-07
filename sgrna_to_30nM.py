#!/usr/bin/env python3

"""
Calculate how to dilute sgRNA to 300nM

Usage:
    sgrna_to_30nM.py <name> <ng_uL> [options]

Options:
    -c --target-concentration <nM>  [default: 300]
        The desired final concentration.

    -v --target-volume <uL>
        The desired final volume.

    -w --target-water <uL>
        The desired volume of water to dilute with.

    -r --target-sgrna <uL>
        The desired volume of sgRNA to dilute.
"""

import docopt
import nonstdlib
import sgrna_helper

args = docopt.docopt(__doc__)
sgrna = sgrna_helper.from_name(args['<name>'])
initial_ng_uL = float(args['<ng_uL>'])
initial_nM = initial_ng_uL * 1e6 / sgrna.mass('rna')
target_nM = float(args['--target-concentration'])

if args['--target-volume']:
    target_uL = float(args['--target-volume'])
    sgrna_to_add = target_nM * target_uL / initial_nM
    water_to_add = target_uL - sgrna_to_add

elif args['--target-water']:
    water_to_add = float(args['--target-water'])
    sgrna_to_add = water_to_add * target_nM / (initial_nM - target_nM)

elif args['--target-sgrna']:
    sgrna_to_add = float(args['--target-sgrna'])
    water_to_add = initial_nM * initial_uL / target_nM - sgrna_to_add

print('{:>6.2f} μL {} ng/uL sgRNA'.format(sgrna_to_add, initial_ng_uL))
print('{:>6.2f} μL nuclease-free water'.format(water_to_add))
print(30 * '-')
print('{:>6.2f} μL {:.1f} nM sgRNA'.format(sgrna_to_add + water_to_add, target_nM))
