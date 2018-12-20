#!/usr/bin/env python3

"""\
Make a table containing all the results from this experiment.

Usage:
    tabulate_everything.py
"""

import docopt
import numpy as np
import pandas as pd
from pathlib import Path
from sgrna_sensor import densiometry, render_latex_table
from pprint import pprint

DATA_DIR = Path(__file__).parent / 'densiometry'
DESIGN_ORDER = 'on', 'off', 'mhf 30', 'rxb 11,1'

def parse_spacers(spacer_order):
    from typing import NamedTuple

    spacers = {}
    tsv_path = Path(__file__).parent / 'doench_spacers.tsv'

    class SpacerInfo(NamedTuple): #
        num: int
        seq: str
        score: float

    with open(tsv_path) as file:
        for line in file:
            key, seq, score = line.split()
            if key not in spacer_order:
                continue

            num = 1 + np.where(spacer_order == key)[0][0]
            seq = seq[0:4].lower() + seq[4:24].upper() + seq[24:30].lower()
            score = float(score)

            spacers[key] = SpacerInfo(num, seq, score)

    return spacers

def get_construct(x):
    names = {
            'on': 'pos',
            'off': 'neg',
            'mhf 30': r'\ligrnaF{}',
            'rxb 11,1': r'\ligrnaB{}',
    }
    return names[x]


args = docopt.docopt(__doc__)

# Parse the densiometry data.
df = densiometry.load_cleavage_data_from_xlsx_dir(DATA_DIR)
df = densiometry.calc_mean_change(df)

# Add NaNs for the experiments that didn't work.
df = df.append({'spacer': 'd9', 'design': 'on'}, ignore_index=True)

# Add a column for the names I want to display.
df = df[df.design.isin(DESIGN_ORDER)]
df['construct'] = df.design.apply(get_construct)

# Put the rows in the order I want to display them in.
spacer_order = densiometry.sort_spacers_by_activity(df, ['mhf 30', 'rxb 11,1'])
df['spacer'] = pd.Categorical(df.spacer, spacer_order)
df['design'] = pd.Categorical(df.design, DESIGN_ORDER)
df = df.sort_values(['spacer', 'design']).reset_index()

n = len(df)//2
context = { #
        'df': df,
        'spacers': parse_spacers(spacer_order),
        'isnull': pd.isnull,
}

render_latex_table('raw_data.tex', context)

