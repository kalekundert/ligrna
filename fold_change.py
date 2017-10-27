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

    -b --baseline <expt>
        Normalize all the experiments by the average fluorescence value of the 
        this experiment over all concentrations tested.  This normalization  
        helps iron out slight variations in the relative levels of GFP and RFP 
        between experiments.

    -n --normalize-by <channel>
        Normalize the channel of interest (see --channel) by the given channel.
        For example, you might specify "FSC-A", "SSC-A", or "FSC-A + m * SSC-A" 
        to normalize by cell size.  By default the data is normalized by GFP-A 
        (GFP expression) if the channel of interest is PE-Texas Red-A or 
        DsRed-A (RFP expression) and vice versa.

    -N --no-normalize
        Show raw, unnormalized data.

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
        Only show experiments of the indicated quality or better.  Understood 
        quality levels are 'all', 'good', and 'bad'.  All data is assumed to be 
        good by default, but certain data points can marked as bad by setting 
        `discard: True` in the *.yml file.

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
        many cells are excluded.  The default is to include all cells.

    -x --expression-gate <signal>       [default: 1e3]
        Exclude cells where the signal on the fluorescence control channel is 
        less than the given value.  The purpose of this gate is to get rid of 
        cells that weren't expressing much fluorescent protein, for whatever 
        reason.  Note that this gate is in absolute units, not log units.

    -p --pdf
        Normalize the cell distributions such they all have the same area, and 
        are thus PDFs.  By default, the area of each curve reflects the number 
        of cells that were counted from that well.

    -f --fold-change-xlim <xmax>
        Set the extent of the x-axis for the fold-change plot.  By default this 
        axis is automatically scaled to fit the data, but this option is useful 
        if you want to compare different plots.

    -d --distribution-xlim <xmin,xmax>
        Set the range of the x-axis for the cell distribution plots.  By 
        default this is based on the minimum and maximum data points, but 
        sometimes it can be useful to zoom in a little more closely.

    -l --log-toggle
        Plot the data on a linear scale if it would normally be plotted on a 
        log scale, and vice versa.  In most cases, this means plotting the 
        fluorescent channels on a linear scale and the size channels on a log 
        scale.

    -m --loc-metric <median|mean|mode>
        Specify which metric should be used to determine the "centers" of the 
        cell distributions for the purpose of calculating the fold change in 
        signal.  By default the mode is used for this calculation.  Note that 
        the mean and the mode will both change depending on whether or not the 
        data has been log-transformed (see --log-toggle).

    -Q --trace-quality <samples>        [default: 100]
        Set the number of points to evaluate along each trace.  More points 
        will make the traces smoother, while fewer points will make the plot 
        render faster.

    -I --inkscape
        Create an SVG output file that works well with inkscape by having 
        matplotlib create a PDF, then converting it to SVG in a second step.  
        For some reason the SVG files generated directly by matplotlib cause 
        inkscape to run really slow and chew up a lot of memory.  I played 
        around with one of these files a bit, and I think the problem might 
        have to do with the use of clones.  In any case, generating PDF files 
        and converting them to SVG seems to avoid the problem.

    -e --export-dataframe
        Exports a dataframe with the values used to generate the figure

    -v --verbose
        Print out information on all the processing steps.
