#!/usr/bin/env python3

"""\
Display flow cytometry data comparing the red and green fluorescence of cells 
in different CRISPRi conditions.

Usage:
    my_analysis.py <experiments> [<plots>] [options]

Arguments:
    <experiments>
        Path to a YAML file specifying which wells and which plates should be 
        compared with each other.

    <plots>
        What kinds of plots to generate.  Not yet implemented.

Options:
    -o --output <path>
        If an output path is specified, the resulting plot is written to that 
        path and the GUI isn't opened.  Dollar signs ($) in the output path 
        are replaced by the base name of the given experiment, minus the '.yml' 
        suffix.  By default, no output is generated and the plot is shown in 
        the GUI.

    -c --channel <channel>
        The channel to plot.  By default, this is deduced from the YAML file. 
        If an experiment has a 'channel' attribute, that channel is displayed.  
        Otherwise, if the experiment's name contains "sgGFP" or "sgRFP", the 
        'FITC-A' or 'PE-Texas Red-A' channels are displayed, respectively.  It 
        is an error if no channel is specified and no channel can be deduced.

    -n --normalize-by <channel>
        Normalize the channel of interest (see --channel) by the given channel.
        For example, you might specify "FSC-A", "SSC-A", or "FSC-A + m * SSC-A" 
        to normalize by cell size.  By default no normalization is done.

    -N --normalize-by-internal-control
        Normalize by FITC-A (GFP expression) if the channel of interest is 
        PE-Texas Red-A (RFP expression) and vice versa.  This assumes that the 
        fluorescent protein that isn't of interest is being constitutively 
        expressed, and therefore can be used as an internal control for cell 
        size and expression level.

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
        signal.  By default the medians are used for this calculation.
"""

import fcmcmp
import numpy as np
import matplotlib.pyplot as plt
import warnings; warnings.simplefilter("error", FutureWarning)
from pathlib import Path
from pprint import pprint

fluorescence_controls = {
        'FITC-A': 'PE-Texas Red-A',
        'PE-Texas Red-A': 'FITC-A', 
}

class ResolveChannels(fcmcmp.ProcessingStep):

    def __init__(self, view=None, normalize_by=None):
        self.view = view
        self.normalize_by = normalize_by

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

        # If normalization is requested but no particular channel is given, try 
        # to find a default fluorescent control channel.
        if self.normalize_by is True:
            try: control_channel = fluorescence_controls[channel]
            except KeyError: raise fcmcmp.UsageError("No internal control for '{}'".format(channel))

        # If no normalization is requested, don't set a control channel.
        elif not self.normalize_by:
            control_channel = None

        # If the user manually specifies a channel to normalize with, use it.
        else:
            control_channel = self.internal_control

        # Indicate in the experiment which channels are being viewed.  This 
        # information affects gating and the colors of the final plots.
        experiment['channel'] = channel
        experiment['control_channel'] = control_channel


class SetupVisualization(fcmcmp.ProcessingStep):

    def process_well(self, experiment, well):
        channel = experiment['channel']
        control_channel = experiment['control_channel']

        # Save the actual data to plot in a column with a standard name.

        if control_channel is None:
            well['view'] = well[channel]
        else:
            well['view'] = well[channel] / well[control_channel]


class GateLowFluorescence(fcmcmp.GatingStep):

    def __init__(self, threshold=1e3):
        self.threshold = threshold

    def gate(self, experiment, well):
        channel = fluorescence_controls.get(experiment['channel'])
        if channel is not None:
            return well[channel] < self.threshold



