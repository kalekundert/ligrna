#!/usr/bin/env python3

"""\
Usage:
    make_heatmap.py [options]

Options:
    -o --output <path>
        If an output path is specified, the resulting plot is written to that 
        path and the GUI isn't opened.  The <path> "lpr" is treated specially 
        and causes the plot to be sent to the printer via 'lpr'.  By default, 
        no output is generated and the plot is shown in the GUI.
        
    -O --output-size <width "x" height>
        Specify what the width and height of the resulting figure should be, in 
        inches.  The two numbers must be separated by an "x".

    -A --show-all-designs
        Include all of the sgRNAs (including the controls) in the heatmap.  By 
        default, only rxb/11/1 and mhf/30 are included.

    -L --no-label-spacers
        Don't label the spacers.
"""

import docopt
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
from sgrna_sensor import densiometry
from color_me import ucsf
from pprint import pprint

DATA_DIR = Path(__file__).parent / 'densiometry'

class SpacerHeatmap:
    rows = 3
    designs = None
    all_designs = 'on', 'off', 'rxb 11,1', 'mhf 30', 'mhf 37'
    select_designs = 'rxb 11,1', 'mhf 30'
    show_all_designs = False
    label_spacers = True
    width_ratio = 20
    fig_size = None

    def __init__(self, df):
        self.df = df

    def plot(self):
        self._pick_designs()
        self._setup_figure()
        self._setup_axes()
        self._setup_colorbar()
        self._plot_data()
        self._plot_controls()
        return self.fig

    def _pick_designs(self):
        """
        Decide which designs to include in the heatmap.  The decision is made 
        in such a way to the user can easily control the result.
        """
        # Don't do anything if the user manually provided a list of designs to 
        # show.
        if self.designs is not None:
            return

        # Otherwise, check a flag to see if we should include all the designs, 
        # or just the ones we want to focus on in the paper.
        if self.show_all_designs:
            self.designs = self.all_designs
        else:
            self.designs = self.select_designs

    def _setup_figure(self):
        """
        Create a figure, and size it according to the number of rows that will 
        be plotted.
        """
        if self.fig_size:
            size = self.fig_size
        else:
            size = 6, 1.0 + 0.42 * len(self.designs) * self.rows

        self.fig = plt.figure(figsize=size)

    def _setup_axes(self):
        grid = mpl.gridspec.GridSpec(
                self.rows, 2,
                width_ratios=[self.width_ratio, 1],
        )
        self.ax = [
                self.fig.add_subplot(grid[y,0])
                for y in range(self.rows)
        ]
        self.cax = self.fig.add_subplot(grid[:,1])

    def _setup_colorbar(self):
        self.norm = LinearSegmentedNorm([
            (-1.0, 0.000),
            (-0.3, 0.125),
            ( 0.3, 0.875),
            ( 1.0, 1.000),
        ])
        self.cmap = mpl.colors.LinearSegmentedColormap.from_list('mhf_rxb', [
            (self.norm(-1.0), ucsf.navy[0]),
            (self.norm( 0.0), ucsf.white[0]),
            (self.norm( 1.0), ucsf.teal[0]),
        ])
        self.sm = plt.cm.ScalarMappable(cmap=self.cmap)
        self.sm.set_array([])

        # Draw the color bar, and show where the linear scale changes using 
        # ticks.  Note that the ticks are in normalized units [0,1].
        cb = mpl.colorbar.Colorbar(self.cax, self.sm)
        ticks = np.arange(-1.0, 1.05, 0.1)
        cb.set_ticks(self.norm(ticks))
        cb.set_ticklabels([
                '' if 0.35 < abs(x) < 0.95 else f'{100 * x:.0f}%'
                for x in ticks
        ])

    def _plot_data(self):
        df = densiometry.calc_mean_change(self.df)
        df = densiometry.sort_by_activity(df, self.select_designs)

        if self.designs:
            designs = self.designs
        elif self.show_all_designs:
            designs = self.all_designs
        else:
            designs = self.select_designs

        data = np.vstack([
            df[df.design == x].mean_change.values
            for x in designs
        ])

        spacers = df['spacer'].unique()
        num_spacers = len(spacers)
        spacers_per_row = int(np.ceil(num_spacers / self.rows))

        for i in range(self.rows):
            j0 = spacers_per_row * (i + 0)
            j1 = spacers_per_row * (i + 1)

            self.ax[i].pcolor(data[:,j0:j1], cmap=self.cmap, norm=self.norm)
            self.ax[i].set_yticks(0.5 + np.arange(len(self.designs)))
            self.ax[i].set_yticklabels(self.designs)
            self.ax[i].set_xticks(0.5 + np.arange(spacers_per_row))
            self.ax[i].set_xticklabels(spacers[j0:j1] if self.label_spacers else [])
            self.ax[i].axis('image')

    def _plot_controls(self):
        """
        Draw an error bar representing the controls on top of the color bar.  
        This is meant to illustrate which colors are significantly different 
        than the controls.
        """
        df = densiometry.calc_percent_change(self.df)
        designs = df.index.get_level_values(level='design')
        controls = df[designs.isin(['on', 'off'])]

        n = len(controls)
        mu = controls.percent_change.mean()
        sig = controls.percent_change.std()

        x = np.mean(self.cax.get_xlim())
        self.cax.plot(
                [x, x], [self.norm(mu+sig), self.norm(mu-sig)],
                linestyle='-', marker='_', color=ucsf.dark_grey[0],
        )
        print(f"{n} control measurements")


class LinearSegmentedNorm(mpl.colors.Normalize):

    def __init__(self, segments):
        # 'xp and 'fp' correspond to the parameters for `np.interp()`.
        self.xp, self.fp = zip(*segments)
        super().__init__(min(self.xp), max(self.xp))

    def __call__(self, x, clip=None):
        """
        Convert data point (x) to normalized units.
        """
        f = np.interp(x, self.xp, self.fp)
        return np.ma.masked_array(f)

    def inv(self, f):
        """
        Convert a normalized value (f) back to data units.
        """
        x = np.interp(f, self.fp, self.xp)
        return np.ma.masked_array(x)



if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    df = densiometry.load_cleavage_data_from_xlsx_dir(DATA_DIR)

    heatmap = SpacerHeatmap(df)
    heatmap.show_all_designs = args['--show-all-designs']
    heatmap.label_spacers = not args['--no-label-spacers']
    if args['--output-size']:
        heatmap.fig_size = [float(x) for x in args['--output-size'].split('x')]

    with densiometry.plot_or_savefig(args['--output'], '20170329_test_multiple_spacers'):
        heatmap.plot()
