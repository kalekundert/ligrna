#!/usr/bin/env python3

"""\
Print a basic statistical description of all the wells in a given experiment.

Usage:
    dump_info.py <yml_path> [<keyword>]
"""

import fcmcmp, docopt
from pprint import pprint

args = docopt.docopt(__doc__)
experiments = fcmcmp.load_experiments(args['<yml_path>'])
keyword = args['<keyword>']

for experiment, condition, well in fcmcmp.yield_wells(experiments):
    if keyword is None or \
            keyword in experiment['label'] or \
            keyword == condition or \
            keyword == well.label:

        print('Experiment:')
        pprint(experiment)
        print()
        print(well, end=':\n')
        print()
        print(well.data.describe())
        print()
    

