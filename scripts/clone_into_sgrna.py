#!/usr/bin/env python3

"""\
Design inverse PCR primers that can be used to clone a new sgRNA into a plasmid 
already harboring a related sgRNA.

Usage:
    clone_into_sgrna.py <constructs>... [options]

Arguments:
    <constructs>...
        The names of one or more constructs to clone (e.g. rhf/6).  You can 
        also specify any command-line that would be valid on its own for this 
        command (e.g. 'rhf/6 -c 10').  Any options specified in this way will 
        only apply to the constructs named within the sub-command-line.

Options:
    -q, --quikchange
        Design primers for Quikchange instead of inverse PCR.  Quikchange is 
        slightly easier for point mutations or very small insertions or 
        deletions.
        
    -b, --backbone <name>
        The name of the sgRNA to clone into.  By default this is the "on" 
        positive control sgRNA.

    -s, --spacer <name>
        The spacer sequence of the wildtype plasmid.  For some designs, this 
        doesn't matter because the primers won't overlap the spacer.  But for 
        other designs, particularly upper stem designs, different primers are 
        needed for each spacer.

    -c, --cut <index>
        Manually specify where the index where the insert should be split, 
        relative to the insert itself.  By default, the cut site is chosen to 
        make the primers the same length.  

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
default_backbone_name = args['--backbone'] or 'on'
default_spacer = args['--spacer'] or 'none'
default_quikchange = args['--quikchange']
default_cut = args['--cut']
default_tm = args['--tm']
default_verbose = args['--verbose']

primers = {}

for name in args['<constructs>']:
    sub_cli = shlex.split(name)
    sub_args = docopt.docopt(__doc__, sub_cli)

    for sub_name in sub_args['<constructs>']:
        designer = mut.PrimerDesigner()
        designer.name = sub_name
        designer.spacer = sub_args['--spacer'] or default_spacer
        designer.quikchange = sub_args['--quikchange'] or default_quikchange
        designer.cut = mut.int_or_none(sub_args['--cut'] or default_cut)
        designer.tm = mut.float_or_none(sub_args['--tm'] or default_tm)
        designer.verbose = sub_args['--verbose'] or default_verbose

        sgrna = sgrna_sensor.from_name(sub_name, target=designer.spacer)
        after_sgrna = 'tgaagcttgggcccgaacaaaaactcatct'
        designer.name = sgrna.underscore_name
        designer.construct = sgrna.dna + after_sgrna
        designer.backbone = sgrna_sensor.from_name(
                sub_args['--backbone'] or default_backbone_name,
                target=designer.spacer).dna + after_sgrna

        primers.update(designer.design_primers())

primers = mut.consolidate_duplicate_primers(primers)

if args['--table']:
    mut.report_primers_to_table(primers)
else:
    mut.report_primers_for_elim(primers)
