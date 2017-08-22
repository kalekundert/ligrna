#!/usr/bin/env python3

"""\
Transform an sgRNA library into yeast using the Benatuil electroporation
protocol.

Usage:
    yeast_library_prep.py <num_transformations>
"""

import docopt
import dirty_water
from nonstdlib import plural

args = docopt.docopt(__doc__)
N = int(eval(args['<num_transformations>']))
day_1 = dirty_water.Protocol()
day_2 = dirty_water.Protocol()

## Day 1

ypd_mL = 40 * N
overnight_mL = 0.3 * ypd_mL / 10.0

day_1 += f"""\
Prepare 10 100 cm² selective plates."""

sorbitol_mL = N * (115 + 5)
sorbitol_g = sorbitol_mL * 182.17 / 1000

day_1 += f"""\
Prepare {sorbitol_mL} mL 1M sorbitol:

- {sorbitol_g:.2f} g sorbitol
- water to {sorbitol_mL} mL"""
   
day_1 += f"""\
Reserve {5*N} mL 1M sorbitol (in a falcon tube)."""

day_1 += f"""\
Prepare {115*N} mL "electroporation buffer" with the 
remaining 1M sorbitol:

- {115*N} mL 1M sorbitol
- {115*N} μL 1M CaCl₂
- sterile filter"""

day_1 += f"""\
Chill the following items and reagents overnight 
in the cold room:

- 5 50 mL pipets
- 1 box 1000 μL pipet tips
- {200*N} mL milliQ water
- {115*N} mL "electroporation buffer"""

day_1 += f"""\
Start a {overnight_mL:.1f} mL overnight culture in YPD from a 
fresh colony."""

print(f"""\
Day 1
=====
{day_1}
""")

## Day 2

day_2 += f"""\
Inoculate {ypd_mL} mL YPD with all {overnight_mL} mL of the 
overnight culture.  The OD should be near 0.3."""

day_2 += f"""\
Incubate the cells at 30°C with shaking at 225 rpm 
in a 1L baffled flask until they reach OD 1.6.  
This should take about 5h."""

day_2 += f"""\
Setup a NotI digestion to linearize {N*8} μg of your 
library [1]:

Reagent             Conc       Vol
──────────────────────────────────
Water                     to 20 μL
Plasmid DNA               {N*8:>5d} μg
CutSmart Buffer      10x      2 μL
NotI             20 U/μL      2 μL

- Incubate 1h at 37°C, then 20 min at 65°C, then 
  hold at 12°C."""

day_2 += f"""\
Once the NotI digestion is complete, desalt the 
DNA using drop dialysis.

- Fill a petri dish about halfway (~20 mL) with 
  milliQ water.

- Float a nitrocellulose membrane shiny-side up 
  on the water [2].  Handle the membrane with 
  tweezers and make sure no air gets caught 
  underneath it.  

- Let the membrane sit for 5 min to allow it to 
  completely soak with water.

- Pipet the entire NotI digestion reaction (20 μL) 
  onto the center of the membrane.

- Dialyze for 4h.

- Pipet the droplet off the membrane and into a 
  clean tube."""
 
day_2 += f"""\
Prepare {20*N} mL "conditioning buffer":

- {2*N} mL 1M LiOAc
- {200*N} μL 1 M DTT
- water to {20*N} mL"""

day_2 += f"""\
Wash the cells:

- Pellet 3270g, 4°C, 5 min.
- Resuspend in {50*N} mL chilled water.

- Pellet 3270g, 4°C, 5 min.
- Resuspend in {50*N} mL chilled water again.

- Pellet 3270g, 4°C, 5 min.
- Resuspend in {50*N} mL "electroporation buffer".

- Pellet 3270g, 4°C, 5 min.
- Resuspend in {20*N} mL "conditioning buffer"."""

day_2 += f"""\
Incubate the cells at 30°C for 30 min with shaking 
at 225 rpm."""

day_2 += f"""\
Prepare {10*N} mL "recovery media":

- {5*N} mL YPD
- {5*N} mL 1M sorbitol
- Sterile filter.
- Pre-warm to 30°C."""

day_2 += f"""\
Make {N} aliquots of DNA (the volume of the DNA 
changes during dialysis), then chill the DNA on 
ice along with {N} electroporation cuvettes (with 
2 mm gaps)."""

day_2 += f"""\
Wash the cells again:

- Pellet 3270g, 4C, 5 min.
- Resuspend in {50*N} mL "electroporation buffer".

- Pellet 3270g, 4C, 5 min.
- Add "electroporation buffer" to a final volume 
  of {N*0.4} mL."""

day_2 += f"""\
Pipet once to mix 400 μL of cells with each 
aliquot of DNA, then transfer the mixed cells to 
a chilled cuvette."""
  
day_2 += f"""\
Electroporate each cuvette as follows:

- Voltage: 2500 V
- Capacitance: 25 μF
- Resistance: 200 Ω [3]
- Gap length: 2 mm"""

day_2 += f"""\
Immediately suspend the cells in {10*N} mL "recovery 
media".  Prepare a series of 5x dilutions to 
measure transformation efficiency:

- Pipet 40 μL YPD into each of 5 tubes.
- Dilute 10 μL cells into the first tube and mix 
  well.
- Continue the serial dilution by transferring
  10 μL each time.
- Plate 20 μL of each dilution.
- Incubate the plates at 30°C for 2-3 days."""

day_2 += f"""\
Incubate at 30°C for 1h with shaking at 225 rpm."""

day_2 += f"""\
Spread the transformed yeast across 10 selective 
plates:

- Pellet 3270g, 4C, 5 min.
- Resuspend in 1000 μL selective media.
- Plate 100 μL on each plate."""

print(f"""\
Day 2
=====
{day_2}
""")

## Footnotes

print(f"""\
Footnotes
=========
[1] We're doing {plural(N):? transformation/s}, and the actual 
    insert is only about half of the plasmid, so this 
    corresponds to 4 μg/rxn.  Benatuil et al. tested 
    insert concentrations from 4 μg/rxn to 16 μg/rxn 
    and found that they all gave similar numbers of 
    transformants, so we're sticking to the low end 
    of that range.

[2] The reason for using the nitrocellulose membrane 
    shiny-side up is explained on the Millipore 
    website.  It's helpful but not crucial, so don't 
    worry if you can't really tell which side is the 
    shiny one:

       Most researchers may not even notice that 
       there is a "sidedness" to filters, and, for 
       most applications, orientation will not affect 
       filter performance.  However, membranes do 
       have a slightly asymmetric pore structure: the 
       shiny side of the membrane is the "tighter" 
       side.  In some applications, you can take 
       advantage of this difference by selecting a 
       specific filter orientation.  Membranes should 
       always be used shiny side up for drop dialysis 
       (a buffer exchange technique in which a few 
       drops of DNA or protein are placed on a 0.05 
       or 0.025 μm filter and floated on a buffer 
       solution).  Apply the sample to the shiny side 
       of the filter and float the filter dull side 
       to the buffer.  This measure will enhance 
       buffer exchange and discourage sample loss.  

[3] Benatuil et al. didn't specify a resistance, so I 
    took the 200 Ω resistance parameter from the 
    preset S. cerevisiae protocol on the BioRad 
    electroporator.
""")
  
## Reference
print(f"""\
Reference
=========
Benatuil, Perez, Belk, Hsieh.  An improved yeast 
transformation method for the generation of very 
large human antibody libraries.  Protein Eng Des Sel 
(2010) 23:4:155–159.""")


# vim: tw=50 ts=2 sts=2 sw=2
