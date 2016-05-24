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

## Inverse PCR

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

## Top10 transformation

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

- For each aliquot you're transforming, chill an 
  electroporation cuvette and 1 μg of DNA on ice.  
  Pre-warm 1 mL SOC and an LB + Carb plate.

- Thaw the competent cells on ice for ~10 min.

- Pipet once to mix the cells with the DNA, then 
  load into the cuvette.  Tap to remove bubbles.

- Shock at 1.8 kV with a 5 ms decay time (for 
  cuvettes with a 1 mm gap).

- Immediately add 1 mL pre-warmed SOC.  If you're 
  transforming multiple aliquots of cells with the 
  same DNA, combine them.

- Before recovering, plate several 10x dilutions 
  of cells (e.g. from 10⁻³ to 10⁻⁶) to count how 
  many were transformed.

- Recover at 37°C for 1h.
  
- Add 4 volumes LB + 5/4x Carb and grow overnight 
  at 37°C."""

## Miniprep

protocol += """\
Miniprep to isolate library plasmid.

- Make a glycerol stock.

- Miniprep 4 mL of overnight culture.  The yield 
  should be ~400 ng/μL.

- Elute in 50 μL water."""

protocol += """\
If necessary, combine libraries in proportion to 
the number of unique members in each."""

## MG1655 transformation

protocol += """\
Transform the combined library into MG1655 cells 
by electroporation.

- It's best to do the transformation immediately, 
  so as much of the DNA as possible will be 
  supercoiled.  With MG1655 (but not Top10) cells, 
  I find that supercoiled DNA gives 100x more 
  transformants than relaxed DNA.

- Use the transformation protocol described above, 
  but use Carb + Chlor instead of just Carb."""

## Glycerol stock

protocol += """\
Store the library as a glycerol stock.

- 333 μL 80% glycerol
- 1000 μL overnight culture

- Place at -80°C without snap-freezing."""


print(protocol)

# vim: tw=50
