#!/usr/bin/env python3

# Areas: doesn't work when x-axis scale dramatically changes.  Have to set 
# height of largest plot, then set areas equal to that.
#
# Fold repression: assumes 'view' is on a log axis.  Maybe don't even show that 
# panel if we're looking at a non-std view.  But can also look at the std view 
# on a linear axis, so need to be more general than that.

"""\
Usage:
    my_analysis.py <experiments> [<plots>] [options]

Arguments:
    <experiments>
        Path to a YAML file specifying which wells and which plates should be 
        compared with each other.

    <plots>
        What kinds of plots to generate.

Options:
    -o --output <path>
        If an output path is specified, the resulting plot is written to that 
        path and the GUI isn't opened.  Dollar signs ($) in the output path 
        are replaced by the base name of the given experiment, minus the '.yml' 
        suffix.  By default, no output is generated and the plot is shown in 
        the GUI.

    -v --view <channel>
        The channel to plot.  By default, this is deduced from the YAML file. 
        If an experiment has a 'channel' attribute, that channel is displayed.  
        Otherwise, if the experiment's name contains "sgGFP" or "sgRFP", the 
        'FITC-A' or 'PE-Texas Red-A' channels are displayed, respectively.

    -i --internal-control <channel>
        The channel to use weight the channel of interest.  By default this is 
        PE-Texas Red-A when the FITC-A channel if of interest, and vice versa.  
        You might specify FSC-A or SSC-A to normalize fluorescence by cell 
        size, or "none" to not normalize at all.

    -z --size-gate <percentile>         [default: 40]
        Exclude the smallest cells from the analysis.  Size is defined as 
        ``FSC + m * SSC``, where ``m`` is the slope of the linear regression 
        relating the two scatter channels.  The given percentile specifies how 
        many cells are excluded.

    -x --expression-gate <signal>       [default: 1e3]
        Exclude cells where the signal on the fluorescence control channel is 
        less than the given value.  The purpose of this gate is to get rid of 
        cells that weren't expressing much fluorescent protein, for whatever 
        reason.  Note that this gate is in absolute units, not log units.

    -H --histogram
        Display the cell distributions using histograms rather than Gaussian 
        kernel density estimates.  Histograms are faster to compute, but are 
        sensitive to the choice of bin size.  This is especially true for weak 
        fluorescence signals, which have smaller bins due to the logarithmic 
        scaling of the data.  Smaller bins are noisier and make the modes less 
        reliable (see --mode).  Larger bins may hide features.  
        
    -p --pdf
        Normalize the cell distributions such they all have the same area, and 
        are thus PDFs.  By default, the area of each curve reflects the number 
        of cells that were counted from that well.

    -l --linear
        Display the fluorescent channels on a linear scale instead of the 
        default logarithmic scale.  The scatter channels are always displayed 
        on a linear scale.

    -m --mode
        Use the modes of the cell distributions to calculate fold-changes in 
        fluorescence.  By default the medians are used for this calculation.
"""

import fcmcmp
from pylab import *
from pathlib import Path
from pprint import pprint
import warnings; warnings.simplefilter("error", FutureWarning)

fluorescence_controls = {
        'FITC-A': 'PE-Texas Red-A',
        'PE-Texas Red-A': 'FITC-A', 
}

