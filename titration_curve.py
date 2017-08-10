#!/usr/bin/env python3

"""\
Show the changes between populations of cells in different conditions.

Usage:
    titration_curve.py <yml_path> [options]

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

    -O --output-size <width,height>
        Specify what the width and height of the resulting figure should be, in 
        inches.  The two numbers must be separated by a comma.

    -c --channel <channel>
        The channel to plot.  By default, this is deduced from the YAML file.  
        If an experiment has a 'channel' attribute, that channel is displayed.  
        Otherwise, a default channel may be chosen based on the name of the 
        experiment.  It is an error if no channel is specified and no channel 
        can be deduced.

    -n --normalize-by <channel>
        Normalize the channel of interest (see --channel) by the given channel.
        For example, you might specify "FSC-A", "SSC-A", or "FSC-A + m * SSC-A" 
        to normalize by cell size.  By default the data is normalized by GFP-A 
        (GFP expression) if the channel of interest is PE-Texas Red-A or 
        DsRed-A (RFP expression) and vice versa.

    -N --no-normalize
        Show raw, unnormalized data.

    -q --query <regex>
        Only show experiments if their label matches the given regular 
        expression.  This option is meant to help show interesting subsets of 
        really high throughput experiments.

    -Q --exclude-query <regex>
        Only show experiments if their label *doesn't* match the given regular 
        expression.  This option is meant to help show interesting subsets of 
        really high throughput experiments.

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

    -m --loc-metric <median|mean|mode>
        Specify which metric should be used to determine the "centers" of the 
        cell distributions for the purpose of calculating the fold change in 
        signal.  By default the mode is used for this calculation.

    -B --no-baseline
        Don't normalize the curves by the average fluorescence values of the 
        negative control.  The processing normally helps iron out slight 
        variations in the relative levels of GFP and RFP between experiments.

    -1 --combine-curves
        Combine all the replicates for each titration into a single line with 
        error bars.  The default is to show a separate line for each replicate.

    -y --ylim <ymin,ymax>
        Set the y-axis limits.  By default this axis is automatically scaled to 
        fit the data, but this option is useful is you want to compare 
        different plots.

    -L --no-legend
        Don't include a legend in the plot.  This might be useful if the legend 
        is covering something up (and the colors of the lines are clear enough) 
        or if you're preparing a figure for a paper.
"""

import re
import fcmcmp, analysis_helpers, nonstdlib
import numpy as np, matplotlib.pyplot as plt
from matplotlib.ticker import Locator
from statistics import mean, stdev
from pprint import pprint

