#!/usr/bin/env python3

"""\
Usage:
    percent_on.py <yml_path> [<keyword>] [options]

Options:
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

import docopt, fcmcmp, analysis_helpers
import matplotlib.pyplot as plt
from pprint import pprint

args = docopt.docopt(__doc__)
experiments = fcmcmp.load_experiments(args['<yml_path>'])

shared_steps = analysis_helpers.SharedProcessingSteps()
shared_steps.early_event_threshold = float(args['--time-gate'])
shared_steps.small_cell_threshold = float(args['--size-gate'])
shared_steps.low_fluorescence_threshold = float(args['--expression-gate'])
shared_steps.process(experiments)

table = []

for experiment, condition, well in fcmcmp.yield_wells(experiments, args['<keyword>']):
    well = analysis_helpers.AnalyzedWell(experiment, well, normalize_by=True)
    percent_on = sum(well.measurements < -0.3) / len(well.measurements)
    table.append((experiment['label'], condition, percent_on))

previous_label = None
max_label_len = max_condition_len = 0

for label, condition, percent_on in table:
    max_label_len = max(len(label), max_label_len)
    max_condition_len = max(len(condition), max_condition_len)

for label, condition, percent_on in table:
    print('{:{}s} {:{}s} {:.2f}%'.format(
        label, max_label_len,
        condition, max_condition_len,
        100 * percent_on))
