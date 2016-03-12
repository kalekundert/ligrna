#!/usr/bin/env python3

import contextlib, fcmcmp
import numpy as np, matplotlib.pyplot as plt
import warnings; warnings.simplefilter("error", FutureWarning)
from pprint import pprint

fluorescence_controls = {
        'FITC-A': 'PE-Texas Red-A',
        'PE-Texas Red-A': 'FITC-A', 
}

class GateLowFluorescence(fcmcmp.GatingStep):

    def __init__(self, threshold=1e3):
        self.threshold = threshold

    def gate(self, experiment, well):
        channel = fluorescence_controls.get(experiment['channel'])
        if channel is not None:
            return well.data[channel] < self.threshold


class SharedProcessingSteps:

    def __init__(self):
        self.early_event_gate = None
        self.small_cell_gate = None
        self.low_fluorescence_gate = None
        self.log_transformation = True

    def process(self, experiments):
        gate_nonpositive_events = fcmcmp.GateNonPositiveEvents()
        gate_nonpositive_events.channels = 'FITC-A', 'PE-Texas Red-A'
        gate_nonpositive_events(experiments)

        gate_early_events = fcmcmp.GateEarlyEvents()
        gate_early_events.throwaway_secs = 100 * self.early_event_threshold
        gate_early_events(experiments)

        gate_small_cells = fcmcmp.GateSmallCells()
        gate_small_cells.save_size_col = True
        gate_small_cells.threshold = self.small_cell_threshold
        gate_small_cells(experiments)

        gate_low_fluorescence = GateLowFluorescence()
        gate_low_fluorescence.threshold = self.low_fluorescence_threshold
        gate_low_fluorescence(experiments)

        if self.log_transformation:
            log_transformation = fcmcmp.LogTransformation()
            log_transformation.channels = 'FITC-A', 'PE-Texas Red-A'
            log_transformation(experiments)



class ExperimentPlot:
    """
    Create a grid of shared axes, with one axis for each well in a single 
    experiment.  Provide a few helper functions relating to that grid, such as 
    setting the titles and converting row and column indices into wells and 
    conditions.
    """

    def __init__(self, experiment):
        # Settings configured by the user.
        self.experiment = experiment

        # Internally used plot attributes.
        self.figure = None
        self.axes = None
        self.num_rows = None
        self.num_cols = None

    def plot(self):
        raise NotImplementedError

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
        

    def _set_titles(self):
        """
        Label each plot with the name of the experiment, the condition, and the 
        replicate number.
        """
        self.figure.suptitle(self.experiment['label'], size=14)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                well = self._get_well(row, col)
                condition = self._get_condition(row)
                title = '{} ({})'.format(well.label, condition)
                self.axes[row, col].set_title(title, size=12)

    def _get_rows_cols(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                yield row, col

    def _plot_channel_vs_time(self, row, col):
        axis = self.axes[row, col]
        well = self._get_well(row, col)
        channel = analysis_helpers.pick_channel(experiment, self.channel)
        color = analysis_helpers.pick_color(self.experiment)

        axis.plot(
                well.data['Time'],
                well.data[channel],
                marker=',',
                linestyle='',
                color=color,
                rasterized=self.rasterize_points,
        )

    def _get_condition(self, row):
        return ('before', 'after')[row]

    def _get_well(self, row, col):
        return self.experiment['wells'][self._get_condition(row)][col]



def pick_color(experiment):
    """
    Pick a color for the given experiment.

    The return value is a hex string suitable for use with matplotlib.
    """
    # I made this a wrapper function so that I could easily change the color 
    # scheme, if I want to, down the road.
    return pick_tango_color(experiment)

def pick_tango_color(experiment):
    """
    Pick a color from the Tango color scheme for the given experiment.

    The Tango color scheme is best known for being the basis of GTK icons, 
    which are used heavily on Linux systems.  The colors are bright, and the 
    scheme includes a few tints of each color.
    """

    white, black = '#ffffff', '#000000'
    grey = '#eeeeec', '#d3d7cf', '#babdb6', '#888a85', '#555753', '#2e3436'
    red =    '#ef2929', '#cc0000', '#a40000'
    orange = '#fcaf3e', '#f57900', '#ce5c00'
    yellow = '#fce94f', '#edd400', '#c4a000'
    green =  '#8ae234', '#73d216', '#4e9a06'
    blue =   '#729fcf', '#3465a4', '#204a87'
    purple = '#ad7fa8', '#75507b', '#5c3566'
    brown =  '#e9b96e', '#c17d11', '#8f5902'

    if experiment['label'].startswith('sgRFP'):
        return red[1]
    elif experiment['label'].startswith('sgGFP'):
        return green[2]
    elif experiment['label'] in ('wt', 'dead', 'null'):
        return grey[4]
    elif experiment['label'].startswith('us('):
        return blue[1]
    elif experiment['label'].startswith('nx('):
        return red[1]
    elif experiment['label'].startswith('cb('):
        return green[1]
    elif experiment['label'].startswith('sh('):
        return orange[1]
    elif experiment['label'].startswith('rb('):
        return purple[1]
    else:
        return brown[2]

def pick_channel(experiment, users_choice=None):
    return users_choice or experiment.get('channel', 'PE-Texas Red-A')

@contextlib.contextmanager
def plot_or_savefig(output_path=None, substitution_path=None):
    """
    Either open the plot in the default matplotlib GUI or export the plot to a 
    file, depending on whether or not an output path is given.  If an output 
    path is given and it contains dollar signs ('$'), they will be replaced 
    with the given substitution path.
    """
    import os, sys, matplotlib.pyplot as plt
    from pathlib import Path

    # We have to decide whether or not to fork before plotting anything, 
    # otherwise X11 will complain, and we only want to fork if we'll end up 
    # showing the GUI.  So first we calculate the output path, then we either 
    # fork or don't, then we yield to let the caller plot everything, then we 
    # either display the GUI or save the figure to a file.

    if not output_path and os.fork():
        sys.exit()

    yield

    if output_path and substitution_path:
        output_path = output_path.replace('$', Path(substitution_path).stem)

    if output_path:
        plt.savefig(output_path, dpi=300)
    else:
        plt.gcf().canvas.set_window_title(' '.join(sys.argv))
        plt.show()

