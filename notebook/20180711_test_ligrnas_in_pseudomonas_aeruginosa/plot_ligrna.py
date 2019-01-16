#!/usr/bin/env python3

"""\
Plot growth curves for ligRNA+ showing theophylline-dependent inhibition of 
DHFR.

Usage:
    plot_tmp_titration.py [<ligrna>...] [options]

Arguments:
    <ligrna>
        The name of the ligRNA to plot.  The default is mhf/30, since it works 
        better, but rxb/11/1 is also a valid option.

Options:
    -o --output PATH
        Path of the image file to save.  '$' will be replaced by the name 
        (without extension) of the TOML file used to load the data.

    -t --time HOURS  [default: 12]
        The time for which to display the MIC curves.  Comma-separated values 
        can be given

    -c --conc UG_ML  [default: 32.0]
        The concentration of TMP (µg/mL) for which to display the growth 
        curves.
"""

import docopt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from plot_tmp_mic import load_data
from sgrna_sensor import style
from sgrna_sensor.style import pick_style
from matplotlib.ticker import StrMethodFormatter, MultipleLocator
from matplotlib.offsetbox import AnchoredText

def pick_linestyle(theo_mM, standard=1):
    if theo_mM == 0:
        return {'linestyle': '--'}
    elif theo_mM == standard:
        return {'linestyle': '-'}
    else:
        raise ValueError(f"[theo] == {theo_mM}, not 0.0 or 1.0")

style.pick_linestyle = pick_linestyle

def plot_mic_curve(ax, df, time_hr=12):

    # Pick a time to display.
    t = df['minutes'].unique()
    dt = abs(t - (60 * time_hr))
    time_min = t[dt.argmin()]

    df = df.query('minutes == @time_min')

    for key, group in df.groupby(['sgrna', 'theo_mM']):
        sgrna, theo_mM = key
        style = pick_style(sgrna, theo_mM, color_controls=True)

        # Drop points with only one measurement.
        q = group.groupby('tmp_ug_mL').filter(lambda x: len(x) > 1)

        reps = q.groupby('tmp_ug_mL')
        concs = reps.apply(lambda x: x.name)
        means = reps.mean()['read']
        stdevs = reps.std()['read']

        ## Growth curves.

        ax.semilogy(
                concs,
                means,
                **style,
        )

        ## Error bars:

        # I can't just use `ax.errorbar()`, because it doesn't have allow the 
        # error bar lines to be styled, and I need the style to distinguish apo 
        # from holo.
        x_err = np.array([concs, concs])
        y_err = np.array([means + stdevs/2, means - stdevs/2])

        if style['color'] == 'black':
            style['linestyle'] = '-'

        ax.semilogy(
                x_err,
                y_err,
                marker='_',
                **style,
        )

    label = AnchoredText(f"{int(time_hr)} hr", loc='upper right')
    ax.add_artist(label)
            
    ax.set_xlabel('TMP (µg/mL)')
    ax.set_xlim(0, 64)
    ax.set_xticks([0, 4, 8, 16, 32, 48, 64])
    #ax.xaxis.set_minor_locator(MultipleLocator(4))

    ax.set_ylabel('OD600')
    ax.set_ylim(0.053, 1.2)
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.1f}"))

def plot_growth_curve(ax, df, tmp_ug_mL=32.0):
    # Pick a TMP concentration to display.
    c = df['tmp_ug_mL'].unique()
    dc = abs(c - (tmp_ug_mL))
    tmp_ug_mL = c[dc.argmin()]

    df = df.query('tmp_ug_mL == @tmp_ug_mL')

    for key, group in df.groupby(['sgrna', 'theo_mM']):
        sgrna, theo_mM = key
        style = pick_style(sgrna, theo_mM, color_controls=True)

        reps = group.groupby('minutes')
        times = reps.apply(lambda x: x.name) / 60
        means = reps.mean()['read']
        log_means = 10**reps['read'].agg(lambda x: np.mean(np.log10(x)))
        medians = reps.median()['read']
        stdevs = reps.std()['read']

        x = times
        y = medians

        ## Growth curves.

        # Plotting the means is smoother, but more affected by outliers 
        # (especially for the positive control on a log-scale).
        ax.semilogy(x, y, **style)

        ## Error bars:

        # I can't just use `ax.errorbar()`, because it doesn't have allow the 
        # error bar lines to be styled, and I need the style to distinguish apo 
        # from holo.
        x_err = np.array([times, times])
        y_err = np.array([y + stdevs/2, y - stdevs/2])

        # Stagger the apo and holo error bars, so they don't overlap.
        k = 6
        i = k//2 * int(theo_mM)

        if style['color'] == 'black':
            style['linestyle'] = '-'

        ax.semilogy(
                x_err[:,i::k],
                y_err[:,i::k],
                marker='_',
                **style,
        )

    label = AnchoredText(f"{tmp_ug_mL} µg/mL TMP", loc='upper left')
    ax.add_artist(label)
            
    ## Axis decorations:
    ax.set_xlabel('time (h)')
    ax.set_xticks([0, 4, 8, 12, 16, 20])
    ax.set_xlim(0, 20)

    ax.set_ylabel('OD600')
    ax.set_ylim(0.053, 1.00)
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.1f}"))


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    ligrnas = args['<ligrna>'] or ['mhf/30']
    n = len(ligrnas)

    def parse_option(option, cast=float):
        options = [cast(x) for x in option.split(',')]
        if len(options) == 1:
            options *= n
        return options

    times = parse_option(args['--time'])
    concs = parse_option(args['--conc'])

    toml_path = Path(__file__).parent/'data'/'20181114_pseudomonas_mic_all_expts.toml'
    df = load_data(toml_path)
    df = df.query('theo_mM in [0.0, 1.0]')

    fig, axes = plt.subplots(
            2, n,
            #figsize=(3.34*n, 3.81474-0.039),
            figsize=(3.34*n, 3.81474-0.039+0.532+0.068),
            squeeze=False,
    )

    for ax, ligrna, time, conc in zip(axes.T, ligrnas, times, concs):
        q = df.query('sgrna in [@ligrna, "on", "pa14"]')
        plot_mic_curve(ax[0], q, time)
        plot_growth_curve(ax[1], q, conc)

    for ax in axes[:,1:].flat:
        ax.set_ylabel('')
        ax.tick_params(labelleft=False)

    fig.tight_layout(pad=0, h_pad=0.5, w_pad=1)

    if args['--output']:
        path = args['--output'].replace('$', toml_path.stem)
        print("Saving plot to:", path)
        plt.savefig(path)

    plt.show()



