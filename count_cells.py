#!/usr/bin/env python3

"""\
Usage:
    count_cells.py <counts>... [options]

Options:
    -v --volume <μL>    [default: 1000]
        The total volume of recovered cells.  By default, this is 1 mL, which 
        is the amount of SOC I typically add after electroporation.  However, 
        the volume should technically also include the volume of the competent 
        cells (50-100 μL) and the volume of the added DNA (1-5 μL).
"""

import docopt
from pylab import *

args = docopt.docopt(__doc__)
counts = array([int(n) for n in args['<counts>']])
volume = float(args['--volume'])
dilutions = arange(len(counts))
transformants = volume * (200 / 2) * (200 / 20)**dilutions * (counts / 100)

print('Dilution  # CFU  # transformants')
print('========  =====  ===============')
for i in dilutions:
    print('1e-{:<5d}  {:>5d}  {:>14.2e}'.format(
        i + 3,
        counts[i],
        transformants[i],
    ))


