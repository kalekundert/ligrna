#!/usr/bin/env python3

import bio96
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from sgrna_sensor.style import pick_color, pick_style, FoldChangeLocator

def load(toml_path, query=None, aggregate=None, genes=None):
    toml_path = Path(toml_path)

    def biorad(path):
        df = pd.read_csv(path / 'Quantification Cq Results.csv')
        df = df.rename({'Well': 'well0', 'Cq': 'cq'}, axis='columns')
        return df[['well0', 'cq']]
        
    def applied_biosystems(path):
        df = pd.read_excel(path, sheet_name='Results', header=43)
        df = df.dropna(thresh=3)
        df = df.rename({'Well Position': 'well', 'CT': 'cq'})
        return df[['well', 'cq']]

    with toml_path.open() as f:
        first_line = f.read().lower()

    if "applied biosystems" in first_line:
        load_unlabeled_cq = applied_biosystems
        merge_cols = {'well': 'well'},
    else:  # biorad
        load_unlabeled_cq = biorad
        merge_cols = {'well0': 'well0'}

    df, options = bio96.load(
            toml_path,
            load_unlabeled_cq,
            merge_cols,
            path_guess='{0.stem}/',
    )

    if query:
        n0 = len(df)
        df = df.query(query)
        print(f"Kept {len(df)}/{n0} observations where {query}")

    if aggregate:
        df = calc_cq(df, aggregate)

    if genes:
        df = calc_Δcq(df, genes)

    return df, options

def load_efficiencies(json_path):
    with open(json_path) as f:
        return json.load(f)

def calc_cq(df, attrs):

    def aggregate_cq(df):
        row = pd.Series()
        row['n'] = len(df['cq'])
        row['n_nan'] = df['cq'].isnull().sum()
        row['cq_mean'] = df['cq'].mean()
        row['cq_median'] = df['cq'].median()
        row['cq_min'] = df['cq'].min()
        row['cq_max'] = df['cq'].max()
        row['cq_std'] = df['cq'].std()
        return row

    return df.groupby(attrs).apply(aggregate_cq)

def calc_Δcq(cq, genes):
    x = cq.loc[genes['expt']]
    x0 = cq.loc[genes['ref']]

    df = pd.DataFrame(index=x.index)
    df['Δcq_mean'] = x['cq_mean'] - x0['cq_mean']
    df['Δcq_median'] = x['cq_median'] - x0['cq_median']
    # https://stats.stackexchange.com/questions/112351/standard-deviation-after-subtracting-one-mean-from-another
    # https://stats.stackexchange.com/questions/25848/how-to-sum-a-standard-deviation
    df['Δcq_std'] = np.sqrt(x['cq_std']**2 + x0['cq_std']**2)

    # Assume perfect efficiency (i.e. 2).  If the reference and target genes 
    # have very different efficiencies, I might need to use the Pfaffl method.
    df['fold_change'] = 2**(-df['Δcq_mean'])
    df['fold_change_bound'] = 2**(-df['Δcq_mean'] + df['Δcq_std'])
    df['fold_change_err'] = df['fold_change_bound'] - df['fold_change']

    return df

def plot_Δcq(df):
    def iter_keys():
        for sgrna in ['on', 'off', '11', '30']:
            for time in [30, 60, 90, 120]:
                for ligand in [False, True]:
                    yield sgrna, time, ligand

    def name_from_key(key):
        sgrna, time, ligand = key
        return f"{sgrna} {time} ({'holo' if ligand else 'apo'})"

    fig, ax = plt.subplots(1, figsize=(6, 4))

    xticks = []
    xtick_labels = []

    for i, key in enumerate(iter_keys()):
        row = df.loc[key]
        sgrna, time, ligand = key
        sgrna = {'on': 'on', 'off': 'off', '11': 'rxb/11/1', '30': 'mhf/30'}[sgrna]

        fold_change = 2**(-row['Δcq_mean'])
        fold_change_bound = 2**(-row['Δcq_mean'] + row['Δcq_std'])
        fold_change_err = fold_change_bound - fold_change

        x = [i, i]
        y = [0, fold_change]
        style = dict(
                linewidth=5,
                color=pick_color(sgrna),
        )
        ax.plot(x, y, **style)

        x = x[-1:]
        y = y[-1:]
        y_err = [fold_change_err]
        style = dict(
                ecolor=pick_color(sgrna),
                capsize=2.5,
        )
        ax.errorbar(x, y, y_err, **style)

        xticks.append(i)
        xtick_labels.append(name_from_key(key))

    ax.set_ylabel('GFP Expression\n[rel. to 16S rRNA]')
    ax.set_xlim(xticks[0] - 0.5, xticks[-1] + 0.5)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, rotation='vertical')
    ax.grid(axis='y')
    #ax.yaxis.set_major_locator(FoldChangeLocator())

    fig.tight_layout(pad=0)

    return fig
