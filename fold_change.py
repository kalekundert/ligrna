#!/usr/bin/env python3

"""\
Show the changes between populations of cells in different conditions.

Usage:
    fold_change.py <yml_path> [options]

Arguments:
    <yml_path>
        Path to a YAML file specifying which wells and which plates should be 
        compared with each other.

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

    -T --title <str>
        Provide a title for the plot.

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

    -s --sort-by <attribute>
        Sort the traces by the specified attribute.  The following attributes 
        are understood: name (n), fold-change (f), most-wt (w), most-dead (d).  
        You can use either the full names or the one-letter abbreviations.  By 
        default the traces are shown in the order they appear in the YAML file.

    -q --query <regex>
        Only show experiments if their label matches the given regular 
        expression.  This option is meant to help show interesting subsets of 
        really high throughput experiments.

    -u --quality-filter <level>         [default: good]
        Only show experiments of the indicated quality or better.  Understood quality 
        levels are 'all', 'good', and 'bad'.  All data is assumed to be good by 
        default, but certain data point can marked as bad by setting `discard: 
        True` in the *.yml file.

    -i --indices <selection>
        Only show experiments with the given indices (counting from 1).  The 
        indices should be comma separated, and ranges of indices can be 
        specified using a hyphen (e.g. 2-8).  This option is meant to help when 
        viewing data from really high-throughput experiments.

    -t --time-gate <secs>               [default: 0]
        Exclude the first cells recorded from each well if you suspect that 
        they may be contaminated with cells from the previous well.  The 
        default is to keep all the data.

    -z --size-gate <percentile>         [default: 0]
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
        reliable (see --loc-metric).  Larger bins may hide features.  
        
    -p --pdf
        Normalize the cell distributions such they all have the same area, and 
        are thus PDFs.  By default, the area of each curve reflects the number 
        of cells that were counted from that well.

    -f --fold-change-xlim <xlim>
        Set the extent of the x-axis for the fold-change plot.  By default this 
        axis is automatically scaled to fit the data, but this option is useful 
        if you want to compare different plots.

    -l --log-toggle
        Plot the data on a linear scale if it would normally be plotted on a 
        log scale, and vice versa.  In most cases, this means plotting the 
        fluorescent channels on a linear scale and the size channels on a log 
        scale.

    -m --loc-metric <median|mean|mode>
        Specify which metric should be used to determine the "centers" of the 
        cell distributions for the purpose of calculating the fold change in 
        signal.  By default the median is used for this calculation.  Note that 
        the mean and the mode will both change depending on whether or not the 
        data has been log-transformed (see --log-toggle).  The mode will also 
        change based on how data is histogrammed (see --histogram).
"""

import fcmcmp, analysis_helpers, nonstdlib, re
import numpy as np, matplotlib.pyplot as plt
from pprint import pprint

