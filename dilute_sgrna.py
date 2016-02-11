#!/usr/bin/env python3

"""
Calculate how to dilute sgRNA to particular concentration.

Usage:
    sgrna_to_300nM.py <name> <ng_uL> [options]
    sgrna_to_300nM.py <tsv> [options]

Options:
    -c --target-conc <nM>  [default: 1500]
        The desired final concentration.

    -v --target-volume <uL>
        The desired final volume.

    -r --target-sgrna <uL>
        The desired volume of sgRNA to dilute.

    -w --target-water <uL>
        The desired volume of water to dilute with.

    -p --print-nM
        Print the initial concentration in units of nM.
"""

import sys; sys.path.append('../scripts')
import docopt
import nonstdlib
import sgrna_sensor
import pandas as pd
import os

args = docopt.docopt(__doc__)

def process_sample(sgrna, initial_ng_uL, args):
    initial_nM = initial_ng_uL * 1e6 / sgrna.mass('rna')

    if args['--target-conc'].endswith('x'):
        target_nM = 300 * float(args['--target-conc'][:-1])
    else:
        target_nM = float(args['--target-conc'])

    if initial_nM < target_nM:
        print("Warning: Cannot reach {:.1f} nM!\n".format(target_nM))
        target_nM = initial_nM
        
    if args['--target-volume']:
        target_uL = float(args['--target-volume'])
        sgrna_to_add = target_nM * target_uL / initial_nM
        water_to_add = target_uL - sgrna_to_add

    elif args['--target-water']:
        water_to_add = float(args['--target-water'])
        sgrna_to_add = water_to_add * target_nM / (initial_nM - target_nM)

    elif args['--target-sgrna']:
        sgrna_to_add = float(args['--target-sgrna'])
        water_to_add = initial_nM * sgrna_to_add / target_nM - sgrna_to_add

    elif args['--print-nM']:
        print('{:>.2f} nM'.format(initial_nM))
        return

    else:
        raise docopt.DocoptExit("""\
    Must specify one of:
        -v, --target-volume <uL>
        -r, --target-sgrna <uL>
        -w, --target-water <uL>
        -p, --print-nM
    """)

    print('{:>6.2f} μL {} ng/uL {}'.format(sgrna_to_add, initial_ng_uL, sgrna.function_name))
    print('{:>6.2f} μL nuclease-free water'.format(water_to_add))
    print(30 * '─')
    print('{:>6.2f} μL {:.1f} nM {}'.format(sgrna_to_add + water_to_add, target_nM, sgrna.function_name))


# Figure out if name is filename or sgRNA name
if args['<tsv>']:
    df = pd.read_csv(args['<tsv>'], sep='\t', encoding='latin_1')
    for row in df.iterrows():
        sgrna = sgrna_sensor.from_name( row[1]['Sample ID'].lower() )
        initial_ng_uL = float(row[1]['Nucleic Acid'])
        process_sample(sgrna, initial_ng_uL, args)
        print()

elif args['<name>']:
    sgrna = sgrna_sensor.from_name(args['<name>'])
    initial_ng_uL = float(args['<ng_uL>'])
    process_sample(sgrna, initial_ng_uL, args)