"""

import fcmcmp, analysis_helpers, nonstdlib, re
import numpy as np, matplotlib.pyplot as plt
from pprint import pprint

class FoldChange:

    def __init__(self, experiments):
        # Settings configured by the user.
        self.experiments = experiments
        self.reference_condition = 'apo'
        self.baseline_expt = 'off'
        self.apply_baseline = True
        self.channel = None
        self.control_channel = None
        self.sort_by = None
        self.label_filter = None
        self.quality_filter = None
        self.show_indices = None
        self.log_toggle = None
        self.pdf = None
        self.loc_metric = None
        self.output_size = None
        self.title = None
        self.fold_change_xlim = None
        self.distribution_xlim = None
        self.trace_quality = None

        # Internally used plot attributes.
        self.figure = None
        self.axes = None
        self.comparisons = None
        self.max_dist_height = 0.7
        self.location_depth = 0.2
        self.dist_line_width = 1
        self.fold_change_bar_width = 6
        self.max_fold_change_ticks = 6

    def plot(self):
        self._setup_figure()
        self._setup_axes()
        self._analyze_wells()
        self._pick_xlim()
        self._estimate_distributions()
        self._rescale_distributions()
        self._sort_wells()
        self._filter_wells()

        for i, comparison in enumerate(reversed(self.comparisons)):
            self._plot_fold_change(i, comparison)

            for well in comparison.reference_wells:
                self._plot_distribution(i, comparison, well, True)
                self._plot_location(i, comparison, well, True)

            for well in comparison.condition_wells:
                self._plot_distribution(i, comparison, well, False)
                self._plot_location(i, comparison, well, False)

        self._pick_xlabels()
        self._pick_xticks()
        self._pick_ylim()
        self._pick_yticks()

        self.figure.tight_layout()
        return self.figure

    def _setup_figure(self):
        """
        Make two subplots with a shared y-axis.
        """
        self.figure, self.axes = plt.subplots(
            1, 2,
            sharey=True,
            figsize=self.output_size,
            facecolor='y',
            gridspec_kw=dict(
                width_ratios=(0.65, 0.35),
            ),
        )

        # Don't show that ugly dark grey border around the plot.
        self.figure.patch.set_alpha(0)
        if self.title:
            self.figure.suptitle(self.title)

    def _setup_axes(self):
        """
        Turn on grid lines, but put them behind everything else.
        """
        self.axes[0].set_xscale('log')

        for ax in self.axes:
            ax.xaxis.grid(True)
            ax.set_axisbelow(True)

    def _analyze_wells(self):
        analysis_helpers.analyze_wells(
                self.experiments,
                channel=self.channel,
                control_channel=self.control_channel,
                log_toggle=self.log_toggle,
                pdf=self.pdf,
                loc_metric=self.loc_metric,
                num_samples=self.trace_quality,
        )
        self.comparisons = list(analysis_helpers.yield_related_wells(
                self.experiments,
                self.reference_condition,
        ))

    def _yield_wells(self):
        yield from fcmcmp.yield_wells(self.experiments)

    def _pick_xlim(self):
        """
        Decide what the x-limits should be for the distributions plot.  This
        has to be decided before the distributions themselves are calculated.
        """
        if self.distribution_xlim:
            x_min, x_max = self.distribution_xlim
        else:
            x_min = x_01 = np.inf
            x_max = x_99 = -np.inf
            for _, _, well in self._yield_wells():
                x_min = min(x_min, np.min(well.log_measurements))
                x_max = max(x_max, np.max(well.log_measurements))

        self.axes[0].set_xlim(10**x_min, 10**x_max)

    def _estimate_distributions(self):
        """
        Once the x-limits have been picked, estimate the distribution of cells
        along the channel of interest for each well.
        """
        for _, _, well in self._yield_wells():
            xlim = self.axes[0].get_xlim()
            well.estimate_distribution(np.log10(xlim))

    def _rescale_distributions(self):
        """
        Scale all the distributions such that the tallest one has the desired
        height.
        """
        max_height = 0

        # Find the distribution with the tallest peak.

        for _, _, well in self._yield_wells():
            max_height = max(max_height, np.max(well.y))

        # Scale each distribution relative to the one with the tallest peak.

        scale_factor = self.max_dist_height / max_height

        for _, _, well in self._yield_wells():
            well.y *= scale_factor

    def _sort_wells(self):
        if self.sort_by is None:
            return

        if self.sort_by.lower() in {'n', 'name'}:
            key = lambda comp: (comp.label, comp.condition)
            reverse = self.sort_by[0].isupper()

        elif self.sort_by.lower() in {'f', 'fold-change'}:
            key = lambda comp: self._get_fold_change(comp)[0]
            reverse = not self.sort_by[0].isupper()

        elif self.sort_by.lower() in {'w', 'most-wt'}:
            key = lambda comp: min(
                np.mean([w.loc for w in comp.condition_wells]),
                np.mean([w.loc for w in comp.reference_wells]))
            reverse = False

        elif self.sort_by.lower() in {'d', 'most-dead'}:
            key = lambda comp: max(
                np.mean([w.loc for w in comp.condition_wells]),
                np.mean([w.loc for w in comp.reference_wells]))
            reverse = True

        self.comparisons.sort(key=key, reverse=reverse)

    def _filter_wells(self):
        # Filter out data points that are marked as being high or low quality.
        if self.quality_filter == 'good' or self.quality_filter is None:
            self.comparisons = [
                comp for comp in self.comparisons
                if not comp.experiment.get('discard')
            ]
        elif self.quality_filter == 'bad':
            self.comparisons = [
                comp for comp in self.comparisons
                if comp.experiment.get('discard')
            ]
        elif self.quality_filter == 'all':
            pass
        else:
            raise ValueError("unknown quality filter '{}'".format(self.quality_filter))

        # Filter out experiments with labels that don't match the user given
        # regular expression.
        if self.label_filter is not None:
            label_filter = re.compile(self.label_filter)
            self.comparisons = [
                comp for comp in self.comparisons
                if label_filter.search(comp.label)
            ]

        # Filter out experiments that aren't in the user given list of indices.
        # This filter is applied after the regex filter, so if the user wants
        # to use both, the indices will be relative to what appears in the GUI.
        if self.show_indices is not None:
            self.comparisons = [
                comp for i, comp in enumerate(self.comparisons)
                if i in self.show_indices
            ]

    def _get_label(self, comparison):
        if comparison.solo:
            label = comparison.label
        else:
            label = comparison.label + '\n' + comparison.condition

        return label.replace('//', '\n')

    def _get_fold_change(self, comparison):

        def get_fold_change(apo, holo):
            # We don't care which direction the fold change is in, so invert
            # the fold change if it's less than 1 (e.g. for a backward design).
            x = holo.linear_loc / apo.linear_loc
            return x if x > 1 else 1 / x

        fold_changes = np.array([
            get_fold_change(apo, holo) for apo, holo in zip(
                comparison.condition_wells, comparison.reference_wells)
        ])
        
        if len(fold_changes) > 0:
            return fold_changes.mean(), fold_changes
        else:
            return 0, fold_changes

    def _plot_fold_change(self, i, comparison):
        # I really don't think this function is comparing distributions or
        # calculating error bars in the right way.  I think it might be best to
        # do some sort of resampling technique.  That would allow me to
        # incorporate knowledge of the underlying distributions into the
        # standard deviation.
        fold_change, fold_changes = self._get_fold_change(comparison)

        # If there isn't enough data to calculate a fold change, bail out here.
        if fold_changes.size == 0:
            return

        # Plot the fold-change with standard-error error-bars.  I use plot()
        # and not barh() to draw the bar plots because I don't want the width
        # of the bars to change with the y-axis (either as more bars are added
        # or as the user zooms in).
        color = analysis_helpers.pick_color(comparison.experiment)

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

    def _plot_distribution(self, i, comparison, well, is_reference):
        """
        Plot the given distributions of cells on the same axis, for comparison.
        """
        style = analysis_helpers.pick_style(comparison.experiment, is_reference)
        self.axes[0].plot(10**well.x, well.y + i, **style)

    def _plot_location(self, i, comparison, well, is_reference):
        """
        Mark the location on each distribution that will be used to calculate a
        fold change.
        """
        if is_reference:
            style = {
                'marker': '+',
                'markeredgecolor': 'black',
                'markerfacecolor': 'none',
                'markeredgewidth': 1,
                'linestyle': ' ',
                'zorder': 1,
            }
        else:
            style = {
                'marker': '+',
                'markeredgecolor': analysis_helpers.pick_color(comparison.experiment),
                'markerfacecolor': 'none',
                'markeredgewidth': 1,
                'linestyle': ' ',
                'zorder': 2,
            }

        self.axes[0].plot(10**well.loc, i - self.location_depth, **style)

    def _pick_xlabels(self):
        label = analysis_helpers.get_channel_label(self.experiments)
        self.axes[0].set_xlabel(label)
        self.axes[1].set_xlabel('fold change')

    def _pick_xticks(self):
        from matplotlib.ticker import MaxNLocator
        max_fold_change_ticks = self.max_fold_change_ticks

        class FoldChangeLocator(MaxNLocator):
            def __init__(self):
                super().__init__(
                    nbins=max_fold_change_ticks - 1,
                    #steps=[0.5, 1, 2, 5, 10, 50, 100],
                    steps=[1, 2, 5, 10],
                )

            def tick_values(self, vmin, vmax):
                ticks = set(super().tick_values(vmin, vmax))
                ticks.add(1);
                ticks.discard(0)
                return sorted(ticks)

        if self.fold_change_xlim is not None:
            self.axes[1].set_xlim(0, self.fold_change_xlim)

        self.axes[1].xaxis.set_major_locator(FoldChangeLocator())

    def _pick_ylim(self):
        margin = 0.3
        y_min = 0 - self.location_depth - margin
        y_max = len(self.comparisons) - 1 + self.max_dist_height + margin
        self.axes[0].set_ylim(y_min, y_max)

    def _pick_yticks(self):
        y_ticks = []
        y_tick_labels = []

        for i, comparison in enumerate(reversed(self.comparisons)):
            y_tick_labels.append(self._get_label(comparison))
            y_ticks.append(i)

        self.axes[0].set_yticks(y_ticks)
        self.axes[0].set_yticklabels(y_tick_labels)

    def export_df(self):
        import pandas as pd
        df = pd.DataFrame()

        columns = ["Design",
                   "Spacer",
                   "Aptamer_Ligand",
                   "Assayed_Ligand",
                   "Fold_Change"
                   ]

        for comparison in self.comparisons:
            label_components = re.split("_|-", self._get_label(comparison))
            # print(label_components)
            if len(label_components) == 2:
                for fold_change in self._get_fold_change(comparison)[1]:
                    temp_series = pd.Series(data={"Design": label_components[0],
                                                  "Spacer": label_components[0].split('.')[0],
                                                  "Aptamer_Ligand": "None",
                                                  "Assayed_Ligand": label_components[1],
                                                  "Fold_Change": fold_change
                                                  }
                                            )
                    # print (temp_series)
                    df = df.append(temp_series, ignore_index=True)
            elif len(label_components) == 3:
                for fold_change in self._get_fold_change(comparison)[1]:
                    temp_series = pd.Series(data={"Design": label_components[0],
                                                  "Spacer": label_components[1],
                                                  "Aptamer_Ligand": "THEO",
                                                  "Assayed_Ligand": label_components[2],
                                                  "Fold_Change": fold_change
                                                  }
                                            )
                    # print (temp_series)
                    df = df.append(temp_series, ignore_index=True)

            elif len(label_components) == 4:
                for fold_change in self._get_fold_change(comparison)[1]:
                    temp_series = pd.Series(data={"Design": label_components[0],
                                                  "Spacer": label_components[1],
                                                  "Aptamer_Ligand": label_components[2],
                                                  "Assayed_Ligand": label_components[3],
                                                  "Fold_Change": fold_change
                                                  }
                                            )
                    # print (temp_series)
                    df = df.append(temp_series, ignore_index=True)

        df.to_csv("Fold_Change_df-LATEST.csv")



if __name__ == '__main__':
    import docopt

    args = docopt.docopt(__doc__)
    experiments = fcmcmp.load_experiments(args['<yml_path>'])

    shared_steps = analysis_helpers.SharedProcessingSteps(args['--verbose'])
    shared_steps.early_event_threshold = float(args['--time-gate'])
    shared_steps.small_cell_threshold = float(args['--size-gate'])
    shared_steps.low_fluorescence_threshold = float(args['--expression-gate'])
    shared_steps.process(experiments)

    analysis = FoldChange(experiments)
    analysis.channel = args['--channel']
    analysis.control_channel = args['--normalize-by'] or not args['--no-normalize']
    analysis.apply_baseline = args['--baseline']
    analysis.sort_by = args['--sort-by']
    analysis.label_filter = args['--query']
    analysis.quality_filter = args['--quality-filter']
    analysis.log_toggle = args['--log-toggle']
    analysis.pdf = args['--pdf']
    analysis.loc_metric = args['--loc-metric']
    analysis.title = args['--title']
    analysis.trace_quality = int(args['--trace-quality'])

    if args['--indices']:
        analysis.show_indices = nonstdlib.indices_from_str(args['--indices'], start=1)
    if args['--output-size']:
        analysis.output_size = map(float, args['--output-size'].split('x'))
    if args['--fold-change-xlim']:
        analysis.fold_change_xlim = float(args['--fold-change-xlim'])
    if args['--distribution-xlim']:
        analysis.distribution_xlim = map(float, args['--distribution-xlim'].split(','))

    with analysis_helpers.plot_or_savefig(
            args['--output'], args['<yml_path>'], args['--inkscape']):
        analysis.plot()

    if args['--export-dataframe']:
        analysis.export_df()
