#!/usr/bin/env python3

"""\
Usage:
    make_bar_plot.py [options]

Options:
    -o --output <path>
        If an output path is specified, the resulting plot is written to that 
        path and the GUI isn't opened.  The <path> "lpr" is treated specially 
        and causes the plot to be sent to the printer via 'lpr'.  By default, 
        no output is generated and the plot is shown in the GUI.
        
    -O --output-size <width "x" height>
        Specify what the width and height of the resulting figure should be, in 
        inches.  The two numbers must be separated by an "x".
"""

import docopt
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
from sgrna_sensor import densiometry
from color_me import ucsf

import types

DATA_DIR = Path(__file__).parent / 'densiometry'

class BarPlot:
    designs = 'mhf 30', 'rxb 11,1'
    controls = 'on', 'off'
    success_cutoff = 15
    fig_size = None

    bar_style = {
            'linewidth': 4,
    }
    err_line_style = {
            'linewidth': 1,
    }
    err_marker_style = {
            'marker': '_',
            'markersize': 4,
    }
    y_max = {
            'mhf 30': 70,
            'rxb 11,1': 100,
    }
    colors = {
            'mhf 30': ucsf.teal[0],
            'rxb 11,1': ucsf.navy[0],
    }

    def __init__(self, df):
        self.df = df

    def plot(self):
        self._setup_figure()
        self._plot_controls()
        self._plot_data()
        plt.tight_layout(pad=0, h_pad=0)
        return self.fig

    def _setup_figure(self):
        self.fig, self.axes = plt.subplots(
                nrows=2,
                ncols=1,
                sharex=True,
                figsize=self.fig_size,
        )
        self.axes[0].set_xlabel('')

    def _plot_controls(self):
        df = densiometry.calc_percent_change(self.df)
        
        for i, control in enumerate(self.controls, 1):
            controls = df.xs(control, level='design')
            mean = controls.percent_change.mean()
            stdev = controls.percent_change.std()

            for axes in self.axes:
                self._plot_bar(axes, i - 3, mean, stdev, ucsf.light_grey[0])

            print(f"{control}: {len(controls)} measurements")

    def _plot_data(self):
        df = densiometry.calc_mean_change(self.df)
        df = densiometry.sort_by_activity(df, self.designs)

        for i, design in enumerate(self.designs):
            success_count = 0

            for j, row in df[df.design == design].reset_index().iterrows():
                success_count += self._plot_bar(
                        self.axes[i], j,
                        row.mean_change,
                        row.std_change,
                        self.colors[design],
                )

            # If a figure size was given, also try to take some steps to ensure 
            # a more regular/representative size.  In particular, use shorter 
            # labels and don't redundant axes.

            y_max = self.y_max[design]
            self.axes[i].set_ylabel('Δ cleavage (%)' if not self.fig_size else 'Δ (%)')
            self.axes[i].set_ylim((0, y_max))
            self.axes[i].set_yticks([0, y_max//2, y_max])


            self.axes[i].set_xlabel('spacer' if i == 1 else '')
            self.axes[i].set_xlim((-3, j+1))
            self.axes[i].set_xticks(range(-2, j+1))
            self.axes[i].set_xticklabels(
                    ['on', 'off'] + [str(x) for x in range(1, j+2)],
                    rotation='vertical'
            )
            self.axes[i].axhline(
                        self.success_cutoff,
                        color=ucsf.light_grey[0],
                        linestyle='--',
            )
        
            print(f'{design}: {success_count}/{j+1}')

    def _plot_bar(self, axes, i, mean, err, color):
        x = i, i
        y = 0, 100 * abs(mean)
        y_err = y[1] - 100 * err, y[1] + 100 * err

        axes.plot(x, y, color=color, **self.bar_style)[0]
        axes.plot(x, y_err, color=color, **self.err_line_style)
        axes.plot(x[1], y_err[1], color=color, **self.err_marker_style)

        return y[1] > self.success_cutoff

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    df = densiometry.load_cleavage_data_from_xlsx_dir(DATA_DIR)

    graphic = BarPlot(df)
    if args['--output-size']:
        graphic.fig_size = [float(x) for x in args['--output-size'].split('x')]

    with densiometry.plot_or_savefig(args['--output'], '20170329_test_multiple_spacers'):
        graphic.plot()
