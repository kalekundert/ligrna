#!/usr/bin/env python3

"""\
Generate a figure for the ligand matrix experiments that James did.

Usage:
    ligand_matrix.py [options]

Options:
    -o --output <path>
        If an output path is specified, the resulting plot is written to that 
        path and the GUI isn't opened.  Dollar signs ($) in the output path 
        are replaced by the base name of the given experiment, minus the '.yml' 
        suffix.  The <path> "lpr" is treated specially and causes the plot to 
        be sent to the printer via 'lpr'.  By default, no output is generated 
        and the plot is shown in the GUI.

    -O --output-size <width "x" height>
        Specify what the width and height of the resulting figure should be, in 
        inches.  The two numbers must be separated by an "x".

    -t --time-gate <secs>               [default: 0]
        Exclude the first cells recorded from each well if you suspect that 
        they may be contaminated with cells from the previous well.  The 
        default is to keep all the data.

    -z --size-gate <percentile>         [default: 0]
        Exclude the smallest cells from the analysis.  Size is defined as 
        ``FSC + m * SSC``, where ``m`` is the slope of the linear regression 
        relating the two scatter channels.  The given percentile specifies how 
        many cells are excluded.  The default is to include all cells.

    -x --expression-gate <signal>       [default: 1e3]
        Exclude cells where the signal on the fluorescence control channel is 
        less than the given value.  The purpose of this gate is to get rid of 
        cells that weren't expressing much fluorescent protein, for whatever 
        reason.  Note that this gate is in absolute units, not log units.

    -f --fast
        Generate the plot for just a single replicate, to make things run 
        faster when debugging.

    -v --verbose
        Print out information on all the processing steps.
"""

import sys, os
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import fcmcmp, analysis_helpers, nonstdlib, re
from typing import NamedTuple
from pprint import pprint

class LigandMatrix:

    def __init__(self, experiments):
        self.experiments = experiments
        self.comparisons = None
        self.figure = None
        self.axes = None
        self.output_size = None
        self.bar_width = 6

    def plot(self):
        self._setup_figure()
        self._analyze_wells()
        self._decorate_axes()
        self._plot_everything()
        self.figure.tight_layout()

    def _setup_figure(self, figure=None, axes=None):
        self.figure, self.axes = plt.subplots(4, 1, figsize=self.output_size)
        self.figure.patch.set_alpha(0)

    def _analyze_wells(self):
        analysis_helpers.analyze_wells(self.experiments)
        self.comparisons = {
                parse_label(x.label): x for x in 
                analysis_helpers.yield_related_wells(self.experiments)
        }

    def _decorate_axes(self):
        for ax in self.axes:
            ax.set_ylim(0, 20)
            ax.yaxis.grid(True)
            ax.yaxis.set_major_locator(analysis_helpers.FoldChangeLocator())

    def _plot_everything(self):
        spacers = 'GFP', 'RFP', 'GFP2', 'RFP2'
        sgrnas = [
                'ON', 'OFF',
                'THEO_MHF30', 'THEO_MHF37', 'THEO_RXB11',
                '3MX_MHF30', '3MX_MHF37', '3MX_RXB11',
        ]

        for row, spacer in enumerate(spacers):
            self.xticks = []
            self.xticklabels = []

            for i, sgrna in enumerate(sgrnas):
                self._plot_sgrna(row, i, spacer, sgrna)

            self.axes[row].set_xlim(min(self.xticks) - 1, max(self.xticks) + 1)
            self.axes[row].set_xticks(self.xticks)
            self.axes[row].set_xticklabels(self.xticklabels,
                    rotation='vertical', fontsize=10)

    def _plot_sgrna(self, row, i, spacer, sgrna):
        ligands = 'CAFF', 'THEO', '3MX'
        colors = {
                'CAFF': '#d1d3d3',  # UCSF light grey
                'THEO': '#716fb2',  # UCSF purple
                '3MX':  '#ae437d',  # UCSF purple/red hybrid
        }
        titles = {
                'ON':    'pos',
                'OFF':   'neg',
                'RXB11': 'ligRNA⁻',
                'MHF30': 'ligRNA⁺',
                'MHF37': 'alt-ligRNA⁻',
        }

        for j, ligand in enumerate(ligands):
            key = LabelInfo(spacer, sgrna, ligand)
            if key not in self.comparisons:
                print(f"Skipping {key}")
                continue

            x = 3*i + j
            y, ys = self.comparisons[key].calc_fold_change()
            err = np.std(ys)
            color = colors[key.ligand]

            self.axes[row].plot(
                    [x,x], [0,y],
                    color=color,
                    linewidth=self.bar_width,
                    solid_capstyle='butt',
            )
            self.axes[row].errorbar(
                    x, y, yerr=err,
                    ecolor=color,
                    capsize=self.bar_width / 2,
            )

            self.xticks.append(x)
            self.xticklabels.append(ligand.lower())

        import matplotlib.transforms as transforms

        label_x = 3*i + 1   # data coords
        label_y = 1.01      # axes coords

        self.axes[row].text(
                label_x, label_y, sgrna,
                horizontalalignment='center',
                transform=transforms.blended_transform_factory(
                    self.axes[row].transData, self.axes[row].transAxes),
        )


