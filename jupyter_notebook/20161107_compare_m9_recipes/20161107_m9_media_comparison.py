#!/usr/bin/env python3

import os, sys, csv, numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from more_itertools import chunked
from pprint import pprint
from datetime import datetime

with open('20161107_m9_media_comparison.epc') as epc_file:
    epc_reader = csv.reader(epc_file)

    header = next(epc_reader)
    plate_rows = int(header[1])
    plate_cols = int(header[2])
    timepoints = int(header[3])

    data = list(epc_reader)

# Discard the three plates of seemingly useless zeros and full stops at the 
# beginning of the file.
data = data[3*plate_rows:]

ods = list(chunked(data, plate_rows))[:timepoints]
ods = [[[float(od) for od in row] for row in plate] for plate in ods]

times = [ #
        datetime.strptime(row[0], '%Y/%m/%d %H:%M:%S')
        for row in data[plate_rows*timepoints:]
]
secs = [(x - times[0]).total_seconds() for x in times]
hours = [x/3600 for x in secs]

traj = lambda row, col: np.array([frame[row][col] for frame in ods])

titles = {
        0: 'EZ',
        1: 'Old M9',
        2: 'M9 + glucose \u2212 thiamine',
        3: 'M9 + glucose + thiamine',
        4: 'M9 + glycerol \u2212 thiamine',
        5: 'M9 + glycerol + thiamine',
}

concs = {
        0: '500 μM',
        1: '158 μM',
        2: '50.0 μM',
        3: '15.8 μM',
        4: '5.00 μM',
        5: '1.58 μM',
        6: '0.50 μM',
        7: 'apo',
}


def plot_col(col, label='', cmap='Blues', **kwargs):
    map = ScalarMappable(Normalize(-7,7), cmap)
    for i in [0,7]:
        t = traj(i,col)
        plt.plot(
                hours, t,
                label='{} {}'.format(label, concs[i]), color=map.to_rgba(i),
                **kwargs
        )

def plot_expt(i, label=''):
    plt.title(titles[i])
    plt.xlim(min(hours), max(hours))
    plt.xlabel('hours')
    plt.ylabel('OD600')
    plot_col(2*i+0, label=label+'on ', cmap='Greys')
    plot_col(2*i+1, label=label+'off ', cmap='Greys', linestyle='--')


if os.fork():
    raise SystemExit

ax = plt.subplot(3, 2, 1)
plot_expt(0)

plt.subplot(3, 2, 2, sharex=ax, sharey=ax)
plot_expt(1)
legend = plt.legend(
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        borderaxespad=0.0,
)

plt.subplot(3, 2, 3, sharex=ax, sharey=ax)
plot_expt(2)

plt.subplot(3, 2, 4, sharex=ax, sharey=ax)
plot_expt(3)

plt.subplot(3, 2, 5, sharex=ax, sharey=ax)
plot_expt(4)

plt.subplot(3, 2, 6, sharex=ax, sharey=ax)
plot_expt(5)

plt.gcf().set_size_inches(9, 8.5)
plt.gcf().canvas.mpl_connect('resize_event', lambda ev: plt.tight_layout())
plt.legend(loc='lower right', prop={'size':8})
plt.tight_layout()
plt.savefig('growth_curves.pdf', additional_artists=[legend])
plt.show()