class ResolveChannels(fcmcmp.ProcessingStep):

    def __init__(self, view=None, internal_control=None, linear=False):
        self.view = view
        self.internal_control = internal_control
        self.linear = False

    def process_experiment(self, experiment):
        # If the user manually specified a channel to view, use it.
        if self.view is not None:
            channel = self.view

        # If a particular channel is associated with this experiment, use it.
        elif 'channel' in experiment:
            channel = experiment['channel']

        # If a channel can be inferred from the name of the experiment, use it. 
        elif 'sgGFP' in experiment['label']:
            channel = 'FITC-A'
        elif 'sgRFP' in experiment['label']:
            channel = 'PE-Texas Red-A'

        # If the user didn't specify a channel, complain about it.
        else:
            raise fcmcmp.UsageError("Don't know which channel to visualize.")

        # By default, normalize known fluorescent channels but nothing else.
        if self.internal_control is None:
            if channel in fluorescence_controls:
                control_channel = fluorescence_controls[channel]
            else:
                control_channel = None

        # If the user wants to see the raw data, show it.
        elif self.internal_control == 'none':
            control_channel = None

        # If the user wants to manually normalize the data, let him/her.
        else:
            control_channel = self.internal_control

        # Show fluorescent channels on a log scale, unless the user requests 
        # otherwise.
        if channel in fluorescence_controls and not self.linear:
            scale = 'log'
        else:
            scale = 'linear'

        # Indicate in the experiment which channels are being viewed.  This 
        # information affects gating and the colors of the final plots.
        experiment['channel'] = channel
        experiment['control_channel'] = control_channel
        experiment['scale'] = scale


class SetupVisualization(fcmcmp.ProcessingStep):

    def process_well(self, experiment, well):
        channel = experiment['channel']
        control_channel = experiment['control_channel']

        # Save the actual data to plot in a column with a standard name.

        well['view'] = well[channel]

        if control_channel is not None:
            well['view'] /= well[control_channel]

        if experiment['scale'] == 'log':
            well['view'] = log10(well['view'])


class GateLowFluorescence(fcmcmp.GatingStep):

    def __init__(self, threshold=1e3):
        self.threshold = threshold

    def gate(self, experiment, well):
        channel = fluorescence_controls.get(experiment['channel'])
        if channel is not None:
            return well[channel] < self.threshold



def plot_medians(experiment, histogram=False, pdf=False):
    import numpy as np
    import matplotlib.pyplot as plt

    y_ticks = []
    y_tick_labels = []

    fig, (ax1, ax2) = plt.subplots(1, 2,
            sharey=True, gridspec_kw=dict(
                hspace=0.001,
                width_ratios=(0.65, 0.35)))

    if experiment[0]['channel'] in fluorescence_controls:
        x1_label = 'fluorescence'
        x2_label = 'fold repression'
    else:
        x1_label = 'size'
        x2_label = 'fold change'
    
    if experiment[0]['control_channel'] is not None:
        x1_label = 'normalized {}'.format(x1_label)

    if experiment[0]['scale'] == 'log':
        x1_label = 'log({})'.format(x1_label)

    ax1.set_xlabel(x1_label)
    ax2.set_xlabel(x2_label)

    pick_xlim(ax1, experiments)

    ax1.xaxis.grid(True)
    ax2.xaxis.grid(True)

    ax1.set_axisbelow(True)
    ax2.set_axisbelow(True)

    plot_distributions(ax1, experiments, histogram=histogram, pdf=pdf)

    for i, experiment in enumerate(reversed(experiments), 1):
        y_ticks.append(i)
        y_tick_labels.append(experiment['label'].replace('//', '\n'))
        color = '#4e9a06' if experiment['channel'] == 'FITC-A' else '#cc0000'
        black = 'black'

        # Plot medians

        before_medians = np.array([
                well['view'].median()
                for well in experiment['wells']['before']
        ])
        before_indices = [i-0.1 for j in range(len(before_medians))]
        before_style = {
                'marker': '+',
                'markeredgecolor': black,
                'markerfacecolor': 'none',
                'markeredgewidth': 1,
                'linestyle': ' ',
        }
        after_medians = np.array([
                well['view'].median()
                for well in experiment['wells']['after']
        ])
        after_indices = [i-0.1 for j in range(len(after_medians))]
        after_style = {
                'marker': '+',
                'markeredgecolor': color,
                'markerfacecolor': 'none',
                'markeredgewidth': 1,
                'linestyle': ' ',
        }

        ax1.plot(before_medians, before_indices, **before_style)
        ax1.plot(after_medians, after_indices, **after_style)

        # Plot fold-repression.

        if experiment['scale'] == 'log':
            fold_repressions = 10**(before_medians - after_medians)
        else:
            fold_repressions = before_medians / after_medians

        fold_repression_style = {
                'color': color,
                'edgecolor': 'none',
                'xerr': fold_repressions.std(),
                'ecolor': color,
        }

        h = 0.1
        ax2.barh(i-h/2, fold_repressions.mean(), h, **fold_repression_style)

    ax1.set_ylim(0.7, len(experiments) + 0.8)
    ax1.set_yticks(y_ticks)
    ax1.set_yticklabels(y_tick_labels)

    x, X = ax2.set_xlim()
    xticks = ax2.get_xticks()
    while len(xticks) > 6:
        dx = abs(2 * xticks[1] - xticks[0])
        xticks = [x]
        while xticks[-1] < X:
            xticks.append(xticks[-1] + dx)
    ax2.set_xlim(xticks[0], xticks[-1])
    ax2.set_xticks(xticks)
        

