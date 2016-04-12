#!/usr/bin/env python3

"""\
Choose a library size that maximizes your chances of finding a functional 
library member.

When doing a directed evolution experiment, the size of your library is really 
the only variable you can tune.  There are other variables that you can try to 
maximize, like how many of your library members work and how many of them you 
can actually screen, but your library can pretty much be as big or as small as 
you want.  The question is, how big should it be?

To answer this question, this script calculates the probability of finding a 
working library member as a function of the size of your library.  If your 
library is too small, you end up checking the same members over and over, which
reduces your chance of finding a working one.  If your library is too big, 
working designs are likely to be more rare, which also reduces your chances of 
finding one.  However, the best compromise depends on how many working designs 
you think are in the library and how many designs you can screen.

Usage:
    best_library_size.py [options]

Options:
    -z, --library-sizes <expr: min,max>
        The library sizes that you are considering making and want to compare.  
        This option sets the axes limits for most of the plots and should be a 
        python expression that evaluates to a tuple with two elements.  By 
        default, libraries up to two orders of magnitude smaller or larger than 
        '--sampling-capacity' will be considered.  If you do specify a range of 
        library size, it will be rounded to start and end on a decade.

    -n, --sampling-capacity <expr>          [default: 6e7]
        The number of library members you have the capacity to sample.  This is 
        ≈6×10⁷ for my FACS experiments, assuming that sorting at 10,000 evt/sec 
        gives reasonable accuracy and that ≈60% of the cells survive sorting.
    
    -q, --quality-peak <expr>               [default: 4**10]
        The library size for which you think the greatest fraction of members 
        will work.  You can also think of this as the number of positions you 
        think you need to randomize, converted to a library size.  The default 
        is 4**10, which corresponds to randomizing a 5bp stem.  I expect this 
        to be a good library size because most communication modules I've seen 
        in the literature are about this length.

    -Q, --quality-trough <expr>             [default: 4**16]
        The library size for which you think working members will be rare, 
        relative to '--quality-peak'.  This can be either smaller or larger 
        than '--quality-peak'.  The default is 4**16, which corresponds to 
        randomizing an 8bp stem.  I don't have anything to back this up, but 
        with that much randomness I just feel like functional designs won't be 
        common anymore.

    -b, --log-base <int>                    [default: 10]
        Which base to display the library size axes in.  The default is 10, 
        because in general it's the easiest to think about.  However, I 
        sometimes like to see the axes in base 4, which in more immediately 
        interpretable as "number of base pairs randomized".
"""

from pylab import *
from pprint import pprint
from matplotlib.colors import LogNorm
import warnings; warnings.simplefilter('ignore')
import pylab; pylab.rcParams['font.family'] = 'DejaVu Sans'

def prob_working(x, mu, sig):
    """
    The probability that each individual library member is active as a function 
    of the size of the library.  This function is really impossible to know 
    quantitatively, but it should be smallest for small libraries (which simply 
    don't have enough variants to get the desired behavior) and big libraries 
    (which are diluted with lots of members that are unlikely to be active).
    
    For the purposes of this script, which is to roughly determine what the best 
    library size is, we can approximate this function using a log-normal 
    distribution, which will look like a normal distribution because the x-axis 
    is on a log-scale.  One advantage of the log-normal distribution is that it 
    has only two parameters, which will allow us to easily show how the best 
    library size depends on the shape of this function.
    """
    return exp(-0.5 * log10(x/mu)**2 / (log10(mu/sig)/2.355)**2)

def num_sampled(x, N):
    return x - x * ((x-1)/x)**N

def prob_sample_working(x, mu, sig, N):
    return prob_working(x, mu, sig) * num_sampled(x, N)

def best_library_size(x, mu, sig, N):
    @vectorize
    def best_for_mu_sig(mu, sig):
        return x[argmax(prob_sample_working(x, mu, sig, N))]
    return best_for_mu_sig(mu, sig)


