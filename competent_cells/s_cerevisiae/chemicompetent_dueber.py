#!/usr/bin/env python3

"""\
Transform an sgRNA library into yeast using the Dueber lab's large-scale 
chemicompetent transformation protocol.

Usage:
    chemicompetent_dueber.py [<num_transformations>]
"""

import docopt
import dirty_water
from nonstdlib import plural
from pprint import pprint

args = docopt.docopt(__doc__)
N = int(args['<num_transformations>'] or 12)
day_1 = dirty_water.Protocol()
day_2 = dirty_water.Protocol()

round = lambda x, n: int((x//n + 1) * n)

## Day 1

day_1 += f"""\
Prepare 10 or more 81 cm² selective plates [1]."""

day_1 += f"""\
Make sure your 50% PEG₃₅₀₀ solution is fewer than 
3 months old."""

day_1 += f"""\
Chill the following items and reagents overnight 
in the cold room:

- 2 50 mL pipets
- 1 box 1000 μL pipet tips
- {round(50 * N * 1.25, 10)} mL milliQ water
- {round(5 * N * 1.25, 5)} mL 100 mM LiOAc
- {round(0.36 * N * 1.00, 5)} 1M LiOAc
- {round(2.4 * N * 1.25, 5)} mL 50% PEG₃₅₀₀"""

day_1 += f"""\
Start a {1*N} mL overnight culture in YPD from a 
fresh colony.  Use sterile-filtered YPD, not 
autoclaved YPD [2]."""

print(f"""\
Day 1
=====
{day_1}
""")

## Day 2

day_2 += f"""\
Inoculate {50*N} mL YPD with all {1*N} mL of the 
overnight culture.  The OD should be near 0.2."""

day_2 += f"""\
Incubate the cells at 30°C with shaking at 225 rpm 
in a 1L baffled flask until they reach OD 1.0.  
This should take about 5h."""

noti_ug = N * 10
noti_uL = round(noti_ug / 1.5, 5)
noti_U = noti_ug  # 1U => 1 μg

day_2 += f"""\
Setup a NotI digestion to linearize {N*10} μg of your 
library:

Reagent             Conc       Vol
──────────────────────────────────
Water                     to {noti_uL} μL
Plasmid DNA               {noti_ug:>5d} μg
CutSmart Buffer      10x   {noti_uL/10:.2f} μL
NotI             20 U/μL   {round(noti_U/20, 1):.2f} μL

- Incubate 1h at 37°C, then 20 min at 65°C, then 
  hold at 12°C."""

day_2 += f"""\
Boil {N*100} μL ssDNA:

- Thaw the ssDNA at room temperature.
- Boil for 5 min in a 100°C heat block.
- Cool on ice."""

day_2 += f"""\
Wash the cells:

- Pellet 3270g, 4°C, 5 min.
- Resuspend in {50*N} mL chilled water.

- Pellet 3270g, 4°C, 5 min.
- Resuspend in {5*N} mL 100 mM LiOAc."""

day_2 += f"""\
Setup the transformation:

- Pellet 3270g, 4°C, 5 min.
- Resuspend in chilled water to a final volume of 
  {0.5*N} mL (usually about {0.22*N} mL).

- Add {2.4*N:.2f} mL 50% PEG₃₅₀₀, vortex

- Add {0.360*N:.2f} mL 1M LiOAc, vortex

- Mix the library DNA with the reboiled ssDNA, 
  then add to cells and vortex."""

day_2 += f"""\
Pre-incubate the cells at 30°C with shaking at 225 
rpm for 30 min."""

day_2 += f"""\
Heat shock the cells in a 42°C water bath for 45 
min."""

day_2 += f"""\
Wash and plate the cells:

- Pellet 3270g, 4°C, 5 min.
- Resuspend in 1 mL water.

- Prepare a series of 10x dilutions (e.g. 5 μL 
  cells into 45 μL water) to assess the number of 
  transformants.  Plate 20 μL of each dilution.

- Spread the remaining cells evenly between all 
  the library plates."""

print(f"""\
Day 2
=====
{day_2}
""")

## Footnotes

print(f"""\
Footnotes
=========
[1] The specific number of plates you use isn't 
    very important.  Usually people want to get 
    individual colonies to minimize the bias due 
    to growth competition, but that's not really 
    practical for libraries bigger than 10⁵ (which 
    require about 40 100 cm² plates to get 
    individual colonies).  Since we're aiming for 
    lawns, more plates means less bias but more 
    effort.  I think 10 is a reasonable trade-off.

[2] The original protocol stresses this point, but 
    doesn't explain why.  Autoclaving YPD does cause 
    the sugars in it to caramelize, but it's not 
    clear why this would be a problem.
""")

# vim: tw=50
