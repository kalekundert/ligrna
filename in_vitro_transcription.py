#!/usr/bin/env python3

"""\
Display a protocol for running the given number of in vitro transcription 
reactions using the Epicentre T7-Flash Ampliscribe kit. 

Usage:
    ./in_vitro_transcription.py <reactions> [options]

Options:
    -d --dna MICROLITERS    [default: 1.0]
        How much template DNA to use (in μL).

    -i --incubate HOURS     [default: 1]
        How long to incubate the transcription reaction.

    -x --extra PERCENT      [default: 10]
        How much extra master mix to create.

    -R --no-rntp-mix
        Indicate that each you're not using a rNTP mix and that you need to add 
        each rNTP individually to the reaction.

    -c --cleanup METHOD     [default: zymo]
        Choose the method for removing free nucleotides from the RNA:
        'none': Carry on the crude reaction mix.
        'zymo': Zymo spin kits.
        'ammonium': Ammonium acetate precipitation.
"""

import docopt
import math

args = docopt.docopt(__doc__)
volume = eval(args['<reactions>']) * (1 + float(args['--extra'] or 0) / 100)
scale = lambda ref, name: (ref * volume, name)
dna = float(args['--dna'])

reagents = [
        scale(6.3 - dna, "nuclease-free water"),
        scale(2.0, "10x reaction buffer"),
]
if args['--no-rntp-mix']:
    reagents += [
        scale(1.8, "100 mM ATP"),
        scale(1.8, "100 mM CTP"),
        scale(1.8, "100 mM GTP"),
        scale(1.8, "100 mM UTP"),
    ]
else:
    reagents += [
        scale(7.2, "100 mM rNTP mix"),
    ]
reagents += [
        scale(2.0, "100 mM DTT"),
        scale(0.5, "RiboGuard RNase inhibitor"),
        scale(2.0, "AmpliScribe T7"),
]


total_amount = sum(amount for amount, reagent in reagents)
longest_amount = int(math.ceil(math.log10(total_amount)))

print("""\
1. Setup {} in vitro transcription reaction(s) by 
   mixing the following reagents at room temperature 
   in the order given.
""".format(args['<reactions>']))

print('   T7 Master Mix for {:.1f} reactions'.format(volume))
print('   ' + 30 * '=')
for amount, reagent in reagents:
    row = '{{:{}.1f}} μL  {{}}'.format(longest_amount + 2)
    print('   ' + row.format(amount, reagent))
print('   ' + 30 * '-')
print('   ' + row.format(total_amount, 'total master mix'))
print()
print('   Each T7 Reaction')
print('   ' + 30 * '=')
print('   ' + row.format(total_amount / volume, 'master mix'))
print('   ' + row.format(dna, '10 ng/μL DNA template'))
print("""\

2. Incubate at 42°C (water bath) for {} hour{}.
""".format(args['--incubate'], '' if int(args['--incubate']) == 1 else 's'))
if args['--cleanup'] == 'zymo':
    print("""\
3. Remove unincorporated ribonucleotides using
   Zymo RNA Clean & Concentrator 25 Spin kits.
   Follow the manufacturer's instructions.
""")

elif args['--cleanup'] == 'ammonium':
    print("""\
3. Remove unincorporated ribonucleotides using
   ammonium acetate precipitation.

   Note that ammonium acetate precipitation only 
   works for constructs that are longer than 100 bp.

   Ammonium Acetate Precipitation
   ==============================
   a. Add 1 volume (20 μL) 5M ammonium acetate to 
      each reaction.

   b. Incubate on ice for 15 min.

   c. Centrifuge at >10,000g for 15 min at 4°C.

   d. Wash pellet with 70% ethanol.

   e. Dissolve pellet in 20μL nuclease-free water.
""")

elif args['--cleanup'] == 'none':
    raise SystemExit

else:
    raise ValueError("unknown RNA clean-up method: '{}'".format(args['--cleanup']))

print("""\
4. Nanodrop to determine the RNA concentration.

5. Make 2 22 μL aliquots in PCR tubes, then 
   flash-freeze in liquid N₂ and store at -80°C.
""")

# vim: tw=53
