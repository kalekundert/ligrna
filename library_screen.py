#!/usr/bin/env python3

"""\
Screen a library to find sgRNAs with aptamers inserted into them to find that 
are sensitive to a small molecule.

Usage:
    library_screen.py [<rounds>] [options]

Options:
    -m --materials
        Print detailed instructions on how to make the media used in this 
        protocol (LBCC, LBCC54, EZCCA, EZCCAT).
"""

import docopt, dirty_water
from nonstdlib import *

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
num_rounds = int(args['<rounds>'] or 4)

if args['--materials']:
    protocol += """\
Prepare the following reagents:

Reagent  Description
─────────────────────────────────────────────────
LBCC     LB, 100 μg/mL carbenicillin, 35 μg/mL 
         chloramphenicol
LBCC54   LB, 125 μg/mL carbenicillin, 43 μg/mL 
         chloramphenicol
EZCCA    MOPS EZ rich defined media (Teknova 
         M2105), 0.1% glucose, 100 μg/mL 
         carbenicillin, 35 μg/mL chloramphenicol, 
         1 μg/mL anhydrotetracycline
EZCCAT   EZCCA, 1 mM theophylline"""

protocol += """\
Make overnight cultures for the library and the 
controls.

- Thaw a glycerol stock of MG1655 cells containing 
  the library on ice for ≈10 min.

- Add 1 mL of thawed glycerol stock to 4 mL LBCC.

- Inoculate 5 mL LBCC with stabs from glycerol 
  stocks for the "wt" and "dead" controls.

- Grow all the cultures overnight at 37°C."""

protocol += """\
Grow the library and the controls with and without 
theophylline, while inducing Cas9.

- Dilute enough of the library to get at least 10x 
  coverage into 50 volumes of EZCCA and EZCCAT.  
  Use at least 1 mL of media.

  My saturated cultures have an OD600 of ≈3.0, 
  which corresponds to ≈2.4×10⁶ cells/μL.  For a 
  library of 5×10⁷, 10x coverage is ≈200 μL.

Overnight volume:           Media volume:

- Make a glycerol stock of the library (1 mL 
  overnight culture, 333 μL 80% glycerol).

- Subculture 20 μL of each control into 50 volumes 
  (i.e. 1 mL) EZCCA and EZCCAT.

- Grow at 37°C for at least 9h."""

protocol += """\
Dilute each culture into PBS.

The following instructions are specific to the 
FACSAria II with a flow rate of "1.0" (≈2 mL/h).
At this flow rate, an OD600 of 3×10⁻³ corresponds 
roughly to an event rate of ≈1000 evt/sec.

- If you want to sort at a particular event rate, 
  dilute the cells to the corresponding OD600 in 
  enough PBS to last the duration of the sort.

- If you want to maximize throughput at the 
  expense of accuracy (e.g. the first screen), you 
  want the sort efficiency to be ≈50%.  This is 
  the point where efficiency starts decreasing 
  faster than event rate can increase.  Start by 
  diluting the library 60x into PBS, then add PBS 
  or cells as necessary to get ≈50% efficiency.  
  The event rate should be about ≈20,000 evt/sec.  
  Expect error rates of up to 30% for fluorescent 
  cells and up to 15% for non-fluorescent cells.
  
- If there are fewer than ≈10⁴ clones remaining in 
  the library (e.g. after the third screen), just 
  dilute 1 μL of the library into 1 mL PBS."""

protocol += """\
Sort the library.

- Record data for the controls to make sure the 
  cells are healthy and to help draw the gates.

- Record data for the library with and without 
  theophylline to track the progress of the 
  screen.

- Keep the cells at room temperature before and 
  after the sort.

- Put 1 mL SOC in each collection tube.

Condition:                  Gate:

Event rate:                 Sort time:

- Dilute the collected cells and the controls 
  in 4 volumes LBCC54.  Grow overnight at 37°C."""

for i in range(num_rounds - 1):
    same_opposite = 'same' if i % 2 else 'opposite'
    protocol += """\
Grow and sort the library as above.  Select for 
the {same_opposite} condition as the first sort.

Overnight volume:           Media volume:

Condition:                  Gate:

Event rate:                 Sort time:"""

protocol += """\
Plate ≈500 cells to individually test."""

print(protocol)

# vim: tw=50
