#!/usr/bin/env python3

"""\
Screen a library.

Usage:
    library_screen.py [options]

Options:
    -i --initial-sort
        Print instructions for reviving the library from a glycerol stock, 
        rather than assuming that you have an overnight culture of cells 
        collected from a previous sort.

    -e --event-rate <cells_per_sec>     [default: 1000]
        The number of cells you want to pass the detector each second.  This is 
        the most important determinant of sorting accuracy, although it's also 
        easier to sort non-fluorescent cells (e.g. wt) than fluorescent cells 
        (e.g. dead).  For reference, here are percentages of incorrectly sorted 
        cells for several different event rates:
        
        Event rate  Expecting wt  Expecting dead
         cells/sec   % incorrect     % incorrect
        ==========  ============  ==============
              3000           0.7             4.7
              9000           1.4            11.3
             27000          15.9            29.9

    -t --sort-time <hours_and_minutes>   [default: 1h00]
        How long you plan to sort for.  You can use the ``unique_variants.py``
        script to work out how different combinations of event rate and sort 
        time will affect library coverage.
        
"""

import docopt
import dirty_water
from nonstdlib import *

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()

if args['--initial-sort']:
    protocol += """\
Make overnight cultures for the library and the 
controls.

- Thaw a glycerol stock of MG1655 cells containing 
  the library on ice for ≈10 min.

- Add 1 mL of thawed glycerol stock to 4 mL LBCC 
  (LB + 100 μg/mL Carb + 35 μg/mL Chlor).

- Inoculate 5 mL LBCC with stabs from glycerol 
  stocks for the "wt" and "dead" controls.

- Grow all the cultures overnight at 37°C."""

overnight_vol = 50 if args['--initial-sort'] else 25
media_vol = 2 if args['--initial-sort'] else 1

protocol += """\
Grow the library and the controls with and without 
theophylline, while inducing Cas9.

- Subculture {overnight_vol} μL of each overnight into {media_vol} mL
  EZCCA (EZ media + 0.1% glucose + 100 μg/mL Carb 
  + 35 μg/mL Chlor + 1000 μg/mL ATC) and 2 mL 
  EZCCAT (EZCCA + 1 mM theophylline).

  My saturated cultures have an OD600 of ≈3.0, 
  which corresponds to ≈2.4×10⁶ cells/μL.  For a 
  library of 10⁷, 10x coverage is 40 μL.

- Grow at 37°C for at least 9h."""

target_od = sci(1.93e-6 * eval(args['--event-rate']), 2)
pbs_vol = int(2 * minutes(args['--sort-time']) / 60)

protocol += """\
Dilute the library and the controls into PBS for 
sorting.

- Measure the OD600 of the library using the 
  nanodrop.

- Work out how to dilute the library given that 2 
  mL of sample lasts about 1h and that an OD600 of 
  1.93×10⁻³ corresponds to an event rate of about 
  1000 cells/sec (on the FACSAria II with the flow 
  rate set to "1.0").

  Planned event rate:

  Planned sort time:

- Dilute 1 μL of each control into 1 mL PBS."""

protocol += """\
Record the cell populations for the library and 
the controls."""

protocol += """\
Sort the library.

Gate:"""

protocol += """\
Dilute the collected cells and the controls in 4 
volumes LB + 5/4x Carb + 5/4x Chlor.  Grow 
overnight at 37°C."""

print(protocol)

# vim: tw=50
