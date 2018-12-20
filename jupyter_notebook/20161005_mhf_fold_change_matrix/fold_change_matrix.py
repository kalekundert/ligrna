#!/usr/bin/env python3

import sys
import fcmcmp
import analysis_helpers
import sgrna_sensor
import numpy as np
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Roboto']
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pprint import pprint

class FoldChangeMatrix:

    spacers = list(reversed([
            'gfp',
            'rfp',
            'gfp2',
            'rfp2',
    ]))
    constructs = [
            'on',
            'off',
            'mhf 3',
            'mhf 4',
            'mhf 7',
            'mhf 13',
            'mhf 16',
            'mhf 20',
            'mhf 21',
            'mhf 25',
            'mhf 26',
            'mhf 30',
            'mhf 35',
            'mhf 37',
            'mhf 38',
            'mhf 41',
    ]

    def __init__(self):
        self.cell_width = 1
        self.cell_height = 1

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal')
        xmin = xmax = ymin = ymax = 0
        w, h = self.cell_width, self.cell_height

        cmap = mpl.cm.plasma
        norm = mpl.colors.Normalize(1, 14)
        mapper = mpl.cm.ScalarMappable(norm, cmap)
        mapper.set_array(np.linspace(1, 14))

        xticks = {}
        yticks = {}
        
        for (x, y), construct, spacer in self.yield_cells():

            # Decide what color to make this cell.  If there is data for this 
            # cell, a color is picked from a color map.  If there isn't data, a 
            # grey color is used.

            try:
                fold_change = get_fold_change(construct, spacer)
                rect_style = {
                        'facecolor': mapper.to_rgba(fold_change),
                }
            except DataMissing:
                rect_style = {
                        'hatch': r'\\\\',
                        'facecolor': '#eeeeec',
                }

            # Update the axis limits.
            x *= w; y *= h
            xmin, xmax = min(xmin, x), max(xmax, x + w)
            ymin, ymax = min(ymin, y), max(ymax, y + h)

            # Update the tick labels.
            yticks[y + w/2] = spacer

            # Draw a rectangle.
            rect = patches.Rectangle((x, y), w, h, **rect_style)
            ax.add_patch(rect)

        fig.canvas.set_window_title(' '.join(sys.argv))

        colorbar = fig.colorbar(
                mapper, ax=ax, orientation='horizontal', pad=0.035, aspect=35)
        colorbar.set_ticks([1, 2, 4, 6, 8, 10, 12, 14])
        colorbar.set_label('fold change')

        fig.patch.set_visible(False)
        ax.patch.set_visible(False)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.set_xlim(xmin, xmax+0.1)
        ax.set_ylim(ymin-0.1, ymax)

        ax.set_xticks([w * (x + 1/2) for x in range(len(self.constructs))])
        ax.set_xticklabels(self.constructs, rotation='vertical')

        ax.set_yticks(list(yticks.keys()))
        ax.set_yticklabels(list(yticks.values()))

        ax.tick_params(axis=u'both', which=u'both',length=0)
        ax.xaxis.set_tick_params(labeltop='on', labelbottom='off')

    def yield_cells(self):
        for x, construct in enumerate(self.constructs):
            for y, spacer in enumerate(self.spacers):
                # Yield a cell for each combination of construct and spacer.
                yield (x, y), construct, spacer

                # See if this construct has any unexpected mutations, and if it 
                # does, also yield a cell that excludes them.
                expected_only = construct + ',1'
                y_offset = self.cell_height * (len(self.spacers) + 1/2)
                if design_exists(expected_only):
                    yield (x, y - y_offset), expected_only, spacer


class DataMissing (Exception):
    pass


initial_picks = fcmcmp.load_experiments('../../results/facs/20160727_screen_mhf.yml')
recloned_hits = fcmcmp.load_experiments('../../results/facs/20160923_test_mhf_hits.yml')

shared_steps = analysis_helpers.SharedProcessingSteps()
shared_steps.process(initial_picks + recloned_hits)

def get_fold_change(construct, spacer):
    expt = find_experiment(construct, spacer)
    apo_well = analysis_helpers.AnalyzedWell(expt, expt['wells']['apo'][0])
    holo_well = analysis_helpers.AnalyzedWell(expt, expt['wells']['holo'][0])

    xlim = 0, 5
    apo_well.estimate_distribution(xlim)
    holo_well.estimate_distribution(xlim)
    fold_change = 10**(apo_well.loc - holo_well.loc)

    return fold_change
    
def find_experiment(construct, spacer):
    # Figure out where the data for this experiment is stored.

    if spacer == 'orig':
        experiments = initial_picks
    else:
        experiments = recloned_hits

    # Put together the label for this experiment.

    if spacer == 'orig':
        raise NotImplementedError
    else:
        label = spacer + ' ' + construct
    
    # Return the experiment with the correct label in the correct data file.  
    # If no experiment can be found, raise DataMissing.

    for experiment in experiments:
        if experiment['label'] == label:
            return experiment
    raise DataMissing

def design_exists(construct):
    try: sgrna_sensor.from_name(construct)
    except ValueError: return False
    else: return True


matrix = FoldChangeMatrix()
matrix.plot()

plt.show()
#plt.savefig('raw_fold_change_matrix.svg')
