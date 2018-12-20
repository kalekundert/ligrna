#!/usr/bin/env python3

"""\
Design primers to clone the Doench spacers into the pCR2.1-AAVS vector.

Usage:
    ./design_doench_primers.py [<indices>] [options]

Options
    -t --tsv
        Output the primers in the TSV format, rather than in lists ready to be 
        copied into the Elim form.
"""

import docopt, copy
import sgrna_sensor.primers as mut
from nonstdlib import indices_from_str

# Parse command-line arguments.
args = docopt.docopt(__doc__)

# Define the sequences around where we're cloning.
cr21 = ( #
    'tgggtacttttatctgtcccctccacccca',
    'CAGTGGGGCCACTAGGGACAGGATTGGTGA',
    'cagaaaagccccatccttaggcctcctcct',
)
pblo = ( #
    'aattctaaagatcttatagtaataatacgactcactatag',
    'CATCTAATTCAACAAGAATT',
    'gtttcagagctatgctggaaacagcatagcaagttgaaat',
)
mhf37 = ( #
    'aattctaaagatcttatagtaataatacgactcactatag',
    'CATCTAATTCAACAAGAATT',
    'gtttcagagcatgctggaaacagcatagcaagttgaaata',
)

# Create primer designers.
cr21_designer = mut.PrimerDesigner()
cr21_designer.backbone = ''.join(cr21)

pblo_designer = mut.PrimerDesigner()
pblo_designer.backbone = ''.join(pblo)
pblo_designer.cut = 2   # The default cut is usually either 1 or 2.  This 
                        # ensures that the reverse primer is always the same.
mhf37_designer = mut.PrimerDesigner()
mhf37_designer.backbone = ''.join(mhf37)
mhf37_designer.cut = 2

# Load the Doench16 spacers.
with open('doench_spacers.tsv') as file:
    doench_spacers = [x.split() for x in file.readlines()]

# Decide how many spacers to use.
if args['<indices>'] is None:
    batch = doench_spacers
else:
    batch = [doench_spacers[x-1] for x in indices_from_str(args['<indices>'])]

# Design primers...
primers = {}
for i, (name, spacer, score) in enumerate(batch):
    # ...for the target DNA plasmid.
    cr21_designer.name = f'cr21_{name}'
    cr21_designer.construct = cr21[0] + spacer + cr21[2]
    primers.update(cr21_designer.design_primers())

    # ...for the sgRNA plasmid.
    pblo_designer.name = f'pblo_{name}'
    pblo_designer.construct = pblo[0] + spacer[4:24] + pblo[2]
    primers.update(pblo_designer.design_primers())

    # ...for the mhf/37 plasmid (which is the same as the sgRNA plasmid, but 
    # with an unexpected deletion in the lower stem).
    mhf37_designer.name = f'pblo_{name}_mhf_37'
    mhf37_designer.construct = mhf37[0] + spacer[4:24] + mhf37[2]
    primers.update(mhf37_designer.design_primers())

# Display the primers.

def sort_for_96_well_plate(name): #
    fields = name.split('_')
    plasmid, spacer, direction = fields[0], fields[1], fields[-1]
    num = int(spacer.strip('D')) - 1
    return ',' in name, plasmid, 'MHF' in name, num // 8, direction, num

primers = mut.consolidate_duplicate_primers(primers)

if args['--tsv']:
    mut.report_primers_to_table(primers)
else:
    mut.report_primers_for_elim(primers, key=sort_for_96_well_plate)



