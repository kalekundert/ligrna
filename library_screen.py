#!/usr/bin/env python3

"""\
Screen a library to find sgRNAs with aptamers inserted into them to find that 
are sensitive to a small molecule.

Usage:
    library_screen.py [options]

Options:
    -m --materials
        Print detailed instructions on how to make the media used in this 
        protocol (LBCC, LBCC54, EZCCA, EZCCAT).
"""

import docopt
import dirty_water
from nonstdlib import *

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()

if args['--materials']:
    protocol += """\
Prepare the following reagents:

Reagent  Description
───────────────────────────────────────────
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

Overnight volume, media volume:

- Subculture 20 μL of each control into 50 volumes 
  (i.e. 1 mL) EZCCA and EZCCAT.

- Grow at 37°C for at least 9h."""

protocol += """\
Dilute each culture into PBS.

- Measure the OD600 of the library using the 
  nanodrop.

- Work out how to dilute the library given that 2 
  mL of sample lasts about 1h and that an OD600 of 
  1.93×10⁻³ corresponds to an event rate of about 
  1000 cells/sec (on the FACSAria II with the flow 
  rate set to "1.0").

Planned event rate, sort time:

Culture volume, PBS volume:

- Dilute 1 μL of each other culture into 1 mL 
  PBS."""

protocol += """\
Sort the library.

- Keep the cells at room temperature before and 
  after the sort.

- Put 1 mL SOC in each collection tube.

- Record data for the controls to make sure the 
  cells are halthy and to help draw the gates.

- Record data for the library with and without 
  theophylline to track the progress of the 
  screen.

Gate:
   
- Dilute the collected cells and the controls 
  in 4 volumes LBCC54.  Grow overnight at 37°C."""

for i in range(3):
    protocol += """\
Grow the library and the controls as above.

Overnight volume, media volume:"""

    protocol += """\
Dilute the cultures as above.

Planned event rate, sort time:

Culture volume, PBS volume:"""

    protocol += """\
Sort the library as above.

Gate:"""

print(protocol)

# vim: tw=50