def plot_everything(experiment, linear=False, histogram=False, pdf=False, mode=False):
    # Make two subplots with a shared y-axis.

    fig, (ax1, ax2) = plt.subplots(1, 2,
            sharey=True, gridspec_kw=dict(
                hspace=0.001,
                width_ratios=(0.65, 0.35)))

    # Turn on grid lines, but put them behind everything else.

    ax1.xaxis.grid(True); ax1.set_axisbelow(True)
    ax2.xaxis.grid(True); ax2.set_axisbelow(True)

    # Decide what the x-limits should be for the distributions plot.  This has 
    # to be decided before the distributions themselves are calculated.

    pick_xlim(ax1, experiments, linear=linear)

    # Plot the data.

    estimate_distributions(
            experiments, ax1.get_xlim(),
            linear=linear, histogram=histogram, mode=mode, pdf=pdf,
    )
    rescale_distributions(
            experiments, desired_height=0.7,
    )

    for i, experiment in enumerate(reversed(experiments)):
        plot_distributions(ax1, i, experiment)
        plot_locations(ax1, i, experiment)
        plot_fold_change(ax2, i, experiment,
                linear=linear, bar_height=0.025 * len(experiments))

    # Decide how the x- and y-axes should be labeled.  This comes after all the 
    # data has been plotted, so that the final x- and y-limits are known.

    pick_xticks(ax2)
    pick_xlabels(ax1, ax2, experiments, linear=linear)
    pick_yticks(ax1, experiments)

    return fig

def estimate_distributions(experiments, xlim, linear=False, histogram=False, pdf=False, mode=False):

    class EstimatedDistribution:

        def __init__(self, data):
            if not linear:
                data = np.log10(data)

            x = np.linspace(*xlim, num=100)

            if histogram:
                y, bins = np.histogram(data, x, density=True)
                x = (bins[:-1] + bins[1:]) / 2
            else:
                from scipy.stats import gaussian_kde
                kernel = gaussian_kde(data)
                y = kernel.evaluate(x)

            area = np.trapz(y, x)
            num_cells = len(data)

            y /= area
            if not pdf:
                y *= num_cells

            self.x = x
            self.y = y
            self.area = area
            self.num_cells = num_cells
            self.loc = np.median(data) if not mode else x[np.argmax(y)]
            self.raw_data = data

        def __repr__(self):
            return 'EstimatedDistribution(median={:.2f})'.format(
                    np.median(self.raw_data))


    for experiment in experiments:
        experiment['distributions'] = {
                flavor: [
                    EstimatedDistribution(x['view'])
                    for x in experiment['wells'][flavor]
                ]
                for flavor in experiment['wells']
        }

def rescale_distributions(experiments, desired_height):
    max_height = 0

    # Find the distribution with the tallest peak.

    for experiment in experiments:
        for flavor in experiment['distributions']:
            for dist in experiment['distributions'][flavor]:
                max_height = max(max_height, np.max(dist.y))

    # Scale each distribution relative to the one with the tallest peak.

    scale_factor = desired_height / max_height

    for experiment in experiments:
        for flavor in experiment['distributions']:
            for dist in experiment['distributions'][flavor]:
                dist.y *= scale_factor

def plot_distributions(ax, i, experiment):
    styles = {
            'before': {
                'color': 'black',
                'dashes': [5,2],
                'linewidth': 1,
                'zorder': 1,
            },
            'after': {
                'color': pick_color(experiment),
                'linestyle': '-',
                'linewidth': 1,
                'zorder': 2,
            },
    }

    # Plot each distribution.

    for flavor in experiment['distributions']:
        for dist in experiment['distributions'][flavor]:
            ax.plot(dist.x, dist.y + i, **styles[flavor])

def plot_locations(ax, i, experiment, y_offset=0.1):
    styles = {
            'before': {
                'marker': '+',
                'markeredgecolor': 'black',
                'markerfacecolor': 'none',
                'markeredgewidth': 1,
                'linestyle': ' ',
            },
            'after': {
                'marker': '+',
                'markeredgecolor': pick_color(experiment),
                'markerfacecolor': 'none',
                'markeredgewidth': 1,
                'linestyle': ' ',
            },
    }

    # Mark the location of each distribution.

    for flavor in experiment['distributions']:
        for dist in experiment['distributions'][flavor]:
            ax.plot(dist.loc, i - y_offset, **styles[flavor])

def plot_fold_change(ax, i, experiment, linear=False, bar_height=0.1):
        locations = {
                flavor: np.array([
                    dist.loc for dist in experiment['distributions'][flavor]])
                for flavor in experiment['distributions']
        }

        if linear:
            fold_repressions = locations['before'] / locations['after']
        else:
            fold_repressions = 10**(locations['before'] - locations['after'])

        ax.barh(
                i - bar_height/2,
                fold_repressions.mean(),
                bar_height,
                color=pick_color(experiment),
                edgecolor='none',
                xerr=fold_repressions.std(),
                ecolor=pick_color(experiment),
        )

