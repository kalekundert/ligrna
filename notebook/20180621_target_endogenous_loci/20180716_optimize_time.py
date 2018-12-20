#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from itertools import product
from color_me import ucsf
from plate_reader import BetaGalExperiment

expts = {
        '2h': BetaGalExperiment('plate_reader/20180716_optimize_time_2h.xlsx'),
        '4h': BetaGalExperiment('plate_reader/20180716_optimize_time_4h_2h.xlsx'),
        '6h': BetaGalExperiment('plate_reader/20180716_optimize_time_6h_4h_2h.xlsx'),
}

delays = {
        '2h': 20,
        '4h': 21,
        '6h': 49,
}

def get_normalized_absorbance(expt, nm, well):
    a420 = expts[expt].kinetic[420][well]
    a550 = expts[expt].kinetic[550][well]
    od660 = expts[expt].reads[660][well]
    return (a420 - 1.75*a550) / od660

def get_kinetic(expt, well, nm):
    return expts[expt].kinetic[nm][well]

def get_read(expt, well, nm):
    return expts[expt].reads[nm][get_od_well(well)]

def get_od_well(well):
    row, col = well[0], int(well[1:])
    return f'{row}{col-4}' if col > 5 else well

def get_miller_units(expt, well, time_min=None, normalize='linear'):
    if time_min is None:
        time_min = expts[expt].kinetic[420].minutes + delays[expt]

    volume_ml = 0.1  # Volume of cells, e.g. 100 µL.
    a420 = expts[expt].kinetic[420][well]
    a550 = expts[expt].kinetic[550][well]
    od660 = expts[expt].reads[660][get_od_well(well)]


    if normalize == '550':
        return 1000 * (a420 - 1.75*a550) / (time_min * volume_ml * od660)
    elif normalize == 'linear':
        m, b = np.polyfit(time_min, a420, 1)
        return 1000 * (a420 - b        ) / (time_min * volume_ml * od660)
    elif normalize == 'none':
        return 1000 * (a420            ) / (time_min * volume_ml * od660)
    else:
        raise ValueError(f"unknown normalization '{normalize}'")


def construct_2h_series():
    df = pd.DataFrame()
    df['t'] = t = expts['2h'].kinetic_420.minutes + delays['2h']
    df['2h/off/-iptg/plate'] = get_miller_units('2h', 'A3', t)
    df['2h/off/-iptg/plate/420'] =  get_kinetic('2h', 'A3', 420)
    df['2h/off/-iptg/plate/550'] =  get_kinetic('2h', 'A3', 550)
    df['2h/off/-iptg/plate/660'] =     get_read('2h', 'A3', 660)
    df['2h/off/+iptg/plate'] = get_miller_units('2h', 'A5', t)
    df['2h/off/+iptg/plate/420'] =  get_kinetic('2h', 'A5', 420)
    df['2h/off/+iptg/plate/550'] =  get_kinetic('2h', 'A5', 550)
    df['2h/off/+iptg/plate/660'] =     get_read('2h', 'A5', 660)
    df['2h/off/-iptg/tube']  = get_miller_units('2h', 'A7', t - 1)
    df['2h/off/-iptg/tube/420'] =   get_kinetic('2h', 'A7', 420)
    df['2h/off/-iptg/tube/550'] =   get_kinetic('2h', 'A7', 550)
    df['2h/off/-iptg/tube/660'] =      get_read('2h', 'A7', 660)
    df['2h/off/+iptg/tube']  = get_miller_units('2h', 'A9', t - 3)
    df['2h/off/+iptg/tube/420'] =   get_kinetic('2h', 'A9', 420)
    df['2h/off/+iptg/tube/550'] =   get_kinetic('2h', 'A9', 550)
    df['2h/off/+iptg/tube/660'] =      get_read('2h', 'A9', 660)
    return df

def construct_4h_series():
    raise ValueError("""missing OD660 data for the 4h timepoint.

I forgot to measure OD660 for the 4h timepoint, so I can't calculate Miller 
units for any of these samples.""")