class BestLibrarySize:

    def __init__(self):
        # User-controlled parameters.
        self.library_sizes = None
        self.sampling_capacity = None
        self.quality_peak = None
        self.quality_trough = None
        self.log_base = None

        # Internally-used plotting objects.
        self.fig = None
        self.axes = None
        self.prob_working_artist = None
        self.num_sampled_artist = None
        self.prob_sample_working_artist = None
        self.best_library_artist = None
        self.best_library_lines = [None, None, None]
        self.major_lines = {
                'color': 'black',
                'linestyle': '-',
        }
        self.minor_lines = {
                'color': 'grey',
                'linestyle': ':',
        }

    def plot(self):
        self._setup_figure()
        self._setup_prob_working()
        self._setup_num_sampled()
        self._setup_prob_sample_working()
        self._setup_best_library_size()
        self._update_plots()

    def _setup_figure(self):
        self.fig, self.axes = subplots(2, 2)
        self.fig.subplots_adjust(hspace=0.4, wspace=0.4)
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)

    def _setup_prob_working(self):
        self.prob_working_artist, = self.axes[0,0].plot([], [], **self.major_lines)
        self.best_library_lines[0] = self.axes[0,0].axvline(1, **self.minor_lines)
        self.axes[0,0].set_xscale('log', basex=self.log_base)
        self.axes[0,0].set_xlabel("library size")
        self.axes[0,0].set_ylabel("fraction of library\nthat works")
        self.axes[0,0].set_ylim(bottom=0, top=1.1)
        self.axes[0,0].yaxis.set_ticks_position('none')
        self.axes[0,0].yaxis.set_ticklabels([])

    def _setup_num_sampled(self):
        self.num_sampled_artist, = self.axes[0,1].plot([], [], **self.major_lines)
        self.best_library_lines[1] = self.axes[0,1].axvline(1, **self.minor_lines)
        self.axes[0,1].set_xscale('log', basex=self.log_base)
        self.axes[0,1].set_yscale('log', basey=self.log_base)
        self.axes[0,1].set_xlabel("library size")
        self.axes[0,1].set_ylabel("number of library\nmembers sampled")

    def _setup_prob_sample_working(self):
        self.prob_sample_working_artist, = self.axes[1,0].plot([], [], **self.major_lines)
        self.best_library_lines[2] = self.axes[1,0].axvline(1, **self.minor_lines)
        self.axes[1,0].set_xscale('log', basex=self.log_base)
        self.axes[1,0].set_xlabel("library size")
        self.axes[1,0].set_ylabel("number of working\nlibrary members found")
        self.axes[1,0].yaxis.set_ticks_position('none')
        self.axes[1,0].yaxis.set_ticklabels([])

    def _setup_best_library_size(self):
        x = self._library_size_axis()
        mu = self._two_decades_around(self.quality_peak)
        sig = self._two_decades_around(self.quality_trough)
        mu_2d, sig_2d = meshgrid(mu, sig)
        best = best_library_size(x, mu_2d, sig_2d, self.sampling_capacity)
        self.best_library_artist = self.axes[1,1].pcolor(
                mu, sig, best,
                cmap=cm.Spectral_r, norm=LogNorm(), rasterized=True)
        self.axes[1,1].contour(
                mu, sig, best,
                [self.sampling_capacity],
                colors='black')
        self.axes[1,1].contour(
                mu, sig, best,
                [self.sampling_capacity / 10, self.sampling_capacity * 10],
                colors='black', linestyles=':')
        self.cursor_artist, = self.axes[1,1].plot([], [], 'ko')
        self.fig.colorbar(self.best_library_artist, ax=self.axes[1,1])
        self.axes[1,1].set_xscale('log', basex = self.log_base)
        self.axes[1,1].set_yscale('log', basey = self.log_base)
        self.axes[1,1].set_xlabel("quality peak")
        self.axes[1,1].set_ylabel("quality trough")

    def _on_click(self, event):
        if event.inaxes is self.axes[1,1]:
            self.quality_peak = event.xdata
            self.quality_trough = event.ydata
            self._update_plots()

    def _update_plots(self):
        x = self._library_size_axis()
        X = best_library_size(x, self.quality_peak, self.quality_trough,
                self.sampling_capacity)

        self.prob_working_artist.set_xdata(x)
        self.prob_working_artist.set_ydata(
                prob_working(x, self.quality_peak, self.quality_trough))

        self.num_sampled_artist.set_xdata(x)
        self.num_sampled_artist.set_ydata(
                num_sampled(x, self.sampling_capacity))

        self.prob_sample_working_artist.set_xdata(x)
        self.prob_sample_working_artist.set_ydata(
                prob_sample_working(x, self.quality_peak, self.quality_trough,
                    self.sampling_capacity))

        for line in self.best_library_lines:
            line.set_xdata(X)

        for ax in self.axes.flat:
            if ax is self.axes[1,1]: continue
            ax.relim()
            ax.autoscale_view()

        self.cursor_artist.set_xdata([self.quality_peak])
        self.cursor_artist.set_ydata([self.quality_trough])

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def _library_size_axis(self, num=500):
        _log = lambda x: log(x) / log(self.log_base)

        if self.library_sizes is not None:
            start = _log(self.library_sizes[0])
            stop = _log(self.library_sizes[1])
        else:
            start = _log(self.quality_peak / 100)
            stop = _log(self.quality_peak * 100)

        return logspace(floor(start), ceil(stop), num, base=self.log_base)

    def _two_decades_around(self, x):
        _log = lambda x: log(x) / log(self.log_base)
        start = _log(x / 100)
        stop = _log(x * 100)
        return logspace(floor(start), ceil(stop), base=self.log_base)



if __name__ == '__main__':
    import os, docopt
    args = docopt.docopt(__doc__)
    if os.fork():
        raise SystemExit

    analysis = BestLibrarySize()
    analysis.library_sizes = eval(args['--library-sizes'] or 'None') 
    analysis.sampling_capacity = eval(args['--sampling-capacity'])
    analysis.quality_peak = eval(args['--quality-peak'])
    analysis.quality_trough = eval(args['--quality-trough'])
    analysis.log_base = int(args['--log-base'])
    analysis.plot()
    show()

    raise SystemExit

