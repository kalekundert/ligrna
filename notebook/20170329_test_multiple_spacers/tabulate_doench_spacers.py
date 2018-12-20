#!/usr/bin/env python3

"""\
Make a table of the randomly generated spacer sequences.

Usage:
    tabulate_doench_spacers.py
"""

from os.path import join, dirname
from sgrna_sensor import render_latex_table
from pprint import pprint

fields = []
context = {'fields': fields}
doench_tsv = join(dirname(__file__), 'doench_spacers.tsv')

with open(doench_tsv) as file:
    for line in file:
        d_id, seq, score = line.split()
        id = int(d_id.strip('d'))
        row = 1 + (id - 1) // 8
        col = 1 + (id - 1) % 8
        seq = seq[0:4].lower() + seq[4:24].upper() + seq[24:30].lower()
        score = float(score)

        if id <= 24:
            fields.append((id, row, col, seq, score))

render_latex_table('doench_spacers.tex', context)
