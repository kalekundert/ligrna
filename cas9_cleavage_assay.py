#!/usr/bin/env python3
# encoding: utf-8

"""\
Display a protocol for running the given number of Cas9 cleavage reactions. 

Usage:
    ./cas9_master_mix.py <reactions> [options]

Options:
    -s --sgrna MICROLITERS      [default: 3.0]
        How much sgRNA to use (in μL).

    -c --cas9-rxn-conc NANOMOLAR        [default: 30.0]
        The working concentration of Cas9 (in nM)
        How much Cas9 to use (in μL).

    -C --cas9-stock-conc MICROMOLAR     [default: 4.0]
        The stock Cas9 concentration (in μM).

    -d --dna MICROLITERS        [default: 3.0]
        How much target DNA to use (in μL).

    -t --theo MICROLITERS       [default: 10.0]
        How much theophylline to use (in μL).

    -x --extra PERCENT          [default: 10]
        How much extra master mix to create.

    -r --robot
        Display the protocol for having the Eppendorf liquid handling robot
        setup and carry out the Cas9 reaction.

    -f --fresh-theo
        Include a step for preparing fresh theophylline, if you've run out of
        frozen stocks.
"""

import docopt
import math

steps = []

## Parse the command line arguments.

args = docopt.docopt(__doc__)
using_robot = args['--robot']
num_reactions = eval(args['<reactions>'])
num_scaled_reactions = num_reactions * (1 + float(args['--extra'] or 0) / 100)
num_sgrnas = num_reactions // 2

## Calculate how much of each reagent will be needed.

sgrna = float(args['--sgrna'])
cas9_stock_conc = float(args['--cas9-stock-conc'])
cas9_rxn_conc = float(args['--cas9-rxn-conc'])
cas9 = 30 * cas9_rxn_conc / cas9_stock_conc / 1000
dna = float(args['--dna'])
theo = float(args['--theo'])
water = 27 - sgrna - cas9 - dna - theo
cas9_mm = 30 - theo - sgrna - dna

def scale(*reagents):   # (no fold)
    volume_per_reaction = sum(amount for amount, x in reagents)

    if using_robot:
        scaled_volume = num_reactions * volume_per_reaction + 14
    else:
        scaled_volume = num_scaled_reactions * volume_per_reaction

    scaled_reagents = [
            (ref * scaled_volume / volume_per_reaction, name)
            for ref, name in reagents]

    return scaled_reagents, scaled_volume

cas9_reagents, cas9_volume = scale(
        (water, "nuclease-free water"),
        (3.0, "10x reaction buffer"),
        (cas9, "{} μM Cas9 (NEB)".format(cas9_stock_conc)),
)
kag_reagents, kag_volume = scale(
        (0.337, "Proteinase K (Denville)"),
        (3.371, "Buffer P1 with RNase A (Qiagen)"),
        (6.292, "Orange G loading buffer"),
)

def cas9_master_mix():  # (no fold)
    return '\n'.join([
        "Cas9 Master Mix for {} reactions".format(num_reactions),
        35 * '='] + [
        row.format(amount, reagent) for amount, reagent in cas9_reagents] + [
        35 * '-',
        row.format(cas9_volume, "total master mix"),
    ])

def kag_master_mix():   # (no fold)
    return '\n'.join([
        "3x KAG Master Mix for {} reactions".format(num_reactions),
        35 * '='] + [
        row.format(amount, reagent) for amount, reagent in kag_reagents] + [
        35 * '-',
        row.format(kag_volume, "total master mix"),
    ])

max_volume = sum(x for x, y in cas9_reagents + kag_reagents) 
max_digits = int(math.ceil(math.log10(max_volume)))
row = '{{:{}.2f}} μL  {{}}'.format(max_digits + 3)

## Setup the reagents.

