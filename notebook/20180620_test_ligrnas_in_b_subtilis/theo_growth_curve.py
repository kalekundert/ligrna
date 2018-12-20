#!/usr/bin/env python3

"""\
Plot the growth rate of B. subtilis for different concentrations of 
theophylline.

Usage:
    theo_growth_curve.py <layout.toml> [options]

Options:
    -s --show
        Open the figures in a GUI.

    -o --od-only
        Only show the growth curves and the doubling time comparison.

    -g --gfp-only
        Only show the GFP plot.

    -F --hide-fits
        Don't include the fits in the OD plots (e.g. because they suck).
"""

import docopt, toml
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict, namedtuple
from scipy.optimize import curve_fit
from scipy.integrate import odeint
from sgrna_sensor import plate_reader
from color_me import ucsf

formats = {
        'PerkinElmer': plate_reader.PerkinElmerExperiment,
        'Biotek': plate_reader.BiotekExperiment,
}

class TheoGrowthCurve:

    def __init__(self, params):
        self.params = params
        self.colors = params.get('colors', {
                'on': ucsf.black[1],
                'off': ucsf.black[0],
                '11': ucsf.navy[0],
                '30': ucsf.teal[0],
        })
        self.expt = formats[params['format']](params['expt'])
        self.layout = params['layout']
        self._subtract_blanks()
        self.num_sgrnas = len(self.layout)
        self.num_conc = max(len(v) for v in self.layout.values())
        self.hide_fits = False

        # These are calculated in `plot_od600()`, so that needs to be called 
        # before anything else.
        self.fit_params = {
                k: defaultdict(lambda: [])
                for k in self.layout
        }

    def plot_od600(self, path=None, figsize=2):
        od600 = self.expt.reads['absorbance_600_nm']
        t_vis = self.params.get('t_lim', (0, 300))
        od_vis = self.params.get('od_lim', (0.00, 0.10))
        t_fit_min = self.params.get('fit_min_t', 0)
        od_fit_max = self.params.get('fit_max_od', 0.04)

        FitParams = namedtuple('FitParams', ['od0', 't12', 'blank'])
        p0 = FitParams(1e-3, 30, 0)  # Initial guess.
        bounds = [
                (   0,      0, -np.inf),
                (0.05, np.inf,  np.inf),
        ]
        def growth_curve(t, *fit):
            return fit[0] * 2**(t / fit[1]) + fit[2]

        # FitParams = namedtuple('FitParams', ['od0', 't12', 'lag'])
        # p0 = FitParams(0.01, 30, 0)  # Initial guess.
        # bounds = [
        #         (0.00,  10,   0),
        #         (0.05, 100, 120),
        # ]
        # def growth_curve(t, *fit):
        #     fit = FitParams(*fit)
        #     od = fit.od0 * 2**((t - fit.lag) / fit.t12)
        #     od[t < fit.lag] = fit.od0
        #     return od

        # FitParams = namedtuple('FitParams', ['od0', 'r', 'c', 'od_min', 'od_max'])
        # p0 = 1, 30, 0.01, 1.00
        # bounds = None
        # def dod_dt(od, t, *params):
        #     r, c, od_min, od_max = params
        #     return (1/r) * od * (1 - od/od_max) * (1 - od_min/od)**c
        # def growth_curve(t, od0, *params):
        #     return odeint(dod_dt, od0, t, params).ravel()
            
        size_in = self.num_conc * figsize, self.num_sgrnas * figsize
        fig = plt.figure(figsize=size_in)
        axes = fig.subplots(
                self.num_sgrnas, self.num_conc,
                sharex=True, sharey=True,
        )

        for i in range(axes.shape[0]):
            axes[i,0].set_ylabel('OD600')
        for j in range(axes.shape[1]):
            axes[-1,j].set_xlabel('time (min)')

        for i, j, sgrna, conc, wells in self._iter_wells():
            color = self.colors[sgrna]
            style = dict(linestyle='none', marker='+')
            label = f'{sgrna} [{conc}]'

            ax = axes[i,j]
            ax.set_title(label)
            ax.set_xlim(*t_vis)
            ax.set_ylim(*od_vis)

            for well in wells:
                df = od600[od600['well'] == well]
                t = df['minutes']
                od = df['absorbance_600_nm']

                i_min = abs(t  -  t_fit_min).idxmin()
                i_max = abs(od - od_fit_max).idxmin()

                t_fit  =  t.loc[i_min:i_max]
                od_fit = od.loc[i_min:i_max]
                t_lin  = np.linspace(0, t_vis[-1])

                try:
                    fit, cov = curve_fit(
                            growth_curve, t_fit, od_fit,
                            p0=p0, bounds=bounds,
                    )
                    fit = FitParams(*fit)
                except RuntimeError:
                    print(f'failed to fit {well}')
                else:
                    self.fit_params[sgrna][conc].append(fit)
                    if not self.hide_fits:
                        ax.plot(
                                t_lin, growth_curve(t_lin, *fit),
                                color=color,
                                zorder=3,
                        )

                ax.plot(
                        t_fit, od_fit,
                        markerfacecolor='none',
                        markeredgecolor=color,
                        zorder=4,
                        marker='o',
                        linestyle='none',
                ),
                ax.plot(
                        t, od,
                        color=color,
                        zorder=4,
                        **style,
                )
                for other_ax in axes.flat:
                    if other_ax is not ax:
                        other_ax.plot(t, od, color=ucsf.light_grey[0], zorder=1, **style)

        return self._finalize_fig(fig, path)

    def plot_t12(self, path=None):
        fig, axes = plt.subplots(3, 1)
        axes_xticks = []
        y_labels = 'Initial OD', 't½ (min)', 'Blank error'
        # y_labels = 'Initial OD', 't½ (min)', 'Lag time (min)'

        for i, ax in enumerate(axes):
            x = 0
            ax.set_ylabel(y_labels[i])

            for _, _, sgrna, conc, wells in self._iter_wells():
                num_reps = len(self.fit_params[sgrna][conc])
                ys = [
                        self.fit_params[sgrna][conc][rep][i] 
                        for rep in range(num_reps)
                ]
                y = np.mean(ys)
                yerr = np.std(ys)
                color = self.colors[sgrna]

                ax.plot([x, x], [0, y], color=color, linewidth=5)
                ax.errorbar([x], [y], [yerr], color=color)
                if i == 0:
                    axes_xticks.append((x, f'[{conc}] {sgrna}'))

                x += 1

        xticks, xticklabels = zip(*axes_xticks)
        for ax in axes:
            ax.set_xticks(xticks)
            ax.set_xlim(xticks[0] - 0.5, xticks[-1] + 0.5)
            ax.tick_params(labelbottom=False)

        axes[2].set_xticklabels(xticklabels, rotation='vertical')
        axes[2].tick_params(labelbottom=True)

        return self._finalize_fig(fig, path)

    def plot_gfp(self, path=None, figsize=3):
        gfp = self.expt.reads['gfp']
        gfp_lim = self.params.get('gfp_lim')

        cmap = mpl.colors.LinearSegmentedColormap.from_list('ucsf', [
            mpl.colors.to_rgb(ucsf.orange[0]),
            mpl.colors.to_rgb(ucsf.purple[0]),
        ])
        norm = mpl.colors.Normalize(vmin=0, vmax=self.num_conc - 1)
        gradient = mpl.cm.ScalarMappable(norm, cmap)

        fig = plt.figure(figsize=(figsize*self.num_sgrnas, figsize))
        axes = fig.subplots(1, self.num_sgrnas, sharex=True, sharey=True)
        axes[0].set_ylabel('GFP (RFU)')
        for ax in axes:
            ax.set_xlabel('time (min)')
    
        for i, j, sgrna, conc, wells in self._iter_wells():
            ax = axes[i]
            ax.set_title(f'{sgrna}')
            ax.set_xlim(0, 600)
            if gfp_lim:
                ax.set_ylim(*gfp_lim)

            for k, well in enumerate(wells):
                df = gfp[gfp['well'] == well]
                ax.plot(
                        df.minutes, df.gfp,
                        color=gradient.to_rgba(j),
                        label=conc if i == 0 and k == 0 else '_nolabel_',
                )

        axes[0].legend(loc='upper left')
        return self._finalize_fig(fig, path)

    def _iter_wells(self):
        for i, sgrna in enumerate(self.layout):
            for j, conc in enumerate(self.layout[sgrna]):
                yield i, j, sgrna, conc, self.layout[sgrna][conc]

    def _subtract_blanks(self):
        # Problem: the indices don't match up because the times aren't the 
        # same...
        # Hacky solution: Use the median blank measurement.
        reads = self.expt.reads

        for i, j, sgrna, conc, wells in self._iter_wells():
            if conc == 'blank':
                continue

            blank_wells = self.layout[sgrna].get('blank')
            if not blank_wells:
                continue

            for well, blank in zip(wells, blank_wells):
                for wavelength in reads:
                    df = reads[wavelength]
                    df.loc[df.well == well, wavelength] -= \
                            df.loc[df.well == blank, wavelength].median()

        for concs in self.layout.values():
            if 'blank' in concs:
                del concs['blank']

    def _finalize_fig(self, fig, path):
        fig.tight_layout()
        if path: fig.savefig(path)
        return fig

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    in_path = args['<layout.toml>']
    out_path = Path(in_path).stem
    layout = toml.load(in_path)
    analyst = TheoGrowthCurve(layout)
    analyst.hide_fits = args['--hide-fits']

    if not args['--gfp-only']:
        analyst.plot_od600(f'./{out_path}_od600.png')
        analyst.plot_t12(  f'./{out_path}_t12.svg')
    if not args['--od-only']:
        analyst.plot_gfp(  f'./{out_path}_gfp.svg')

    if args['--show']:
        try: plt.show()
        except KeyboardInterrupt: print()

