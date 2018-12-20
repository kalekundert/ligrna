#!/usr/bin/env python3

"""\
Usage:
    gfp_timecourse.py <toml> [options]

Arguments:
    <toml>
        A path to a TOML file describing the layout of a qPCR plate.  See 
        https://pypi.org/project/bio96/ for more details.

Options:
    -o --output PATH
        Save the plot to the given path.  The file type will be inferred from 
        the extension.  '$' will be replaced with the name of the input TOML 
        file (minus the extension).

    -O --drop-outliers
        Remove any data points labeled as outliers.
"""

import docopt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from inspect import getfullargspec
from numpy import inf
from scipy.optimize import curve_fit
from sgrna_sensor import qpcr
from sgrna_sensor.style import pick_style, pick_data_style

def decay(t, k, y0, y_inf):
    return y0 * 2**(-t/k) + y_inf

def fit_decay(df):
    t = df.index.get_level_values('time')
    y = df['fold_change']

    p0 = 5, max(y), min(y)
    bounds = (
            (0, 0, 0),
            (inf, inf, inf),
    )

    fit_args = getfullargspec(decay).args[1:]
    fit_params, fit_covar = curve_fit(decay, t, y, p0, bounds=bounds)

    col_names = fit_args + [f'{x}_std' for x in fit_args]
    col_values = list(fit_params) + list(np.sqrt(np.diag(fit_covar)))
    return pd.Series(dict(zip(col_names, col_values)))

args = docopt.docopt(__doc__)
toml_path = Path(args['<toml>'])

attrs = ['primers', 'sgrna', 'ligand', 'time']
query = 'outlier == False' if args['--drop-outliers'] else None
df = qpcr.load(toml_path, query=query, aggregate=attrs, reference='16s')

pd.set_option('display.max_rows', 10000)
print(df)

sgrnas = sorted(df.index.get_level_values('sgrna').unique(),
        key=lambda x: ['on', 'off', 'rxb/11/1', 'mhf/30'].index(x))
ligands = sorted(df.index.get_level_values('ligand_after').unique(),
        key=lambda x: [False, True].index(x))
times = df.index.get_level_values('time').unique()

fig, axes = plt.subplots(
        len(ligands),
        len(sgrnas),
        figsize=(4*len(sgrnas), 4*len(ligands)),
        sharex=True,
        squeeze=False,
)

for i, ligand in enumerate(ligands):
    for j, sgrna in enumerate(sgrnas):
        ax = axes[i,j]
        fit_style = pick_style(sgrna, ligand)
        data_style = pick_data_style(sgrna, ligand)

        q = df.loc[sgrna, ligand]

        t = q.index.get_level_values('time')
        y = q['fold_change']

        ax.plot(t, y, label='_', **data_style)

        fit = fit_decay(q)
        t_fit = np.linspace(0, max(t), 500)
        y_fit = decay(t_fit, fit.k, fit.y0, fit.y_inf)
        label = f'''\
k={fit.k:.1e} ± {fit.k_std:.1e}
y0={fit.y0:.1e} ± {fit.y0_std:.1e}
y∞={fit.y_inf:.1e} ± {fit.y_inf_std:.1e}'''

        ax.plot(t_fit, y_fit, label=label, **fit_style)
        ax.legend(loc='best')

for ax in axes[:,0]:
    ax.set_ylabel("GFP mRNA level\n[rel. to 16S rRNA]")
for ax in axes[-1,:]:
    ax.set_xlabel("Time [min]")
for i, ax in enumerate(axes[0,:]):
    ax.set_title(sgrnas[i])
for ax in axes.flat:
    ax.set_xlim(min(times), max(times))

fig.tight_layout()

if args['--output']:
    path = args['--output'].replace('$', toml_path.stem)
    fig.savefig(path)

plt.show()
