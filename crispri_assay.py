#!/usr/bin/env python3

"""\
Usage:
    crispri_assay.py [--time <hours>] [--time-course] [--verbose]

Options:
    -t --time <time>  [default: 9h]
        The number of hours to grow the cells for.

    -T --time-course
        Take time-points every hour.

    -v --verbose
        Print out the more pedantic details about the protocol, namely 
        cytometer settings and things like that.
"""

import docopt
import dirty_water

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
hours = args['--time']

protocol += """\
Make 1 mL overnight cultures of the designs you 
want to test."""

protocol += f"""\
Grow each culture with and without ligand, 
while inducing Cas9:

- Subculture 4 μL of each overnight into 1 mL 
  apo media and 1 mL holo media.

- Grow at 37°C for {hours}
"""

if args['--time-course']:
    protocol += """\
Take a time point every hour, starting at 6h:

- Prepare plates with 200 μL PBS + Sp.  Keep at 
  4°C.

- If the cultures are totally transparent, dilute 
  2 μL into the PBS + Sp.

- If the cultures are visibly cloudy, but not 
  saturated, dilute 1 μL into the PBS + Sp.

- If the cultures are saturated, dilute 0.5 μL 
  into the PBS + Sp.
"""

protocol += """\
Dilute 0.5 μL of each culture into 200 μL PBS.
"""

protocol += """\
Measure the GFP and RFP fluorescence of each 
culture by flow cytometry.
"""

print(protocol)

if args['--verbose']:
    import lsrii_params
    print()
    print(lsrii_params.__doc__)

# vim: tw=50
