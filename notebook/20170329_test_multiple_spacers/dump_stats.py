#!/usr/bin/env python3

"""\
Show summary statistics (mean, median, mode,min, max, etc.) for the positive 
control.

Usage:
    dump_stats.py 
"""

import docopt
from pathlib import Path
from sgrna_sensor import densiometry

DATA_DIR = Path(__file__).parent / 'densiometry'

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    df = densiometry.load_cleavage_data_from_xlsx_dir(DATA_DIR)
    df = densiometry.calc_percent_change(df).reset_index()

    on = df[df.design == 'on']
    off = df[df.design == 'off']

    print(on.describe())
