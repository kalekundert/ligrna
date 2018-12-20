#!/usr/bin/env python3

"""\
Plot plate reader data titrating TMP in order to determine its MIC in different 
conditions.

Usage:
    plot_tmp_titration.py <toml> [options]

Arguments:
    <toml>
        A TOML-formatted file describing the plate layout.  The file format is 
        described here: https://pypi.org/project/bio96/

Options:
    -o --output PATH
        The path to save the resulting plot.  The extension determines the file 
        format.  If "$" is present in the path,. it will be replaced with the 
        name of the given TOML file (minus the extension).

    -x --explicit-controls
        Show separate plots for the controls.  Without this, the positive and 
        negative controls can't be distinguished expect by how they look.  So 
        if you're not sure the controls worked, use this option.
"""

import docopt
import bio96
import pandas as pd
import sgrna_sensor
from pathlib import Path
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter
from sgrna_sensor import plate_reader, style
from sgrna_sensor.style import pick_style

def pick_linestyle(theo_mM, standard=1):
    if theo_mM == 0:
        return {'linestyle': ':'}
    elif theo_mM == standard:
        return {'linestyle': '-'}
    else:
        return {'linestyle': '--'}

style.pick_linestyle = pick_linestyle


def load_data(toml_path):

    def load_biotek(path):
        expt = plate_reader.BiotekExperiment(path)
        return expt.kinetic[600]

    df, options = bio96.load(
            toml_path, load_biotek, {'well': 'well'},
            path_guess='{0.stem}.xlsx',
    )

    print(f"{df.read.isna().sum()}/{len(df)} data points discarded.")
    return df.dropna(subset=['read'])


def plot_growth_curves(ax, df, sgrnas, ref_theo_mM=1):
    df_sgrnas = df[df.sgrna.isin(sgrnas)]

    for key, sele in df_sgrnas.groupby(['sgrna', 'theo_mM', 'path', 'well']):
        sgrna, theo_mM, well, path = key
        style = pick_style(sgrna, theo_mM, color_controls=True, standard_mM=ref_theo_mM)
        #ax.semilogy(sele.minutes/60, sele.read, **style)

        #time_hr = sele.minutes / 60
        #smoothed_reads = savgol_filter(sele.read, 21, 1)
        sele = sele.sort_values('minutes')
        hours, reads = sele.minutes / 60, sele.read

        ax.semilogy(hours, reads, **style)

def plot_data(df, explicit_controls=True, ref_theo_mM=1):
    tmp_concs = df.groupby(['tmp_ug_mL'])

    fig, axes = plt.subplots(
            len(tmp_concs), 4 if explicit_controls else 2,
            sharex=True, sharey=True,
            figsize=(8.5 if explicit_controls else 6, 1.5 * len(tmp_concs)),
    )

    y_labels = []
    if explicit_controls:
        x_labels = 'on', 'off', 'rxb 11,1', 'mhf 30'
    else:
        x_labels = 'rxb 11,1', 'mhf 30'

    for i, (key, group) in enumerate(tmp_concs):
        y_labels.append(key)
        if explicit_controls:
            plot_growth_curves(axes[i,0], group, ['on'])
            plot_growth_curves(axes[i,1], group, ['off'])
            plot_growth_curves(axes[i,2], group, ['on', 'off', 'rxb/11/1'])
            plot_growth_curves(axes[i,3], group, ['on', 'off', 'mhf/30'])
        else:
            plot_growth_curves(axes[i,0], group, ['pa14'])
            plot_growth_curves(axes[i,0], group, ['on', 'off', 'rxb/11/1'])
            plot_growth_curves(axes[i,1], group, ['on', 'off', 'mhf/30'])
    
    for i, ax in enumerate(axes[0,:]):
        ax.set_title(x_labels[i])
    for ax in axes[-1,:]:
        ax.set_xlabel('time [hr]')
        ax.set_xlim(0, 24)
        ax.set_xticks(range(0, 25, 4))
    for i, ax in enumerate(axes[:,0]):
        ax.set_ylim(df.read.min(), max(1, df.read.max()))
        ax.set_ylabel(f'[TMP]\n{y_labels[i]} µg/mL\n\nOD600')

    fig.tight_layout()

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    toml = Path(args['<toml>'])
    df = load_data(toml)
    plot_data(df, args['--explicit-controls'])

    if args['--output']:
        plt.savefig(args['--output'].replace('$', toml.stem))
    else:
        plt.show()



