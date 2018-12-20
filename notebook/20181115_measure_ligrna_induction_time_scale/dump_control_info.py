#!/usr/bin/env python3

"""\
Usage:
    ./controls.py <toml>

"""

import pandas as pd
from sgrna_sensor import qpcr
from pathlib import Path

if __name__ == '__main__':
    import docopt

    args = docopt.docopt(__doc__)
    df, op = qpcr.load(args['<toml>'])
    df['control'].fillna('timepoint', inplace=True)

    # Report the Cq values of the various controls
    cq = qpcr.calc_cq(df, ['control', 'sgrna', 'primers'])
    print(cq)
    print()

    cq = qpcr.calc_cq(df, ['control', 'primers'])
    print(cq)




