#!/usr/bin/env python3

"""\
Design inverse PCR primers that can be used to change the spacer in the sgRNA 
plasmids.

Usage:
    swap_spacer.py <spacers>... [options]

Arguments:
    <spacers>...
        The names of one or more spacers to clone (e.g. g1).

Options:
    -T, --tm <celsius>
        The desired melting temperature for the primers.  The default is 60°C 
        for inverse PCR primers and 78°C for Quikchange.  (Note that Tm is 
        calculated differently for the two cloning strategies.)

    -t, --table
        Report the primers in a tab-separated table.

    -v, --verbose
        Show extra debugging output.
"""

import docopt
import shlex
import sgrna_sensor
import sgrna_sensor.primers as mut

args = docopt.docopt(__doc__)

primers = {}
context = "gatctttgacagctagctcagtcctaggtataatactagt{}gtttcagagctatgctggaaacagcatagcaagttgaaat"

for name in args['<spacers>']:
    designer = mut.PrimerDesigner()
    designer.name = name
    designer.tm = args['--tm']
    designer.verbose = args['--verbose']

    spacer = sgrna_sensor.spacer(name)
    designer.construct = context.format(spacer.dna)
    designer.backbone = context.format("")

    primers.update(designer.design_primers())

primers = mut.consolidate_duplicate_primers(primers)

if args['--table']:
    mut.report_primers_to_table(primers)
else:
    mut.report_primers_for_elim(primers)
