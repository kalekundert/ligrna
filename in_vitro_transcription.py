#!/usr/bin/env python3

"""\
Display a protocol for running the given number of in vitro transcription 
reactions.

Usage:
    ./in_vitro_transcription.py <reactions> [options]

Options:
    -d --dna MICROLITERS    [default: 1.0]
        How much template DNA to use (in μL).

    -k --kit BRAND   [default: hiscribe]
        Which in vitro transcription kit to use.  Valid options are 'hiscribe'
        and 'ampliscribe'.

    -i --incubate HOURS
        How long to incubate the transcription reaction.  The default depends
        on which kit you're using.

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

## Calculate reagent volumes.

args = docopt.docopt(__doc__)
volume = eval(args['<reactions>']) * (1 + float(args['--extra'] or 0) / 100)
scale = lambda ref, name: (ref * volume, name)
dna = float(args['--dna'])

if 'hiscribe'.startswith(args['--kit'].lower()):
    incubation_time = args['--incubate'] or 4
    incubation_temp = '37'
    reagents = [
            scale(11.0 - dna, "nuclease-free water"),
            scale(1.5, "10x reaction buffer"),
    ]
    if args['--no-rntp-mix']:
        reagents += [
            scale(1.5, "100 mM ATP"),
            scale(1.5, "100 mM CTP"),
            scale(1.5, "100 mM GTP"),
            scale(1.5, "100 mM UTP"),
        ]
    else:
        reagents += [
            scale(6.0, "100 mM rNTP mix"),
        ]
    reagents += [
            scale(1.5, "HiScribe T7 (NEB)"),
    ]
elif 'ampliscribe'.startswith(args['--kit'].lower()):
    incubation_time = args['--incubate'] or 1
    incubation_temp = '42'
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
            scale(2.0, "AmpliScribe T7 (Epicentre)"),
    ]
else:
    print("Unknown in vitro transcription kit: '{}'".format(args['--kit']))
    print("Known kits are: 'hiscribe' or 'ampliscribe'")
    raise SystemExit

total_amount = sum(amount for amount, reagent in reagents)
longest_amount = int(math.ceil(math.log10(total_amount)))

## Run the reactions.

print("""\
1. Setup {} in vitro transcription reaction(s) by 
   mixing the following reagents at room temperature 
   in the order given.
""".format(args['<reactions>']))

print('   T7 Master Mix for {:.1f} reactions'.format(volume))
print('   ' + 30 * '=')
for amount, reagent in reagents:
    row = '{{:{}.2f}} μL  {{}}'.format(longest_amount + 3)
    print('   ' + row.format(amount, reagent))
print('   ' + 30 * '-')
print('   ' + row.format(total_amount, 'total master mix'))
print()
print('   Each T7 Reaction')
print('   ' + 30 * '=')
print('   ' + row.format(total_amount / volume, 'master mix'))
print('   ' + row.format(dna, '10 ng/μL DNA template'))
print("""\

2. Incubate at {}°C (thermocycler) for {} hour{}.
""".format(
    incubation_temp,
    incubation_time, '' if int(incubation_time) == 1 else 's'))

## Clean up the reactions.

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

5. Dilute (if desired) enough sgRNA to make several 
   15 μL aliquots.  Keep any left-over RNA undiluted.  
   Flash-freeze in liquid N₂ and store at -80°C.
""")

# vim: tw=53
