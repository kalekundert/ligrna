#!/usr/bin/env python3

import re
from sgrna_sensor import dna_reverse_complement

seq = 'ATGGCACGACCGCTGGCGATGATCGCCGCCCTTGGCGAGAACCGCGCGATCGGCATCGACAACCGCCTGCCCTGGCGCCTGCCGGCCGACCTCAAGCATTTCAAGGCGATGACCCTCGGCAAGCCGGTGATCATGGGGCGCAAGACCTGGGACTCGCTGGGTCGGCCGCTGCCGGGCCGGCTCAACCTGGTGGTCAGCCGCCAGGCCGGCCTGGCACTGGAGGGTGCGGAAGTGTTCGCCAGCCTGGACGCCGCGCTGGCGCGCGCCGAGGCGTGGGCGCAGGCGGAGGACGCCGACGAACTGATGCTGATCGGCGGCGCCCAGCTCTATGCCGAGGCCTTGCCGCGCGCCGCGCGCCTCTACCTGACCCGGGTGGGCCTGGCGCCGGAAGGCGACGCCTTTTTCCCCGAGATCGATGGCGCGGCCTGGCGCCTGGCGTCGAGCATCGAACACGCCGCGGCTGACGATGCGCCTGCCTACGCCTTCGAGGTATGGGAGCGCCGCTGA'
seq = dna_reverse_complement(seq)

# From the list Jiuxin sent me.  Several of the spacers appear to be in the 
# promoter region, which is not included in the sequence I was sent, so I 
# manually entered them here.  I had to type these sequences by hand, so I 
# should carefully check them for mistakes.
hits = [
        ('TCCACGATGAGGTAACCCCA', 'TGG', 'sense'),
        ('TGGGGTTACCTCATCGTGGA', 'AGG', 'anti'),
        ('GCCATGGGGTTACCTCATCG', 'TGG', 'anti'),
        ('TAACCCCATGGCACGACCGC', 'TGG', 'sense'),
        ('TCGCCAGCGGTCGTGCCATG', 'GGG', 'anti'),
        ('ATCGCCAGCGGTCGTGCCAT', 'GGG', 'anti'),
        ('CATCGCCAGCGGTCGTGCCA', 'TGG', 'anti'),
]
N = len(hits)

for i in range(0, len(seq)-1):
    spacer = seq[i+0:i+20]
    pam = seq[i+20:i+23]
    if pam[1:] == 'GG':
        hits.insert(N, (spacer, pam, 'anti'))

pprint(hits)

with open('folA_spacers.tsv', 'w') as file:
    for i, (spacer, pam, orientation) in enumerate(hits, 1):
        file.write(f'fol{i}\t{spacer}\t{pam}\t{orientation}\n')

