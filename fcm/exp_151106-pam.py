#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')
from klab.fcm.fcm import Plate, PlateInfo, make_gating_fig
import klab.fcm.fcm as fcm
import os
import numpy as np
import scipy
import scipy.stats
from FlowCytometryTools import FCMeasurement, PolyGate, ThresholdGate
import FlowCytometryTools
import matplotlib.pyplot as plt
import numpy.random as npr
import sys
import scipy.optimize
import scikits.bootstrap as bootstrap
import copy
import gc
import subprocess

fast_run = True
channel_name = 'PE-Texas Red-A'
colors = [(0,0,1,0.3), (0,1,0,0.3), (1,0,0,0.3)]
well_types = ['Pos', 'Neg']

two_pm_dir = '/home/kyleb/data/cas9/151106/kyleb/151106-2pm_001/96 Well - Flat bottom'
four_pm_dir = '/kortemmelab/data/kyleb/cas9/151106/kyleb/151106-4pm_001/96 Well - Flat bottom'
dir_to_load = four_pm_dir

plate_1 = Plate([
    PlateInfo('Control-Pos', None, ['E1']),
    PlateInfo('Control-Neg', None, ['E2']),
    PlateInfo('design-4-Pos', None, ['E3']),
    PlateInfo('design-4-Neg', None, ['E4']),
    PlateInfo('design-7-Pos', None, ['E5']),
    PlateInfo('design-7-Neg', None, ['E6']),
], sample_dir = dir_to_load,
    name = 'replicate_1',
)

plate_2 = Plate([
    PlateInfo('Control-Pos', None, ['F1']),
    PlateInfo('Control-Neg', None, ['F2']),
    PlateInfo('design-4-Pos', None, ['F3']),
    PlateInfo('design-4-Neg', None, ['F4']),
    PlateInfo('design-7-Pos', None, ['F5']),
    PlateInfo('design-7-Neg', None, ['F6']),
], sample_dir = dir_to_load,
    name = 'replicate_2',
)

plate_3 = Plate([
    PlateInfo('Control-Pos', None, ['G1']),
    PlateInfo('Control-Neg', None, ['G2']),
    PlateInfo('design-4-Pos', None, ['G3']),
    PlateInfo('design-4-Neg', None, ['G4']),
    PlateInfo('design-7-Pos', None, ['G5']),
    PlateInfo('design-7-Neg', None, ['G6']),
], sample_dir = dir_to_load,
    name = 'replicate_3',
)

all_plates = [plate_1, plate_2, plate_3]

