#!/usr/bin/env python3

"""\
Plot various channels vs time.  

Usage:
    time_course.py <yml_path> <experiment> [options]

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
        suffix.  By default, no output is generated and the plot is shown in 
        the GUI.

    -c --channel <channel>
        The channel to plot.  By default, this is deduced from the YAML file.  
        If an experiment has a 'channel' attribute, that channel is displayed.  
        Otherwise, a default channel may be chosen based on the name of the 
        experiment.  It is an error if no channel is specified and no channel 
        can be deduced.

    --force-vector
        If the scatter plots would be exported to a vector file format like PDF 
        or SVG (either via the command-line or the GUI), force ``matplotlib`` 
        to represent each individual point as a vector object.  By default, 
        these points (but not the lines or the text that make up the rest of 
        the figure) would be rasterized.  This option makes the resulting file 
        much larger and makes exporting and viewing that file take much longer.  
"""

import docopt, fcmcmp, analysis_helpers
import numpy as np, matplotlib.pyplot as plt
from pprint import pprint

class TimeChannel(analysis_helpers.ExperimentPlot):

    def __init__(self, experiment):
        super().__init__(experiment)

        # Settings configured by the user.
        self.channel = None
        self.rasterize_points = None

    def plot(self):
        self._create_axes()
        self._set_titles()

        for row, col in self._get_rows_cols():
            self._plot_channel_vs_time(row, col)

        self._set_limits()

    def _set_limits(self):
        min_time = float('inf')
        max_time = -float('inf')

        for condition in self.experiment['wells']:
            for well in self.experiment['wells'][condition]:
                min_time = min(min_time, min(well.data['Time']))
                max_time = max(max_time, max(well.data['Time']))
        
        self.axes[0,0].set_xlim(min_time, max_time)

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



if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    experiment = fcmcmp.load_experiment(args['<yml_path>'], args['<experiment>'])

    log_transformation = fcmcmp.LogTransformation()
    log_transformation.channels = 'FITC-A', 'PE-Texas Red-A'
    log_transformation([experiment])

    analysis = TimeChannel(experiment)
    analysis.channel = args['--channel']
    analysis.rasterize_points = args['--force-vector']

    with analysis_helpers.plot_or_savefig(args['--output'], args['<yml_path>']):
        analysis.plot()


