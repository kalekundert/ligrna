#!/usr/bin/env python3

"""\
Usage:
    crispri_titration.py [--time <hours>] [--verbose]

Options:

    -t --time <time>  [default: 8h]
        The number of hours to grow the cells for.

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
Make 1 mL overnight cultures from recently  
transformed (within ≈2 weeks) colonies of the 
sensors you want to test and their corresponding 
controls.
"""

protocol += """\
Prepare media with serially diluted ligand.

- Put 2 mL holo media in the first column of a 96 
  well block.

- Put 1 mL apo media in the remaining columns of 
  the block.

- Perform 11 serial dilutions, starting from the 
  first column, transferring 1 mL of media each 
  time.  Leave the last column with apo media.

- Do the serial dilution for both the sensors and 
  the controls.
"""

protocol += """\
Inoculate each well with 4 μL overnight culture.
"""

protocol += """\
Grow at 37°C with shaking at 225 rpm for {hours}.
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
