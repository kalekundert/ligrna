#!/usr/bin/env python3

import color_me
import numpy as np
import matplotlib.pyplot as plt

pixels_from_imagej = {
        'gfp on':         ( 1765.698,  8073.731,  2635.477,  8091.296),
        'gfp off':        (10088.681,     0.000,  9214.974,     0.000),
        'gfp rxb 11,1':   ( 8747.803,  3984.033, 10905.530,   165.263),
        'gfp mhf 30':     (12104.530,   236.971, 10533.510,   498.799),
        'gfp mhf 37':     ( 9846.167,  2001.406,  4337.033,  7625.539),
        # '"CCG" on':       (10475.459,  3719.518,  8720.146,  1676.698),
        # '"CCG" off':      (11972.530,     0.000,  8721.539,     0.000),
        # '"CCG" rxb 11,1': (10822.480,     0.000, 10090.924,     0.000),
        # '"CCG" mhf 30':   ( 8632.388,     0.000,  9472.288,     0.000),
        # '"CCG" mhf 37':   (10779.652,     0.000,  9950.581,     0.000),
        # '"CAG" on':       ( 5125.154,  6977.761,  8128.368,  7574.175),
        # '"CAG" off':      (12046.309,     0.000, 11950.288,     0.000),
        # '"CAG" rxb 11,1': (12166.602,   707.406, 11878.338,    98.435),
        # '"CAG" mhf 30':   (13122.108,  1831.355, 11776.258,  1516.941),
        # '"CAG" mhf 37':   (13563.551,   171.728, 11715.480,  2035.527),
        # '"CCT" on':       ( 9158.075,  5490.326,  9257.045,  5749.569),
        # '"CCT" off':      (13273.359,     0.000, 23485.789,     0.000),
        # '"CCT" rxb 11,1': (12154.631,   279.213, 11814.803,    88.142),
        # '"CCT" mhf 30':   (11501.116,   375.627, 12766.794,   690.213),
        # '"CCT" mhf 37':   (11425.874,   233.971, 10569.853,  1994.698),
}
absolute_percents = {
        k: (v[1]/(v[0]+v[1]),
            v[3]/(v[2]+v[3]))
        for k,v in pixels_from_imagej.items()
}
control_percents = {
        k: k.split()[0] + ' on'
        for k,v in absolute_percents.items()
}
relative_percents = {
    k: (v[0] / max(absolute_percents[control_percents[k]]),
        v[1] / max(absolute_percents[control_percents[k]])) 
    for k,v in absolute_percents.items()
}

color_table = {
    'gfp': '#90BD31',
    # '"CCG"': color_me.ucsf.blue[0],
    # '"CAG"': color_me.ucsf.blue[0],
    # '"CCT"': color_me.ucsf.blue[0],
}
get_color = lambda k: color_table[k.split()[0]]


def plot_fold_change():
    fig, ax1 = plt.subplots(figsize=(6,4), facecolor='white')
    # ax2 = ax1.twinx()
    # ax12 = ax1, ax2

    bar_sep = 1
    group_sep = 2 * bar_sep
    xticks = []
    xticklabels = []
    xtickcolors = []

    for i,k in enumerate(pixels_from_imagej):
        x = bar_sep * i + group_sep * (i // 5)
        y_apo = absolute_percents[k][0] 
        y_holo = absolute_percents[k][1]

        bar_color = get_color(k)
        arrow_color = '#999999'

        xticks.append(x)
        xticklabels.append(k)
        xtickcolors.append(bar_color)

        if y_holo == 0 and y_apo == 0:
            fold_change = 1
        else:
            fold_change = y_holo / y_apo
            if fold_change < 1:
                fold_change **= -1

        ax1.plot(
                (x, x), (0, fold_change),
                color=bar_color,
                solid_capstyle='butt',
                linewidth=12,
                zorder=1,
        )
        # ax2.plot(
        #         [x, x], [y_apo, y_holo],
        #         color=arrow_color,
        #         linewidth=2,
        # )
        # ax2.plot(
        #         [x], [y_apo],
        #         color=arrow_color,
        #         markeredgewidth=2,
        #         linewidth=2,
        #         marker='_',
        # )
        # ax2.plot(
        #         [x], [y_holo],
        #         color=arrow_color,
        #         markeredgewidth=0,
        #         linewidth=2,
        #         marker='^' if y_holo > y_apo else 'v',
        # )

    ax1.set_ylabel('fold change')
    # ax2.set_ylabel('% cleavage', rotation=270, va='bottom', color=arrow_color)
    # ax2.tick_params('y', colors=arrow_color)
    # ax2.spines['right'].set_color(arrow_color)
    # ax2.set_ylim(0, 1)

    # for ax in ax12:
    #     ax.spines['top'].set_visible(False)
    #     ax.tick_params('x', bottom='off', top='off')


    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.tick_params('x', bottom='off', top='off')
    ax1.tick_params('y', right='off')

    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xticklabels, rotation=270)

    #for t, c in zip(ax1.get_xticklabels(), xtickcolors):
        #t.set_color(c)

    ax1.set_xlim(-1, x + 1)
    fig.facecolor = 'white'
    fig.tight_layout()


if __name__ == '__main__':
    plot_fold_change()
    plt.savefig('in_vitro_fold_change.pdf')
    plt.show()
