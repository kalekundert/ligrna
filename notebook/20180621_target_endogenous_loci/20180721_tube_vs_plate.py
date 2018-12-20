#!/usr/bin/env python3

import numpy as np
from sgrna_sensor.plate_reader import BiotekExperiment
from matplotlib import pyplot as plt, gridspec
from color_me import ucsf

# Rows
# ====
# A: OD660
# B: Debris controls
# C: Non-stopped reactions ("plate")
# D: 30 min stopped reaction ("tube")
# E: 60 min stopped reaction ("tube")
# F: 120 min stopped reaction ("tube")
#
# Columns
# =======
# 1: Blank
# 2: lz/on
# 3: lx/off

cultures = BiotekExperiment('plate_reader/20180721_plate_vs_tube_od660.xlsx')
expts = {
        ('plate', 32):  BiotekExperiment('plate_reader/20180721_plate_vs_tube_a420_plate_32min.xlsx'),
        ('plate', 61):  BiotekExperiment('plate_reader/20180721_plate_vs_tube_a420_plate_61min.xlsx'),
        ('plate', 121): BiotekExperiment('plate_reader/20180721_plate_vs_tube_a420_plate_121min.xlsx'),
        ('tube', 30):   BiotekExperiment('plate_reader/20180721_plate_vs_tube_a420_tube_30min.xlsx'),
        ('tube', 60):   BiotekExperiment('plate_reader/20180721_plate_vs_tube_a420_tube_60min.xlsx'),
        ('tube', 120):  BiotekExperiment('plate_reader/20180721_plate_vs_tube_a420_tube_120min.xlsx'),
}
rows = {
        ('plate', 32):  'C',
        ('plate', 61):  'C',
        ('plate', 121): 'C',
        ('tube', 30):   'D',
        ('tube', 60):   'E',
        ('tube', 120):  'F',
}
debris_rows = {
        'C': 'B',
}
columns = {
        'blank': 1,
        'lz/on': 2,
        'lz/off': 3,
}
times_min = {
        'plate': [32, 61, 121],
        'tube':  [30, 60, 120],
}
volumes_mL = {
        'plate': 0.100,
        'tube':  0.070,
}
colors = {
        ('tube',  'lz/on'):  ucsf.blue[0],
        ('plate', 'lz/on'):  ucsf.blue[1],
        ('tube',  'lz/off'): ucsf.olive[0],
        ('plate', 'lz/off'): ucsf.olive[1],
}

def well_from_args(decoratee):

    class Well:
        pass

    def decorator(reaction, sample, time_min):
        expt = expts[reaction, time_min]

        well = Well()
        well.reaction = reaction
        well.sample = sample
        well.time_min = time_min
        well.args = reaction, sample, time_min
        well.row = rows[reaction, time_min]
        well.col = columns[sample]
        well.id = f'{well.row}{well.col}'

        return decoratee(expt, well)

    return decorator

def yield_wells():
    i = 0
    for sample in ('lz/on', 'lz/off'):
        for reaction in ('plate', 'tube'):
            for time_min in times_min[reaction]:
                yield i, reaction, sample, time_min
                i += 1


@well_from_args
def raw_od660(expt, well):
    return cultures.reads[660][f'A{well.col}']
    
@well_from_args
def normed_od660(expt, well):
    return raw_od660(*well.args) - cultures.reads[660]['A1']

@well_from_args
def raw_a420(expt, well):
    return expt.reads[420][well.id]

@well_from_args
def debris_a420(expt, well):
    if well.reaction == 'plate':
        return expt.reads[420][f'{debris_rows[well.row]}{well.col}']
    elif well.reaction == 'tube':
        return expt.reads[420][f'{well.row}1']

@well_from_args
def normed_a420(expt, well):
    return raw_a420(*well.args) - debris_a420(*well.args)

