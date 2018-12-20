#!/usr/bin/env python3

import matplotlib.pyplot as plt
from plate_reader import BetaGalExperiment
from color_me import ucsf

expts = {
        2: BetaGalExperiment('../../data/plate_reader/20180713_optimize_time_2h.xlsx'),
        3: BetaGalExperiment('../../data/plate_reader/20180713_optimize_time_3h.xlsx'),
        4: BetaGalExperiment('../../data/plate_reader/20180713_optimize_time_4h.xlsx'),
        5: BetaGalExperiment('../../data/plate_reader/20180713_optimize_time_5h.xlsx'),
        6: BetaGalExperiment('../../data/plate_reader/20180713_optimize_time_6h.xlsx'),
}

colors = {
        2: ucsf.purple[0],
        3: ucsf.blue[0],
        4: ucsf.olive[0],
        5: ucsf.orange[0],
        6: ucsf.navy[0],
}

for time, expt in expts.items():
    print(time)
    print(expt)
    df = expt.kinetic_420
    on, off = df.columns[2], df.columns[3]
    color = colors[time]
    activity = lambda col: df[col] / ((df.Minutes + 1) * expt.reads_660[col])
    print(activity(on))
    #plt.plot(df.Minutes, activity(on), label=f'on ({time}h)', color=color)
    #plt.plot(df.Minutes, activity(off), label=f'off ({time}h)', color=color, linestyle=':')
    plt.plot(df.Minutes, df[on], label=f'on ({time}h)', color=color)
    plt.plot(df.Minutes, df[off], label=f'off ({time}h)', color=color, linestyle=':')

plt.legend(loc='best')
plt.show()