class LabelInfo(NamedTuple):
    spacer: str
    sgrna: str
    ligand: str

def parse_label(label):
    """
    Return the spacer, sgrna, aptamer, and ligand communicated by the given 
    label.
    """
    spacer_pat = 'RFP|RFP2|GFP|GFP2'
    ligand_pat = 'THEO|3MX|CAFF'
    control_pat = 'on|off'
    sgrna_pat = 'MHF30|MHF37|rxb11[.-]1'

    _ = {
            'on': 'ON',
            'off': 'OFF',
            'rxb11.1': 'RXB11',
            'rxb11-1': 'RXB11',
            'MHF30': 'MHF30',
            'MHF37': 'MHF37',
    }

    match = re.match(
            f'({spacer_pat})[._]({control_pat})-({ligand_pat})', label)
    if match:
        spacer, sgrna, ligand = match.groups()
        return LabelInfo(spacer, _[sgrna], ligand)

    match = re.match(
            f'({sgrna_pat})_({spacer_pat})-({ligand_pat})', label)
    if match:
        sgrna, spacer, ligand = match.groups()
        return LabelInfo(spacer, f'THEO_{_[sgrna]}', ligand)

    match = re.match(
            f'({sgrna_pat})_({spacer_pat})_3MX-({ligand_pat})', label)
    if match:
        sgrna, spacer, ligand = match.groups()
        return LabelInfo(spacer, f'3MX_{_[sgrna]}', ligand)

    raise ValueError(f"couldn't parse '{label}'")


if __name__ == "__main__":
    import docopt

    args = docopt.docopt(__doc__)
    root = os.path.dirname(__file__)
    yml_path = (
        'data/'
            '20170214-Ligand_Screen-Replicate_9-COLUMNS/'
                'Replicate_9-All_and_Columns.yaml'
        if args['--fast'] else
        'data/'
            '20170214-Ligand_Screen-Replicate_9-COLUMNS/'
                'Replicates_1-3_7-9_Working.yaml'
    )
    experiments = fcmcmp.load_experiments(os.path.join(root, yml_path))

    shared_steps = analysis_helpers.SharedProcessingSteps(args['--verbose'])
    shared_steps.early_event_threshold = float(args['--time-gate'])
    shared_steps.small_cell_threshold = float(args['--size-gate'])
    shared_steps.low_fluorescence_threshold = float(args['--expression-gate'])
    shared_steps.process(experiments)

    analysis = LigandMatrix(experiments)

    if args['--output-size']:
        analysis.output_size = map(float, args['--output-size'].split('x'))

    with analysis_helpers.plot_or_savefig(args['--output'], '20170214_ligand_matrix'):
        analysis.plot()