@well_from_args
def fit_a420(expt, well):
    time_min = times_min[well.reaction]
    a420 = np.array([
            normed_a420(well.reaction, well.sample, t)
            for t in time_min
    ])
    m, b = np.polyfit(time_min, a420, 1)
    a420 -= b
    return a420[time_min.index(well.time_min)]

@well_from_args
def miller_units(expt, well):
    a420 = fit_a420(*well.args)
    od660 = normed_od660(*well.args)
    volume_mL = volumes_mL[well.reaction]
    time_min = well.time_min

    return 1000 * a420 / (od660 * volume_mL * time_min)


def print_table():
    # Print a table showing how the Miller units were calculated.
    print("""\
────────────────────────────────────────────────────────────
                  Time  OD660  OD660   A420   A420    Miller
sgRNA   Reaction  (min)  (raw) (norm)  (raw) (norm)    Units 
────────────────────────────────────────────────────────────""")

    for i, reaction, sample, time_min in yield_wells():
        args = reaction, sample, time_min
        print(f'{sample:6s}  {reaction:8s}  {time_min:4d}  '
              f'{raw_od660(*args):5.3f}  {normed_od660(*args):5.3f}  '
              f'{raw_a420(*args):5.3f}  {normed_a420(*args):5.3f}  '
              f'{miller_units(*args):8.3f}')

    print("""\
────────────────────────────────────────────────────────────""")

def print_plate_vs_cuvette():
    # Compare the ODs measured in the plate to those measured in cuvettes 
    # (which are presumably more accurate).
    plate_ods = cultures.reads[660]['A2'] / cultures.reads[660]['A3']
    cuvette_ods = '???'
    print(f"""\
OD[on] / OD[off]:
  plate:   {plate_ods:.3f}
  cuvette: {cuvette_ods}""")

def plot_reactions():
    fig = plt.figure(figsize=(7,10), tight_layout=True)
    grid = gridspec.GridSpec(3, 2)

    ax1 = fig.add_subplot(grid[0,0])
    ax2 = fig.add_subplot(grid[0,1])
    ax3 = fig.add_subplot(grid[1,0])
    ax4 = fig.add_subplot(grid[1,1])
    ax5 = fig.add_subplot(grid[2,:])

    plot_trace(ax1, 'lz/on',  fit_a420, "A420 − debris − b")
    plot_trace(ax2, 'lz/off', fit_a420, "A420 − debris − b")
    plot_trace(ax3, 'lz/on',  debris_a420, "debris")
    plot_trace(ax4, 'lz/off', debris_a420, "debris")
    plot_activities(ax5)

    plt.tight_layout()
    plt.savefig('20180721_tube_vs_plate.svg')
    plt.show()

def plot_trace(ax, sample, func, label=None):
    t_lim = 0, 140
    ax.set_xlim(*t_lim)
    ax.set_xlabel("Time (min)")
    ax.set_ylabel(label or func.__name__)

    for reaction in ('plate', 'tube'):
        t = times_min[reaction]
        a = [func(reaction, sample, x) for x in t]
        m, b = np.polyfit(t, a, 1)
        tt = np.linspace(*t_lim)
        color = colors[reaction, sample]

        ax.plot(tt, m * tt + b, color=color, linestyle=':')
        ax.plot(t, a, 'o', color=color,)

def plot_activities(ax):
    xticks = []
    xtick_labels = []

    for i, reaction, sample, time_min in yield_wells():
        xticks.append(i)
        xtick_labels.append(f't={time_min} {reaction} {sample}')
        color = colors[reaction, sample]
        rate = miller_units(reaction, sample, time_min)

        x, y = [i, i], [0, rate]
        ax.plot(x, y, color=color, linewidth=5)

    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels, rotation='vertical')
    ax.set_xlim(-0.5, i+0.5)
    ax.set_ylabel('Miller units')
    ax.grid(axis='y')


if __name__ == '__main__':
    print_table()
    print()
    print_plate_vs_cuvette()
    plot_reactions()
