#!/usr/bin/env python3

"""\
Plot fluorescence values for different populations of cells.  This is a more 
compact representation of the same information plotted by `fold_change.py`.

Usage:
    bar_chart.py <yml_path> [options]

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
        to normalize by cell size.  By default the data is normalized by GFP-A 
        (GFP expression) if the channel of interest is PE-Texas Red-A or 
        DsRed-A (RFP expression) and vice versa.

    -N --no-normalize
        Show raw, unnormalized data.

    -y --ylim <signal>
        The maximum extent of the vertical axis.  This is set from the data by 
        default, but this option is useful if you want plots from two different 
        invocations to line up.

    -q --query <regex>
        Only show experiments if their label matches the given regular 
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
        signal.  By default the mode is used for this calculation.  Note that 
        the mean and the mode will both change depending on whether or not the 
        data has been log-transformed (see --log-toggle).

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
import fcmcmp
import analysis_helpers
import numpy as np
import matplotlib.pyplot as plt

from pprint import pprint
from sgrna_sensor.style import pick_color, pick_dot_colors

class BarChart:

    def __init__(self, experiments):
        # User controlled parameters:
        self.experiments = experiments
        self.title = None
        self.output_size = None
        self.channel = None
        self.control_channel = None
        self.loc_metric = None
        self.label_filter = None
        self.ylim = None
        self.verbose = False

        # Internal plot parameters:
        self.figure = None
        self.axis = None
        self.bar_width = 6
        self.experiment_padding = 2
        self.condition_padding = 1

    def plot(self, figure=None, axis=None):
        """
        Create the bar chart and return the resulting figure.
        """
        self._setup_figure(figure, axis)
        self._setup_axes()

        self._analyze_wells()
        self._filter_wells()
        self._plot_experiments()

        self.figure.tight_layout()

    def _setup_figure(self, figure=None, axes=None):
        # Make a figure if were weren't given one.
        if figure is not None:
            self.figure = figure
            self.axes = axes
        else:
            print(self.output_size)
            self.figure, self.axes = plt.subplots(
                    1, 1,
                    figsize=self.output_size,
            )

        # Don't show that ugly dark grey border around the plot.
        self.figure.patch.set_alpha(0)

        # Set the figure title, if we have one.
        if self.title:
            self.figure.suptitle(self.title)

    def _setup_axes(self):
        # Initially I was using a log-scale on the y-axis:
        # 
        #   self.axes.set_yscale('log')
        # 
        # I now think a log scale is inappropriate because the bottom of the 
        # bars will just be the nearest major tick.  If I plot RFP and GFP data 
        # side-by-side, the bars could be dramatically different heights.
        #
        # Obviously on a log scale it's the difference between the tops of the 
        # bars that really matters, but big differences in height will still 
        # draw peoples' eyes to the wrong things.
        pass

    def _analyze_wells(self):
        analysis_helpers.analyze_wells(
                self.experiments,
                channel=self.channel,
                control_channel=self.control_channel,
                loc_metric=self.loc_metric,
        )

    def _filter_wells(self):
        # Filter out experiments with labels that don't match the user given
        # regular expression.
        if self.label_filter is not None:
            label_filter = re.compile(self.label_filter)
            self.experiments = [
                x for x in self.experiments
                if label_filter.search(x['label'])
            ]

    def _plot_experiments(self):
        self.x_ticks = []
        self.x_tick_labels = []

        x = 0
        for experiment in self.experiments:
            x = self._plot_experiment(x, experiment)
            x += self.experiment_padding

        self.axes.set_xlim(-self.experiment_padding, x-self.condition_padding)
        self.axes.set_xticks(self.x_ticks)
        self.axes.set_xticklabels(self.x_tick_labels, 
                rotation='vertical', fontsize=10)

        channel = analysis_helpers.get_channel_label(self.experiments)
        self.axes.set_ylabel(channel)
        if self.ylim:
            self.axes.set_ylim(0, self.ylim)

        self.axes.tick_params(axis='x', which='both',length=0)

    def _plot_experiment(self, x, experiment):
        """
        Make a tightly-spaced cluster of bars for all the conditions in the 
        given experiment.  Keep more space between this experiment and the 
        next.
        """
        x0 = x
        for j, condition in enumerate(experiment['wells']):
            wells = experiment['wells'][condition]
            self._plot_condition(x, experiment, condition, wells)
            x += self.condition_padding

        # Add the experiment label below the individual bar labels.

        import matplotlib.transforms as transforms

        label_x = (x0 + x -self.condition_padding) / 2  # data coords
        label_y =  1.01                                 # axes coords

        self.axes.text(
                label_x, label_y, experiment['label'],
                horizontalalignment='center',
                transform=transforms.blended_transform_factory(
                    self.axes.transData, self.axes.transAxes),
        )

        return x

    def _plot_condition(self, x, experiment, condition, wells):
        # Plot the fluorescence data.

        ys = np.array([x.linear_loc for x in wells])
        xs = np.full(ys.shape, x)
        y = np.mean(ys)
        err = np.std(ys)

        label = experiment.get('family', experiment['label']).lower()
        bar_color = pick_color(label)
        dot_colors = pick_dot_colors(label, ys)

        self.axes.plot(
                [x,x], [0,y],
                color=bar_color,
                linewidth=self.bar_width,
                solid_capstyle='butt',
                zorder=1,
        )
        self.axes.scatter(
                xs, ys,
                c=dot_colors,
                marker='+',
                zorder=2,
        )

        #self.axes.errorbar(
        #        x, y, yerr=err,
        #        ecolor=color,
        #        capsize=self.bar_width / 2,
        #)

        # Label the axis.

        self.x_ticks.append(x)
        self.x_tick_labels.append(condition)



if __name__ == '__main__':
    import docopt

    args = docopt.docopt(__doc__)
    experiments = fcmcmp.load_experiments(args['<yml_path>'])

    shared_steps = analysis_helpers.SharedProcessingSteps(args['--verbose'])
    shared_steps.early_event_threshold = float(args['--time-gate'])
    shared_steps.small_cell_threshold = float(args['--size-gate'])
    shared_steps.low_fluorescence_threshold = float(args['--expression-gate'])
    shared_steps.process(experiments)

    analysis = BarChart(experiments)
    analysis.title = args['--title']
    analysis.channel = args['--channel']
    analysis.control_channel = args['--normalize-by'] or not args['--no-normalize']
    analysis.loc_metric = args['--loc-metric']
    analysis.label_filter = args['--query']
    analysis.verbose = args['--verbose']

    if args['--output-size']:
        analysis.output_size = tuple(map(float, args['--output-size'].split('x')))
    if args['--ylim']:
        analysis.ylim = float(args['--ylim'])

    with analysis_helpers.plot_or_savefig(
            args['--output'], args['<yml_path>'], args['--inkscape']):
        analysis.plot()

