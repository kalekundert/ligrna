#!/usr/bin/env python3

"""
Usage:
    find_apparent_kd.py [gui]
"""

import docopt
from pylab import *
from scipy.optimize import curve_fit

args = docopt.docopt(__doc__)

data = np.array([
        # Sep 23
        #(10000, 0.834),
        #(5000,  0.815),
        #(2500,  0.732),
        #(1250,  0.600),
        #(625,   0.496),
        #(313,   0.399),
        #(156,   0.335),
        #(78,    0.243),
        #(39,    0.207),
        #(20,    0.163),
        #(10,    0.133),
        #(5,     0.106),
        #(2,     0.098),
        #(1,     0.069),
        #(0,     0.072),

        # Oct 3
        (10000, 0.880),
        (5000,  0.863),
        (2500,  0.773),
        (1250,  0.524),
        (625,   0.303),
        (313,   0.280),
        (156,   0.181),
        (78,    0.106),
        (39,    0.060),
        (20,    0.036),
        (10,    0.041),
        (5,     0.031),
        (2,     0.026),
        (1,     0.023),
        (0,     0.019),
])

conc = data[:,0]
cut = data[:,1]
x = zeros(1), geomspace(conc[-2], conc[0])
x = concatenate(x)

one_site_binding = lambda x, Bmax, Kd: (Bmax * x) / (Kd + x)
initial_guess = 1, 100
bounds = (0, 0), (1, inf)
Bmax, Kd = curve_fit(
        one_site_binding, conc, cut, p0=initial_guess, bounds=bounds)[0]
y = one_site_binding(x, Bmax, Kd)
summary = f'Kd={Kd:.2f} μM, Bmax={100*Bmax:.2f}%'

def logistic_ec50(x, Ymin, Ymax, ec50): #
    y = empty(x.shape)
    y[x != 0] = Ymin + (Ymax - Ymin) / (1 + (ec50 / x[x != 0]))
    y[x == 0] = Ymin
    return y

initial_guess = 0, 1, 100
bounds = (0, 0, 0), (1, 1, inf)
Ymin, Ymax, ec50 = curve_fit(
        logistic_ec50, conc[conc > 0], cut[conc > 0], p0=initial_guess, bounds=bounds)[0]
y = logistic_ec50(x, Ymin, Ymax, ec50)
summary = f'ec50={ec50:.2f} μM, Ymin={100*Ymin:.1f}%, Ymax={100*Ymax:.1f}%'


#axvline(Kd, linestyle='--', color='grey')
axvline(ec50, linestyle='--', color='grey')
plot(conc, cut, 'o', label='data')
plot(x, y, label=f'fit ({summary})', color='C0')
xscale('symlog')
ylim(0, 1)
xlim(min(conc), max(conc))
xlabel('theo [μM]')
xlabel('cleavage (%)')
legend(loc='best')
tight_layout()

if args['gui']:
    show()

savefig('find_apparent_kd.svg')
