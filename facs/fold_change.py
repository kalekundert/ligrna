#!/usr/bin/env python3

"""\
Show the changes between populations of cells in different conditions.

Usage:
    my_analysis.py <yml_path> [options]

Arguments:
    <yml_path>
        Path to a YAML file specifying which wells and which plates should be 
        compared with each other.

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
        Otherwise, a default channel may be chosen based on the name of the 
        experiment.  It is an error if no channel is specified and no channel 
        can be deduced.

    -n --normalize-by <channel>
        Normalize the channel of interest (see --channel) by the given channel.
        For example, you might specify "FSC-A", "SSC-A", or "FSC-A + m * SSC-A" 
        to normalize by cell size.  By default no normalization is done.

    -N --normalize-by-internal-control
        Normalize by FITC-A (GFP expression) if the channel of interest is 
        PE-Texas Red-A or DsRed-A (RFP expression) and vice versa.  This 
        assumes that the fluorescent protein that isn't of interest is being 
        constitutively expressed, and therefore can be used as an internal 
        control for cell size and expression level.

    -t --time-gate <secs>               [default: -1]
        Exclude the first cells recorded from each well if you suspect that 
        they may be contaminated with cells from the previous well.  In most 
        cases, the default (indicated by a negative value) is to keep all the 
        data.  However, if the data was collected on the LSRII, the default is 
        to throw out the first 2 secs.

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

    -l --log-toggle
        Plot the data on a linear scale if it would normally be plotted on a 
        log scale, and vice versa.  In most cases, this means plotting the 
        fluorescent channels on a linear scale and the size channels on a log 
        scale.

    -m --mode
        Use the modes of the cell distributions to calculate fold-changes in 
        signal.  By default the medians are used for this calculation.
"""

import fcmcmp, analysis_helpers
import numpy as np, matplotlib.pyplot as plt
from pprint import pprint

