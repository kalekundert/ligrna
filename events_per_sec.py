#!/usr/bin/env python3

"""\
Plot the number of events recorded per second for all the wells in the given 
set of experiments.

Usage:
    ./events_per_sec.py <yml_path> [<keyword>] [options]

Arguments:
    <yml_path>
        Path to a YAML file specifying which wells and which plates should be 
        compared with each other.

    <keyword>
        Only include wells that match the given keyword.  A well matches if any 
        of the following conditions are met:
        1. The keyword exactly equals the well's label.
        2. The keyword exactly equals the name of the well's condition.
        3. The keyword makes up part of the well's experiment's label.

Options:
    -o --output <path>
        If an output path is specified, the resulting plot is written to that 
        path and the GUI isn't opened.  Dollar signs ($) in the output path 
        are replaced by the base name of the given experiment, minus the '.yml' 
        suffix.  By default, no output is generated and the plot is shown in 
        the GUI.

    -l --show-legend
        Show which lines came from which wells.
        
    --histogram-bins <num>              [default: 100]
        The number of bins to use in the time dimension when calculating the 
        number of events per second.
"""

import docopt, fcmcmp, analysis_helpers
import numpy as np, matplotlib.pyplot as plt
from pprint import pprint

class EventsPerSec:

    def __init__(self, experiments):
        self.experiments = experiments
        self.keyword = None
        self.show_legend = None
        self.histogram_bins = None

    def plot(self):
        min_time, max_time = analysis_helpers.get_duration(self.experiments)
        data = fcmcmp.yield_unique_wells(self.experiments, self.keyword)

        for experiment, condition, well in data:
            times = well.data['Time'] * float(well.meta['$TIMESTEP'])
            bins = np.linspace(min_time, max_time, self.histogram_bins)
            events_per_bin, bin_edges = np.histogram(times, bins)
            secs_per_bin = bin_edges[1] - bin_edges[0]
            events_per_sec = events_per_bin / secs_per_bin
            time_coord = (bin_edges[1:] + bin_edges[:-1]) / 2
            nonzero = events_per_sec.nonzero()

            plt.plot(
                    time_coord[nonzero],
                    events_per_sec[nonzero],
                    label=well.label,
                    **analysis_helpers.pick_style(experiment, condition)
            )

        plt.xlim(min_time, max_time)
        plt.xlabel('Collection time (sec)')
        plt.ylabel('Events/sec')

        if self.keyword:
            plt.title(self.keyword)
        if self.show_legend:
            plt.legend(loc='best')


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    experiments = fcmcmp.load_experiments(args['<yml_path>'])

    analysis = EventsPerSec(experiments)
    analysis.keyword = args['<keyword>']
    analysis.show_legend = args['--show-legend']
    analysis.histogram_bins = args['--histogram-bins']

    with analysis_helpers.plot_or_savefig(args['--output'], args['<yml_path>']):
        analysis.plot()
