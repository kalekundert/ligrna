#!/usr/bin/env python3

"""
Create a plot showing the likelihood the distribution of nucleotides observed 
at each position in the spacer.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from debugtools import p, pp, pv
from pprint import pprint
from color_me import ucsf

positions = np.arange(18)
j_from_nuc = dict(A=0, T=1, G=2, C=3)
nuc_from_j = {v:k for k, v in j_from_nuc.items()}

def calc_frequencies(spacers):
    frequencies = [np.zeros(4) for i in positions]

    for spacer in spacers:
        for i, nuc in enumerate(spacer):
            frequencies[i][j_from_nuc[nuc]] += 1

    return frequencies

def calc_pvals(frequencies):
    from scipy.stats import chisquare as chi2
    pvals = np.array([chi2(f).pvalue for f in frequencies])

    # Apply the Bonferroni multiple testing correction.  This correction seems to 
    # be generally frowned upon, but it's appropriate in this case because I'm 
    # interesting in the global null hypothesis (e.g. are all the null hypothesis 
    # rejected/accepted).  It's also known to be conservative, which means that if 
    # the null hypothesis is rejected, I can be pretty confident that something 
    # else is going on.

    return pvals * len(pvals)


if __name__ == '__main__':
    # Load the spacer sequences.

    with open('n17_spacers.tsv') as file:
        sequenced_spacers = [x.strip() for x in file.readlines()]

    with open('doench_spacers.tsv') as file:
        doench_spacers = [x.split()[1][7:25] for x in file.readlines()]

    random_spacers = [
            ''.join(random.choice('ATCG') for _ in positions)
            for _ in sequenced_spacers
    ]

    # Calculate χ² p-values for both sets of spacers.

    sequenced_freqs = calc_frequencies(sequenced_spacers)
    sequenced_pvals = calc_pvals(sequenced_freqs)

    doench_freqs = calc_frequencies(doench_spacers)
    doench_pvals = calc_pvals(doench_freqs)

    random_freqs = calc_frequencies(random_spacers)
    random_pvals = calc_pvals(random_freqs)

    # Plot the p-values on the left axis.

    fig, ax1 = plt.subplots()
    fig.patch.set_color('white')

    ax1.plot(positions, -np.log10(sequenced_pvals), 'ko', mec='none', label='Sequenced spacers')
    ax1.plot(positions, -np.log10(doench_pvals), 'k^', mec='none', label='Doench spacers')
    ax1.plot(positions, -np.log10(random_pvals), 'ko', mfc='none', label='Uniform random spacers')
    ax1.axhline(-np.log10(0.01), color='k', linestyle='--', label='99% confidence level')
    ax1.set_xlabel('position')
    ax1.set_ylabel('χ² uniformity test\n-log(Bonferonni-corrected p)')
    ax1.set_xticks(positions)
    ticklabels = list(17 - positions)
    ticklabels[-1] = -1
    ax1.set_xticklabels(ticklabels)
    ax1.set_xlim(min(positions) - 0.5, max(positions) + 0.5)
    ax1.legend(loc='best')

    # Plot the nucleotide frequencies on the right axis.

    ax2 = ax1.twinx()
    ax1.set_zorder(ax2.get_zorder()+1)
    ax1.patch.set_visible(False)

    color = ucsf.dark_grey[0]
    color_from_nuc = dict(
            A=ucsf.blue[2],
            T=ucsf.orange[2],
            G=ucsf.olive[2],
            C=ucsf.red[2],
    )

    for i in positions:
        for j in range(4):
            nuc = nuc_from_j[j]
            freq = sequenced_freqs[i][j] / sum(sequenced_freqs[i])
            ax2.text(i, freq, nuc,
                    color=color_from_nuc[nuc],
                    family='monospace',
                    horizontalalignment='center',
                    verticalalignment='center',
                    zorder=10,
            )

    ax2.tick_params('y', colors=color)
    ax2.set_ylim(0, 1)
    ax2.set_ylabel('nucleotide frequencies\n(sequenced spacers)',
            rotation=270,
            verticalalignment='baseline',
            color=color)

    fig.tight_layout()
    plt.savefig('n17_spacer_uniformity_test.svg')
    plt.show()




