#!/usr/bin/env python3

"""\
Plot various metrics describing the rational designs (e.g. insert length, 
insert GC content, etc.) against the success of those designs.

Usage:
    ./make_plots.py

Input:
    Cleavage data is automatically loaded from the XLSX files in the 
    './densiometry' directory.

Output:
    An SVG file called 'metrics_vs_cleavage.svg' containing the plots.
"""

import docopt, toml, re
import pandas as pd
import matplotlib.pyplot as plt
import subprocess as subp
from sgrna_sensor import densiometry, beeswarm
from sgrna_sensor.usage import from_name
from sgrna_sensor.style import pick_ucsf_color
from make_tables import Strategy, AlignGroup
from color_me import ucsf

def load_rational_designs():
    from make_tables import load_rational_designs
    df = load_rational_designs()

    # Drop the controls.
    df = df[df.align_group != AlignGroup.CONTROL.value]

    # This column is useless and distracting.
    del df['pretty_sequence']

    # Load information about the inserts:
    inserts = toml.load('inserts.toml')

    def inserts_from_name(row):
        insert = inserts[row.design]
        insert_seq = ''.join(insert).replace('-', '')

        replace_5 = insert[0]
        insert_5  = insert[1].strip('-')
        insert_3  = insert[2].strip('-')
        replace_3 = insert[3]

        row['replace_5'] = replace_5
        row['insert_5']  =  insert_5
        row['insert_3']  =  insert_3
        row['replace_3'] = replace_3

        row['seq_5']     = replace_5.strip('-') + insert_5
        row['seq_3']     = insert_3 + replace_3.strip('-')

        row['insert_len'] = sum([
                -replace_5.count('-'),
                len(insert_5),
                len(insert_3),
                -replace_3.count('-'),
        ])
        row['insert_gc'] = (
                (insert_seq.count('G') + insert_seq.count('C')) / 
                len(insert_seq) 
                if insert_seq else float('nan')
        )
        return row

    df = df.apply(inserts_from_name, axis='columns')

    return df

def plot_attributes(df):
    stems = [
            AlignGroup.STEMS.value,
            AlignGroup.NEXUS.value,
            AlignGroup.HAIRPIN.value,
    ]
    metrics = [
            plot_strategy,
            plot_insert_len,
            plot_insert_gc,
            plot_delta_g,
    ]
    n_rows = len(stems)
    n_cols = len(metrics)

    stem_names = {
            AlignGroup.STEMS.value: "Upper Stem",
            AlignGroup.NEXUS.value: "Nexus",
            AlignGroup.HAIRPIN.value: "Hairpin",
    }
    stem_colors = {
            AlignGroup.STEMS.value: pick_ucsf_color('upper stem'),
            AlignGroup.NEXUS.value: pick_ucsf_color('nexus'),
            AlignGroup.HAIRPIN.value: pick_ucsf_color('hairpin'),
    }
    stem_ylims = {
            AlignGroup.STEMS.value: (-0.1, 0.8),
            AlignGroup.NEXUS.value: (0.1, -0.8),
            AlignGroup.HAIRPIN.value: (-0.1, 0.8),
            #AlignGroup.NEXUS.value: (0.05, -0.5),
            #AlignGroup.HAIRPIN.value: (-0.04, 0.4),
    }

    fig, axes = plt.subplots(
            n_rows, n_cols,
            figsize=(7,5),
            squeeze=False,
    )

    # Plot the metrics.
    for i in range(n_rows):
        for j in range(n_cols):
            sub_df = df[df.align_group == stems[i]]
            color = stem_colors[stems[i]]
            metrics[j](axes[i,j], sub_df, color)

    # Remove redundant axis ticks/labels.
    for ax in axes[:-1,:].flat:
        ax.tick_params(
                axis='x',
                top=False,   labeltop=False,
                bottom=True, labelbottom=False,
        )
    for ax in axes[:,1:].flat:
        ax.tick_params(
                axis='y',
                left=False,  labelleft=False,
                right=False, labelright=False,
        )

    # Label the rows and columns of plots.
    for i in range(n_rows):
        axes[i,0].set_ylabel(stem_names[stems[i]])
        for ax in axes[i,:]:
            ax.set_ylim(*stem_ylims[stems[i]])
    for j in range(n_cols):
        axes[0,j].set_xlabel(metrics[j].label)

    # Enable the grid.
    for ax in axes.flat:
        ax.yaxis.grid()

    fig.tight_layout(pad=0)
    return fig