class TitrationCurve:

    def __init__(self, experiments):
        self.experiments = experiments
        self.channel = None
        self.normalize_by = None
        self.loc_metric = None
        self.label_filter = None
        self.exclude_label_filter = None
        self.combine_curves = True
        self.legend_loc = 'upper left'
        self.legend = True
        self.output_size = None
        self.baseline_expt = 'off'
        self.apply_baseline = True
        self.ylim = None

        self.figure = None
        self.axes = None
        self.baseline = None
        self.y_max = None
        self.y_min = None

    def plot(self):
        self._setup_figure()
        self._filter_experiments()
        self._count_replicates()

        for experiment in self.experiments:
            self._find_concentrations(experiment)
            self._analyze_wells(experiment)

        self._find_baseline()

        for experiment in self.experiments:
            self._plot_experiment(experiment)

        self._pick_ylim()
        self._pick_labels()

        if self.legend:
            self.axes.legend(loc=self.legend_loc)
            
    def _setup_figure(self):
        self.figure, self.axes = plt.subplots(1, 1, figsize=self.output_size)

        # Don't show that ugly dark grey border around the plot.
        self.figure.patch.set_alpha(0)

        self.axes.set_yscale('log')
        self.axes.set_xscale('symlog')
        self.axes.xaxis.set_minor_locator(MinorSymLogLocator())

    def _filter_experiments(self):
        if self.label_filter is not None:
            label_filter = re.compile(self.label_filter)

            self.experiments = [
                expt for expt in self.experiments
                if label_filter.search(expt['label'])
            ]

        if self.exclude_label_filter is not None:
            label_filter = re.compile(self.exclude_label_filter)

            self.experiments = [
                expt for expt in self.experiments
                if not label_filter.search(expt['label'])
            ]

    def _count_replicates(self):
        # If there are replicates, make sure each one has data for every 
        # concentration of ligand.  If data is missing, there's no way to tell 
        # which replicate it's missing from (this is a shortcoming of the 
        # `fcmcmp` file format).

        replicates = set(
            len(expt['wells'][conc])
            for expt in self.experiments
            for conc in expt['wells']
        )

        if len(replicates) != 1:
            raise ValueError(f"Inconsistent number of replicates for the '{experiment['label']}' experiment.")

        self.num_replicates = replicates.pop()

    def _find_concentrations(self, experiment):

        def conc_from_label(label):
            from numbers import Real
            if label == 'apo': return 0
            if isinstance(label, Real): return label
            return eval(label)

        experiment['wells'] = {
                conc_from_label(k): v
                for k, v in experiment['wells'].items()
        }

        if 0 not in experiment['wells']:
            raise ValueError("no apo well for '{}' experiment".format(experiment['label']))

    def _analyze_wells(self, experiment):
        experiment['wells'] = {
                conc: [
                    analysis_helpers.AnalyzedWell(
                        experiment, well,
                        channel=self.channel,
                        normalize_by=self.normalize_by,
                        loc_metric=self.loc_metric,
                    )
                    for well in wells
                ]
                for conc, wells in experiment['wells'].items()
        }

    def _find_baseline(self):
        if not self.apply_baseline:
            self.baseline = np.ones([self.num_replicates])

        else:
            expt_map = {x['label']: x for x in self.experiments}
            baseline_expt = expt_map[self.baseline_expt]

            self.baseline = np.array([
                np.mean([
                    baseline_expt['wells'][conc][i].linear_loc
                    for conc in baseline_expt['wells']
                ])
                for i in range(self.num_replicates)
            ])

    def _plot_experiment(self, experiment):
        locs = {
                conc: np.array([w.linear_loc for w in wells]) / self.baseline
                for conc, wells in experiment['wells'].items()
        }
        concs = sorted(experiment['wells'].keys())
        style = analysis_helpers.pick_style(experiment)

        if experiment['label'] not in ('on', 'off'):
            label = experiment['label']
        else:
            label = ''

        # Draw a single line with error bars.
        if self.combine_curves and self.num_replicates > 1:
            means = np.array([mean(locs[x]) for x in concs])
            errors = np.array([stdev(locs[x]) for x in concs])

            self.axes.errorbar(concs, means, errors, label=label, **style)

            y_max = np.amax(np.amax(means + errors))
            y_min = np.amin(np.amin(means - errors))

        # Draw separate lines for each titration.
        else:
            series = np.array([locs[x] for x in concs]).T

            for i in range(self.num_replicates):
                label_once = label if i == 0 else ''
                self.axes.plot(concs, series[i], label=label_once, **style)

            y_max = np.amax(series)
            y_min = np.amin(series)

        self.y_max = max(y_max, self.y_max or y_max)
        self.y_min = min(y_min, self.y_min or y_min)

    def _pick_ylim(self):
        if self.ylim:
            self.axes.set_ylim(self.ylim)
        else:
            padding = 0.05 * (self.y_max - self.y_min)
            self.axes.set_ylim(self.y_min - padding, self.y_max + padding)

    def _pick_labels(self):
        # Decide which ligand to label.
        ligand = analysis_helpers.get_ligand(self.experiments)

        # Decide which unit to label.
        units = {expt.get('unit', '') for expt in self.experiments}
        if len(units) > 1:
            raise ValueError(f"multiple units {units} specified in yaml file.")
        unit = units.pop()

        # Decide how to label the y-axes
        y_label = analysis_helpers.get_channel_label(self.experiments)
        if self.apply_baseline:
            y_label += ' [relative to max]'

        self.axes.set_xlabel(f'{ligand} [{unit}]')
        self.axes.set_ylabel(y_label)


class MinorSymLogLocator(Locator):
    """
    Dynamically find minor tick positions based on the positions of
    major ticks for a symlog scaling.

    From David Zwicker:
    http://stackoverflow.com/questions/20470892/how-to-place-minor-ticks-on-symlog-scale
    """
    def __init__(self, linthresh=1.0):
        """
        Ticks will be placed between the major ticks.
        The placement is linear for x between -linthresh and linthresh,
        otherwise its logarithmically
        """
        self.linthresh = linthresh

    def __call__(self):
        'Return the locations of the ticks'
        majorlocs = self.axis.get_majorticklocs()

        # iterate through minor locs
        minorlocs = []

        # handle the lowest part
        for i in range(1, len(majorlocs)):
            majorstep = majorlocs[i] - majorlocs[i-1]
            if abs(majorlocs[i-1] + majorstep/2) < self.linthresh:
                ndivs = 10
            else:
                ndivs = 9
            minorstep = majorstep / ndivs
            locs = np.arange(majorlocs[i-1], majorlocs[i], minorstep)[1:]
            minorlocs.extend(locs)

        return self.raise_if_exceeds(np.array(minorlocs))

    def tick_values(self, vmin, vmax):
        raise NotImplementedError('Cannot get tick locations for a '
                                  '%s type.' % type(self))



if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)
    experiments = fcmcmp.load_experiments(args['<yml_path>'])

    shared_steps = analysis_helpers.SharedProcessingSteps()
    shared_steps.early_event_threshold = float(args['--time-gate'])
    shared_steps.small_cell_threshold = float(args['--size-gate'])
    shared_steps.low_fluorescence_threshold = float(args['--expression-gate'])
    shared_steps.process(experiments)

    analysis = TitrationCurve(experiments)
    analysis.channel = args['--channel']
    analysis.normalize_by = args['--normalize-by'] or not args['--no-normalize']
    analysis.loc_metric = args['--loc-metric']
    analysis.apply_baseline = not args['--no-baseline']
    analysis.label_filter = args['--query']
    analysis.exclude_label_filter = args['--exclude-query']
    analysis.combine_curves = args['--combine-curves']
    analysis.legend = not args['--no-legend']

    if args['--output-size']:
        analysis.output_size = map(float, args['--output-size'].split('x'))

    with analysis_helpers.plot_or_savefig(args['--output'], args['<yml_path>']):
        analysis.plot()

