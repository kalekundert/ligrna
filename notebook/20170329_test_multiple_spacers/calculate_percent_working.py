#!/usr/bin/env python3

"""\
Calculate the percentage of spacers that "work".  These spacers are defined as 
having a >99% chance of being different than the controls.

Usage:
    calculate_percent_working.py [-t] [-v]

Options:
    -t --make-table
        Create a table summarizing the data.

    -v --verbose
        Print some extra information you can use to make sure the T-test 
        results seem reasonable.
"""

import docopt
import numpy as np
from scipy.stats import ttest_ind
import analysis_helpers as helpers
from color_me import ucsf
from pprint import pprint

SENSORS = 'mhf 30', 'rxb 11'
ALIASES = {'rxb 11': '"backward"', 'mhf 30': '"forward"'}
COLORS = {'rxb 11': ucsf.red[0], 'mhf 30': ucsf.blue[0]}
P_THRESHOLD = 0.01

args = docopt.docopt(__doc__)
data = helpers.CleavageData()
num_tried = {k:0 for k in SENSORS}
num_active = {k:0 for k in SENSORS}

def make_latex_table(path, num_tried, num_active):
    import jinja2
    from sh import xelatex

    loader = jinja2.FileSystemLoader('.')
    env = jinja2.Environment(loader=loader)
    template = env.get_template('percent_working_table.tex.jinja')
    context = {
            'sensors': SENSORS,
            'aliases': ALIASES,
            'p_threshold': P_THRESHOLD,
            'num_tried': num_tried,
            'num_active': num_active,
    }
    template.stream(context).dump(path)
    xelatex(path)

def make_pie_charts(path, num_tried, num_active):
    import matplotlib.pyplot as plt
    plt.rcParams['font.family'] = 'Liberation Sans'

    fig, axes = plt.subplots(1, len(SENSORS))
    fig.patch.set_color('white')
    for ax in axes.flat:
        ax.set(adjustable='box-forced', aspect='equal')

    for i, sensor in enumerate(SENSORS):
        percent_active = num_active[sensor] / num_tried[sensor]

        slices = percent_active, 1 - percent_active
        labels = f"{num_active[sensor]}/{num_tried[sensor]} active*\n({int(100 * percent_active)}%)", ""
        colors = COLORS[sensor], ucsf.light_grey[0]

        axes[i].pie(slices, labels=labels, colors=colors,
                startangle=90,
                wedgeprops=dict(
                    linewidth=0,
                ),
        )

    plt.savefig(path)
    plt.show()


controls = np.concatenate([
        data.calc_percent_change(sensor, spacer)
        for sensor in ['on', 'off']
        for spacer in data.spacers
])

for sensor in SENSORS:
    for spacer in sorted(data.spacers):
        changes = data.calc_percent_change(sensor, spacer)
        t, p = ttest_ind(controls, changes)
        active = p < P_THRESHOLD

        num_tried[sensor] += 1
        num_active[sensor] += active

        print(f"{spacer} {sensor}: p={p:.4e} active={active}")
        if args['--verbose']:
            print(f"  mean (controls):  {np.mean(controls):.4e}")
            print(f"  mean ({spacer} {sensor}): {np.mean(changes):.4e}")
            print(f"  measurements ({spacer} {sensor}): {changes}")

make_pie_charts('percent_working.svg', num_tried, num_active)

if args['--make-table']:
    make_latex_table('percent_working_table.tex', num_tried, num_active)