def pick_xlim(ax, experiments, cutoff=1):
    x_min = inf
    x_max = -inf

    for experiment in experiments:
        for flavor in experiment['wells']:
            for well in experiment['wells'][flavor]:
                x_min = min(x_min, min(well['view']))
                x_max = max(x_max, max(well['view']))

    ax.set_xlim(x_min, x_max)

def plot_distributions(ax, experiments, histogram=False, pdf=False):
    # The largest area any distribution can have.  The purpose of this 
    # parameter is to make the graph look nice and to prevent distributions 
    # from overlapping with each other.

    max_area = 0.10

    # Figure out the most cells that were measured in any well.  This 
    # information will be used to scale all the distributions, unless the user 
    # requested a PDF.

    

    max_num_cells = 0
    for experiment in experiments:
        for flavor in experiment['wells']:
            for well in experiment['wells'][flavor]:
                max_num_cells = max(max_num_cells, len(well))

    for i, experiment in enumerate(reversed(experiments), 1):
        color = '#4e9a06' if experiment['channel'] == 'FITC-A' else '#cc0000'
        black = 'black'

        # Plot cell distributions.

        def plot_distribution(d, **style):
            m, M = ax.get_xlim()

            if histogram:
                y, bins = np.histogram(d, linspace(m,M,100))
                x = (bins[:-1] + bins[1:]) / 2
            else:
                from scipy.stats import gaussian_kde
                k = gaussian_kde(d)
                x = linspace(m,M,100)
                y = k.evaluate(x)

            a = np.trapz(y, x)
            k = max_area / a * (1 if pdf else len(d) / max_num_cells)
            ax.plot(x, k*y+i, **style)

        before_style = {
                'color': black,
                'dashes': [5,2],
                'linewidth': 1,
        }
        after_style = {
                'color': color,
                'linestyle': '-',
                'linewidth': 1,
        }

        for well in experiment['wells']['before']:
            plot_distribution(well['view'], **before_style)
        for well in experiment['wells']['after']:
            plot_distribution(well['view'], **after_style)


if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)
    experiments = fcmcmp.load_experiments(args['<experiments>'])

    resolve_channels = ResolveChannels()
    resolve_channels.view = args['--view']
    resolve_channels.internal_control = args['--internal-control']
    resolve_channels.linear = args['--linear']
    gate_nonpositive_events = fcmcmp.GateNonPositiveEvents()
    gate_nonpositive_events.channels = 'FITC-A', 'PE-Texas Red-A'
    gate_small_cells = fcmcmp.GateSmallCells()
    gate_small_cells.threshold = int(args['--size-gate'])
    gate_low_fluorescence = GateLowFluorescence()
    gate_low_fluorescence.threshold = float(args['--expression-gate'])
    setup_visualization = SetupVisualization()
    fcmcmp.run_all_processing_steps(experiments)

    plot_medians(
            experiments,
            histogram=args['--histogram'],
            pdf=args['--pdf'],
    )
    if args['--output']:
        savefig(args['--output'].replace(
                '$', Path(args['<experiments>']).stem))
    else:
        show()

