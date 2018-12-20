#!/usr/bin/env python3

"""
Calculate how to dilute sgRNA to particular concentration.

Usage:
    dilute_sgrna.py <name> <ng_uL> [options]
    dilute_sgrna.py <tsv> [options]

Options:
    -c --target-conc <nM>  [default: 1500]
        The desired final concentration.

    -v --target-volume <uL>
        The desired final volume.

    -r --target-sgrna <uL>
        The desired volume of sgRNA to dilute.

    -R --max-sgrna <uL>
        The maximum volume of sgRNA that can be diluted.  Any recipes that need 
        more sgRNA than this will be scaled down.

    -w --target-water <uL>
        The desired volume of water to dilute with.

    -p --print-nM
        Print the initial concentration in units of nM.

    -e --encoding <utf>  [default: utf-16le]
        The encoding of <tsv>.  The nanodrop outputs UTF-16le by default, but 
        if you use gnumeric to input the names, it exports as UTF-8.
"""

import docopt
import nonstdlib
import sgrna_sensor
import pandas as pd
import os

args = docopt.docopt(__doc__)

def get_molecular_weight(name):
    if name.startswith('pcr21'):
        return 2686183.94
    else:
        sgrna = sgrna_sensor.from_name(name.lower())
        return sgrna.mass('rna')

def process_sample(name, initial_ng_uL, args):
    initial_nM = initial_ng_uL * 1e6 / get_molecular_weight(name)

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

    max_sgrna = args['--max-sgrna']

    if max_sgrna is not None and float(max_sgrna) < sgrna_to_add:
        sgrna_to_add *= float(max_sgrna) / sgrna_to_add
        water_to_add *= float(max_sgrna) / sgrna_to_add

    print('{:>6.2f} μL {:.1f} ng/uL {}'.format(sgrna_to_add, initial_ng_uL, name))
    print('{:>6.2f} μL nuclease-free water'.format(water_to_add))
    print(30 * '─')
    print('{:>6.2f} μL {:.1f} nM {}'.format(sgrna_to_add + water_to_add, target_nM, name))


# Figure out if name is filename or sgRNA name
if args['<tsv>']:
    df = pd.read_csv(args['<tsv>'], sep='\t', encoding=args['--encoding'])
    for row in df.iterrows():
        try: name = row[1]['Sample ID']
        except KeyError: name = row[1]['Sample Name']
        try: conc = row[1]['Nucleic Acid']
        except KeyError: conc = row[1]['Nucleic Acid(ng/uL)']

        process_sample(name, float(conc), args)
        print()

elif args['<name>']:
    initial_ng_uL = float(args['<ng_uL>'])
    process_sample(args['<name>'], initial_ng_uL, args)

