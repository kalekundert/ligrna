#!/usr/bin/env python3

"""\
Display a protocol for running the given number of in vitro transcription 
reactions using the Epicentre T7-Flash Ampliscribe kit. 

Usage:
    ./in_vitro_transcription.py <reactions> [--zymo | --ammonium] [options]

Options:
    -d --dna MICROLITERS   [default: 1.0]
        How much template DNA to use (in μL).

    -x --extra PERCENT     [default: 10]
        How much extra master mix to create.

    --zymo
        Use the Zymo spin cleanup kits to purify RNA.

    --ammonium
        Use ammonium acetete precipitation to purify RNA.
"""

import docopt
import math

args = docopt.docopt(__doc__)

# Set Zymo kit extraction to be the default
# Note to Kale: is there a better way to set this default in docopt directly?
if not args['--zymo'] and not args['--ammonium']:
    args['--zymo'] = True

volume = eval(args['<reactions>']) * (1 + float(args['--extra'] or 0) / 100)
scale = lambda ref, name: (ref * volume, name)
dna = float(args['--dna'])

reagents = [
        scale(6.3 - dna, "nuclease-free water"),
        scale(2.0, "10x reaction buffer"),
        scale(1.8, "100 mM ATP"),
        scale(1.8, "100 mM CTP"),
        scale(1.8, "100 mM GTP"),
        scale(1.8, "100 mM UTP"),
        scale(2.0, "100 mM DTT"),
        scale(0.5, "RiboGuard RNase inhibitor"),
        scale(2.0, "AmpliScribe T7"),
]

total_amount = sum(amount for amount, reagent in reagents)
longest_amount = int(math.ceil(math.log10(total_amount)))

print("""\
1. Setup {} in vitro transcription reactions.
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
print("\n2. Incubate at 42°C (water bath) for 1 hour.\n")

if args['--zymo']:
    print("""\
3. Remove unincorporated ribonucleotides using
   Zymo RNA Clean & Concentrator 25 Spin kits.

   Zymo Clean & Concentrator 25 Kit
   ================================
   Follow the manufacturer's instructions.
""")

elif args['--ammonium']:
    print("""\
3. Remove unincorporated ribonucleotides using
   ammonium acetate precipitation.

   Ammonium acetate precipitation is much cheaper, 
   but takes a little longer and only works for 
   constructs that are longer than 100 bp.

   Ammonium Acetate Precipitation
   ==============================
   a. Add 1 volume (20 μL) 5M ammonium acetate to 
      each reaction.

   b. Incubate on ice for 15 min.

   c. Centrifuge at >10,000g for 15 min at 4°C.

   d. Wash pellet with 70% ethanol.

   e. Dissolve pellet in 20μL nuclease-free water.
""")

print("""\
4. Nanodrop to determine the RNA concentration.

5. Dilute each reaction to 300 nM.  Calculate recipes
   using the `sgrna_to_300nM.py` script.

6. Make ~8 30 μL aliquots in a strip of PCR tubes, 
   then flash-freeze in liquid N₂ and store at -80°C.
""")

# vim: tw=53
