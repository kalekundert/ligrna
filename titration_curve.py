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
        to normalize by cell size.  By default no normalization is done.

    -N --normalize-by-internal-control
        Normalize by FITC-A (GFP expression) if the channel of interest is 
        PE-Texas Red-A or DsRed-A (RFP expression) and vice versa.  This 
        assumes that the fluorescent protein that isn't of interest is being 
        constitutively expressed, and therefore can be used as an internal 
        control for cell size and expression level.

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

    -m --loc-metric <median|mean|mode>
        Specify which metric should be used to determine the "centers" of the 
        cell distributions for the purpose of calculating the fold change in 
        signal.  By default the median is used for this calculation.  Note that 
        the mean and the mode will both change depending on whether or not the 
        data has been log-transformed (see --log-toggle).  The mode will also 
        change based on how data is histogrammed (see --histogram).

    -y --ylim <ymin,ymax>
        Set the y-axis limits.  By default this axis is automatically scaled to 
        fit the data, but this option is useful is you want to compare 
        different plots.
"""

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
        self.legend_loc = 'upper left'
        self.ylim = None

        self.figure = None
        self.axes = None
        self.y_max = None
        self.y_min = None

    def plot(self):
        self._setup_figure()

        for experiment in self.experiments:
            self._find_concentrations(experiment)
            self._analyze_wells(experiment)
            self._plot_experiment(experiment)

        self._pick_ylim()
        self._pick_labels()

        self.axes.legend(loc=self.legend_loc)
            
    def _setup_figure(self):
        self.figure, self.axes = plt.subplots(1, 1)

        # Don't show that ugly dark grey border around the plot.
        self.figure.patch.set_alpha(0)


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

        # Calculate the "location" of each distribution.  Use very tight limits 
        # to get a reliable value for the mode (if we're using that metric).
        for wells in experiment['wells'].values():
            for well in wells:
                x_min = np.percentile(well.measurements, 10)
                x_max = np.percentile(well.measurements, 90)
                well.estimate_distribution((x_min, x_max))

    def _plot_experiment(self, experiment):
        locs = {
                conc: [float(well.loc) for well in wells]
                for conc, wells in experiment['wells'].items()
        }
        concs = sorted(experiment['wells'].keys())
        means = [mean(locs[x]) for x in concs]
        style = analysis_helpers.pick_style(experiment)

        if experiment['label'] not in ('on', 'off'):
            style.update({'label': experiment['label']})

        self.axes.plot(concs, means, **style)
        self.axes.set_xscale('symlog')
        self.axes.xaxis.set_minor_locator(MinorSymLogLocator())

        min_num_data = min(len(data) for data in locs.values())
        if min_num_data > 1:
            stdevs = [stdev(locs[x]) for x in concs]
            self.axes.errorbar(concs, means, stdevs, **style)

        # Keep track of the lowest and highest data points.
        y_max = max(means)
        y_min = min(means)

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
        apo_wells = [expt['wells'][0][0] for expt in self.experiments]
        channels = {w.channel for w in apo_wells}
        control_channels = {w.control_channel for w in apo_wells}
        log_scales = {w.log_scale for w in apo_wells}

        if len(channels) != 1:
            y_label = 'fluorescence'
        else:
            fluorophores = {'FITC-A': 'GFP', 'Red-A': 'RFP'}
            channel = channels.pop()
            if channel not in fluorophores:
                raise ValueError(f"unexpected channel: {channel}")
            y_label = fluorophores[channel]

        control_channels.discard(None)
        if control_channels:
            y_label = f'normalized {y_label}'

        if len(log_scales) > 1:
            raise ValueError("can't plot multiple log scales")
        if log_scales.pop():
            y_label = 'log({})'.format(y_label)

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
    analysis.normalize_by = args['--normalize-by'] or args['--normalize-by-internal-control']
    analysis.loc_metric = args['--loc-metric']

    with analysis_helpers.plot_or_savefig(args['--output'], args['<yml_path>']):
        analysis.plot()

