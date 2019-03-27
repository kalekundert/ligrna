#!/usr/bin/env python3

import bio96
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.offsetbox
import matplotlib.lines
from sgrna_sensor.style import pick_color, pick_style, FoldChangeLocator

def parse_labels():
    df = bio96.load('20181002_sgrna_qpcr.toml')
    df = df.set_index('well')
    return df

def pick_style(promoter, primers):
    from color_me import ucsf

    if primers == '16s':
        return dict(color=ucsf.light_grey[0], linestyle='--', zorder=-1)
    if promoter == 'j23119':
        return dict(color=ucsf.red[0])
    if promoter == 'j23150':
        return dict(color=ucsf.blue[0])

    return {}
    raise ValueError(f"no style for '{promoter}' with '{primers}' primers")

def make_legend(ax, **kwargs):
    ax.legend(
            handles=[
                matplotlib.lines.Line2D(
                    [], [], label="J23150",
                    **pick_style('j23150', 'sgrna'),
                ),
                matplotlib.lines.Line2D(
                    [], [], label="J23119",
                    **pick_style('j23119', 'sgrna'),
                ),
                matplotlib.lines.Line2D(
                    [], [], label="16S rRNA",
                    **pick_style('', '16s'),
                ),
            ],
            **kwargs,
    )


def load_pcr_data(labels):
    df = pd.read_excel('20181002_sgrna_qpcr.xlsx', sheet_name='Amplification Data', header=43)
    df = df.merge(labels, left_on='Well Position', right_index=True)
    df = df.query('discard == False')
    return df

def load_melt_data(labels):
    df = pd.read_excel('20181002_sgrna_qpcr.xlsx', sheet_name='Melt Curve Raw Data', header=43)
    df = df.merge(labels, left_on='Well Position', right_index=True)
    df = df.query('discard == False')
    return df

def plot_curves(df_pcr, df_melt):
    sgrnas = 'on', 'off', 'rxb 11,1', 'mhf 30'

    n = len(sgrnas)
    fig, axes = plt.subplots(n, 2, sharex='col', figsize=(8, 3*n))

    for i, sgrna in enumerate(sgrnas):
        ax_pcr = axes[i,0]
        ax_melt = axes[i,1]

        # Plot the PCR curves.

        label = matplotlib.offsetbox.AnchoredText(sgrna, loc="upper left")
        ax_pcr.add_artist(label)

        q = df_pcr[df_pcr.sgrna == sgrna]

        for key, well in q.groupby(['promoter', 'primers', 'Well Position']):
            promoter, primers, label = key
            ax_pcr.semilogy(
                    well.Cycle,
                    well.Rn,
                    label=label,
                    basey=2,
                    **pick_style(promoter, primers),
            )

        ax_pcr.set_ylim(2**-1, 2**4)
        ax_pcr.set_xlim(1, ax_pcr.get_xlim()[1])
        ax_pcr.set_ylabel("Rn")
        ax_pcr.grid(True)

        # Plot the melting curves.

        q = df_melt[df_melt.sgrna == sgrna]

        for key, well in q.groupby(['promoter', 'primers', 'Well Position']):
            promoter, primers, label = key
            ax_melt.plot(
                    well.Temperature,
                    well.Derivative / 10000,
                    label=label,
                    **pick_style(promoter, primers),
            )

        x = well.Temperature
        ax_melt.set_xlim(x.min(), x.max())
        ax_melt.set_ylim(0, ax_melt.get_ylim()[1])
        ax_melt.set_ylabel("dFluor/dT (×10⁴)")
        ax_melt.grid(True)

    make_legend(axes[0,1], loc="upper left")
    ax_pcr.set_xlabel("Cycle")
    ax_melt.set_xlabel("Temperature (°C)")
    fig.tight_layout()

    return fig


def load_ct_data(labels):
    data = pd.read_excel('20181002_sgrna_qpcr.xlsx', sheet_name='Results', header=43)
    data = data.dropna(thresh=3)
    data = data.dropna(axis='columns', how='all')
    data.index = data['Well Position']

    labeled_data = labels.merge(data, left_index=True, right_index=True) 
    labeled_data = labeled_data.query('discard == False')

    def aggregate_ct(df):
        row = pd.Series()
        row['ct_mean'] = df['CT'].mean()
        row['ct_std'] = df['CT'].std()
        return row

    return labeled_data.groupby(['primers', 'promoter', 'sgrna', 'ligand']).apply(aggregate_ct)

