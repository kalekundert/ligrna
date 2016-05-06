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
    -p --plate-volume <μL>          [default: 20]
        The volume of cells that were plated for each dilution.  By default 
        this is 20 μL, which is a good amount for titering 16 measurements on a 
        single plate.
        
    -r --recovery-volume <μL>       [default: 1000]
        The total volume of recovered cells.  By default, this is 1 mL, which 
        is the amount of SOC I typically add after electroporation.  However, 
        the volume should technically also include the volume of the competent 
        cells (50-100 μL) and the volume of the added DNA (1-5 μL).
"""

import docopt
from pylab import *

args = docopt.docopt(__doc__)
cfus = array([eval(n) for n in args['<cfus>']])
plate_volume = float(args['--plate-volume'])
recovery_volume = float(args['--recovery-volume'])
dilutions = (200 / 2) * (200 / 20)**arange(len(cfus))
transformants = recovery_volume * dilutions * (cfus / plate_volume)
num_data = len(cfus[cfus != 0])

print('Dilution  # CFU  # transformants')
print('========  =====  ===============')
for i in range(len(cfus)):
    if cfus[i] > 0:
        print('1e-{:<5d}  {:>5d}  {:>14.2e}'.format(
            i + 3,
            cfus[i],
            transformants[i],
        ))

if num_data > 1:
    print("Weighted average: {:13.2e}".format(
        np.average(transformants, weights=cfus)))

