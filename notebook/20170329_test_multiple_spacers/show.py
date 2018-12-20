#!/usr/bin/env python3

"""
Usage:
    show.py [<designs>...]

Examples:
    $ ./show.py "d1 mhf 30"
"""

import docopt
import more_itertools
import analysis_helpers

args = docopt.docopt(__doc__)
df = analysis_helpers.load_cleavage_data_from_xlsx_dir('densiometry')
pc = analysis_helpers.calc_percent_cut(df)
pd = analysis_helpers.calc_percent_change(df)


for last, name in more_itertools.tag_last(args['<designs>']):
    spacer, design = name.split(None, 1)
    print(pc[(pc.spacer == spacer) & (pc.design == design)])
    print()
