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
        suffix.  The <path> "lpr" is treated specially and causes the plot to 
        be sent to the printer via 'lpr'.  By default, no output is generated 
        and the plot is shown in the GUI.

    -l --show-legend
        Show which lines came from which wells.

    -w --time-window <secs>          [default: 2]
        Specify how long of a time interval to consider when calculating the 
        number of events per second.  Longer time intervals will give smoother 
        plots, but will lag relative to shorter intervals.
"""

import docopt, fcmcmp, analysis_helpers
import numpy as np, matplotlib.pyplot as plt
from pprint import pprint

class EventsPerSec:

    def __init__(self, experiments):
        self.experiments = experiments
        self.keyword = None
        self.show_legend = False
        self.time_window = 1

    def plot(self):
        data = fcmcmp.yield_unique_wells(self.experiments, self.keyword)
        min_time, max_time = analysis_helpers.get_duration(self.experiments)
        time_coord = np.linspace(min_time, max_time, num=500)

        for experiment, condition, well in sorted(data, key=lambda x: x[2]):
            times = well.data['Time'] * float(well.meta['$TIMESTEP'])
            events_per_sec = np.zeros(time_coord.shape)

            for i, x in enumerate(time_coord):
                time_range = x - self.time_window/2, x + self.time_window/2
                a, b = np.searchsorted(times, time_range)
                b -= 1 # keep ``b`` in bounds.
                dt = times.iloc[b] - times.iloc[a]
                events_per_sec[i] = (b - a) / dt

            plt.plot(
                    time_coord,
                    events_per_sec,
                    label='{} ({})'.format(well.label, condition),
                    **analysis_helpers.pick_style(experiment, condition)
            )

        plt.xlim(min_time, max_time)
        plt.ylim(0, plt.ylim()[1])
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
    analysis.time_window = float(args['--time-window'])

    with analysis_helpers.plot_or_savefig(args['--output'], args['<yml_path>']):
        analysis.plot()
