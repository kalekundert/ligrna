#!/usr/bin/env python3

"""\
Usage:
    scatter_plot.py <experiments> <name>
"""

## Things to do:
# - Parse command line arguments.
# - Pick nicer colors.
# - Show gated cells.


import os, collections, fcmcmp, docopt
import numpy as np, matplotlib.pyplot as plt
import warnings; warnings.simplefilter("error", FutureWarning)
from pprint import pprint

args = docopt.docopt(__doc__)
experiment = fcmcmp.load_experiment(args['<experiments>'], args['<name>'])

class ScatterPlot:

    Histogram = collections.namedtuple('Histogram', 'x y z')

    def __init__(self, experiment):
        # Settings configured by the user.
        self.experiment = experiment
        self.show_sizes = False
        self.histogram_bins = 50
        self.enable_smoothing = True
        self.zoom_level = 3
        self.contour_steps = 7
        self.cell_alpha = 0.2
        self.rasterize_cells = True

        # Internally used plot attributes.
        self.histograms = None
        self.figure = None
        self.axes = None
        self.num_rows = None
        self.num_cols = None
        self.x_channel = None
        self.y_channel = None
        self.min_coord = None
        self.max_coord = None
        self.contour_levels = None

    def plot(self):
        self._create_axes()
        self._set_channels()
        self._set_limits()
        self._set_titles()

        self._create_histograms()
        self._set_levels()

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self._plot_cells(row, col)
                self._plot_contours(row, col)

        return self.figure

    def _create_axes(self):
        """
        Work out how many wells need to be shown.
        
        There will be two rows and as many columns as necessary to show all the 
        wells.  The first row is for the "before" wells and the second row is 
        for the "after" ones.
        """
        num_before = len(self.experiment['wells']['before'])
        num_after = len(self.experiment['wells']['after'])

        self.num_rows = 2
        self.num_cols = max(num_before, num_after)

        # The 'squeeze=False' argument guarantees that the returned axes are 
        # always a 2D array, even if one of the dimensions happens to be 1.

        self.figure, self.axes = plt.subplots(
                self.num_rows, self.num_cols,
                sharex=True, sharey=True, squeeze=False,
        )
        

    def _set_channels(self):
        """
        Decide what data to plot on the x- and y-axes.
        """
        if self.show_sizes:
            self.x_channel = 'FSC-A'
            self.y_channel = 'SSC-A'
        else:
            self.x_channel = 'FITC-A'
            self.y_channel = 'PE-Texas Red-A'

        # Label the axes with the chosen channel names.

        for ax in self.axes[-1,:]:
            ax.set_xlabel(self.x_channel)
        for ax in self.axes[:,0]:
            ax.set_ylabel(self.y_channel)

    def _set_limits(self):
        """
        Decide what the axes limits should be.

        The axes are fixed to a particular size based on which channels are 
        being shown.  Not rescaling to the data itself makes it easier to 
        compare plots from different experiments.  The axes are also forced to 
        be square.
        """
        self.min_coord = 0
        self.max_coord = 6 if not self.show_sizes else 5000

        self.axes[0,0].set_xlim(self.min_coord, self.max_coord)
        self.axes[0,0].set_ylim(self.min_coord, self.max_coord)

    def _set_titles(self):
        """
        Label each plot with the name of the experiment, the condition, and the 
        replicate number.
        """
        self.figure.suptitle(self.experiment['label'], size=14)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                title = '{} #{}'.format(self._get_condition(row), col + 1)
                self.axes[row, col].set_title(title, size=12)

    def _create_histograms(self):
        self.histograms = {x: [] for x in experiment['wells']}

        for condition in self.experiment['wells']:
            self.histograms[condition] = []

            for well in self.experiment['wells'][condition]:
                z, x_bins, y_bins = np.histogram2d(
                        well[self.x_channel],
                        well[self.y_channel],
                        bins=np.linspace(
                            self.min_coord, self.max_coord,
                            self.histogram_bins),
                )
                x = (x_bins[1:] + x_bins[:-1]) / 2
                y = (y_bins[1:] + y_bins[:-1]) / 2

                if self.enable_smoothing:
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
        self.contour_levels = np.linspace(0, max_z, self.contour_steps+1)[1:]

    def _plot_cells(self, row, col):
        axis = self.axes[row, col]
        well = self._get_well(row, col)

        axis.plot(
                well[self.x_channel],
                well[self.y_channel], 
                marker=',',
                linestyle='',
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
                colors='white',
                zorder=2,
        )

    def _get_condition(self, row):
        return ('before', 'after')[row]

    def _get_well(self, row, col):
        return self.experiment['wells'][self._get_condition(row)][col]

    def _get_histogram(self, row, col):
        return self.histograms[self._get_condition(row)][col]



gate_nonpositive = fcmcmp.GateNonPositiveEvents()
gate_nonpositive.channels = 'FITC-A', 'PE-Texas Red-A'
log_transformation = fcmcmp.LogTransformation()
log_transformation.channels = 'FITC-A', 'PE-Texas Red-A'
fcmcmp.run_all_processing_steps([experiment])

if os.fork():
    raise SystemExit

analysis = ScatterPlot(experiment)
analysis.plot()
plt.show()

