#!/usr/bin/env python3

"""
Print a protocol for switching the spacer in the middle of a yeast screen.  The 
process involves amplifying the library off of the yeast genome, inserting in 
into a vector with a different spacer using Golden Gate assembly, transforming 
it into bacteria, then transforming it back into yeast.

Usage:
    swap_spacer.py [options]

Options:
    --btgzi
        Use BtgZI to swap the spacer for upper stem/bulge libraries, that are 
        too close to the spacer to use BsaI.

    -v --verbose
        Print some extra information explaining how the protocol was developed.
"""

import os, sys; sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'general'))
import docopt
import dirty_water
import electrotransformation
from pprint import pprint

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
enzyme = 'BsaI-HF' if not args['--btgzi'] else '5 U/μL BtgZI'
backbone = 'pKBK017' if not args['--btgzi'] else 'pKBK027'

protocol += """\
Setup a zymolase reaction:

- 46.1 μL water
- 3.3 μL OD=10 yeast culture
- 0.6 μL 5 U/μL zymolase
"""

protocol += """\
Incubate at 37°C for 30 min, then 95°C for 10 min.
"""

protocol += """\
Setup a 50 μL PCR reaction:

- 15 μL water
- 5 μL primer mix
- 5 μL zymolase reaction
- 25 μL 2x Q5 master mix
"""

protocol += """\
Run the PCR reaction:

- 22 cycles
- 12s extension time
- 60°C annealing temperature
"""

protocol += """\
Do a PCR cleanup and elute in 25 μL water.
"""

protocol += """\
Setup the restriction digest of the destination
vector:

- 7 μL ≈800 ng/μL {backbone}
- 1 μL 10x CutSmart buffer
- 2 μL {enzyme}
"""

protocol += """\
Incubate at 37°C for 30 min, then 65°C for 20 min.
"""

protocol += """\
Gel purify the entire reaction.
"""

protocol += """\
Setup a Golden Gate reaction:

- 1.0 μL ≈160 ng/μL {backbone} (linearized)
- 25.0 colony PCR product
- 3.1 μL 10x T4 ligase buffer
- 1.0 μL T4 ligase
- 1.0 μL {enzyme}
"""

protocol += """\
Run the following thermocycler protocol:

- 42°C for 5 min
- 16°C for 5 min
- 30 cycles
"""

protocol += electrotransformation.protocol

print(protocol)

if args['--verbose']:
    print("""\
Notes
=====
The protocols for yeast colony PCR that I can find online all assume that 
you're actually starting from a colony.  I wanted to use about the same numbers 
of cells as those protocols, even though I'm starting from liquid culture, so I 
looked up some bio-numbers:

- Number of cells in a yeast colony: ≈1e6
- Number of cells in 1 mL of OD=1 culture: ≈3e7

Assuming my overnight cultures are at OD=10, that means I would need 3.3 μL to 
get about a colony-worth of cells.
""")

# vim: tw=50
