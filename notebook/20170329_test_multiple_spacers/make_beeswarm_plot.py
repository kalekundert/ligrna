#!/usr/bin/env python3
#!/usr/bin/env python3

"""\
Produce a plot showing how sensitive my sgRNA sensors are to the spacer 
sequence, in the context of the in vitro cleavage assay.

Usage:
    plot_data.py
"""

import sys
import docopt
import color_me
import numpy as np
import matplotlib.pyplot as plt
import analysis_helpers as helpers
from pprint import pprint

args = docopt.docopt(__doc__)
data = helpers.CleavageData()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.axhline(linestyle='-', color=color_me.ucsf.black[0])

for i, sensor in enumerate(helpers.SENSORS):
    y = [data.calc_percent_change(sensor, x) for x in data.spacers]
    y_mean = np.array([(100 * yi).mean() for yi in y])
    y_std = np.array([(100 * yi).std() for yi in y])
    x = helpers.unclump_points(y_mean, y_std + 2.0, i, 0.08)

    ax.errorbar(x, y_mean, yerr=y_std,
            linestyle='None',
            marker='o',
            markerfacecolor=helpers.COLORS[sensor],
            markeredgecolor='none',
            ecolor=color_me.ucsf.light_grey[0],
            elinewidth=1,
            #capsize=10,
    )

xlabels = [x.replace(' ', '\n') for x in helpers.SENSORS]
ax.set_xticks(range(len(xlabels)))
ax.set_xticklabels(xlabels, ha='center')
ax.set_ylabel("ligand sensitivity (Δ%)")

fig.canvas.set_window_title(' '.join(sys.argv))
plt.savefig('test_multiple_spacers.svg')
plt.show()

