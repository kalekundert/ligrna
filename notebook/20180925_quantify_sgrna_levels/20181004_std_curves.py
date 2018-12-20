#!/usr/bin/env python3

"""\
Plot the standard curves for the various primer pairs we used for qPCR.

Usage:
    20181004_std_curves.py

The standard curves were done in two experiments.  The plate layouts for both 
experiments are described in: `20181004_std_curves.toml`

In this plot, we want to merge the data from the two experiments.  The 16S 
primers were actually tested in both experiments, and we want to use the data 
from the second experiment.
"""

import bio96
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.offsetbox
from scipy.stats import linregress
from sgrna_sensor.style import pick_color, pick_style
from sgrna_sensor.latex import render_latex_table
from color_me import ucsf
from more_itertools import one

pd.set_option('display.max_rows', 100)

keys = [
        'gfp',
        '30',
        '11',
        '16s',
]
styles = {
        '11':   dict(color=ucsf.navy[0]),
        '30':   dict(color=ucsf.teal[0]),
        'gfp':  dict(color=ucsf.olive[0]),
        '16s':  dict(color=ucsf.dark_grey[0]),
        'ihfB': dict(color=ucsf.light_grey[0]),
}
labels = {
        '30':   'ligRNA⁺',
        '11':   'ligRNA⁻',
        'gfp':  'sfGFP',
        '16s':  '16S rRNA',
}
latex_labels = {
        '30':   r'ligRNA\textsuperscript{+}',
        '11':   r'ligRNA\textsuperscript{−}',
}

def load_pcr_data(toml_path):

    def pcr_from_xlsx(xlsx_path):
        return pd.read_excel(
                xlsx_path, sheet_name='Amplification Data', header=43)

    df, opt = bio96.load(
            toml_path,
            pcr_from_xlsx,
            {'well': 'Well Position'},
    )
    df = drop_outliers(df)
    return df

def load_ct_data(toml_path):

    def ct_from_xlsx(xlsx_path):
        ct = pd.read_excel(xlsx_path, sheet_name='Results', header=43)
        ct = ct.dropna(thresh=3)
        ct = ct.dropna(axis='columns', how='all')
        return ct

    df, opt = bio96.load(
            toml_path,
            ct_from_xlsx,
            {'well': 'Well Position'},
    )
    df = drop_outliers(df)
    return df

def load_melt_data(toml_path):
    def melt_from_xlsx(xlsx_path):
        return pd.read_excel(
                xlsx_path, sheet_name='Melt Curve Raw Data', header=43)

    df, opt = bio96.load(
            toml_path,
            melt_from_xlsx,
            {'well': 'Well Position'},
    )
    df = drop_outliers(df)
    return df

def drop_outliers(df):
    n0 = len(df)
    df = df.query('discard == False')
    if len(df) != n0:
        print(f"Dropped {n0-len(df)}/{n0} outliers")
    return df


def plot_ct_fits(df):
    fig, ax = plt.subplots(figsize=(3.1, 2.1))
    fits = {}
    artists = {}

    for key in keys:
        q = df.query('primers == @key')

        x = q['dilution']
        y = q['CT'].astype(float)
        x_log = np.log10(x)

        m, b, r, p, err = linregress(x_log, y)
        x_fit = np.logspace(0, 5)
        y_fit = np.polyval((m,b), np.log10(x_fit))

        fits[key] = {
                'm': m,
                'b': b,
                'r2': r**2,
                'efficiency': 100 * (10**(1/m) - 1),
                'factor': 10**(1/m),
        }

        ax.plot(x, y, '+', label='_', **styles[key])[0]
        ax.plot(x_fit, y_fit, label=labels[key], **styles[key])[0]

    locmaj = matplotlib.ticker.LogLocator(base=10, subs=[1.0])
    ax.xaxis.set_major_locator(locmaj)

    locmin = matplotlib.ticker.LogLocator(base=10.0, subs=0.1*np.arange(2, 10))
    ax.xaxis.set_minor_locator(locmin)
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    
    ax.set_ylabel('CT cycle')
    ax.set_xlabel('Dilution')
    ax.set_xscale('log')
    ax.grid(True)
    ax.legend(loc='best', prop=dict(size=8))

    ## JSON

    with open('20181004_std_curves.json', 'w') as file:
        json.dump(fits, file)

    ## LaTeX

    def emph_if_bad(sgrna, param, unit=''):
        precision = {'r2': '.4f', 'efficiency': '.1f'}
        good_fmt = '{:%s}%s' % (precision.get(param, '.2f'), unit)
        bad_fmt = '\\cancel{{%s}}' % good_fmt

        x = fits[sgrna][param]

        if param == 'm':
            fmt = good_fmt if 3.4 < x < 3.6 else bad_fmt

        elif param == 'r2':
            fmt = good_fmt if x > 0.98 else bad_fmt

        elif param == 'efficiency':
            fmt = good_fmt if 90 < x < 110 else bad_fmt

        else:
            fmt = good_fmt

        return fmt.format(x)

    fig.tight_layout(pad=0)
    fig.savefig('20181004_std_curve_fits.svg')

    render_latex_table('20181004_std_curve_fits.tex', {**locals(), **globals()})

def plot_curves(ct, pcr, melt):
    fig, axes = plt.subplots(
            2, len(keys),
            sharex='row', sharey='row',
            figsize=(7.0, 3.5),
    )
    fits = {}
    artists = {}

    ct = ct.set_index(['primers'])
    pcr = pcr.set_index(['primers'])
    melt = melt.set_index(['primers'])

    for key, ax in zip(keys, axes[0]):
        # Label the plots:
        label = matplotlib.offsetbox.AnchoredText(
                labels[key], loc="upper left", prop=dict(size=8))
        ax.add_artist(label)

        # Plot the amplification curves:
        for _, well in pcr.loc[key].groupby(['Well Position']):
            ax.plot(well['Cycle'], well['Delta Rn'], **styles[key])

        # Show the Ct threshold:
        ct_threshold = one(ct.loc[key]['Ct Threshold'].unique())
        ax.axhline(ct_threshold, 0, 1, color=ucsf.black[0], dashes=[1,1], zorder=-1)

        ax.grid(True)

    for key, ax in zip(keys, axes[1]):
        # Plot the melting curves.
        for _, well in melt.loc[key].groupby(['Well Position']):
            ax.plot(
                    well['Temperature'],
                    well['Derivative'] / 1e4,
                    **styles[key],
            )

        x = well.Temperature
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(0, 25)
        ax.grid(True)

    axes[0,0].set_ylabel('ΔRn')
    axes[0,0].set_ylim(0, 12)
    axes[0,0].set_yticks([0, 2, 4, 6, 8, 10, 12])

    for ax in axes[0,:]:
        ax.set_xlabel('Cycle')
        ax.set_xlim(1, 40)
        ax.set_xticks([1, 10, 20, 30, 40])

    axes[1,0].set_ylabel("dRn/dT (×10⁴)")

    for ax in axes[1,:]:
        ax.set_xlabel("Temperature (°C)")

    fig.tight_layout(pad=0, w_pad=0.5, h_pad=0.5)
    fig.savefig('20181004_std_curve_pcr_melt.svg')
    plt.show()


if __name__ == '__main__':
    ct = load_ct_data('20181004_std_curves.toml')
    pcr = load_pcr_data('20181004_std_curves.toml')
    melt = load_melt_data('20181004_std_curves.toml')

    plot_ct_fits(ct)
    plot_curves(ct, pcr, melt)
