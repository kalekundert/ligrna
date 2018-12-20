#!/usr/bin/env python3

import matplotlib.pyplot as plt
from pathlib import Path
from sgrna_sensor import qpcr
from mpl_toolkits.axes_grid1 import make_axes_locatable

toml_path = Path('20181122_optimize_tm_primer_conc_gfp_16s.toml')
df = qpcr.load(toml_path, aggregate=['primer', 'temperature', 'primer_conc'])

def matrix_from_df(df):
    return df.reset_index().pivot(
            index='primer_conc',
            columns='temperature',
            values='cq_mean',
    )

def colorbar(mappable):
    # https://joseph-long.com/writing/colorbars/
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.25)
    return fig.colorbar(mappable, cax=cax)

mat_gfp = matrix_from_df(df.loc['gfp'])
mat_16s = matrix_from_df(df.loc['16s'])

fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.set_ylabel('sfGFP\n[Primers] (nM)')
im = ax1.matshow(mat_gfp)
colorbar(im).set_label('Cq', rotation='horizontal', ha='left')

ax2.set_ylabel('16S rRNA\n[Primers] (nM)')
im = ax2.matshow(mat_16s)
colorbar(im).set_label('Cq', rotation='horizontal')

ax1.set_xlabel("Tm (°C)")
ax1.xaxis.set_label_position('top') 
ax1.set_xticklabels([''] + list(mat_gfp.columns))
ax2.set_xticklabels([])
for ax in (ax1, ax2):
    ax.set_yticklabels([''] + list(mat_gfp.index))

fig.tight_layout()
plt.show()

fig.savefig(f'{toml_path.stem}.svg')
