#!/usr/bin/env python3
# encoding: utf-8

"""\
Usage:
    library_prep.py <num_libraries> [options]

Options:
    -t --annealing-temp <celsius>
        The annealing temperature for the PCR reaction.  I typically use NEB's 
        online "Tm Calculator" to determine this setting.
"""

import docopt
import dirty_water

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
num = int(eval(args['<num_libraries>']))
s = 's' if num > 1 else ''

## PCR cloning

ta = (args['--annealing-temp'] or '__') + '°C'
pcr_rxn = dirty_water.Reaction('''\
Reagent                Conc  Each Rxn  Master Mix
================  =========  ========  ==========
water                           19 μL         yes
pBLO2 template    100 pg/μL      1 μL         yes
primer mix              10x      5 μL
Q5 master mix            2x     25 μL         yes
''')
pcr_rxn.num_reactions = num + 1
pcr_rxn.extra_master_mix = 0

protocol += """\
Setup {num} PCR reaction{s} and 1 negative control:

{pcr_rxn}"""

protocol += """\
Run the following thermocycler protocol:

98°C → 98°C → {ta} → 72°C → 72°C → 12°C
30s    10s    20s    2min   2min   ∞
      └──────────────────┘
               35x """

## Gel extraction

protocol += """\
Purify the PCR product{s} by gel extraction.

- 1% agarose/TAE/GelRed gel at 130V for 1h.

- For the PE wash step, only do one wash, but let 
  it sit for 5 min.

- Elute in 50 μL water."""

## Ligation

lig_rxn = dirty_water.Reaction('''\
Reagent                Conc  Each Rxn  Master Mix
================  =========  ========  ==========
PCR product       ≈30 ng/μL  50.00 μL
T4 ligase buffer        10x   5.67 μL
T4 ligase          400 U/μL   1.00 μL
''')
lig_rxn.show_master_mix = False

protocol += """\
Setup {num} ligation reaction{s}.

{lig_rxn}"""

protocol += """\
Incubate overnight at 16°C."""

## Transformation

protocol += """\
Desalt and concentrate the ligated DNA using a 
Zymo spin column with the Qiagen buffers:

- Add 285 μL PB to the ligation reaction.

- Transfer to a Zymo spin column.

- Wash with 200 μL PE.

- Wash with 200 μL PE again.

- Elute in 10 μL water."""

protocol += """\
Transform the ligated DNA into Top10 cells by 
electroporation.

- Plate 10⁻³, 10⁻⁴, 10⁻⁵, and 10⁻⁶ dilutions of 
  the transformation, to determine how much of the 
  library was successfully transformed."""

## Miniprep

protocol += """\
Transfer the cells to selective media:

- Pellet the cells by spinning at 1000g for 5 min.

- Resuspend in 5 mL LB + Carb."""

protocol += """\
Grow overnight at 37°C."""

protocol += """\
Miniprep to isolate library plasmid.  Store at 
-20°C until ready for use."""


print(protocol)

# vim: tw=50