class FoldChange:

    def __init__(self, experiments):
        # Settings configured by the user.
        self.experiments = experiments
        self.channel = None
        self.control_channel = None
        self.normalize_by = None
        self.sort_by = None
        self.label_filter = None
        self.quality_filter = None
        self.show_indices = None
        self.log_toggle = None
        self.histogram = None
        self.pdf = None
        self.loc_metric = None
        self.output_size = None
        self.title = None
        self.fold_change_xlim = None

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
        self._sort_wells()
        self._filter_wells()

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

        self.figure.tight_layout()

    def _setup_figure(self):
        """
        Make two subplots with a shared y-axis.
        """
        self.figure, self.axes = plt.subplots(
                1, 2,
                sharey=True,
                figsize=self.output_size,
                gridspec_kw=dict(
                    width_ratios=(0.65, 0.35),
                ),
        )

        if self.title:
            self.figure.suptitle(self.title)

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
                        loc_metric=self.loc_metric,
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

    def _sort_wells(self):
        if self.sort_by is None:
            return

        if self.sort_by.lower() in {'n', 'name'}:
            key = lambda expt: self._get_label(expt)
            reverse = self.sort_by[0].isupper()

        elif self.sort_by.lower() in {'f', 'fold-change'}:
            key = lambda expt: self._get_fold_change(expt)[0]
            reverse = not self.sort_by[0].isupper()

        elif self.sort_by.lower() in {'w', 'most-wt'}:
            key = lambda expt: min(
                    np.mean([w.loc for w in expt['apo']]),
                    np.mean([w.loc for w in expt['holo']]))
            reverse = False

        elif self.sort_by.lower() in {'d', 'most-dead'}:
            key = lambda expt: max(
                    np.mean([w.loc for w in expt['apo']]),
                    np.mean([w.loc for w in expt['holo']]))
            reverse = True

        self.analyzed_wells.sort(key=key, reverse=reverse)

    def _filter_wells(self):
        # Filter out data points that are marked as being high or low quality.
        if self.quality_filter == 'good' or self.quality_filter is None:
            self.analyzed_wells = [
                    expt for expt in self.analyzed_wells
                    if not expt['apo'][0].experiment.get('discard')
            ]
        elif self.quality_filter == 'bad':
            self.analyzed_wells = [
                    expt for expt in self.analyzed_wells
                    if expt['apo'][0].experiment.get('discard')
            ]
        elif self.quality_filter == 'all':
            pass
        else:
            raise ValueError("unknown quality filter '{}'".format(self.quality_filter))

        # Filter out experiments with labels that don't match the user given 
        # regular expression.
        if self.label_filter is not None:
            label_filter = re.compile(self.label_filter)
            self.analyzed_wells = [
                    expt for expt in self.analyzed_wells
                    if label_filter.search(expt['apo'][0].experiment['label'])
            ]

        # Filter out experiments that aren't in the user given list of indices.  
        # This filter is applied after the regex filter, so if the user wants 
        # to use both, the indices will be relative to what appears in the GUI.
        if self.show_indices is not None:
            self.analyzed_wells = [
                    expt for i, expt in enumerate(self.analyzed_wells)
                    if i in self.show_indices
            ]

    def _get_label(self, experiment):
        return experiment['apo'][0].experiment['label']

    def _get_fold_change(self, experiment):

        def get_fold_change(apo, holo):
            # We don't care which direction the fold change is in, so invert 
            # the fold change if it's less than 1 (e.g. for a backward design).
            x = holo.linear_loc / apo.linear_loc
            return x if x > 1 else 1/x

        fold_changes = np.array([
                get_fold_change(apo, holo)
                for apo, holo in zip(experiment['apo'], experiment['holo'])
        ])
        if fold_changes.size > 0:
            return fold_changes.mean(), fold_changes
        else:
            return 0, fold_changes

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
                'apo': {
                    'marker': '+',
                    'markeredgecolor': 'black',
                    'markerfacecolor': 'none',
                    'markeredgewidth': 1,
                    'linestyle': ' ',
                    'zorder': 1,
                },
                'holo': {
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

    def _plot_fold_change(self, i, experiment):
        # I really don't think this function is comparing distributions or 
        # calculating error bars in the right way.  I think it might be best to 
        # do some sort of resampling technique.  That would allow me to 
        # incorporate knowledge of the underlying distributions into the 
        # standard deviation.

        fold_change, fold_changes = self._get_fold_change(experiment)

        # If there isn't enough data to calculate a fold change, bail out here.
        if fold_changes.size == 0:
            return

        # Plot the fold-change with standard-error error-bars.  I use plot() 
        # and not barh() to draw the bar plots because I don't want the width 
        # of the bars to change with the y-axis (either as more bars are added 
        # or as the user zooms in).
        experiment = next(iter(experiment.values()))[0].experiment
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
        from matplotlib.ticker import MaxNLocator
        max_fold_change_ticks = self.max_fold_change_ticks

        class FoldChangeLocator(MaxNLocator):

            def __init__(self):
                super().__init__(
                        nbins=max_fold_change_ticks-1,
                        steps=[0.5, 1, 2, 5, 10, 50, 100],
                )
            def tick_values(self, vmin, vmax):
                ticks = set(super().tick_values(vmin, vmax))
                ticks.add(1); ticks.discard(0)
                return sorted(ticks)

        if self.fold_change_xlim is not None:
            self.axes[1].set_xlim(0, self.fold_change_xlim)

        self.axes[1].xaxis.set_major_locator(FoldChangeLocator())

    def _pick_ylim(self):
        margin = 0.3
        y_min = 0 - self.location_depth - margin
        y_max = len(self.analyzed_wells) - 1 + self.max_dist_height + margin
        self.axes[0].set_ylim(y_min, y_max)

    def _pick_yticks(self):
        y_ticks = []
        y_tick_labels = []

        for i, experiment in enumerate(reversed(self.analyzed_wells)):
            label = self._get_label(experiment).replace('//', '\n')
            y_tick_labels.append(label)
            y_ticks.append(i)

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
    analysis.sort_by = args['--sort-by']
    analysis.label_filter = args['--query']
    analysis.quality_filter = args['--quality-filter']
    analysis.log_toggle = args['--log-toggle']
    analysis.histogram = args['--histogram']
    analysis.pdf = args['--pdf']
    analysis.loc_metric = args['--loc-metric']
    analysis.title = args['--title']

    if args['--indices']:
        analysis.show_indices = nonstdlib.indices_from_str(args['--indices'], start=1)
    if args['--output-size']:
        analysis.output_size = map(float, args['--output-size'].split('x'))
    if args['--fold-change-xlim']:
        analysis.fold_change_xlim = float(args['--fold-change-xlim'])

    with analysis_helpers.plot_or_savefig(args['--output'], args['<yml_path>']):
        analysis.plot()

