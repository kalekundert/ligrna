#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sgrna_sensor.plate_reader import BiotekExperiment
from color_me import ucsf

# Rows
# ====
# A,B: Non-stopped reactions ("plate")
# C,D: 30 min stopped reaction ("tube")
# E,F: 60 min stopped reaction ("tube")
# G,H: 120 min stopped reaction ("tube")
#
# Columns
# =======
# 1: apo;  lz/on
# 2: apo;  lz/off
# 3: apo;  lz/rxb/11/1
# 4: apo;  lz/mhf/30
# 5: holo; lz/on
# 6: holo; lz/off
# 7: holo; lz/rxb/11/1
# 8: holo; lz/mhf/30

cultures = BiotekExperiment('plate_reader/20180718_plate_vs_tube_od660.xlsx')
expts = {
        ('plate',  42): BiotekExperiment('plate_reader/20180718_plate_vs_tube_a420_plate_42min.xlsx'),
        ('plate', 121): BiotekExperiment('plate_reader/20180718_plate_vs_tube_a420_plate_121min.xlsx'),
        ('plate', 295): BiotekExperiment('plate_reader/20180718_plate_vs_tube_a420_plate_295min.xlsx'),
        ('tube',   34): BiotekExperiment('plate_reader/20180718_plate_vs_tube_a420_tube_34min.xlsx'),
        ('tube',  120): BiotekExperiment('plate_reader/20180718_plate_vs_tube_a420_tube_120min.xlsx'),
        ('tube',  293): BiotekExperiment('plate_reader/20180718_plate_vs_tube_a420_tube_293min.xlsx'),
}
rows = {
        ('plate',  42): list('AB'),
        ('plate', 121): list('AB'),
        ('plate', 295): list('AB'),
        ('tube',   34): list('CD'),
        ('tube',  120): list('EF'),
        ('tube',  293): list('GH'),
}
columns = {
        ('apo',  'lz/on'):  1,
        ('apo',  'lz/off'): 2,
        ('apo',  'lz/11'):  3,
        ('apo',  'lz/30'):  4,
        ('holo', 'lz/on'):  5,
        ('holo', 'lz/off'): 6,
        ('holo', 'lz/11'):  7,
        ('holo', 'lz/30'):  8,
}
blanks = {
        'A': 'A9',
        'B': 'A9',
        'C': 'C9',
        'D': 'C9',
        'E': 'E9',
        'F': 'E9',
        'G': 'G9',
        'H': 'G9',
}
times = {
        'plate': [42, 121, 295],
        'tube':  [34, 120, 293],
}
od660_rows = {
        0: 'A',
        1: 'B',
}
od660_blanks = {
        0: 'A11',
        1: 'A12',
}
colors = {
        ('tube',  'lz/on'):  ucsf.dark_grey[0],
        ('plate', 'lz/on'):  ucsf.light_grey[0],
        ('tube',  'lz/off'): ucsf.dark_grey[0],
        ('plate', 'lz/off'): ucsf.light_grey[0],
        ('tube',  'lz/11'):  ucsf.navy[0],
        ('plate', 'lz/11'):  ucsf.navy[1],
        ('tube',  'lz/30'):  ucsf.teal[0],
        ('plate', 'lz/30'):  ucsf.teal[1],
}

def well_from_args(decoratee):

    class Well:
        pass

    def decorator(reaction, ligand, sample, time_min, replicate):
        expt = expts[reaction, time_min]

        well = Well()
        well.reaction = reaction
        well.ligand = ligand
        well.sample = sample
        well.time_min = time_min
        well.replicate = replicate
        well.args = reaction, ligand, sample, time_min, replicate
        well.row = rows[reaction, time_min][replicate]
        well.col = columns[ligand, sample]
        well.id = f'{well.row}{well.col}'
        well.blank = blanks[well.row]
        well.color = colors[reaction, sample]

        return decoratee(expt, well)

    return decorator

def yield_wells():
    i = 0
    for sample in ('lz/on', 'lz/off', 'lz/11', 'lz/30'):
        for reaction in ('plate', 'tube'):
            for ligand in ('apo', 'holo'):
                for time_min in times[reaction]:
                    yield i, reaction, ligand, sample, time_min
                    i += 1


@well_from_args
def raw_od660(expt, well):
    row = od660_rows[well.replicate]
    return cultures.reads[660][f'{row}{well.col}']
    
@well_from_args
def normed_od660(expt, well):
    blank = od660_blanks[well.replicate]
    # Divide by two because I loaded 200 µL of cells in the OD wells, but only 
    # 100 µL in the actual reactions.
    return (raw_od660(*well.args) - cultures.reads[660][blank]) / 2

@well_from_args
def raw_a420(expt, well):
    return expt.reads[420][well.id]

@well_from_args
def normed_a420(expt, well):
    return raw_a420(*well.args) - expt.reads[420][well.blank]

@well_from_args
def miller_units(expt, well):
    a420 = normed_a420(*well.args)
    od660 = normed_od660(*well.args)
    volume_mL = 0.1
    time_min = well.time_min

    return 1000 * a420 / (od660 * volume_mL * time_min)


def make_dataframe():
    rows = []

    for i, reaction, ligand, sample, time_min in yield_wells():
        for replicate in (0,1):
            args = reaction, ligand, sample, time_min, replicate
            row = dict(
                    reaction     = reaction,
                    ligand       = ligand,
                    sample       = sample,
                    time_min     = time_min,
                    replicate    = replicate,
                    raw_od660    = raw_od660(*args),
                    normed_od660 = normed_od660(*args),
                    raw_a420     = raw_a420(*args),
                    normed_a420  = normed_a420(*args),
                    miller_units = miller_units(*args),
            )
            rows.append(row)

    return pd.DataFrame(rows)

def make_plot():
    plt.gcf().set_size_inches(11, 8)
    xticks = []
    xtick_labels = []

    for i, reaction, ligand, sample, time_min in yield_wells():
        xticks.append(i)
        xtick_labels.append(f't={time_min} {ligand} {reaction} {sample}')
        rates = [
                miller_units(reaction, ligand, sample, time_min, replicate)
                for replicate in (0, 1)
        ]
        x = [i, i]
        y = [0, np.mean(rates)]
        yerr = [np.std(rates)]
        color = colors[reaction, sample]

        plt.plot(x, y, linewidth=5, color=color)
        plt.errorbar(x[1:], y[1:], yerr, color=color)

    plt.xticks(xticks, xtick_labels, rotation='vertical')
    plt.xlim(-0.5, i+0.5)
    plt.ylabel('β-galactosidase activity (Miller units)')
    plt.grid(axis='y')

    plt.tight_layout()
    plt.savefig('20180717_tube_vs_plate.svg')
    plt.show()




pd.set_option('display.max_rows', 1000)
print(make_dataframe())

make_plot()

