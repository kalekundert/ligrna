#!/usr/bin/env python3

"""\
Make scatter plots showing the relationship between two channels for every cell 
in a single flow cytometry experiment.  The ``fold_change.py`` script presents 
a lot of the same information in a more compact way, but it can still be useful 
to look at the scatter plots if you want a less processed view of your data.

Usage:
    scatter_plot.py <yml_path> <experiment> [options]

Arguments:
    <yml_path>
        Path to a YAML file specifying which wells and which plates should be 
        compared with each other.

    <experiment>
        The label name of one of the experiments in the given YAML file.

Options:
    -o --output <path>
        If an output path is specified, the resulting plot is written to that 
        path and the GUI isn't opened.  Dollar signs ($) in the output path 
        are replaced by the base name of the given experiment, minus the '.yml' 
        suffix.  The <path> "lpr" is treated specially and causes the plot to 
        be sent to the printer via 'lpr'.  By default, no output is generated 
        and the plot is shown in the GUI.

    -C --size-channels
        Show forward scatter vs. side scatter plots (which reflect the size of 
        the particles passing the detector) rather than red fluorescence vs. 
        green fluorescence plots.

    -t --time-gate <secs>               [default: 0]
        Exclude the first cells recorded from each well if you suspect that 
        they may be contaminated with cells from the previous well.  The 
        default is to keep all the data.

    -z --size-gate <percentile>         [default: 0]
        Exclude the smallest cells from the analysis.  Size is defined as 
        ``FSC + m * SSC``, where ``m`` is the slope of the linear regression 
        relating the two scatter channels.  The given percentile specifies how 
        many cells are excluded.

    -x --expression-gate <signal>       [default: 1e3]
        Exclude cells where the signal on the fluorescence control channel is 
        less than the given value.  The purpose of this gate is to get rid of 
        cells that weren't expressing much fluorescent protein, for whatever 
        reason.  Note that this gate is in absolute units, not log units.

    -n --contour-steps <num>            [default: 4]
        How many contour levels should be shown for the highest peak of all the 
        wells being plotted.  Showing more contours allows more peaks to be 
        seen, but showing too many makes it hard to distinguish the individual 
        levels.

    -a --cell-alpha <value>             [default: 0.5]
        The transparency level of the points representing cells in the scatter 
        plot.  Values must be between 0 and 1.

    --histogram-bins <num>              [default: 50]
        The number of bins to use in each dimension when calculating the 
        contour lines.

    --raw-contours
        Disable the spline interpolation algorithm that is used by default to 
        smooth the contour lines.  The smoothing algorithm ameliorates the 
        inherent blockiness of the binned histogram without changing the shape 
        of the contours, so you should rarely want to disable it.

    --zoom-level <magnification>        [default: 3]
        The smoothing algorithm work by "zooming in" on the data by a certain 
        amount, filling in the extra pixels using a spline interpolation, then 
        zooming back out.  This parameter tells the algorithm how much to zoom 
        in, but I've found that it doesn't have much effect on the results.

    --force-vector
        If the scatter plots would be exported to a vector file format like PDF 
        or SVG (either via the command-line or the GUI), force ``matplotlib`` 
        to represent each individual point as a vector object.  By default, 
        these points (but not the lines or the text that make up the rest of 
        the figure) would be rasterized.  This option makes the resulting file 
        much larger and makes exporting and viewing that file take much longer.  
"""

import collections, docopt, fcmcmp, analysis_helpers
import numpy as np, matplotlib.pyplot as plt
from pprint import pprint
from debugtools import p, pp, pv

