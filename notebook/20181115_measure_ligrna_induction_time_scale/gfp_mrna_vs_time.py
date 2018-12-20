#!/usr/bin/env python3

"""\
Usage:
    gfp_mrna_vs_time.py <toml> [options]

Arguments:
    <toml>
        A path to a TOML file describing the layout of a qPCR plate.  See 
        https://pypi.org/project/bio96/ for more details.

Options:
    -o --output <path>
        Save the plot to the given path.  The file type will be inferred from 
        the extension.  '$' will be replaced with the name of the input TOML 
        file (minus the extension).

    -O --output-size <width,height>
        Specify what the width and height of the resulting figure should be, in 
        inches.  The two numbers must be separated by an 'x'.

    -x --drop-outliers
        Remove any data points labeled as outliers.

    -H --horizontal
        Arrange the two subplots horizontally, rather than vertically.
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

def load_data(toml_path, drop_outliers):
    attrs = ['primers', 'sgrna', 'ligand', 'time']
    query = 'outlier == False' if drop_outliers else None
    genes = dict(expt='gfp', ref='16s')
    df, _ = qpcr.load(toml_path, query=query, aggregate=attrs, genes=genes)
    df.reset_index(level='time', inplace=True)

    minutes = df['time'].apply(lambda x: x.minute + x.second/60)
    df.insert(loc=1, column='minutes', value=minutes)

    return df

def plot_timecourses(df, *args, **kwargs):
    sgrnas = 'mhf/30', 'rxb/11/1'
    ligands = 'apo→apo', 'apo→holo', 'holo→apo', 'holo→holo'

    fig, axes = create_axes(*args, **kwargs)

    for ax, sgrna in zip(axes, sgrnas):
        for ligand in ligands:
            plot_timecourse(ax, df, sgrna, ligand)

    return fig

def plot_timecourse(ax, df, sgrna, ligand):
    lig0 = ligand.split('→')[0]

    try:
        q0 = df.loc[sgrna, lig0]
        q1 = df.loc[sgrna, ligand]
        q = pd.concat([q0, q1])
    except KeyError:
        return

    x = q['minutes']
    y = q['fold_change']

    std = q['fold_change_err']
    x_err = np.array([x, x])
    y_err = np.array([y + std/2, y - std/2])

    styles = {
            'apo→apo':   pick_style('control', 0, color_controls=True),
            'apo→holo':  pick_style(sgrna,     1, color_controls=True),
            'holo→apo':  pick_style(sgrna,     0, color_controls=True),
            'holo→holo': pick_style('control', 1, color_controls=True),
    }
    style = styles[ligand]

    ax.semilogy(x, y, **style)
    ax.semilogy(x_err, y_err, marker='_', **style)

def create_axes(output_size, horz=False):
    vert = not horz

    fig, axes = plt.subplots(
            nrows=2 if vert else 1,
            ncols=1 if vert else 2,
            figsize=output_size or ((3, 4) if vert else (6, 2)),
            sharex=True,
            sharey=horz,
    )

    for ax in axes: ax.set_ylim(3e-3,4e-1)
    for ax in axes: ax.set_xlim(0, 30)

    if vert:
        axes[1].set_xlabel("time (min)")
        for ax in axes: ax.set_ylabel("GFP mRNA")
    else:
        for ax in axes: ax.set_xlabel("time (min)")
        axes[0].set_ylabel("GFP mRNA")

    fig.tight_layout(pad=0, w_pad=0.4, h_pad=0.4)

    return fig, axes


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    toml_path = Path(args['<toml>'])
    output_size = [float(x) for x in args['--output-size'].split('x')] \
            if args['--output-size'] else None

    df = load_data(toml_path, args['--drop-outliers'])
    fig = plot_timecourses(df, output_size, args['--horizontal'])

    if args['--output']:
        path = args['--output'].replace('$', toml_path.stem)
        fig.savefig(path)
        print("Figure saved to:", path)
    else:
        plt.show()
