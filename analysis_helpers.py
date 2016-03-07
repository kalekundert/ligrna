#!/usr/bin/env python3

import contextlib, fcmcmp

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
    elif experiment['label'].startswith('us('):
        return blue[1]
    elif experiment['label'].startswith('nx('):
        return red[1]
    elif experiment['label'].startswith('nx('):
        return green[1]
    elif experiment['label'].startswith('cb('):
        return orange[1]
    elif experiment['label'].startswith('sh('):
        return purple[1]
    else:
        return brown[1]

def pick_channel(experiment):
    pass

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