def load_Δct_data(ct_data):
    x = ct_data.loc['sgrna']
    x0 = ct_data.loc['16s']

    df = pd.DataFrame(index=x.index)
    df['Δct_mean'] = x['ct_mean'] - x0['ct_mean']
    # https://stats.stackexchange.com/questions/112351/standard-deviation-after-subtracting-one-mean-from-another
    # https://stats.stackexchange.com/questions/25848/how-to-sum-a-standard-deviation
    df['Δct_std'] = np.sqrt(x['ct_std']**2 + x0['ct_std']**2)

    return df

def load_ΔΔct_data(Δct_data):
    y = Δct_data.loc['j23119']
    y0 = Δct_data.loc['j23150']

    df = pd.DataFrame(index=y.index)
    df['ΔΔct_mean'] = y['Δct_mean'] - y0['Δct_mean']
    df['ΔΔct_std'] = np.sqrt(y['Δct_std']**2 + y0['Δct_std']**2)
    df['fold_change'] = 2**(-df['ΔΔct_mean'])
    df['lower_bound'] = 2**(-df['ΔΔct_mean'] - df['ΔΔct_std'])
    df['upper_bound'] = 2**(-df['ΔΔct_mean'] + df['ΔΔct_std'])
    df['lower_err'] = df['fold_change'] - df['lower_bound']
    df['upper_err'] = df['upper_bound'] - df['fold_change'] 

    return df

def plot_Δct_data(df):
    def iter_keys():
        for promoter in ['j23119', 'j23150']:
            for sgrna in ['on', 'off', 'rxb 11,1']:
                for ligand in [False, True]:
                    yield promoter, sgrna, ligand
    def name_from_key(key):
        promoter, sgrna, ligand = key
        return f"{promoter} {sgrna} ({'holo' if ligand else 'apo'})"

    fig, ax = plt.subplots(1, figsize=(4, 3.25))

    xticks = []
    xtick_labels = []

    for i, key in enumerate(iter_keys()):
        row = df.loc[key]
        promoter, sgrna, ligand = key

        fold_change = 2**(-row['Δct_mean'])
        fold_change_bound = 2**(-row['Δct_mean'] + row['Δct_std'])
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

    ax.set_ylabel('RNA Expression\n[rel. to 16S rRNA]')
    ax.set_xlim(xticks[0] - 0.5, xticks[-1] + 0.5)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, rotation='vertical')
    ax.grid(axis='y')
    #ax.yaxis.set_major_locator(FoldChangeLocator())

    fig.tight_layout(pad=0)
    #fig.savefig('20181002_sgrna_qpcr_Δct.svg')

    return fig

def plot_ΔΔct_data(df):
    keys = [
            ('on',       False),
            ('on',       True ),
            ('off',      False),
            ('off',      True ),
            ('rxb 11,1', False),
            ('rxb 11,1', True ),
    ]
    def name_from_key(key):
        sgrna, ligand = key
        return f"{sgrna} ({'holo' if ligand else 'apo'})"

    fig, ax = plt.subplots(1, figsize=(4, 3))

    xticks = []
    xtick_labels = []

    for i, key in enumerate(keys):
        row = df.loc[key]
        sgrna, ligand = key

        x = [i, i]
        y = [0, row['fold_change']]
        style = dict(
                linewidth=5,
                color=pick_color(sgrna),
        )
        ax.plot(x, y, **style)

        x = x[-1:]
        y = y[-1:]
        y_err = [row['upper_err']]
        style = dict(
                ecolor=pick_color(sgrna),
                capsize=2.5,
        )
        ax.errorbar(x, y, y_err, **style)

        xticks.append(i)
        xtick_labels.append(name_from_key(key))

    ax.set_ylabel('J23119 / J23150')
    ax.set_xlim(xticks[0] - 0.5, xticks[-1] + 0.5)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, rotation='vertical')
    ax.grid(axis='y')
    ax.yaxis.set_major_locator(FoldChangeLocator())

    fig.tight_layout(pad=0)
    fig.savefig('20181002_sgrna_qpcr_ΔΔct.svg')

    return fig


if __name__ == '__main__':
    labels = parse_labels()

    #pcr_data = load_pcr_data(labels)
    #melt_data = load_melt_data(labels)
    #curve_fig = plot_curves(pcr_data, melt_data)
    #curve_fig.savefig('20181002_sgrna_qpcr_curves.svg')
    #curve_fig.savefig('20181002_sgrna_qpcr_curves.pdf')

    ct_data = load_ct_data(labels)
    Δct_data = load_Δct_data(ct_data)
    ΔΔct_data = load_ΔΔct_data(Δct_data)

    plot_Δct_data(Δct_data)
    #plot_ΔΔct_data(ΔΔct_data)

    plt.show()