class FoldChange:

    def __init__(self, experiments):
        # Settings configured by the user.
        self.experiments = experiments
        self.channel = None
        self.control_channel = None
        self.normalize_by = None
        self.log_toggle = None
        self.histogram = None
        self.pdf = None
        self.mode = None

        # Internally used plot attributes.
        self.figure = None
        self.axes = None
        self.analyzed_wells = None
        self.max_dist_height = 0.7
        self.location_depth = 0.2
        self.dist_line_width = 1
        self.fold_change_bar_width = 6
        self.max_fold_change_ticks = 6

    def plot(self):
        self._setup_figure()
        self._setup_grid_lines()
        self._analyze_wells()
        self._pick_xlim()
        self._estimate_distributions()
        self._rescale_distributions()

        for i, experiment in enumerate(reversed(self.analyzed_wells)):
            self._plot_fold_change(i, experiment)
            for condition in experiment:
                for well in experiment[condition]:
                    self._plot_distribution(i, well, condition)
                    self._plot_location(i, well, condition)

        self._pick_xlabels()
        self._pick_xticks()
        self._pick_ylim()
        self._pick_yticks()

    def _setup_figure(self):
        """
        Make two subplots with a shared y-axis.
        """
        self.figure, self.axes = plt.subplots(
                1, 2,
                sharey=True,
                gridspec_kw=dict(
                    hspace=0.001,
                    width_ratios=(0.65, 0.35),
                ),
        )

    def _setup_grid_lines(self):
        """
        Turn on grid lines, but put them behind everything else.
        """
        for ax in self.axes:
            ax.xaxis.grid(True)
            ax.set_axisbelow(True)

    def _analyze_wells(self):
        """
        Create a data structure that mirrors ``self.experiments'', but holds 
        more specific information on the distribution of cells in each well.
        """
        self.analyzed_wells = [{
                condition: [
                    analysis_helpers.AnalyzedWell(
                        experiment, well,
                        channel=self.channel,
                        normalize_by=self.normalize_by,
                        log_toggle=self.log_toggle,
                        histogram=self.histogram,
                        pdf=self.pdf,
                        mode=self.mode,
                    )
                    for well in experiment['wells'][condition]
                ]
                for condition in experiment['wells']
            }
            for experiment in self.experiments
        ]
        self.reference_well = next(iter(self.analyzed_wells[0].values()))[0]

    def _yield_analyzed_wells(self):
        for experiment in self.analyzed_wells:
            for condition in experiment:
                for well in experiment[condition]:
                    yield well.experiment, condition, well

    def _pick_xlim(self):
        """
        Decide what the x-limits should be for the distributions plot.  This 
        has to be decided before the distributions themselves are calculated.
        """
        x_min = x_01 = np.inf
        x_max = x_99 = -np.inf

        for _, _, well in self._yield_analyzed_wells():
            x_min = min(x_min, np.min(well.measurements))
            x_max = max(x_max, np.max(well.measurements))
            x_01 = min(x_01, np.percentile(well.measurements,  1))
            x_99 = max(x_99, np.percentile(well.measurements, 99))

        self.axes[0].set_xlim(x_min, x_max)

    def _estimate_distributions(self):
        """
        Once the x-limits have been picked, estimate the distribution of cells 
        along the channel of interest for each well.
        """
        for _, _, well in self._yield_analyzed_wells():
            well.estimate_distribution(self.axes[0])

    def _rescale_distributions(self):
        """
        Scale all the distributions such that the tallest one has the desired 
        height.
        """
        max_height = 0

        # Find the distribution with the tallest peak.

        for _, _, well in self._yield_analyzed_wells():
            max_height = max(max_height, np.max(well.y))

        # Scale each distribution relative to the one with the tallest peak.

        scale_factor = self.max_dist_height / max_height

        for _, _, well in self._yield_analyzed_wells():
            well.y *= scale_factor

    def _plot_distribution(self, i, well, condition):
        """
        Plot the given distributions of cells on the same axis, for comparison.
        """
        self.axes[0].plot(well.x, well.y + i,
                **analysis_helpers.pick_style(well.experiment, condition))

    def _plot_location(self, i, well, condition):
        """
        Mark the location on each distribution that will be used to calculate a 
        fold change.
        """
        location_styles = {
                'before': {
                    'marker': '+',
                    'markeredgecolor': 'black',
                    'markerfacecolor': 'none',
                    'markeredgewidth': 1,
                    'linestyle': ' ',
                    'zorder': 1,
                },
                'after': {
                    'marker': '+',
                    'markeredgecolor': analysis_helpers.pick_color(well.experiment),
                    'markerfacecolor': 'none',
                    'markeredgewidth': 1,
                    'linestyle': ' ',
                    'zorder': 2,
                },
        }
        self.axes[0].plot(
                well.loc,
                i - self.location_depth,
                **location_styles[condition])

    def _plot_fold_change(self, i, analyzed_wells):
        # I really don't think this function is comparing distributions or 
        # calculating error bars in the right way.  I think it might be best to 
        # do some sort of resampling technique.  That would allow me to 
        # incorporate knowledge of the underlying distributions into the 
        # standard deviation.

        # Calculate fold changes between the before and after distributions, 
        # accounting for the fact that the distributions may be in either 
        # linear or log space.
        locations = {
                condition: np.array([
                    well.loc for well in analyzed_wells[condition]])
                for condition in analyzed_wells
        }

        if self.reference_well.log_scale:
            fold_changes = 10**(locations['before'] - locations['after'])
        else:
            fold_changes = locations['before'] / locations['after']

        # We don't care which direction the fold change is in, so invert the 
        # fold change if it's less than 1 (e.g.  for a backward design).
        fold_change = fold_changes.mean()
        if fold_change < 1.0: fold_change **= -1

        # Plot the fold-change with standard-error error-bars.  I use plot() 
        # and not barh() to draw the bar plots because I don't want the width 
        # of the bars to change with the y-axis (either as more bars are added 
        # or as the user zooms in).
        experiment = next(iter(analyzed_wells.values()))[0].experiment
        color = analysis_helpers.pick_color(experiment)

        self.axes[1].plot(
                [0, fold_change], [i, i],
                color=color,
                linewidth=self.fold_change_bar_width,
                solid_capstyle='butt',
        )
        self.axes[1].errorbar(
                fold_change, i,
                xerr=fold_changes.std(),
                ecolor=color,
                capsize=self.fold_change_bar_width / 2,
        )

    def _pick_xlabels(self):
        if self.reference_well.channel in analysis_helpers.fluorescence_controls:
            x1_label = 'fluorescence'
        else:
            x1_label = 'size'
        
        if self.reference_well.control_channel is not None:
            x1_label = 'normalized {}'.format(x1_label)

        if self.reference_well.log_scale:
            x1_label = 'log({})'.format(x1_label)

        self.axes[0].set_xlabel(x1_label)
        self.axes[1].set_xlabel('fold change')

    def _pick_xticks(self):
        x_min, x_max = self.axes[1].get_xlim()
        x_ticks = self.axes[1].get_xticks()

        while len(x_ticks) > self.max_fold_change_ticks:
            dx = abs(2 * x_ticks[1] - x_ticks[0])
            x_ticks = [x_min]
            while x_ticks[-1] < x_max:
                x_ticks.append(x_ticks[-1] + dx)

        #x_ticks = [0, 0.5, 1.0, 1.5, 2.0]
        self.axes[1].set_xlim(x_ticks[0], x_ticks[-1])
        self.axes[1].set_xticks(x_ticks)

    def _pick_ylim(self):
        margin = 0.3
        y_min = 0 - self.location_depth - margin
        y_max = len(self.experiments) - 1 + self.max_dist_height + margin
        self.axes[0].set_ylim(y_min, y_max)

    def _pick_yticks(self):
        y_ticks = []
        y_tick_labels = []

        for i, experiment in enumerate(reversed(self.experiments)):
            y_ticks.append(i)
            y_tick_labels.append(experiment['label'].replace('//', '\n'))

        self.axes[0].set_yticks(y_ticks)
        self.axes[0].set_yticklabels(y_tick_labels)



if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)
    experiments = fcmcmp.load_experiments(args['<yml_path>'])

    shared_steps = analysis_helpers.SharedProcessingSteps()
    shared_steps.early_event_threshold = float(args['--time-gate'])
    shared_steps.small_cell_threshold = float(args['--size-gate'])
    shared_steps.low_fluorescence_threshold = float(args['--expression-gate'])
    shared_steps.process(experiments)

    analysis = FoldChange(experiments)
    analysis.channel = args['--channel']
    analysis.normalize_by = args['--normalize-by'] or args['--normalize-by-internal-control']
    analysis.log_toggle = args['--log-toggle']
    analysis.histogram = args['--histogram']
    analysis.pdf = args['--pdf']
    analysis.mode = args['--mode']

    with analysis_helpers.plot_or_savefig(args['--output'], args['<yml_path>']):
        analysis.plot()

