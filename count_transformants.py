#!/usr/bin/env python3

"""\
Calculate how cells were successfully transformed via electroporation.

This is a fairly brittle script meant to help with a calculation I frequently 
make.  When I do an electro-transformation, I plate up to four dilutions: 10⁻³, 
10⁻⁴, 10⁻⁵, 10⁻⁶.  This script takes the number of colony-forming units (CFUs) 
from each plate and converts that into the number of transformants.  It also 
reports a weighted average, based on the number of counts at each level, which 
I treat as the true number of transformants.

Usage:
    count_transformed_cells.py <cfus>... [options]

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
cfus = array([int(n) for n in args['<cfus>']])
volume = float(args['--volume'])
dilutions = arange(len(cfus))
transformants = volume * (200 / 2) * (200 / 20)**dilutions * (cfus / 100)

print('Dilution  # CFU  # transformants')
print('========  =====  ===============')
for i in dilutions:
    print('1e-{:<5d}  {:>5d}  {:>14.2e}'.format(
        i + 3,
        cfus[i],
        transformants[i],
    ))

print("Weighted average: {:13.2e}".format(
    np.average(transformants, weights=cfus)))

