#!/usr/bin/env python3

import re, contextlib, fcmcmp
import numpy as np, matplotlib.pyplot as plt
import warnings; warnings.simplefilter("error", FutureWarning)
from pprint import pprint

plt.rcParams['font.family'] = 'Liberation Sans'

class AnalyzedWell(fcmcmp.Well):

    def __init__(self, experiment, well, channel=None, normalize_by=None, 
            log_scale=None, log_toggle=False, pdf=False, loc_metric='median', 
            num_samples=None):

        super().__init__(well.label, well.meta, well.data)

        self.experiment = experiment
        self.channel_override = channel
        self.normalize_by = normalize_by
        self.log_scale = log_scale
        self.log_toggle = log_toggle
        self.calc_pdf = pdf
        self.loc_metric = loc_metric
        self.num_samples = num_samples

        self.measurements = None
        self.linear_measurements = None
        self.log_measurements = None
        self.unnormalized_linear_measurements = None
        self.unnormalized_log_measurements = None
        self.normalized_linear_measurements = None
        self.normalized_log_measurements = None
        self.kde = None
        self.channel = None
        self.control_channel = None
        self.x = self.y = None
        self.mean = None
        self.median = None
        self.mode = None
        self.loc = None
        self.linear_loc = None

        self._find_measurements()
        self._find_locations()

    def estimate_distribution(self, axes_or_xlim=(1,5)):
        if isinstance(axes_or_xlim, plt.Axes):
            xlim = axes_or_xlim.get_xlim()
        else:
            xlim = axes_or_xlim

        self._find_distribution(xlim)

    def _find_measurements(self):
        # Pick the channel to display based on what the user asked for, or the 
        # properties of the experiment if nothing was asked for.
        self.channel = pick_channel(self.experiment, self.channel_override)

        # Pick the channel that will be used to normalize the data.
        self.control_channel = pick_control_channel(
                self.experiment, self.channel, self.normalize_by)

        # Decide whether or not the data should be presented on a log-axis. 
        if self.log_scale is None:
            self.log_scale = is_fluorescent_channel(self.channel)
            if self.log_toggle:
                self.log_scale = not self.log_scale

        # Save the measurements, from the appropriate channel, with the 
        # appropriate normalization, and on the appropriate scale.
        self.linear_measurements = self.unnormalized_linear_measurements = self.data[self.channel]
        self.log_measurements = self.unnormalized_log_measurements = np.log10(self.linear_measurements)

        if self.control_channel is not None:
            self.linear_measurements = self.normalized_linear_measurements = self.unnormalized_linear_measurements / self.data[self.control_channel]
            self.log_measurements = self.normalized_log_measurements = np.log10(self.normalized_linear_measurements)

        self.measurements = self.log_measurements if self.log_scale else self.linear_measurements

    def _find_locations(self):
        # Calculate the median, mean, and mode of the data.  The advantage of 
        # the median is that it's unaffected by whether or not the data has 
        # been log-transformed.  The advantage of the mode is that it's 
        # unaffected by the shoulders that seem to be caused by intermittent 
        # plasmid loss.
        self.median = np.median(self.measurements)
        self.mean = np.mean(self.measurements)

        # Calculate the mode by finding the maximum of the Gaussian kernel 
        # density estimate (KDE) of the measured cell population.  We use the 
        # default scipy optimization algorithm (which at this time is BFGS) to 
        # find the maximum as accurately and as quickly as possible.
        if self.measurements.empty:
            raise ValueError("no measurements for {}, well {}".format(self.experiment['label'], self.well.label))

        from scipy.optimize import minimize
        self.kde = CachedGaussianKde(self.measurements)
        result = minimize(self.kde.objective, self.median)
        self.mode = result.x

        # Store the "location" (i.e. median, mean or mode) that the user wants 
        # to use to calculate fold change.  The default is the mode.
        if self.loc_metric == 'median':
            self.loc = self.median
        elif self.loc_metric == 'mean':
            self.loc = self.mean
        elif self.loc_metric == 'mode' or self.loc_metric is None:
            self.loc = self.mode
        else:
            raise ValueError("No such metric '{}'".format(self.loc_metric))

        self.linear_loc = 10**self.loc if self.log_scale else self.loc
        self.log_loc = self.loc if self.log_scale else np.log10(self.loc)

    def _find_distribution(self, xlim):
        # Evaluate the Gaussian KDE across the whole x-axis for visualization 
        # purposes.  Because each evaluation of the KDE is relatively expensive 
        # and we want the plot to be nice and smooth, we focus most of the 
        # evaluations in a narrow range (30% of the x-axis) around the mode.  
        # The points that were evaluated in the calculation of the mode are 
        # also included in the plot.
        n = self.num_samples or 100
        n_dense = int(0.7 * n)
        n_sparse = n - n_dense
        dx = 0.20 * (xlim[1] - xlim[0])
        x_dense = np.linspace(self.mode - dx, self.mode + dx, num=n_dense)
        x_sparse = np.linspace(*xlim, num=n_sparse)

        self.kde.evaluate(x_dense)
        self.kde.evaluate(x_sparse)
        self.x, self.y = self.kde.xy

        # Scale the distribution to make it's area meaningful.  By default, the 
        # area will be proportional to the amount of data.  If the user wants 
        # the data presented as a PDF, the area is set to unity.
        self.y /= np.trapz(self.y, self.x)
        if not self.calc_pdf:
            self.y *= len(self.measurements)