def pick_xlim(ax, experiments, linear=False):
    x_min = x_01 = np.inf
    x_max = x_99 = -np.inf

    for experiment in experiments:
        for flavor in experiment['wells']:
            for well in experiment['wells'][flavor]:
                x_min = min(x_min, np.min(well['view']))
                x_max = max(x_max, np.max(well['view']))
                x_01 = min(x_01, np.percentile(well['view'],  1))
                x_99 = max(x_99, np.percentile(well['view'], 99))

    if linear:
        x_min = 0
        x_max = x_99
    else:
        x_min = np.log10(x_min)
        x_max = np.log10(x_max)

    ax.set_xlim(x_min, x_max)

def pick_xlabels(ax1, ax2, experiments, linear=False):
    if experiments[0]['channel'] in fluorescence_controls:
        x1_label = 'fluorescence'
        x2_label = 'fold repression'
    else:
        x1_label = 'size'
        x2_label = 'fold change'
    
    if experiments[0]['control_channel'] is not None:
        x1_label = 'normalized {}'.format(x1_label)

    if not linear:
        x1_label = 'log({})'.format(x1_label)

    ax1.set_xlabel(x1_label)
    ax2.set_xlabel(x2_label)

def pick_xticks(ax, max_ticks=6):
    x_min, x_max = ax.get_xlim()
    x_ticks = ax.get_xticks()

    while len(x_ticks) > max_ticks:
        dx = abs(2 * x_ticks[1] - x_ticks[0])
        x_ticks = [x_min]
        while x_ticks[-1] < x_max:
            x_ticks.append(x_ticks[-1] + dx)

    ax.set_xlim(x_ticks[0], x_ticks[-1])
    ax.set_xticks(x_ticks)

def pick_yticks(ax, experiments):
    y_ticks = []
    y_tick_labels = []

    for i, experiment in enumerate(reversed(experiments)):
        y_ticks.append(i)
        y_tick_labels.append(experiment['label'].replace('//', '\n'))

    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tick_labels)

def pick_color(experiment):
    """
    Pick a color for the given experiment.  Data from the FITC-A channel are 
    colored green, data from the PE-Texas Red-A channel are colored red, and 
    data from the other channels (presumably FSC-A and SSC-A) are colored 
    brown.  The specific hex values come from the Tango color scheme.
    """
    if experiment['channel'] == 'FITC-A':
        return '#4e9a06'
    elif experiment['channel'] == 'PE-Texas Red-A':
        return '#cc0000'
    else:
        return '#c17d11'


if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)
    experiments = fcmcmp.load_experiments(args['<experiments>'])

    resolve_channels = ResolveChannels()
    resolve_channels.view = args['--channel']
    resolve_channels.normalize_by = args['--normalize-by'] or \
            args['--normalize-by-internal-control']
    gate_nonpositive_events = fcmcmp.GateNonPositiveEvents()
    gate_nonpositive_events.channels = 'FITC-A', 'PE-Texas Red-A'
    gate_small_cells = fcmcmp.GateSmallCells()
    gate_small_cells.save_size_col = True
    gate_small_cells.threshold = int(args['--size-gate'])
    gate_low_fluorescence = GateLowFluorescence()
    gate_low_fluorescence.threshold = float(args['--expression-gate'])
    setup_visualization = SetupVisualization()
    fcmcmp.run_all_processing_steps(experiments)

    # We have to decide whether or not to fork before plotting anything, 
    # otherwise X11 will complain, and we only want to fork if we'll end up 
    # showing the GUI.  So first we calculate the output path, then we either 
    # fork or don't, then we plot everything, then we either display the GUI or 
    # save the figure to a file.

    output_path = args['--output']
    if output_path:
        output_path = output_path.replace(
                '$', Path(args['<experiments>']).stem)

    import os, sys
    if not output_path and os.fork():
        sys.exit()

    fig = plot_everything(
            experiments,
            linear=args['--linear'],
            histogram=args['--histogram'],
            pdf=args['--pdf'],
            mode=args['--mode'],
    )

    if output_path:
        plt.savefig(output_path)
    else:
        fig.canvas.set_window_title(' '.join(sys.argv))
        plt.show()
