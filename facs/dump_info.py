#!/usr/bin/env python3

"""\
Print a basic statistical description of the wells in the given experiment.

Usage:
    dump_info.py <yml_path> [<keyword>]

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
"""

import fcmcmp, docopt
from pprint import pprint

args = docopt.docopt(__doc__)
experiments = fcmcmp.load_experiments(args['<yml_path>'])
data = fcmcmp.yield_unique_wells(self.experiments, args['<keyword>'])

for experiment, condition, well in data:
    print('Experiment:')
    pprint(experiment)
    print()
    print(well, end=':\n')
    print()
    print(well.data.describe())
    print()
    

