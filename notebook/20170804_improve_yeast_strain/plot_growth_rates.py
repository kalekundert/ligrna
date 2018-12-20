#!/usr/bin/env python3

from pylab import *
from nonstdlib import minutes
from color_me import ucsf

# Import growth data.

class GrowthCurve:
    time_strs = []
    ods = []

    def __init__(self):
        self.update()

    def update(self):
        self.name = self.__class__.__name__

        if self.time_strs:
            self.times = [minutes(t) for t in self.time_strs]

        self.fit = self.od0, self.t12 = fit_growth_curve(self.times, self.ods)


class yAHN321(GrowthCurve):
    time_strs = [
            '0h00',
            '3h15',
            '4h05',
            '5h00',
            '6h15',
            '6h50',
    ]
    ods = [
        0.3193 * 1,
        0.3759 * 3,
        0.5451 * 3,
        0.6521 * 4,
        0.9923 * 4,
        1.0091 * 5,
    ]
    color = ucsf.red[0]

    # Discard the last two data points, which fall outside the linear range of 
    # the spectrophotometer.
    time_strs = time_strs[0:4]
    ods = ods[0:4]

class yBMH127(GrowthCurve):
    time_strs = [
            '0h00',
            '3h15',
            '4h05',
            '5h00',
            '6h15',
            '6h50',
    ]
    ods = [
            0.2755 * 1,
            0.1869 * 3,
            0.2395 * 3,
            0.2387 * 4,
            0.3391 * 4,
            0.3295 * 5,
    ]
    color = ucsf.blue[0]

class yBMH139(GrowthCurve):
    time_strs = [
        '0h00',
        '1h55',
        '3h49',
        '5h54',
        '7h04',
        '8h08',
    ]
    ods = [ 
        0.0247,
        0.0582,
        0.1397,
        0.3712,
        0.3309 * 2,
        0.3644 * 3,
    ]
    color = ucsf.olive[0]


# Calculate doubling times.

def growth_curve(t, od0, t12):
    return od0 * 2**(t / t12)

def fit_growth_curve(times, ods):
    from scipy.optimize import curve_fit
    initial_guess = 0.3, 100
    fit_od0, fit_t12 = curve_fit(growth_curve, times, ods, initial_guess)[0]
    return fit_od0, fit_t12


ahn321 = yAHN321()
bmh127 = yBMH127()
bmh139 = yBMH139()

# Make the plot.

def plot_curves(*curves):
    data_style = dict(
            linestyle='none',
            marker='o',
            markeredgecolor='none',
    )
    fit_style = dict(
    )

    clf()

    for curve in curves:
        plot(curve.times, curve.ods, color=curve.color, **data_style)

    t = linspace(*xlim())

    for curve in curves:
        plot(t, growth_curve(t, *curve.fit), color=curve.color,
                label=f'{curve.name} (t½={curve.t12:.1f} min)', **fit_style)

    xlabel("Time [min]")
    ylabel("OD600")

    legend(loc='upper left')


plot_curves(ahn321, bmh127)
savefig('ahn321_bmh127.svg')

plot_curves(bmh139)
savefig('bmh139.svg')

plot_curves(ahn321, bmh127, bmh139)
savefig('ahn321_bmh127_bmh139.pdf')
