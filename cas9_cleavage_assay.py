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
volume = eval(args['<reactions>']) * (1 + float(args['--extra'] or 0) / 100)
scale = lambda ref, name: (ref * volume, name)

sgrna = float(args['--sgrna'])
cas9 = float(args['--cas9'])
dna = float(args['--dna'])
theo = float(args['--theo'])
water = 27 - sgrna - cas9 - dna - theo

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


total_amount = sum(amount for amount, x in cas9_reagents + digestion_reagents)
longest_amount = int(math.ceil(math.log10(total_amount)))
row = '{{:{}.1f}} μL  {{}}'.format(longest_amount + 2)

print("""\
1. Prepare fresh 30 mM theophylline. 

   30 mM Theophylline
   ==============================
      x mg  theophylline
   185x μL  nuclease-free water

   Vortex and incubate at 37°C to dissolve.

2. Setup {} Cas9 reactions.  Add theophylline, 
   sgRNA, and Cas9 master mix in that order to each 
   reaction (as appropriate).
""".format(args['<reactions>']))

print('   Cas9 Master Mix for {:.1f} reactions'.format(volume))
print('   ' + 30 * '=')
for amount, reagent in cas9_reagents:
    print('   ' + row.format(amount, reagent))
print('   ' + 30 * '-')
print('   ' + row.format(total_amount, 'total master mix'))
print()
print('   Each Cas9 Reaction')
print('   ' + 30 * '=')
print('   ' + row.format(theo, "30 mM theophylline (or water)"))
print('   ' + row.format(sgrna, "300 nM sgRNA (or water)"))
print('   ' + row.format(total_amount / volume, 'master mix'))
print('   ' + row.format(dna, "30 nM target DNA"))
print("""\

3. Incubate at room temperature for 10 min.

4. Add target DNA (as appropriate) to each reaction.

5. Incubate at 37°C for 1 hour.

6. Add 7.5 μL of 5x digestion mixture to each 
   reaction.  Prepare immediately before adding.
""")
print('   5x Digestion Mixture')
print('   ' + 30 * '=')
for amount, reagent in digestion_reagents:
    print('   ' + row.format(amount, reagent))
print("""\

7. Incubate at 37°C for 20 min, then at 55°C for 20
   min, then hold at 12°C.

8. Cast a 2% agarose gel.

   2% Agarose Gel (<59 reactions)
   ==============================
   150 mL  1x TAE
     3 g   agarose
    15 μL  10000x GelRed

   Microwave for 90 sec to dissolve.

8. Add 7.5 μL 6x Orange G loading dye to each
   reaction and load the gel.

9. Run the gel at 100V for 1 hour.
""")

# vim: tw=53
