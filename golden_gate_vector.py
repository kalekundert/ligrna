#!/usr/bin/env python3

import numpy as np
np.random.seed(1000)

golden_gate_enzymes = {
        'BsaI^': 'GGTCTCx',
        '^BsaI': 'xGAGACC',
        'BbsI^': 'GAAGACxx',
        '^BbsI': 'xxGTCTTC',
        'BsmBI^': 'CGTCTCx',
        '^BsmBI': 'xGAGACG',
        'SapI^': 'GCTCTTCx',
        '^SapI': 'xGAAGAGC',
}

def fill_in_sequence(template):
    return ''.join(
            nuc if nuc != 'x' else random_nuc()
            for nuc in template.format(**golden_gate_enzymes))

def random_nuc():
    return np.random.choice(list('atcg'), p=[0.3, 0.3, 0.2, 0.2])


#print(fill_in_sequence('{^BsmBI}' + 22 * 'x' + ' ' + 23 * 'x' + '{BsmBI^}'))

import sgrna_sensor
padding = 20
template = padding * 'x' + '{BsmBI^}' + sgrna_sensor.rx(6, 6, target=None).dna[:-6] + '{^BsmBI}' + padding * 'x'
print(fill_in_sequence(template))
