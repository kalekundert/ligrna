#!/usr/bin/env python3

"""\
Make a recipe to create enough master mix for the given number of Epicentre T7 
AmpliScribe Flash in vitro transcription reactions.

Usage:
    ./ampliscribe_master_mix.py <reactions> [options]

Options:
    -x --extra PERCENT
        How much extra master mix to create.
"""

import docopt
import math

args = docopt.docopt(__doc__)
volume = eval(args['<reactions>']) * (1 + float(args['--extra'] or 0) / 100)
scale = lambda ref, name: (ref * volume, name)

reagents = [
        scale(5.3, "nuclease-free water"),
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

print('Master Mix')
print(30 * '=')
for amount, reagent in reagents:
    row = '{{:{}.1f}} μL  {{}}'.format(longest_amount + 2)
    print(row.format(amount, reagent))

print(30 * '-')
print(row.format(total_amount, 'total master mix'))
print()
print('Per Reaction')
print(30 * '=')
print(row.format(total_amount / volume, 'master mix'))
print(row.format(1, '10 ng/μL template'))
