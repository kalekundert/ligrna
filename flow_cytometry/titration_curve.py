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
        inches.  The two numbers must be separated by an 'x'.

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

    -M --no-margin
        Don't include any margin around the edge of the figure.  This can make 
        it easier to fit the plot as a panel in a larger figure.

    -I --inkscape
        Create an SVG output file that works well with inkscape by having 
        matplotlib create a PDF, then converting it to SVG in a second step.  
        For some reason the SVG files generated directly by matplotlib cause 
        inkscape to run really slow and chew up a lot of memory.  I played 
        around with one of these files a bit, and I think the problem might 
        have to do with the use of clones.  In any case, generating PDF files 
        and converting them to SVG seems to avoid the problem.

    -v --verbose
        Print out information on all the processing steps.
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
        self.control_channel = None
        self.loc_metric = None
        self.label_filter = None
        self.exclude_label_filter = None
        self.combine_curves = True
        self.legend_loc = 'upper left'
        self.legend = True
        self.output_size = None
        self.ylim = None
        self.margin = True

        self.figure = None
        self.axes = None
        self.y_max = None
        self.y_min = None

    def plot(self):
        self._setup_figure()
        self._filter_experiments()
        self._count_replicates()

        for experiment in self.experiments:
            self._find_concentrations(experiment)

        self._analyze_wells()

        for experiment in self.visible_experiments:
            self._plot_experiment(experiment)

        self._pick_ylim()
        self._pick_labels()

        if self.legend:
            self.axes.legend(loc=self.legend_loc)

        if not self.margin:
            self.figure.tight_layout(pad=0)

            
    def _setup_figure(self):
        self.figure, self.axes = plt.subplots(1, 1, figsize=self.output_size)

        # Don't show that ugly dark grey border around the plot.
        self.figure.patch.set_alpha(0)

        # The y-axis has to be log-scaled because the variation in the data is 
        # proportional to it magnitude.
        self.axes.set_yscale('log')
        self.axes.set_xscale('symlog')
        self.axes.xaxis.set_minor_locator(MinorSymLogLocator())

    def _filter_experiments(self):
        self.visible_experiments = self.experiments[:]

        if self.label_filter is not None:
            label_filter = re.compile(self.label_filter)

            self.visible_experiments = [
                expt for expt in self.visible_experiments
                if label_filter.search(expt['label'])
            ]

        if self.exclude_label_filter is not None:
            label_filter = re.compile(self.exclude_label_filter)

            self.visible_experiments = [
                expt for expt in self.visible_experiments
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

    def _analyze_wells(self):
        analysis_helpers.analyze_wells(
                self.experiments,
                channel=self.channel,
                control_channel=self.control_channel,
                loc_metric=self.loc_metric,
        )

    def _plot_experiment(self, experiment):
        locs = {
                conc: np.array([w.linear_loc for w in wells])
                for conc, wells in experiment['wells'].items()
        }
        concs = sorted(experiment['wells'].keys())
        style = analysis_helpers.pick_style(experiment)

        if experiment['label'] not in ('on', 'off'):
            label = experiment['label']
        else:
            label = ''

        # Fit a logistic curve to the titration
        if True:
            from scipy.optimize import curve_fit

            data = [(x, y) for x, ys in locs.items() for y in ys]
            x_data, y_data = map(np.array, zip(*data))
            log_y_data = np.log10(y_data)

            def logistic_ec50(x, ec50, y_min, y_max): #
                # https://en.wikipedia.org/wiki/EC50
                # https://en.wikipedia.org/wiki/Hill_equation_(biochemistry)
                y = np.empty(x.shape)
                y[x != 0] = y_min + (y_max - y_min) / (1 + (ec50 / x[x != 0]))
                y[x == 0] = y_min
                return y

            def logistic_ec50_inv(y, ec50, y_min, y_max): #
                return ec50 / (((y_max - y_min) / (y - y_min)) - 1)

            initial_guess = 100, min(log_y_data), max(log_y_data)
            bounds = (0, -np.inf, -np.inf), (np.inf, np.inf, np.inf)

            x_fit = np.geomspace(x_data[x_data > 0].min(), x_data.max())
            x_fit = np.concatenate((np.zeros(1), x_fit))

            # Fit to the log of the fluorescence values, since that's really 
            # the scale we're interested in (i.e. we want the EC50 to be the 
            # middle of the curve in log-space, not linear space).
            fit_params, fit_cov = curve_fit(
                    logistic_ec50, x_data, log_y_data,
                    p0=initial_guess, bounds=bounds)

            y_fit = logistic_ec50(x_fit, *fit_params)

            data_style = style.copy()
            data_style['marker'] = '+'
            data_style['linestyle'] = 'none'
            #data_style['markersize'] = np.sqrt(4)

            if label:
                label += f' (EC50={fit_params[0]:.1f}±{np.sqrt(fit_cov[0,0]):.1f} µM)'


            self.axes.plot(x_data, y_data, label='_nolegend_', **data_style)
            self.axes.plot(x_fit, 10**y_fit, label=label, **style)

            y_max = np.amax(y_data)
            y_min = np.amin(y_data)

        # Draw a single line with error bars.
        elif self.combine_curves and self.num_replicates > 1:
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
            padding = 1 + 1e-3 * (self.y_max / self.y_min)
            self.axes.set_ylim(self.y_min / padding, self.y_max * padding)

    def _pick_labels(self):
        # Decide which ligand to label.
        ligand = analysis_helpers.get_ligand(self.visible_experiments)

        # Decide which unit to label.
        units = {expt.get('unit', '') for expt in self.visible_experiments}
        if len(units) > 1:
            raise ValueError(f"multiple units {units} specified in yaml file.")
        unit = units.pop()

        # Decide how to label the y-axes
        y_label = analysis_helpers.get_channel_label(self.visible_experiments)

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

    shared_steps = analysis_helpers.SharedProcessingSteps(args['--verbose'])
    shared_steps.early_event_threshold = float(args['--time-gate'])
    shared_steps.small_cell_threshold = float(args['--size-gate'])
    shared_steps.low_fluorescence_threshold = float(args['--expression-gate'])
    shared_steps.process(experiments)

    analysis = TitrationCurve(experiments)
    analysis.channel = args['--channel']
    analysis.control_channel = args['--normalize-by'] or not args['--no-normalize']
    analysis.loc_metric = args['--loc-metric']
    analysis.label_filter = args['--query']
    analysis.exclude_label_filter = args['--exclude-query']
    analysis.combine_curves = args['--combine-curves']
    analysis.legend = not args['--no-legend']
    analysis.margin = not args['--no-margin']

    if args['--output-size']:
        analysis.output_size = [float(x) for x in args['--output-size'].split('x')]

    with analysis_helpers.plot_or_savefig(
            args['--output'], args['<yml_path>'], args['--inkscape']):
        analysis.plot()