class ScatterPlot(analysis_helpers.ExperimentPlot):
    Histogram = collections.namedtuple('Histogram', 'x y z')

    def __init__(self, experiment):
        super().__init__(experiment)

        # Settings configured by the user.
        self.show_sizes = None
        self.histogram_bins = None
        self.smooth_contours = None
        self.zoom_level = None
        self.contour_steps = None
        self.cell_alpha = None
        self.rasterize_cells = None

        # Internally used plot attributes.
        self.histograms = None
        self.x_channel = None
        self.y_channel = None
        self.min_coord = None
        self.max_coord = None
        self.contour_levels = None

    def plot(self):
        self._create_axes(square=True)
        self._set_titles()
        self._set_channels()
        self._set_limits()

        self._create_histograms()
        self._set_levels()

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self._plot_cells(row, col)
                self._plot_contours(row, col)

        return self.figure

    def _set_channels(self):
        """
        Decide what data to plot on the x- and y-axes.
        """
        if self.show_sizes:
            self.x_channel = 'FSC-A'
            self.y_channel = 'SSC-A'
        elif 'cerevisiae' in self.experiment['species']:
            self.x_channel = 'FSC-A'
            self.y_channel = 'FITC-A'
        else:
            self.x_channel = 'FITC-A'
            self.y_channel = 'Red-A'

        # Label the axes with the chosen channel names.

        self._set_labels(self.x_channel, self.y_channel)

    def _set_limits(self):
        """
        Decide what the axes limits should be.

        The axes are fixed to a particular size based on which channels are 
        being shown.  Not rescaling to the data itself makes it easier to 
        compare plots from different experiments.  It also forces the axes to 
        be square.
        """
        self.min_coord = 1
        self.max_coord = 6

        self.axes[0,0].set_xlim(self.min_coord, self.max_coord)
        self.axes[0,0].set_ylim(self.min_coord, self.max_coord)

        # Only put ticks on integer values.  Fractional ticks (like 3.5) are 
        # harder to interpret (because these are log units) and tend to clutter 
        # up the axis.
        if not self.show_sizes:
            from matplotlib.ticker import MultipleLocator
            self.axes[0,0].xaxis.set_major_locator(MultipleLocator())
            self.axes[0,0].yaxis.set_major_locator(MultipleLocator())

    def _create_histograms(self):
        self.histograms = {x: [] for x in experiment['wells']}

        for condition in self.experiment['wells']:
            self.histograms[condition] = []

            for well in self.experiment['wells'][condition]:
                z, x_bins, y_bins = np.histogram2d(
                        well.data[self.x_channel],
                        well.data[self.y_channel],
                        bins=np.linspace(
                            self.min_coord, self.max_coord,
                            self.histogram_bins),
                )
                x = (x_bins[1:] + x_bins[:-1]) / 2
                y = (y_bins[1:] + y_bins[:-1]) / 2

                if self.smooth_contours:
                    # Smooth the histogram by "zooming in" and using spline 
                    # interpolation to fill in the extra "pixels".
                    import scipy.ndimage
                    z = scipy.ndimage.zoom(z, self.zoom_level)
                    x = np.linspace(x.min(), x.max(), len(x) * self.zoom_level)
                    y = np.linspace(y.min(), y.max(), len(y) * self.zoom_level)

                histogram = self.Histogram(x, y, z.T)
                self.histograms[condition].append(histogram)

    def _set_levels(self):
        """
        Pick which contours to draw.

        The contours are chosen to match the data.  The highest peak is found, 
        and then a fixed number of linearly spaced steps are made to get to 
        that level.  Because contours are chosen based on the data, they are 
        not comparable between different experiments.
        """
        max_z = max(
                histogram.z.max()
                for condition in self.histograms
                for histogram in self.histograms[condition]
        )
        self.contour_levels = np.linspace(0, max_z, self.contour_steps+2)[1:]

    def _plot_cells(self, row, col):
        axis = self.axes[row, col]
        well = self._get_well(row, col)

        axis.plot(
                well.data[self.x_channel],
                well.data[self.y_channel],
                marker=',',
                linestyle='',
                color=analysis_helpers.pick_color(self.experiment),
                zorder=1,
                alpha=self.cell_alpha,
                rasterized=self.rasterize_cells,
        )

    def _plot_contours(self, row, col):
        axis = self.axes[row, col]
        histogram = self._get_histogram(row, col)
        axis.contour(
                histogram.x,
                histogram.y,
                histogram.z,
                levels=self.contour_levels,
                colors=analysis_helpers.pick_color(self.experiment, lightness=2),
                zorder=2,
        )

    def _get_histogram(self, row, col):
        return self.histograms[self._get_condition(row)][col]



if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    experiment = fcmcmp.load_experiment(args['<yml_path>'], args['<experiment>'])

    shared_steps = analysis_helpers.SharedProcessingSteps()
    shared_steps.early_event_threshold = float(args['--time-gate'])
    shared_steps.small_cell_threshold = float(args['--size-gate'])
    shared_steps.low_fluorescence_threshold = float(args['--expression-gate'])
    shared_steps.process([experiment])

    log_transformation = fcmcmp.LogTransformation()
    log_transformation.channels = ['FITC-A', 'Red-A', 'FSC-A', 'SSC-A']
    log_transformation([experiment])

    analysis = ScatterPlot(experiment)
    analysis.show_sizes = args['--size-channels']
    analysis.histogram_bins = int(args['--histogram-bins'])
    analysis.smooth_contours = not args['--raw-contours']
    analysis.zoom_level = float(args['--zoom-level'])
    analysis.contour_steps = int(args['--contour-steps'])
    analysis.cell_alpha = float(args['--cell-alpha'])
    analysis.rasterize_cells = not args['--force-vector']

    with analysis_helpers.plot_or_savefig(args['--output'], args['<yml_path>']):
        analysis.plot()
