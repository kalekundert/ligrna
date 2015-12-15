#!/usr/bin/env python3

"""\
Run a limited proteolysis assay to qualitatively determine how well an sgRNA 
design is bound by Cas9.

Usage:
    ./limited_proteolysis.py <reactions> [options]

Options:
    -t --timepoints MINUTES          [default: 5,15,30]
        How many timepoints to take (in min).

    -c --cas9-conc MICROMOLAR            [default: 2.0]
        The working concentration of Cas9 (in μM).

    -s --sgrna-excess FOLD               [default: 1.6]
        The molar excess of sgRNA relative to Cas9.

    -C --stock-cas9-conc MICROMOLAR     [default: 20.0]
        The stock Cas9 concentration (in μM).

    -S --stock-sgrna-conc MICROMOLAR    [default: 32.0]
        The stock sgRNA concentration (in μM).

    -x --extra PERCENT                    [default: 10]
        How much extra master mix to create.
"""

import docopt, dirty_water
from nonstdlib import *

## Setup the reaction based on the command-line arguments

args = docopt.docopt(__doc__)
rxn = dirty_water.Reaction('''\
Reagent   Conc  Each Rxn  Master Mix
=======  =====  ========  ==========
water             6.0 μL         yes
buffer     10x    1.0 μL         yes
Cas9     20 μM    1.0 μL         yes
sgRNA    32 μM    1.0 μL
trypsin    10x    1.0 μL
''')

rxn.num_reactions = args['<reactions>']
rxn.extra_master_mix = args['--extra']

rxn['Cas9'].stock_conc = args['--stock-cas9-conc']
rxn['Cas9'].conc = args['--cas9-conc']
rxn['sgRNA'].stock_conc = args['--stock-sgrna-conc']
rxn['sgRNA'].conc = float(args['--sgrna-excess']) * rxn['Cas9'].conc

timepoints = [int(x) for x in args['--timepoints'].split(',')]
timepoints_str = oxford_comma(timepoints)
num_timepoints = len(timepoints)
s = 's' if rxn.num_reactions != 1 else ''

for reagent in rxn:
    reagent.std_volume *= num_timepoints

## Describe how to run the limited proteolysis assay

protocol = dirty_water.Protocol()

protocol += """\
Thaw the sgRNA by incubating at 95°C for 3 min 
then at 4°C for 1 min."""

protocol += """\
Setup the limited proteolysis reaction{s}:

{rxn}

- Mix {rxn[sgRNA]} into {rxn[master mix]}.

- Incubate at room temperature for 10 min.

- Add {rxn[trypsin]} and start the timer."""

if num_timepoints == 1:
    protocol += """\
Incubate each reaction for {timepoints_str} min at room
temperature."""

else:
    protocol += """\
Aliquot each reaction into {num_timepoints} 10 μL reactions.  
Incubate the reactions for {timepoints_str} min
respectively."""

protocol += """\
When each reaction finishes, quench it by adding 
3.30 μL 4x LSB and incubating at 95°C for 5 min."""

protocol += """\
Load all of each reaction onto a 4-20% TGX PAGE 
gel and run at 200V for 40 min."""

print(protocol)

# vim: tw=50