def analyze_wells(experiments, **kwargs):
    for experiment in experiments:
        for condition in experiment['wells']:
            experiment['wells'][condition] = [
                    AnalyzedWell(experiment, well, **kwargs)
                    for well in experiment['wells'][condition]
            ]

def yield_related_wells(experiments, default_reference='apo'):

    class RelatedWells:

        def __init__(self, experiment, condition, reference, i):
            self.experiment = experiment
            self.label = experiment['label']
            self.condition = condition
            self.condition_wells = experiment['wells'][condition]
            self.reference = reference
            self.reference_wells = experiment['wells'][reference]
            self.solo = len(experiment['wells']) == 2
            self.i = i


    i = 0
    for experiment in experiments:
        reference = experiment.get('reference', default_reference)
        for condition in experiment['wells']:
            if condition == reference: continue
            yield RelatedWells(experiment, condition, reference, i)
            i += 1
    
class CachedGaussianKde:

    def __init__(self, measurements):
        from scipy.stats import gaussian_kde
        self.kernel = gaussian_kde(measurements)
        self.memo = {}

    def evaluate(self, x):
        y = self.kernel.evaluate(x)
        for i, _ in np.ndenumerate(x):
            self.memo[x[i]] = y[i]
        return y

    def objective(self, x):
        return -self.evaluate(x)

    @property
    def xy(self):
        k, v = map(np.array, zip(*self.memo.items()))
        i = np.argsort(k)
        return k[i], v[i]


class GateLowFluorescence(fcmcmp.GatingStep):

    def __init__(self, threshold=1e3):
        self.threshold = threshold

    def gate(self, experiment, well):
        channel = pick_channel(experiment)
        control_channel = pick_control_channel(experiment, channel)
        if control_channel in well.data.columns:
            return well.data[control_channel] < self.threshold


class RenameRedChannel(fcmcmp.ProcessingStep):
    """
    I use different red channels on different cytometers.  In particular, I use 
    the "PE-Texas Red" channel on the BD LSRII and the "DsRed" channel on the 
    BD FACSAriaII.  To allow my scripts to work on data from either machine, I 
    rename the red channel to "Red".  I have to be slightly careful because 
    some of my data from the FACSAriaII also has data in the "PE-Texas Red" 
    channel, so the "DsRed" channel has to take priority if both are present.
    """

    def process_well(self, experiment, well):
        if 'DsRed-A' in well.data.columns:
            red_channel = 'DsRed-A'
        elif 'PE-Texas Red-A' in well.data.columns:
            red_channel = 'PE-Texas Red-A'
        elif 'mCherry-A' in well.data.columns:
            red_channel = 'mCherry-A'
        else:
            return

        well.data.rename(columns={red_channel: 'Red-A'}, inplace=True)


