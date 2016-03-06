#!/usr/bin/env python3

"""\
Print a basic statistical description of all the wells in a given experiment.

Usage:
    dump_info.py <yml_path>
"""

import fcmcmp, docopt
from pprint import pprint

args = docopt.docopt(__doc__)
experiments = fcmcmp.load_experiments(args['<yml_path>'])

for experiment, condition, well in fcmcmp.yield_wells(experiments):
    print('Experiment:')
    pprint(experiment)
    print()
    print(well, end=':\n')
    print()
    print(well.data.describe())
    print()
    