if args['--fresh-theo']:
    steps.append("""\
Prepare solutions with and without theophylline.  
Treat both solutions in exactly the same way, just 
don't add theophylline to one:

30 mM Theophylline
===================================
 x≈5 mg  theophylline
185x μL  nuclease-free water

Vortex and incubate at 37°C to dissolve.  Use 
immediately or store at -20°C.
""")

steps.append("""\
Thaw the water, theophylline, 10x Cas9 buffer, 
and target DNA on the 37°C heat block.
""")

steps.append("""\
Thaw the sgRNAs at room temperature, then refold 
them by incubating at 95°C for 2 min.
""")

## Setup the Cas9 reactions (using the robot).

if using_robot:
    # Prepare the Cas9 master mix.

    steps.append("""\
Prepare the Cas9 master mix:

{}
""".format(cas9_master_mix()))
    
    # Put everything into the robot.

    steps.append("""\
Load the "kyleb/Cas9 Basic Controls" method and 
setup the robot's worktable:

A2: 50 μL filter tips.

B1: Reagents and master mixes in a tube rack:
    19: water
    20: theophylline
    21: Cas9 master mix
    22: target DNA

B2: 50 μL filter tips.

C1: Empty PCR tubes for each reaction in a 96-well 
    thermoblock.  Fill from the top left down.

C2: sgRNAs in a plastic 96-well rack with a 2 mm 
    cardboard support underneath.  There must be 
    at least 15 μL of each sgRNA.  Fill from the 
    top left down, skipping every other column.
""")

    # Setup the Cas9 reactions.

    steps.append("""\
Run the method.  The robot will setup all the 
reactions.  Answer its questions as follows:

- The number of sgRNAs to test: {num_sgrnas}

- The number of reactions to run: {num_reactions}

- Levelsensor settings:
  [ ] Levels
  [x] Tips
  [ ] Locations

Provide reasonably accurate volumes for all the 
reagents.  The volumes of the Cas9 and KAG master 
mixes are included in this protocol.

Watch to make sure that liquid is actually being 
pipetted for each step.
""".format(**locals()))

## Setup the Cas9 reactions (by hand).

else:
    # Setup the Cas9 reactions.

    steps.append('\n'.join(["""\
Setup {} Cas9 reactions.  Add theophylline, 
sgRNA, and Cas9 master mix in that order to each 
reaction (as appropriate).
""".format(args['<reactions>']),
cas9_master_mix(),
'',
'Each Cas9 Reaction',
35 * '=',
row.format(theo, "30 mM theophylline (or water)"),
row.format(sgrna, "300 nM sgRNA (or water)"),
row.format(cas9_mm, 'Cas9 mix (or 3 μL buffer + {:g} μL water)'.format(cas9_mm - 3)),
35 * '-',
row.format(dna, "30 nM target DNA (or water)"),
'',
]))
    steps.append("""\
Incubate at room temperature for 10 min.
""")
    steps.append("""\
Add target DNA (as appropriate) to each reaction.
""")

## Run the Cas9 reactions.

steps.append("""\
Incubate at 37°C for 1 hour (thermocycler).
""")

## Quench the Cas9 reactions.

steps.append("""\
Prepare 3x KAG master mix just before the 
reaction finishes:

{}
""".format(kag_master_mix()))

if using_robot:
    steps.append("""\
Put the KAG master mix in position B1-23 when the 
robot asks for it, then finish running the method.
The robot will add the mix to each reaction.
""")

else:
    steps.append("""\
Add 10 μL 3x KAG master mix to each reaction.  
""")

steps.append("""\
Incubate the reactions at 37°C for 20 min, then at 
55°C for 20 min, then hold at 12°C (thermocycler).
""") 

## Analyze the products.

steps.append("""\
Load on a 2% agarose/TAE/GelRed gel and run at 
100V for 1 hour.""")

## Print the protocol.

from textwrap import indent

for i, step in enumerate(steps, 1):
    number = "{}. ".format(i)
    padding = ' ' * len(number)
    step = indent(number + step, ' ' * len(number)).lstrip()
    print(step)


# vim: tw=50
