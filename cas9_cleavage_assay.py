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
"""

import docopt
import math

args = docopt.docopt(__doc__)
num_reactions = eval(args['<reactions>'])
master_mix = num_reactions * (1 + float(args['--extra'] or 0) / 100)
scale = lambda ref, name: (ref * master_mix, name)

sgrna = float(args['--sgrna'])
cas9 = float(args['--cas9'])
dna = float(args['--dna'])
theo = float(args['--theo'])
water = 27 - sgrna - cas9 - dna - theo
master_mix = 30 - theo - sgrna - dna

cas9_reagents = [
        scale(water, "nuclease-free water"),
        scale(3.0, "10x reaction buffer"),
        scale(cas9, "1 μM Cas9 (NEB)"),
]
digestion_reagents = [
        scale(3.375, "nuclease-free water"),
        scale(0.375, "Proteinase K (NEB)"),
        scale(3.750, "Buffer P1 with RNase A (Qiagen)"),
]


cas9_volume = sum(amount for amount, x in cas9_reagents)
max_volume = sum(x for x, y in cas9_reagents + digestion_reagents) 
max_digits = int(math.ceil(math.log10(max_volume)))
row = '{{:{}.1f}} μL  {{}}'.format(max_digits + 2)

print("""\
1. Prepare fresh 30 mM theophylline. 

   30 mM Theophylline
   ==============================
      x mg  theophylline
   185x μL  nuclease-free water

   Vortex and incubate at 37°C to dissolve.

2. Thaw the sgRNA, then refold it by incubating at 
   95°C for 2 min.

3. Setup {} Cas9 reactions.  Add theophylline, 
   sgRNA, and Cas9 master mix in that order to each 
   reaction (as appropriate).
""".format(args['<reactions>']))

print('   Cas9 Master Mix for {:.1f} reactions'.format(master_mix))
print('   ' + 30 * '=')
for amount, reagent in cas9_reagents:
    print('   ' + row.format(amount, reagent))
print('   ' + 30 * '-')
print('   ' + row.format(cas9_volume, 'total master mix'))
print()
print('   Each Cas9 Reaction')
print('   ' + 30 * '=')
print('   ' + row.format(theo, "30 mM theophylline (or water)"))
print('   ' + row.format(sgrna, "300 nM sgRNA (or water)"))
print('   ' + row.format(master_mix, 'Cas9 mix (or {} μL water + 3 μL buffer)'.format(master_mix - 3)))
print('   ' + 30 * '-')
print('   ' + row.format(dna, "30 nM target DNA (or water)"))
print("""\

4. Incubate at room temperature for 10 min.

5. Add target DNA (as appropriate) to each reaction.

6. Incubate at 37°C for 1 hour.

7. Add 7.5 μL of 5x digestion mixture to each 
   reaction.  Prepare immediately before adding.
""")
print('   5x Digestion Mixture')
print('   ' + 30 * '=')
for amount, reagent in digestion_reagents:
    print('   ' + row.format(amount, reagent))
print("""\

8. Incubate at 37°C for 20 min, then at 55°C for 20
   min, then hold at 12°C.

9. Add 7.5 μL 6x Orange G loading dye to each
   reaction.  Unlike most other dyes, Orange G 
   doesn't overlap the bands we're interested in.

10. Load on a 2% TAE/agarose/GelRed gel and run at 
    100V for 1 hour.
""")

# vim: tw=53