class label:

    def __init__(self, label):
        self.label = label

    def __call__(self, func):
        func.label = self.label
        return func
    
@label("Linker Strategy")
def plot_strategy(ax, df, color):
    strategies = [
            Strategy.STEM_REP.value,
            Strategy.IND_DIM.value,
            Strategy.STR_DISP.value,
    ]
    strategy_labels = {
            Strategy.STEM_REP.value: '(i)',
            Strategy.IND_DIM.value: '(ii)',
            Strategy.STR_DISP.value: '(iii)',
    }
    ticks = []
    ticklabels = []
    scale = 5

    for i, strategy in enumerate(strategies):
        q = df[df.strategy == strategy]

        y = q.mean_change.values
        y_err = q.std_change.values
        x = beeswarm.unclump_points(y, y_err, scale * i, 0.2)

        ax.errorbar(
                x, y, y_err,
                marker='o',
                markerfacecolor=color,
                markeredgecolor='none',
                ecolor=ucsf.light_grey[0],
                elinewidth=1,
                linestyle='None',
        )

        ticks.append(scale * i)
        ticklabels.append(strategy_labels[strategy])

    ax.set_xticks(ticks)
    ax.set_xticklabels(ticklabels)
    ax.set_xlim(-scale * 0.5, scale * (len(strategies) - 0.5))

@label("Insert Length")
def plot_insert_len(ax, df, color):
    plot_with_style(
            ax,
            x=df.insert_len.values,
            y=df.mean_change.values,
            y_err=df.std_change.values,
            color=color,
    )
    ax.set_xlim(-20, 20)

@label("Insert GC%")
def plot_insert_gc(ax, df, color):
    plot_with_style(
            ax,
            x=df.insert_gc.values,
            y=df.mean_change.values,
            y_err=df.std_change.values,
            color=color,
    )
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])

@label("Duplex ΔG")
def plot_delta_g(ax, df, color):

    # Get the 5' and 3' insert sequences from the data frame.
    df = df.query('seq_5 != "" and seq_3 != ""')
    seqs = df[['seq_5', 'seq_3']].values.tolist()
    
    # Run RNAduplex on each pair of sequences.
    p = subp.Popen(
        ['RNAduplex'],
        stdin=subp.PIPE,
        stdout=subp.PIPE,
        stderr=subp.PIPE,
        text=True,
    )
    stdin = '\n'.join(['\n'.join(x) for x in seqs])
    stdout, stderr = p.communicate(stdin)

    if stderr:
        raise RuntimeError(stderr)

    # Parse the output.
    results = []
    lines = stdout.strip().split('\n')

    for (seq_5, seq_3), line in zip(seqs, lines):
        try:
            tokens = line.split()
        except:
            raise RuntimeError(f"Error parsing RNAduplex output:\n\n{line}")

        dg = float(tokens[-1].strip('()'))
        if dg > 100: dg = float('nan')

        result = {}
        result['seq_5'] = seq_5
        result['seq_3'] = seq_3
        result['duplex_bp'] = tokens[0]
        result['duplex_dg'] = dg
        results.append(result)

    # Merge the results back into the data frame.
    vienna_df = pd.DataFrame(results)
    df = df.merge(vienna_df, on=['seq_5', 'seq_3'])

    # Plot the data.
    plot_with_style(
            ax,
            x=df.duplex_dg.values,
            y=df.mean_change.values,
            y_err=df.std_change.values,
            color=color,
    )
    ax.set_xlim(-11, 5)
    ax.set_xticks([-10, -5, 0, 5])


def plot_with_style(ax, x, y, y_err, color):
    ax.errorbar(
            x, y, y_err,
            marker='o',
            markerfacecolor=color,
            markeredgecolor='none',
            ecolor=ucsf.light_grey[0],
            elinewidth=1,
            linestyle='None',
    )


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    df = load_rational_designs()
    fig = plot_attributes(df)

    plt.savefig('metrics_vs_cleavage.svg')
    plt.show()

