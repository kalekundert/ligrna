#!/usr/bin/env python3

from sgrna_sensor import from_name
from itertools import product

spacers = 'fol1', 'fol2', 'fol3', 'fol4'
names = 'on', 'off', 'rxb/11/1', 'mhf/30'
overlap_5 = 'tgcgactactcttgcctactacctatcgactgagctgaaagaattccggttctggcaaatattctgaaatgagctgttgacaattaatcatccggctcgtataattctagt'
overlap_3 = 'tttgaattcatgtggctgaccgttctgttgtctctcgctcttccgagta'

inserts = []
longest_insert = 0
pretty_names = {
        'on': 'pos',
        'off': 'neg',
        'rxb/11/1': 'ligRNA⁻',
        'mhf/30':   'ligRNA⁺',
}

for spacer, name in product(spacers, names):
    sgrna = from_name(name, target=spacer)
    insert = overlap_5 + sgrna.dna + overlap_3
    longest_insert = max(longest_insert, len(insert))
    pretty_name = f'{spacer} {pretty_names.get(name, name)}'
    inserts.append((pretty_name, insert))

print(f'Longest insert: {longest_insert} bp')

with open('gibson_inserts.tsv', 'w') as file:
    for insert in inserts:
        file.write('\t'.join(insert) + '\n')


