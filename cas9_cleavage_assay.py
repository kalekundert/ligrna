#!/usr/bin/env python3
# encoding: utf-8

"""\
Display a protocol for running the given number of Cas9 cleavage reactions. 

Usage:
    ./cas9_master_mix.py <reactions> [options]

Options:
    -x --extra <percent>                [default: 10]
        How much extra master mix to create.

    -r --robot
        Display the protocol for having the Eppendorf liquid handling robot
        setup and carry out the Cas9 reaction.

    -D --short-dna
        Use the 500 bp target DNA instead of the 4 kb target DNA.

    -B --big-rxns
        Make each reaction 30 μL rather than 15 μL, as recommended by NEB.

    -f --fresh-theo
        Include a step for preparing fresh theophylline, if you've run out of
        frozen stocks.

    -C --cas9-stock-conc <μM>           [default: 1.0]
        The stock Cas9 concentration (in μM).

    -c --cas9-conc <fold>               [default: 1.0]
        The working concentration of Cas9 will be the standard amount times 
        this argument.

    -l --ligand-conc <fold>             [default: 1.0]
        The working concentration of ligand will be the standard amount times 
        this argument.

    -s --sgrna-conc <fold>              [default: 1.0]
        The working concentration of sgRNA will be the standard amount times 
        this argument.

    -d --dna-conc <fold>                [default: 1.0]
        The working concentration of DNA will be the standard amount times 
        this argument.

"""

import docopt
import dirty_water

## Parse the command line arguments.

args = docopt.docopt(__doc__)
using_robot = args['--robot']
num_reactions = eval(args['<reactions>'])
num_sgrnas = num_reactions // 2

## Calculate how much of each reagent will be needed.

cas9_rxn = dirty_water.Reaction('''\
Reagent    Conc  Each Rxn  Master Mix
=======  ======  ========  ==========
water             10.1 μL         yes
buffer      10x    3.0 μL         yes
Cas9       1 μM    0.9 μL         yes
ligand    30 mM   10.0 μL
sgRNA    300 nM    3.0 μL
DNA       30 nM    3.0 μL
''')

cas9_rxn.num_reactions = eval(args['<reactions>'])
cas9_rxn.extra_master_mix = args['--extra']
cas9_rxn['Cas9'].stock_conc = args['--cas9-stock-conc']
cas9_rxn['Cas9'].conc *= float(args['--cas9-conc'])
cas9_rxn['ligand'].conc *= float(args['--ligand-conc'])
cas9_rxn['sgRNA'].conc *= float(args['--sgrna-conc'])
cas9_rxn['DNA'].conc *= float(args['--dna-conc'])

kag_rxn = dirty_water.Reaction('''\
Reagent       Conc  Each Rxn  Master Mix
============  ====  ========  ==========
Orange G        6x   5.64 μL         yes
RNase A       200x   0.18 μL         yes
Proteinase K  200x   0.18 μL         yes
''')

kag_rxn.num_reactions = num_reactions
kag_rxn.show_each_rxn = False
kag_rxn.show_totals = False
kag_rxn.extra_master_mix = 2 * float(args['--extra'])

if not args['--big-rxns'] and not args['--short-dna']:
    cas9_rxn.volume /= 2
    kag_rxn.volume /= 2

## Setup the reagents.

protocol = dirty_water.Protocol()

if args['--fresh-theo']:
    protocol += """\
Prepare a 30 mM solution of theophylline:

Reagent        Amount
─────────────────────
theophylline   x≈5 mg
water         185x μL

Vortex and incubate at 37°C to dissolve.  Use 
immediately or store at -20°C."""

protocol += """\
Thaw the water, theophylline, 10x Cas9 buffer, 
and target DNA on the 37°C heat block.  Thaw the 
sgRNAs at room temperature, then refold them by
incubating at 95°C for 3 min then 4°C for 1 min."""

## Setup the Cas9 reactions (using the robot).

if using_robot:
    # Prepare the Cas9 master mix.

    protocol += """\
Prepare the Cas9 master mix:

{cas9_rxn}"""

    # Put everything into the robot.

    protocol += """\
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
    top left down, skipping every other column."""

    # Setup the Cas9 reactions.

    protocol += """\
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
pipetted for each step."""

## Setup the Cas9 reactions (by hand).

else:
    # Setup the Cas9 reactions.

    protocol += """\
Setup {num_reactions} Cas9 reactions:

{cas9_rxn}

- Add {cas9_rxn[ligand].volume_str} water or ligand to each reaction.

- Add {cas9_rxn[sgRNA].volume_str} sgRNA to each reaction.

- Add {cas9_rxn[master mix].volume_str} Cas9 master mix to each reaction.

- Incubate at room temperature for 10 min.

- Add {cas9_rxn[DNA].volume_str} DNA to each reaction."""

## Run the Cas9 reactions.

protocol += """\
Incubate at 37°C for 1 hour (thermocycler)."""

## Quench the Cas9 reactions.

protocol += """\
Add {kag_rxn.volume:.1f} μL 6x KAG master mix to each reaction:
    
{kag_rxn}"""

protocol += """\
Incubate the reactions at 37°C for 20 min, then at 
55°C for 20 min, then hold at 12°C (thermocycler)."""

## Analyze the products.

if args['--short-dna']:
    gel_load = 36
    gel_percent = 2
else:
    gel_load = 18
    gel_percent = 1

protocol += """\
Load {} μL on a {}% agarose/TAE/GelRed gel and run 
at 130V for 45 min.""".format(gel_load, gel_percent)

## Print the protocol.

print(protocol)

# vim: tw=50
