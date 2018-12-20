#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sgrna_sensor.style import pick_style

# There's data in columns 9-12 of the second replicate.  I don't know why, but 
# the data in wells 1-8 seems consistent with the first replicate, so I'm going 
# to keep it.

pd.set_option('display.max_rows', 100000)

def parse_xlsx(path):
    dfs = pd.read_excel(path, sheet_name=None)

    for i, key in enumerate(dfs, 1):
        dfs[key] = dfs[key].transpose()

        # Deal with the temperature "well".
        dfs[key]['temp_c'] = dfs[key].loc['Temperature (C)'][0]
        dfs[key] = dfs[key][dfs[key].index != 'Temperature (C)']

        # Indicate that each sheet is a technical replicate.
        dfs[key]['rep'] = i

    # Combine data from all the sheets.
    df = pd.concat(dfs.values())

    # Give all the columns meaningful names.
    df['well'] = df.index
    df = df.reset_index(drop=True)
    df = df.rename(columns={0: "od600"})

    # Split each well name into a row and a column.
    def parse_well(row):
        row['row'] = row.well[0]
        row['row_i'] = ord(row.row) - ord('A')
        row['col'] = int(row.well[1:])
        row['col_i'] = row.col - 1
        return row

    df = df.apply(parse_well, axis=1)

    return df
    
df = parse_xlsx('20180913_pseudomonas_endpoint_mic.xlsx')

# Indicate how the plates are laid out.

rows = {
        'A': (32.0, 7), # TMP (µg/mL), x-coord
        'B': (16.0, 6),
        'C': ( 8.0, 5),
        'D': ( 4.0, 4),
        'E': ( 2.0, 3),
        'F': ( 1.0, 2),
        'G': ( 0.5, 1),
        'H': ( 0.0, 0),
}
cols = {
        1: ('fol9 on', False),  # construct, theo
        2: ('fol9 on', True),
        3: ('fol1 off', False),
        4: ('fol1 off', True),
        5: ('fol1 rxb 11,1', False),
        6: ('fol1 rxb 11,1', True),
        7: ('fol1 mhf 30', False),
        8: ('fol1 mhf 30', True),
}

def parse_plate(row):
    try:
        row['tmp_ugmL'] = rows[row.row][0]
        row['x'] = rows[row.row][1]
        row['ligrna'] = cols[row.col][0]
        row['theo'] = cols[row.col][1]
    except KeyError:
        pass
    finally:
        return row

df = df.apply(parse_plate, axis='columns').dropna()

# Normalize by the OD600 of the culture with no TMP.

def normalize_od(df):
    df['rel_od600'] = df['od600'] / df['od600'].max()
    return df

df = df.groupby(['col', 'rep']).apply(normalize_od)

# Show the raw data.

def plot_heatmap(ax, df, rep):
    df = df[df.rep == rep]
    img = df.pivot('row', 'col', 'od600')

    ax.matshow(img)

    ax.set_yticks(np.arange(len(img)))
    ax.set_yticklabels(img.index)
    ax.set_xticks(np.arange(len(img.columns)))
    ax.set_xticklabels(img.columns)

reps = sorted(set(df.rep))
fig, axes = plt.subplots(1, len(reps))

for ax, rep in zip(axes.flat, reps):
    plot_heatmap(ax, df, rep)

fig.savefig('20180913_pseudomonas_endpoint_mic_wells.svg')

# Plot the endpoint growth as a function of TMP.

ligrnas = [
        'fol9 on',
        'fol1 off',
        'fol1 rxb 11,1',
        'fol1 mhf 30',
]
titles = {
        'fol9 on': 'positive control\n(different spacer)',
        'fol1 off': 'negative control',
        'fol1 rxb 11,1': 'ligRNA⁻',
        'fol1 mhf 30': 'ligRNA⁺',
}

fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)

for ax, ligrna in zip(axes.flat, ligrnas):
    legend_entries = []

    for theo in [True, False]:
        q = df.query('ligrna == @ligrna and theo == @theo')
        q_mean = q.groupby('well').agg({
            'od600': 'mean',
            'rel_od600': 'mean',
            'x': 'mean',
        })
        trend_style = pick_style(ligrna, not theo)
        trend_style['label'] = '_nolabel_'
        data_style = {
                'linestyle': 'none',
                'marker': 'o',
                'markeredgecolor': 'none' if theo else trend_style['color'],
                'markerfacecolor': trend_style['color'] if theo else 'none',
        }

        ax.set_title(titles[ligrna])
        data, = ax.plot(q.x, q.rel_od600, **data_style)
        trend, = ax.plot(q_mean.x, q_mean.rel_od600, **trend_style)

        legend_entries.append((
                (data, trend),
                '1 mM theo' if theo else '0 mM theo',
        ))

    ax.legend(*zip(*legend_entries), loc='best')

for ax in axes[:,0]:
    ax.set_ylabel('OD600 / max')
for ax in axes[1,:]:
    ax.set_xlabel('TMP (µg/mL)')
    ticks = [0,0.5,1,2,4,8,16,32]
    ax.set_xticks(range(len(ticks)))
    ax.set_xticklabels(ticks)
    ax.set_xlim(0, len(ticks) - 1)

fig.tight_layout()
fig.savefig('20180913_pseudomonas_endpoint_mic.svg')
plt.show()
