#!/usr/bin/env python3

"""\
Design primers to install the GRRT PAM spacers into the vector containing the 
saCas9 sgRNA sequence.

Usage:
    ./design_swap_spacer_primers.py [-v]

Options:
    -v --verbose
        Show extra debugging output
"""

import docopt
import sgrna_sensor
from sgrna_sensor import primers

backbone = (
        'gaattctaaagatctttgacagctagctcagtcctaggtataatactagt'
        '{}'
        'gttttagtactctggaaacagaatctactaaaacaaggcaaaatgccgtg'
)
spacers = [
        #'g1',
        'g2',
        'g3',
        'g4',
        'g5',
        'r1',
        'r2',
        'r3',
        'r4',
]
results = {}

args = docopt.docopt(__doc__)
dna = lambda x: backbone.format(sgrna_sensor.spacer(x, species='sa').dna)

for spacer in spacers:
    designer = primers.PrimerDesigner()
    designer.name = 'sa_' + spacer
    designer.backbone = dna('n21')
    designer.construct = dna(spacer)
    designer.verbose = args['--verbose']

    results.update(designer.design_primers())

results = primers.consolidate_duplicate_primers(results)
primers.report_primers_to_table(results)