def main():
    outer_fig_dir = os.path.join('script_output', os.path.basename(__file__).split('.')[0])
    gate_val = 0.6
    gate_name = 'poly_0.6'
    fig_dir = os.path.join(outer_fig_dir, gate_name)
    if not os.path.isdir(fig_dir):
        os.makedirs(fig_dir)
    gated_plates = make_gating_fig(all_plates, gate_val, gate_name, fig_dir, fast_run=fast_run)

    for plate_num, exp in enumerate(gated_plates):
        data_names = set()
        for p in exp.experimental_parameters:
            data_names.add( p[:-4] )
        data_names = sorted( x for x in data_names )
        plot_rows = len(data_names)
        plot_cols = 1
        plate_fig = plt.figure(figsize=(22.0*plot_cols/3.0, 17.0*plot_rows/3.0), dpi=300)
        plot_num = 1
        plate_fig.suptitle(exp.name, fontsize=12)
        mean_diffs = {}
        for data_name_i, data_name in enumerate(data_names):
            if data_name_i + 1 == len(data_names):
                xlabel = True
            else:
                xlabel = False
            ax = plate_fig.add_subplot(plot_rows, plot_cols, plot_num)
            plot_num += 1
            ax.grid(True)
            if xlabel:
                ax.set_xlabel('%s' % (channel_name), size=18)
            well_means = {}
            hist_output = {}
            for well_type_i, well_type in enumerate(well_types):
                if well_type_i == 0:
                    ax.set_ylabel(data_name, size=18)
                well = exp.single_well_from_set(exp.well_set(data_name + '-' + well_type))
                color = colors[well_type_i % len(colors)]
                well_mean = well.data[channel_name].mean()
                xmax = float('inf')
                xmin = float('-inf')
                channel_data = well.data[channel_name].as_matrix()
                if len(channel_data) == 0:
                    channel_data = [0.0000001]

                # Add pos/neg signal fold diff to mean diffs
                # Fast way to make code work and not bootstrap
                if fast_run:
                    well_mean_low, well_mean_high = (well_mean, well_mean)
                else:
                    # Slow bootstrapping
                    try:
                        well_mean_low, well_mean_high = bootstrap.ci(channel_data, statfunction=np.average, method='pi')
                    except Exception:
                        well_mean_low, well_mean_high = (well_mean, well_mean)

                well_means[(data_name, well_type)] = (well_mean, well_mean_low, well_mean_high)
                hist_output[(data_name, well_type)] = well.plot(channel_name, bins=120, fc=color, lw=1, ax=ax, autolabel=False, stacked=True, label='%s' % (well_type) )
                print exp.name, data_name + '-' + well_type, len(channel_data), channel_data
                # Find 99th percentile limits
                this_xmax = np.max(channel_data)
                if this_xmax < xmax:
                    xmax = this_xmax
                this_xmin = np.min(channel_data)
                if this_xmin > xmin:
                    xmin = this_xmin
            ax.set_xlim( (xmin, xmax) )

            ylim = ax.get_ylim()
            xlim = ax.get_xlim()
            for well_type_i, well_type in enumerate(well_types):
                if data_name not in mean_diffs:
                    mean_diffs[data_name] = {}
                mean_diffs[data_name][exp.name] = well_means[(data_name, 'Neg')][0] / well_means[(data_name, 'Pos')][0]
                color = colors[well_type_i % len(colors)]
                if hist_output[(data_name, well_type)]:
                    n, bins, patches = hist_output[(data_name, well_type)]
                    ax.plot((well_means[(data_name, well_type)][0], well_means[(data_name, well_type)][0]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='-', linewidth=2)
                    if well_means[(data_name, well_type)][0] != well_means[(data_name, well_type)][1] and well_means[(data_name, well_type)][0] != well_means[(data_name, well_type)][2]:
                        ax.plot((well_means[(data_name, well_type)][1], well_means[(data_name, well_type)][1]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='--', linewidth=1)
                        ax.plot((well_means[(data_name, well_type)][2], well_means[(data_name, well_type)][2]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='--', linewidth=1)

                    well = exp.single_well_from_set(exp.well_set(data_name + '-' + well_type))
                    mu, std = scipy.stats.norm.fit(well.data[channel_name]) # distribution fitting
                    # now, mu and std are the mean and
                    # the standard deviation of the fitted distribution
                    # fitted distribution

                    # Plot normalized distibution
                    # Normal normal distribution is scaled to area of 1, so multiply by actual
                    # area of histogram (np.sum(n * np.diff(bins)))
                    pdf_fitted = scipy.stats.norm.pdf(bins, loc=mu, scale=std) * np.sum(n * np.diff(bins))
                    ax.plot(bins, pdf_fitted, color=(color[0], color[1], color[2], 1.0), linewidth=2)

            ax.legend()
        plate_fig.savefig(os.path.join(fig_dir, 'plate-%s.pdf' % exp.name))
        plate_fig.clf()
        plt.close(plate_fig)
        del plate_fig
        # plate_fig.tight_layout()

    # Prepare mean diffs figure
    mean_cis = copy.deepcopy(mean_diffs)
    sig_results = {}
    for name in mean_cis:
        sig_results[name] = 0
        mean, mean_low, mean_high = fcm.mean_confidence_interval( mean_cis[name].values() )
        mean_cis[name] = (mean, mean_low, mean_high, mean_cis[name].values() )
        if mean_low > 1.0 or mean_high < 1.0:
            sig_results[name] += 1
    with open(os.path.join(fig_dir, 'sig_results.txt'), 'w') as f:
        print sig_results
        print
        f.write('Significant results:\n')
        f.write( str(sig_results) )
        f.write('\n')

    diffs_fig = plt.figure()
    axes = []
    legend_info = []
    for name_count, name in enumerate(sorted(mean_cis)):
        if len(axes) == 0:
            ax = diffs_fig.add_subplot(1, len(mean_cis), name_count+1)
        else:
            ax = diffs_fig.add_subplot(1, len(mean_cis), name_count+1, sharey=axes[0])
        axes.append(ax)
        ax.set_ylim( (0.1, 10.0) )

        ind = np.arange(1)  # the x locations for the groups
        num_bars = 1
        width = 0.9 / num_bars # the width of the bars

        group_centers = [[]]
        data = [mean_cis[name][0]]
        yerr = [
            mean_cis[name][0]-mean_cis[name][1]
        ]
        rects = ax.bar(ind + width*num_bars + width/2.0, data, width, color=colors[0])
        bar_centers = [r.get_x()+r.get_width()/2.0 for r in rects]
        for i, center in enumerate(bar_centers):
            group_centers[i].append(center)
        color = colors[0]
        ax.errorbar(bar_centers, data, yerr=yerr,
                    # zorder = 4,
                    linewidth = 1, capthick = 1,
                    # lolims=True, uplims=True,
                    fmt='none', ecolor=(color[0], color[1], color[2], 1.0))

        # Plot all points
        y_pts = []
        x_pts = []
        for i, bar_center in enumerate(bar_centers):
            for y_pt in mean_cis[name][3]:
                x_pts.append(bar_centers[i])
                y_pts.append(y_pt)
        rep_line = ax.plot(x_pts, y_pts, linewidth=0, marker='+', markersize=5.0, color='black')
        if name_count == 0:
            legend_info.append( (rects, name) )

        # Plot stars for significant values
        star_xs = []
        star_ys = []
        for x in bar_centers:
            y, y_min, y_max, y_pts = mean_cis[name]
            if y_min > 1.0 or y_max < 1.0:
                star_xs.append(x)
                star_ys.append(y)
            if len(star_xs) > 0:
                ax.plot(star_xs, star_ys, linewidth=0, marker='*', markersize=10.0, color='gold')
        group_centers = [np.average(x) for x in group_centers]

        # Plot line at 1 for comparison
        xlim = ax.get_xlim()
        ax.plot((xlim[0], xlim[1]), (1.0, 1.0), color='black', linestyle='--', linewidth=1)

        ax.set_yscale("log", nonposy='clip')

        if len(axes) == 1:
            ax.set_ylabel('Fold signal')
        ax.set_title(name)

        subs = [2.0, 4.0, 6.0, 8.0]  # ticks to show per decade
        ax.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(subs=subs)) #set the ticks position
        # ax.yaxis.set_major_formatter(matplotlib.ticker.NullFormatter())   # remove the major ticks
        ax.yaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(fcm.ticks_format))  #add the custom ticks

    stars_proxy = matplotlib.lines.Line2D([], [], linewidth=0, marker='*', markersize=10.0, color='gold')
    pts_proxy = matplotlib.lines.Line2D([], [], linewidth=0, marker='+', markersize=5.0, color='black')
    legend_info.append( (stars_proxy, 'Sig. results') )
    legend_info.append( (pts_proxy, 'Replicates') )
    diffs_fig.suptitle('2015/11/06 - Mean biological replicate fold signal', y=1.04)
    diffs_fig.tight_layout()
    diffs_fig.legend([t[0] for t in legend_info], [t[1] for t in legend_info], loc = 'lower center', ncol=4)
    # diffs_fig.tight_layout()
    diffs_fig.set_size_inches(11.0*len(mean_cis)/3.0, 6.0)
    diffs_fig.savefig(os.path.join(fig_dir, 'diffs.pdf'), dpi=300,  bbox_inches='tight', pad_inches=0.6)
    diffs_fig.clf()
    plt.close(diffs_fig)
    del diffs_fig
    plt.clf()
    plt.cla()
    gc.collect()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        plot_gate_value()
