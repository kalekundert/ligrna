#!/usr/bin/env python3

"""\
Show the changes between populations of cells in different conditions.

Usage:
    titration_curve.py <yml_path> [options]

Arguments:
    <yml_path>
        Path to a YAML file specifying which wells and which plates should be 
        compared with each other.

Options:
    -o --output <path>
        If an output path is specified, the resulting plot is written to that 
        path and the GUI isn't opened.  Dollar signs ($) in the output path 
        are replaced by the base name of the given experiment, minus the '.yml' 
        suffix.  The <path> "lpr" is treated specially and causes the plot to 
        be sent to the printer via 'lpr'.  By default, no output is generated 
        and the plot is shown in the GUI.

    -O --output-size <width,height>
        Specify what the width and height of the resulting figure should be, in 
        inches.  The two numbers must be separated by a comma.

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
"""

import fcmcmp, analysis_helpers, nonstdlib
import numpy as np, matplotlib.pyplot as plt
from statistics import mean, stddev
from pprint import pprint

class TitrationCurve:

    def __init__(self, experiments):
        self.experiments = experiments

    def plot(self):
        concentrations = []
        fold_changes = []
        fold_change_errors = []

        for experiment in self.experiments
            data_point = self._get_data_point(experiment)
            concentrations.append(data_point[0])
            fold_changes.append(data_point[1])
            fold_change_errors.append(data_point[2])

        self.axes.errorbar(concentrations, fold_changes, fold_change_errors)

    def _setup_figure(self):
        self.figure, self.axes = plt.subplots(1, 1)

    def _get_data_point(self, experiment):
        concentration = experiment['conc']
        fold_changes = []

        wells = zip(
                experiment['wells']['apo'],
                experiment['wells']['holo'],
        )

        for apo_well, holo_well in wells:
            apo_analysis = AnalyzedWell(experiment, apo_well)
            holo_analysis = AnalyzedWell(experiment, holo_well)

            apo_analysis.estimate_distribution()
            holo_analysis.estimate_distribution()

            fold_changes.append(
                    apo_analysis.linear_loc / holo_analysis.linear_loc)

        return concentration, mean(fold_changes), stddev(fold_changes)


if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)
    experiments = fcmcmp.load_experiments(args['<yml_path>'])

    shared_steps = analysis_helpers.SharedProcessingSteps()
    shared_steps.early_event_threshold = float(args['--time-gate'])
    shared_steps.small_cell_threshold = float(args['--size-gate'])
    shared_steps.low_fluorescence_threshold = float(args['--expression-gate'])
    shared_steps.process(experiments)

    analysis = TitrationCurve(experiments)

    with analysis_helpers.plot_or_savefig(args['--output'], args['<yml_path>']):
        analysis.plot()

