#!/usr/bin/env python3

"""\
Screen a library of sgRNAs with aptamers inserted into them to find designs 
that are sensitive to a small molecule.

Usage:
    library_screen.py [<screens>] [-v]

Options:
    -v --verbose
        Print out the more pedantic details of screening a library, including 
        recipes for the medias used in this protocol (LBCC, LBCC54, EZCCA, 
        EZCCAT), a discussion about gating strategies, and things like that.
"""

import docopt, dirty_water
from nonstdlib import *

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
num_screens = int(args['<screens>'] or 4)

## Media recipes
if args['--verbose']:
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

## Thaw library
protocol += """\
Make overnight cultures for the library and the 
controls.

- Thaw a glycerol stock of MG1655 cells containing 
  the library on ice for ≈10 min.

- Add 1 mL of thawed glycerol stock to 4 mL LBCC.

- Inoculate 5 mL LBCC with stabs from glycerol 
  stocks for the "wt" and "dead" controls.

- Grow all the cultures overnight at 37°C."""

## Grow day cultures
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

## Sort library (first time)
protocol += """\
Sort the library.

- Dilute each culture into PBS to obtain the 
  desired event rate.  Use the --verbose flag for 
  guidance on choosing an event rate.

- Record data for the controls and the library, 
  with and without theophylline.

- Draw a gate and sort the library.  Have 1 mL SOC 
  in each collection tube.  Keep the cells at room 
  temperature before and after the sort.  Use the 
  --verbose flag for guidance on drawing the gate.
  
Condition:                  Gate:

Event rate:                 Sort time:

- Dilute the collected cells and the controls 
  in 4 volumes LBCC54.  Grow overnight at 37°C."""

## Sort library (subsequent times)
for i in range(num_screens - 1):
    protocol += """\
Grow and sort the library as above.  Select for 
the opposite condition as the previous sort.

Overnight volume:           Media volume:

Condition:                  Gate:

Event rate:                 Sort time:"""

## Plate cells
protocol += """\
Plate ≈500 cells to individually test."""


print(protocol)

## How to choose event rates
if args['--verbose']:
    print("""\

How to choose event rates
─────────────────────────
Your first priority is to get ≈10x coverage of 
your library, and your second priority is to 
maximize accuracy by sorting slowly.

- If you cannot reach 10x coverage, sort at the 
  event rate that maximizes sort rate.  This event 
  rate should be near ≈20,000 evt/sec and is 
  defined by the sort efficiency being ≈50%.  
  Further increases in event rate are more than 
  offset by losses in sort efficiency.
  
  If you are sorting a small population (≈1%) at 
  maximum speed, expect error rates of 15% for 
  non-fluorescent cells and 30% for fluorescent 
  cells.  Sort at less than maximum speed if you 
  feel these error rates are prohibitive.

- If you can reach 10x coverage, decide how long 
  you want to sort for and pick an event rate 
  accordingly.  Don't bother going slower than 
  1000 evt/sec, because at that rate the accuracy 
  is already about as good as it'll get.

- If your library doesn't have many members left, 
  just sort at 1000 evt/sec for 10 min.  It's hard 
  to estimate how many unique members remain after 
  several screens, so it's better to do this that 
  to try getting 10x coverage.""")

## How to dilute cells
if args['--verbose']:
    print("""\

How to dilute cells
───────────────────
The following instructions are specific to the 
FACSAria II with a flow rate of "1.0" (≈2 mL/h).
At this flow rate, 1 μL of an overnight culture 
diluted into 1 mL PBS corresponds roughly to an 
event rate of ≈1500 evt/sec.

Using this as a guide, dilute your overnight 
cultures to approximately the right concentration 
in enough PBS to last the duration of your sort.  
If it's important to get the sort rate right (e.g.  
if you're doing a long sort), load the sample into 
the sorter and adjust as necessary.""")

## How to draw gates

if args['--verbose']:
    print("""\

How to draw gates
─────────────────
Your first priority is to find designs that are 
either fully on or fully off without ligand, and 
your second priority is to find designs with the 
biggest possible change in signal in response to 
ligand:

- For screens without ligand, draw gates based on 
  the control population.  You want to be as 
  stringent as possible while collecting at least 
  one survivng cell for each library member that's
  distributed like the control population.
  
  If you will only see each library member once 
  (1x coverage), draw gates that encompass the 
  entire control population.  If you will see 
  each library member ten times (10x coverage), 
  draw gates that include only the most extreme 
  ≈50% of the library.

- For screens with ligand, draw gates based on the 
  most extreme library members.  If you can, draw 
  gates that are ≈5x more populated with ligand 
  than without it. 
  
  Otherwise, you can usually see one population 
  that looks totally on or off and another sparser 
  population that looks slightly less on or off.  
  Draw gates big enough to include the some of the 
  latter.""")


# vim: tw=50
