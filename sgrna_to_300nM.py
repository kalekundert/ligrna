#!/usr/bin/env python3

"""
Calculate how to dilute sgRNA to particular concentration (300 nM by default).

Usage:
    sgrna_to_300nM.py <name/filename> [options]

Options:
    -c --target-concentration <nM>  [default: 300]
        The desired final concentration.

    -v --target-volume <uL>
        The desired final volume.

    -r --target-sgrna <uL>
        The desired volume of sgRNA to dilute.

    -w --target-water <uL>
        The desired volume of water to dilute with.

    -n --ng_uL <ng/uL>
        Concentration of a single sample in ng/uL.
"""

import sys; sys.path.append('../scripts')
import docopt
import nonstdlib
import sgrna_helper
import pandas as pd
import os

args = docopt.docopt(__doc__)

def process_sample(sgrna, initial_ng_uL, args):
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

    else:
        raise docopt.DocoptExit("""\
    Must specify one of:
        -v, --target-volume <uL>
        -r, --target-sgrna <uL>
        -w, --target-water <uL>
    """)

    print('{:>6.2f} μL {} ng/uL sgRNA'.format(sgrna_to_add, initial_ng_uL))
    print('{:>6.2f} μL nuclease-free water'.format(water_to_add))
    print(30 * '-')
    print('{:>6.2f} μL {:.1f} nM sgRNA'.format(sgrna_to_add + water_to_add, target_nM))

# Figure out if name is filename or sgRNA name
if os.path.isfile(args['<name/filename>']):
    df = pd.read_csv(args['<name/filename>'], sep='\t')
    for row in df.iterrows():
        sgrna = sgrna_helper.from_name( row[1]['Sample ID'].lower() )
        print(sgrna)
        print(30 * '-')
        initial_ng_uL = float(row[1]['Nucleic Acid Conc.'])
        process_sample( sgrna, initial_ng_uL, args )
        print()
else:
    sgrna = sgrna_helper.from_name(args['<name/filename>'])
    initial_ng_uL = float(args['--ng_uL'])
    process_sample( sgrna, initial_ng_uL, args )

