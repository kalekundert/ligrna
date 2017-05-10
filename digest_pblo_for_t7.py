#!/usr/bin/env python3

"""\
Display a protocol for digesting the sgRNA out of the pBLO plasmid prior to *in 
vitro* transcription.  The purpose of doing this is to help the transcription 
reaction produce uniformly sized products.  This protocol makes use of the fact 
that the sgRNA is surrounded by EcoRI and HindIII restriction sites in pBLO.

Usage:
    digest_pblo_for_t7.py <reactions> [options]

Options:
    -x --extra PERCENT      [default: 20]
        How much extra master mix to create.
"""

import docopt
import dirty_water
from nonstdlib import plural

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
digest = dirty_water.Reaction('''\
Reagent               Conc  Each Rxn  Master Mix
===============  =========  ========  ==========
water                         6.0 μL         yes
CutSmart Buffer        10x    0.8 μL         yes
EcoRI-HF           20 U/μL    0.1 μL         yes
HindIII-HF         20 U/μL    0.1 μL         yes
DNA              250 ng/μL    4.0 μL
''')

digest.num_reactions = eval(args['<reactions>'])
digest.extra_master_mix = float(args['--extra'])

protocol += """\
Setup {:? restriction digest reaction/s} by mixing
the following reagents at room temperature in the 
order given.

{}""".format(
        plural(digest.num_reactions), digest)

protocol += """\
Incubate at 37°C for 1h, then at 80°C for 20 min 
(to heat-inactivate the enzyme)."""

protocol += """\
Setup the in vitro transcription {:reaction/s} 
immediately, or store at -20°C.""".format(
        plural(digest.num_reactions))

print(protocol)

# vim: tw=50

