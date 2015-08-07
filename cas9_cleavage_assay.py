#!/usr/bin/env python3
# encoding: utf-8

"""\
Display a protocol for running the given number of Cas9 cleavage reactions. 

Usage:
    ./cas9_master_mix.py <reactions> [options]

Options:
    -s --sgrna MICROLITERS   [default: 3.0]
        How much sgRNA to use (in μL).

    -c --cas9 MICROLITERS    [default: 1.0]
        How much Cas9 to use (in μL).

    -d --dna MICROLITERS     [default: 3.0]
        How much target DNA to use (in μL).

    -t --theo MICROLITERS    [default: 10.0]
        How much theophylline to use (in μL).

    -x --extra PERCENT       [default: 10]
        How much extra master mix to create.

    -r --robot
        Display the protocol for having the Eppendorf liquid handling robot
        setup and carry out the Cas9 reaction.
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
cas9 = float(args['--cas9'])
dna = float(args['--dna'])
theo = float(args['--theo'])
water = 27 - sgrna - cas9 - dna - theo
cas9_mm = 30 - theo - sgrna - dna

def scale(*reagents):   # (no fold)
    volume_per_reaction = sum(amount for amount, x in reagents)
    scaled_volume = num_scaled_reactions * volume_per_reaction

    if using_robot:
        scaled_volume = max(
                scaled_volume,
                num_reactions * volume_per_reaction + 22
        )

    scaled_reagents = [
            (ref * scaled_volume / volume_per_reaction, name)
            for ref, name in reagents]

    return scaled_reagents, scaled_volume

cas9_reagents, cas9_volume = scale(
        (water, "nuclease-free water"),
        (3.0, "10x reaction buffer"),
        (cas9, "1 μM Cas9 (NEB)"),
)
ka_reagents, ka_volume = scale(
        (0.337, "Proteinase K (NEB)"),
        (3.371, "Buffer P1 with RNase A (Qiagen)"),
)

max_volume = sum(x for x, y in cas9_reagents + ka_reagents) 
max_digits = int(math.ceil(math.log10(max_volume)))
row = '{{:{}.2f}} μL  {{}}'.format(max_digits + 2)

## Setup the reagents.

steps.append("""\
Prepare fresh 30 mM theophylline. 

30 mM Theophylline
===================================
 x≈5 mg  theophylline
185x μL  nuclease-free water

Vortex and incubate at 37°C to dissolve.
""")

steps.append("""\
Thaw the sgRNA, then refold it by incubating at 
95°C for 2 min.
""")

## Run the Cas9 reactions (using the robot).

if using_robot:
    # Prepare the Cas9 master mix.

    steps.append('\n'.join([
"Prepare the Cas9 master mix:\n".format(args['<reactions>']),
"Cas9 Master Mix for {} reactions".format(num_reactions),
35 * '='] + [
    row.format(amount, reagent)
    for amount, reagent in cas9_reagents] + [
35 * '-',
row.format(cas9_volume, "total master mix"),
'',
]))
    
    # Put everything into the robot.

    steps.append("""\
Load the "kyleb/Cas9 Basic Controls" method and 
setup the robot's worktable:

A2: 50 μL filter tips.

B1: Reagents and master mixes in a tube rack:
    1: water
    2: theophylline
    3: Cas9 master mix
    4: target DNA

B2: 50 μL filter tips.

C1: Empty PCR tubes for each reaction in a 96-well 
    thermoblock.  Fill from the top left down.

C2: sgRNAs in a plastic 96-well rack with a 2 mm 
    cardboard support underneath.  There must be 
    at least 15 μL of each sgRNA.  Fill from the 
    top left down.
""")

    # Run the Cas9 reactions.

    steps.append("""\
Run the method.  Answer the robot's questions as 
follows:

- The number of sgRNAs to test: {num_sgrnas}

- The number of reactions to test: {num_reactions}

- Levelsensor settings:
  [ ] Levels
  [x] Tips
  [ ] Locations

- Fill in volumes for each reagent.  Specify the 
  minimum values for the Cas9 and KA mixes.  Make 
  sure everything else agrees with the defaults.

Watch to make sure that liquid is actually being 
pipetted for each step.
""".format(**locals()))

    # Quench the Cas9 reactions.

    steps.append('\n'.join(["""\
Just before the 1 hour 37°C incubation finishes, 
prepare the KA master mix:
""",
"≈9x KA Master Mix for {} reactions".format(num_reactions),
35 * '='] + [
    row.format(amount, reagent)
    for amount, reagent in ka_reagents] + [
35 * '-',
row.format(ka_volume, "total master mix"),
'',
]))
    steps.append("""\
Put the KA master mix in position B1-5 when the 
robot asks for it, then finish running the method.
""")

## Run the Cas9 reactions (by hand).

else:
    # Setup the Cas9 reactions.

    steps.append('\n'.join(["""\
Setup {} Cas9 reactions.  Add theophylline, 
sgRNA, and Cas9 master mix in that order to each 
reaction (as appropriate).
""".format(args['<reactions>']),
'Cas9 Master Mix for {:.1f} reactions'.format(num_scaled_reactions),
35 * '='] + [
    row.format(amount, reagent)
    for amount, reagent in cas9_reagents] + [
35 * '-',
row.format(cas9_volume, 'total master mix'),
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

    # Run the Cas9 reactions.

    steps.append("""\
Incubate at 37°C for 1 hour.
""")

    # Quench the Cas9 reactions.

    steps.append('\n'.join(["""\
Add 3.7 μL of ≈9x KA master mix to each 
reaction.  Prepare immediately before adding:
""",
"≈9x KA Master Mix for {:.1f} reactions".format(num_scaled_reactions),
35 * '='] + [
    row.format(amount, reagent)
    for amount, reagent in ka_reagents] + [
'',
]))
    steps.append("""\
Incubate at 37°C for 20 min, then at 55°C for 20
min, then hold at 12°C.
""") 

## Analyze the reactions.

steps.append("""\
Add 6.3 μL 6x Orange G loading buffer to each 
reaction.  Flick to mix and spin to collect.
""")

steps.append("""\
Load on a 2% TAE/agarose/GelRed gel and run at 
100V for 1 hour.""")

## Print the protocol.

from textwrap import indent

for i, step in enumerate(steps, 1):
    number = "{}. ".format(i)
    padding = ' ' * len(number)
    step = indent(number + step, ' ' * len(number)).lstrip()
    print(step)


# vim: tw=50