def construct_6h_series():
    df = pd.DataFrame()
    df['t'] = t = expts['6h'].kinetic_420.minutes + delays['6h']
    df['6h/off/-iptg/plate'] = get_miller_units('6h', 'C3', t)
    df['6h/off/-iptg/plate/420'] =  get_kinetic('6h', 'C3', 420)
    df['6h/off/-iptg/plate/550'] =  get_kinetic('6h', 'C3', 550)
    df['6h/off/-iptg/plate/660'] =     get_read('6h', 'C3', 660)
    df['6h/off/+iptg/plate'] = get_miller_units('6h', 'C5', t)
    df['6h/off/+iptg/plate/420'] =  get_kinetic('6h', 'C5', 420)
    df['6h/off/+iptg/plate/550'] =  get_kinetic('6h', 'C5', 550)
    df['6h/off/+iptg/plate/660'] =     get_read('6h', 'C5', 660)
    df['6h/off/-iptg/tube']  = get_miller_units('6h', 'C7', t - 2)
    df['6h/off/-iptg/tube/420'] =   get_kinetic('6h', 'C7', 420)
    df['6h/off/-iptg/tube/550'] =   get_kinetic('6h', 'C7', 550)
    df['6h/off/-iptg/tube/660'] =      get_read('6h', 'C7', 660)
    df['6h/off/+iptg/tube']  = get_miller_units('6h', 'C9', t - 3)
    df['6h/off/+iptg/tube/420'] =   get_kinetic('6h', 'C9', 420)
    df['6h/off/+iptg/tube/550'] =   get_kinetic('6h', 'C9', 550)
    df['6h/off/+iptg/tube/660'] =      get_read('6h', 'C9', 660)
    return df

fig, ax = plt.subplots(2, 2)

df2 = construct_2h_series()
df6 = construct_6h_series()

df2.plot('t', '2h/off/-iptg/plate/420', ax=ax[0,0], color=ucsf.light_grey[0])
df2.plot('t', '2h/off/-iptg/tube/420',  ax=ax[0,0], color=ucsf.light_grey[0], ls=':')
df2.plot('t', '2h/off/+iptg/plate/420', ax=ax[0,0], color=ucsf.black[0])
df2.plot('t', '2h/off/+iptg/tube/420',  ax=ax[0,0], color=ucsf.black[0], ls=':')

df2.plot('t', '2h/off/-iptg/plate',     ax=ax[1,0], color=ucsf.light_grey[0])
df2.plot('t', '2h/off/-iptg/tube',      ax=ax[1,0], color=ucsf.light_grey[0], ls=':')
df2.plot('t', '2h/off/+iptg/plate',     ax=ax[1,0], color=ucsf.black[0])
df2.plot('t', '2h/off/+iptg/tube',      ax=ax[1,0], color=ucsf.black[0], ls=':')

df6.plot('t', '6h/off/-iptg/plate/420', ax=ax[0,1], color=ucsf.light_grey[0])
df6.plot('t', '6h/off/-iptg/tube/420',  ax=ax[0,1], color=ucsf.light_grey[0], ls=':')
df6.plot('t', '6h/off/+iptg/plate/420', ax=ax[0,1], color=ucsf.black[0])
df6.plot('t', '6h/off/+iptg/tube/420',  ax=ax[0,1], color=ucsf.black[0], ls=':')

df6.plot('t', '6h/off/-iptg/plate',     ax=ax[1,1], color=ucsf.light_grey[0])
df6.plot('t', '6h/off/-iptg/tube',      ax=ax[1,1], color=ucsf.light_grey[0], ls=':')
df6.plot('t', '6h/off/+iptg/plate',     ax=ax[1,1], color=ucsf.black[0])
df6.plot('t', '6h/off/+iptg/tube',      ax=ax[1,1], color=ucsf.black[0], ls=':')

xlim = {
        0: (0, 90),
        1: (0, 155),
}

for i, j in product(range(2), repeat=2):
    ax[i,j].set_xlim(xlim[j])

ax[0,0].tick_params(labelbottom=False)
ax[0,0].set_title('2h')
ax[0,1].tick_params(labelbottom=False)
ax[0,1].set_title('6h')

for x in ax.flat:
    x.set_xlabel('')
    x.set_ylabel('')

ax[0,0].set_ylabel('A420')
ax[1,0].set_ylabel('Activity (Miller units)')
ax[1,0].set_xlabel('time (min)')
ax[1,1].set_xlabel('time (min)')

for a in ax.flat:
    a.legend().remove()

fig.tight_layout()
fig.savefig('20180716_optimize_time.svg')
plt.show()