class SharedProcessingSteps:

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.early_event_threshold = 0
        self.small_cell_threshold = 0
        self.low_fluorescence_threshold = 1e3

    def process(self, experiments):
        rename_red_channel = RenameRedChannel()
        rename_red_channel.verbose = self.verbose
        rename_red_channel(experiments)

        gate_nonpositive_events = fcmcmp.GateNonPositiveEvents()
        gate_nonpositive_events.verbose = self.verbose
        gate_nonpositive_events(experiments)

        gate_early_events = fcmcmp.GateEarlyEvents()
        gate_early_events.throwaway_secs = self.early_event_threshold
        gate_early_events.verbose = self.verbose
        gate_early_events(experiments)

        gate_small_cells = fcmcmp.GateSmallCells()
        gate_small_cells.save_size_col = True
        gate_small_cells.threshold = self.small_cell_threshold
        gate_small_cells.verbose = self.verbose
        gate_small_cells(experiments)

        gate_low_fluorescence = GateLowFluorescence()
        gate_low_fluorescence.threshold = self.low_fluorescence_threshold
        gate_low_fluorescence.verbose = self.verbose
        gate_low_fluorescence(experiments)


class ExperimentPlot:
    """
    Create a grid of shared axes, with one axis for each well in a single 
    experiment.  Provide a few helper functions relating to that grid, such as 
    setting the titles and converting row and column indices into wells and 
    conditions.
    """

    def __init__(self, experiment):
        # Settings configured by the user.
        self.experiment = experiment

        # Internally used plot attributes.
        self.figure = None
        self.axes = None
        self.num_rows = None
        self.num_cols = None

    def plot(self):
        raise NotImplementedError

    def _create_axes(self, square=False):
        """
        Work out how many wells need to be shown.  There will be a column for 
        each well and row for each condition.
        """
        self.num_rows = len(self.experiment['wells'])
        self.num_cols = max(
                len(self.experiment['wells'][cond])
                for cond in self.experiment['wells'])

        # The 'squeeze=False' argument guarantees that the returned axes are 
        # always a 2D array, even if one of the dimensions happens to be 1.

        self.figure, self.axes = plt.subplots(
                self.num_rows, self.num_cols,
                sharex=True, sharey=True, squeeze=False,
        )
        
        # Don't show that ugly dark grey border around the plot.
        self.figure.patch.set_alpha(0)

        # Make the axes square if the user asked for it.  What this really 
        # means is that pixels on the x-axis and the y-axis will have the same 
        # size in axis units.  This relationship is maintained even as the user 
        # zooms in and out.

        if square:
            for ax in self.axes.flat:
                ax.set(adjustable='box-forced', aspect='equal')

    def _set_titles(self):
        """
        Label each plot with the name of the experiment, the condition, and the 
        replicate number.
        """
        self.figure.suptitle(self.experiment['label'], size=14)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                well = self._get_well(row, col)
                condition = self._get_condition(row)
                title = '{} ({})'.format(condition, well.label)
                self.axes[row, col].set_title(title, size=12)

    def _set_labels(self, x_label, y_label):
        for ax in self.axes[-1,:]:
            ax.set_xlabel(x_label)
        for ax in self.axes[:,0]:
            ax.set_ylabel(y_label)

    def _get_rows_cols(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                yield row, col

    def _get_condition(self, row):
        return list(self.experiment['wells'].keys())[row]

    def _get_well(self, row, col):
        return self.experiment['wells'][self._get_condition(row)][col]



def pick_color(experiment, lightness=0):
    """
    Pick a color for the given experiment.

    The return value is a hex string suitable for use with matplotlib.
    """
    if 'color' in experiment:
        return experiment['color'] if lightness == 0 else '#dddddd'
    else:
        return pick_ucsf_color(experiment, lightness)


p = r'\b(%s)(\b|[(])'
control = re.compile(p % '[w]?(on|off|wt|dead)')
upper_stem = re.compile(p % 'us|.u.?')
lower_stem = re.compile(p % 'ls|.l.?')
bulge = re.compile(p % '.b.?')
nexus = re.compile(p % 'nx|.x.?|[wm]11')
hairpin = re.compile(p % '.h.?')

def pick_tango_color(experiment, lightness=0):
    """
    Pick a color from the Tango color scheme for the given experiment.

    The Tango color scheme is best known for being the basis of GTK icons, 
    which are used heavily on Linux systems.  The colors are bright, and the 
    scheme includes a few tints of each color.
    """

    white, black = '#ffffff', '#000000'
    grey = '#eeeeec', '#d3d7cf', '#babdb6', '#888a85', '#555753', '#2e3436'
    red =    '#ef2929', '#cc0000', '#a40000'
    orange = '#fcaf3e', '#f57900', '#ce5c00'
    yellow = '#fce94f', '#edd400', '#c4a000'
    green =  '#8ae234', '#73d216', '#4e9a06'
    blue =   '#729fcf', '#3465a4', '#204a87'
    purple = '#ad7fa8', '#75507b', '#5c3566'
    brown =  '#e9b96e', '#c17d11', '#8f5902'

    i = lambda x: max(x - lightness, 0)

    if 'rfp' in experiment['label'].lower():
        return red[i(1)]
    elif 'gfp' in experiment['label'].lower():
        return green[i(2)]
    elif control.search(experiment['label']):
        return grey[i(4)]
    elif lower_stem.search(experiment['label']):
        return purple[i(1)]
    elif upper_stem.search(experiment['label']):
        return blue[i(1)]
    elif bulge.search(experiment['label']):
        return green[i(1)]
    elif nexus.search(experiment['label']):
        return red[i(1)]
    elif hairpin.search(experiment['label']):
        return orange[i(1)]
    else:
        return brown[i(2)]

def pick_ucsf_color(experiment, lightness=0):
    """
    Pick a color from the official UCSF color scheme for the given experiment.

    The UCSF color scheme is based on primary teal and dark blue colors and is 
    accented by a variety of bright -- but still somewhat subdued -- colors.  
    The scheme includes tints of every color, but not shades.
    """

    navy = ['#002049', '#506380', '#9ba6b6', '#e6e9ed']
    teal = ['#18a3ac', '#5dbfc5', '#a3dade', '#e8f6f7'] 
    olive = ['#90bd31', '#b1d16f', '#d3e4ad', '#f4f8ea'] 
    blue = ['#178ccb', '#5dafdb', '#a2d1ea', '#e8f4fa'] 
    orange = ['#f48024', '#f7a665', '#fbcca7', '#fef2e9'] 
    purple = ['#716fb2', '#9c9ac9', '#c6c5e0', '#f1f1f7'] 
    red = ['#ec1848', '#f25d7f', '#f7a3b6', '#fde8ed'] 
    yellow = ['#ffdd00', '#ffe74d', '#fff199', '#fffce6'] 
    black = ['#000000', '#4d4d4d', '#999999', '#ffffff'] 
    dark_grey = ['#b4b9bf', '#cbced2', '#e1e3e6', '#f8f8f9']
    light_grey = ['#d1d3d3', '#dfe0e0', '#ededee', '#fafbfb'] 

    i = lambda x: min(x + lightness, 3)
    label = experiment.get('family', experiment['label']).lower()

    if 'rfp' in label:
        return red[i(0)]
    elif 'gfp' in label:
        return olive[i(0)]
    elif control.search(label):
        return light_grey[i(0)]
    elif lower_stem.search(label):
        return olive[i(0)]
    elif upper_stem.search(label):
        return olive[i(0)]
    elif bulge.search(label):
        return olive[i(0)]
    elif nexus.search(label):
        return red[i(0)]
    elif hairpin.search(label):
        return blue[i(0)]
    else:
        return navy[i(0)]

def pick_style(experiment, is_reference=False):
    if is_reference:
        return {
                'color': 'black',
                'dashes': [5,2],
                'linewidth': 1,
                'zorder': 1,
        }
    else:
        return {
                'color': pick_color(experiment),
                'linestyle': '-',
                'linewidth': 1,
                'zorder': 2,
        }

def pick_channel(experiment, users_choice=None):
    """
    Pick a channel for the given experiment.

    The channel can either be set directly by the user (typically via the 
    command line) or can be inferred from the name of the experiment.  If 
    nothing else is specified, it will default to the "Red-A" channel.
    """
    # If the user manually specified a channel to view, use it.
    if users_choice:
        return users_choice

    # If a particular channel is associated with this experiment, use it.
    if 'channel' in experiment:
        channel = experiment['channel']
        if channel in ('PE-Texas Red-A', 'DsRed-A'):
            return 'Red-A'
        else:
            return channel

    # If the experiment specifies a spacer, use the corresponding channel.
    if 'spacer' in experiment:
        if 'gfp' in experiment['spacer']:
            return 'FITC-A'
        if 'rfp' in experiment['spacer']:
            return 'Red-A'

    # If a channel can be inferred from the name of the experiment, use it. 
    if 'gfp' in experiment['label'].lower():
        return 'FITC-A'
    if 'rfp' in experiment['label'].lower():
        return 'Red-A'

    # Default to the red channel, if nothing else is specified.
    return 'Red-A'

def pick_control_channel(experiment, channel, users_choice=None):
    # If the user didn't specify a normalization, see if there's a default 
    # associated with the experiment.
    if users_choice is None:
        users_choice = experiment.get('normalize_by')

    # If normalization is requested but no particular channel is given, try to 
    # find a default fluorescent control channel.
    if users_choice is True:
        species = experiment.get('species', 'E. coli')
        size_controls = {
                'e. coli': {
                    'FITC-A': 'Red-A',
                    'Red-A': 'FITC-A', 
                },
                's. cerevisiae': {
                    'FITC-A': 'SSC-A',
                    'Red-A': 'SSC-A',
                }
        }
        try:
            return size_controls[species.lower()][channel]
        except KeyError:
            raise fcmcmp.UsageError("No default control channel for '{}' in {}".format(channel, species))

    # If no normalization is requested, don't set a control channel.
    elif not users_choice:
        return None

    # If the user manually specifies a channel to normalize with, use it.
    else:
        return users_choice

def get_channel_label(experiments):
    channels = set(x.channel for _, _, x in fcmcmp.yield_wells(experiments))
    control_channels = set(x.control_channel for _, _, x in fcmcmp.yield_wells(experiments))
    control_channels.discard(None)

    channel_labels = {
            'FSC-A': 'FSC',
            'SSC-A': 'SSC',
            'FITC-A': 'GFP',
            'Red-A': 'RFP',
    }

    if len(channels) == 1:
        channel = next(iter(channels))
        label = channel_labels[channel]
    elif channels.issubset(fluorescence_controls):
        label = 'fluorescence'
    elif channels.issubset(['FSC-A', 'SSC-A']):
        label = 'size'
    else:
        raise ValueError("inconsistent channels: {}".format(','.join(channels)))

    if len(control_channels) == 1:
        channel = next(iter(control_channels))
        label = '{} / {}'.format(label, channel_labels[channel])
    elif len(control_channels) > 1:
        label = 'normalized {}'.format(label)

    return label

def get_ligand(experiments):
    ligands = {expt.get('ligand', 'ligand') for expt in experiments}
    return ligands.pop() if len(ligands) == 1 else 'ligand'

def get_duration(experiments):
    min_time = float('inf')
    max_time = -float('inf')

    for experiment in experiments:
        for condition in experiment['wells']:
            for well in experiment['wells'][condition]:
                dt = float(well.meta['$TIMESTEP'])
                min_time = min(min_time, min(well.data['Time'] * dt))
                max_time = max(max_time, max(well.data['Time'] * dt))

    return min_time, max_time

def is_fluorescent_channel(channel):
    return any(
            channel.startswith(x)
            for x in ['FITC', 'Red']
    )

@contextlib.contextmanager
def plot_or_savefig(output_path=None, substitution_path=None):
    """
    Either open the plot in the default matplotlib GUI or export the plot to a 
    file, depending on whether or not an output path is given.  If an output 
    path is given and it contains dollar signs ('$'), they will be replaced 
    with the given substitution path.
    """
    import os, sys, subprocess, matplotlib.pyplot as plt
    from pathlib import Path
    from tempfile import NamedTemporaryFile

    # Decide how we are going to display the plot.  We have to do this before 
    # anything is plotted, because if we want to 

    if output_path is None:
        fate = 'gui'
    elif output_path is False:
        fate = 'none'
    elif output_path == 'lpr':
        fate = 'print'
    else:
        fate = 'save'

    # We have to decide whether or not to fork before plotting anything, 
    # otherwise X11 will complain, and we only want to fork if we'll end up 
    # showing the GUI.  So first we calculate the output path, then we either 
    # fork or don't, then we yield to let the caller plot everything, then we 
    # either display the GUI or save the figure to a file.

    if fate == 'gui' and os.fork():
        sys.exit()

    yield

    if fate == 'print':
        temp_file = NamedTemporaryFile(prefix='fcm_analysis_', suffix='.ps')
        plt.savefig(temp_file.name, dpi=300)
        # Add ['-o', 'number-up=4'] to get plots that will fit in a lab 
        # notebook.
        subprocess.call(['lpr', temp_file.name])

    if fate == 'save':
        if substitution_path:
            output_path = output_path.replace('$', Path(substitution_path).stem)
        plt.savefig(output_path, dpi=300)

    if fate == 'gui':
        plt.gcf().canvas.set_window_title(' '.join(sys.argv))
        plt.show()

