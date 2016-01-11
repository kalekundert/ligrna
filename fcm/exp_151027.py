#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')
import multiprocessing as mp
from klab.fcm.fcm import Plate, PlateInfo, make_individual_gating_fig
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

fast_run = False
channel_name = 'PE-Texas Red-A'

plate_1 = Plate([
    PlateInfo('TEP_conc', 0.0, ['A1-B3']),

    PlateInfo('IPTG_conc', 1.0e-3, ['A1-B3']), # 1 mM

    PlateInfo('ATC_conc', 1.0e-6, ['A1-B3']), # 1uM

    PlateInfo('Control-Pos', None, 'B1-B3'),
    PlateInfo('Control-Neg', None, 'A1-A3'),
], sample_dir = '/kortemmelab/data/kyleb/cas9/151027/151027-controls-3pm/96 Well - Flat bottom',
    name = '5hr',
)

plate_2 = Plate([
    PlateInfo('TEP_conc', 0.0, ['A1-B3']),

    PlateInfo('IPTG_conc', 1.0e-3, ['A1-B3']), # 1 mM

    PlateInfo('ATC_conc', 1.0e-6, ['A1-B3']), # 1uM

    PlateInfo('Control-Pos', None, 'B1-B3'),
    PlateInfo('Control-Neg', None, 'A1-A3'),
], sample_dir = '/kortemmelab/data/kyleb/cas9/151027/151027-controls-6,3a,00pm_001/96 Well - Flat bottom',
    name = '8hr',
)

all_plates = [plate_1, plate_2]

exp_tep_concs = [
    (0.0, '0'),
]

def main():
    outer_fig_dir = os.path.join('script_output', 'exp_151027')

    if True:
        plot_gate_value('poly_0.6', 0.6, outer_fig_dir)
    else:
        func_args = []
        # Append fsc threshold gates
        fsc_gate_above = -20000.0
        while fsc_gate_above <= 60000.0:
            func_args.append( ('fsc_%d'% int(fsc_gate_above), fsc_gate_above, outer_fig_dir) )
            fsc_gate_above += 20000.0
        # Append poly gates
        for gate_val in np.arange(0.2,1.0,0.2):
            func_args.append( ('poly_%.1f' % gate_val, gate_val, outer_fig_dir) )

        pool = mp.Pool()
        print func_args
        pool.map(run_subprocess, func_args)
        pool.close()
        pool.join()

def run_subprocess(function_argument_tuple):
    subprocess.call([
        'python', os.path.basename(__file__),
        str(function_argument_tuple[0]),
        str(function_argument_tuple[1]),
        str(function_argument_tuple[2]),
    ])

def plot_gate_value(gate_name=None, gate_val=None, outer_fig_dir=None):
    if not gate_name:
        gate_name = sys.argv[1]
    if not gate_val:
        gate_val = float(sys.argv[2])
    if not outer_fig_dir:
        outer_fig_dir = sys.argv[3]

    fig_dir = os.path.join(outer_fig_dir, gate_name)
    if not os.path.isdir(fig_dir):
        os.makedirs(fig_dir)

    gated_plates = [make_individual_gating_fig(p, gate_val, gate_name, fig_dir, fast_run = fast_run, florescence_channel = channel_name, title = os.path.basename(__file__)) for p in all_plates]
        
    plot_rows = 2
    plot_cols = 3
    plate_fig = plt.figure(figsize=(16.0, 11.0), dpi=300)
    plot_num = 1
    plate_fig.suptitle('Controls in 3mL liquid culture', fontsize=12)
    for plot_row in xrange(plot_rows):
        exp = gated_plates[plot_row]
        plot_row += 1
        for replicate_count in xrange(1, plot_cols+1):
            if replicate_count == 1:
                ylabel = True
            else:
                ylabel = False
            if plot_row == 2:
                xlabel = True
            else:
                xlabel = False
            ax = plate_fig.add_subplot(plot_rows, plot_cols, plot_num)
            ax.grid(True)
            if xlabel:
                ax.set_xlabel('%s - Replicate %d' % (channel_name, replicate_count), size=18)
            if ylabel:
                ax.set_ylabel('Counts - %s'  % exp.name, size=18)
            plot_num += 1
            colors = [(0,0,1,0.3), (0,1,0,0.3), (1,0,0,0.3)]
            exp_means = {}
            hist_output = {}
            for count, sample_type in enumerate(['pos', 'neg']):
                color = colors[count % len(colors)]
                if sample_type == 'pos':
                    exp_well = exp.get_by_well('B%d' % replicate_count)
                elif sample_type == 'neg':
                    exp_well = exp.get_by_well('A%d' % replicate_count)

                exp_mean = exp_well.data[channel_name].mean()

                # Fast way to make code work and not bootstrap
                if True:
                    exp_mean_low, exp_mean_high = (exp_mean, exp_mean)
                else:
                    # Slow bootstrapping
                    try:
                        print 'Starting bootstrap'
                        exp_mean_low, exp_mean_high = bootstrap.ci(exp_well.data[channel_name].as_matrix(), statfunction=np.average, method='bca', n_samples=1000)
                        print 'Done bootstrap'
                    except Exception:
                        print 'Bootstrap error'
                        exp_mean_low, exp_mean_high = (exp_mean, exp_mean)

                exp_means[sample_type] = (exp_mean, exp_mean_low, exp_mean_high)
                sample_data = exp_well.data[channel_name].as_matrix()
                sample_max = np.max(sample_data)
                sample_min = np.min(sample_data)
                nbins = max(3, int(20 * float((sample_max - sample_min) / 2000)))
                hist_output[sample_type] = exp_well.plot(channel_name, bins=40, fc=color, lw=1, ax=ax, autolabel=False, stacked=True, label='%s - mean %.0f' % (sample_type, exp_mean) )

            ylim = ax.get_ylim()
            xlim = ax.get_xlim()
            for count, sample_type in enumerate(['pos', 'neg']):
                color = colors[count % len(colors)]
                n, bins, patches = hist_output[sample_type]
                # ax.plot((exp_means[sample_type][1], exp_means[sample_type][1]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='--', linewidth=1)
                # ax.plot((exp_means[sample_type][0], exp_means[sample_type][0]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='-', linewidth=2)
                # ax.plot((exp_means[sample_type][2], exp_means[sample_type][2]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='--', linewidth=1)

                mu, std = scipy.stats.norm.fit(exp_well.data[channel_name]) # distribution fitting
                # now, mu and std are the mean and
                # the standard deviation of the fitted distribution
                # fitted distribution

                # Plot normalized distibution
                # Normal normal distribution is scaled to area of 1, so multiply by actual
                # area of histogram (np.sum(n * np.diff(bins)))
                pdf_fitted = scipy.stats.norm.pdf(bins, loc=mu, scale=std) * np.sum(n * np.diff(bins))
                ax.plot(bins, pdf_fitted, color=(color[0], color[1], color[2], 1.0), linewidth=2)

            ax.legend()
    plate_fig.savefig(os.path.join(fig_dir, 'all_data.pdf'))
    plate_fig.clf()
    plt.close(plate_fig)
    del plate_fig
    # plate_fig.tight_layout()

    # # Prepare mean diffs figure
    # mean_cis = copy.deepcopy(mean_diffs)
    # sig_results = {}
    # for name in mean_cis:
    #     sig_results[name] = 0
    #     for atc_conc in mean_cis[name]:
    #         for tep_conc in mean_cis[name][atc_conc]:
    #             mean, mean_low, mean_high = mean_confidence_interval( mean_cis[name][atc_conc][tep_conc].values() )
    #             mean_cis[name][atc_conc][tep_conc] = (mean, mean_low, mean_high, mean_cis[name][atc_conc][tep_conc].values() )
    #             if mean_low > 1.0 or mean_high < 1.0:
    #                 sig_results[name] += 1
    # with open(os.path.join(fig_dir, 'sig_results.txt'), 'w') as f:
    #     f.write('Significant results:\n')
    #     f.write( str(sig_results) )
    #     f.write('\n')

    # diffs_fig = plt.figure()
    # axes = []
    # colors = [(0,1,0,0.3), (1,0,0,0.3)]
    # legend_info = []
    # for name_count, name in enumerate(sorted(mean_cis)):
    #     if len(axes) == 0:
    #         ax = diffs_fig.add_subplot(1, len(mean_cis), name_count+1)
    #     else:
    #         ax = diffs_fig.add_subplot(1, len(mean_cis), name_count+1, sharey=axes[0])
    #     axes.append(ax)
    #     ax.set_ylim( (0.1, 10.0) )

    #     atc_concs = sorted( mean_cis[name].keys() )
    #     tep_concs = set()
    #     for atc_conc in atc_concs:
    #         for tep_conc in mean_cis[name][atc_conc]:
    #             tep_concs.add(tep_conc)
    #     tep_concs = sorted([x for x in tep_concs])

    #     ind = np.arange(len(atc_concs))  # the x locations for the groups
    #     width = 0.9 / len(tep_concs) # the width of the bars

    #     group_centers = [[] for x in xrange(len(atc_concs))]
    #     for tep_conc_count, tep_conc in enumerate(tep_concs):
    #         data = [mean_cis[name][atc_conc][tep_conc][0] for atc_conc in atc_concs]
    #         yerr = [
    #             mean_cis[name][atc_conc][tep_conc][0]-mean_cis[name][atc_conc][tep_conc][1]
    #             for atc_conc in atc_concs
    #         ]
    #         rects = ax.bar(ind + width*tep_conc_count + width/2.0, data, width, color=colors[tep_conc_count % len(colors)])
    #         bar_centers = [r.get_x()+r.get_width()/2.0 for r in rects]
    #         for i, center in enumerate(bar_centers):
    #             group_centers[i].append(center)
    #         color = colors[tep_conc_count % len(colors)]
    #         ax.errorbar(bar_centers, data, yerr=yerr,
    #                     # zorder = 4,
    #                     linewidth = 1, capthick = 1,
    #                     # lolims=True, uplims=True,
    #                     fmt='none', ecolor=(color[0], color[1], color[2], 1.0))

    #         # Plot all points
    #         y_pts = []
    #         x_pts = []
    #         for i, atc_conc in enumerate(atc_concs):
    #             for y_pt in mean_cis[name][atc_conc][tep_conc][3]:
    #                 x_pts.append(bar_centers[i])
    #                 y_pts.append(y_pt)
    #         rep_line = ax.plot(x_pts, y_pts, linewidth=0, marker='+', markersize=5.0, color='black')
    #         if name_count == 0:
    #             legend_info.append( (rects, 'TEP %.1E' % tep_conc) )

    #         # Plot stars for significant values
    #         star_xs = []
    #         star_ys = []
    #         for x, tup in zip(bar_centers, [mean_cis[name][atc_conc][tep_conc] for atc_conc in atc_concs]):
    #             y, y_min, y_max, y_pts = tup
    #             if y_min > 1.0 or y_max < 1.0:
    #                 star_xs.append(x)
    #                 star_ys.append(y)
    #         if len(star_xs) > 0:
    #             ax.plot(star_xs, star_ys, linewidth=0, marker='*', markersize=10.0, color='gold')
    #     group_centers = [np.average(x) for x in group_centers]

    #     # Plot line at 1 for comparison
    #     xlim = ax.get_xlim()
    #     ax.plot((xlim[0], xlim[1]), (1.0, 1.0), color='black', linestyle='--', linewidth=1)

    #     ax.set_yscale("log", nonposy='clip')

    #     if len(axes) == 1:
    #         ax.set_ylabel('Fold signal over TEP 0')
    #     ax.set_title(name)
    #     ax.set_xticks(group_centers)
    #     ax.set_xticklabels( atc_concs )
    #     ax.set_xlabel( 'ATC conc. (M)' )

    #     subs = [2.0, 4.0, 6.0, 8.0]  # ticks to show per decade
    #     ax.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(subs=subs)) #set the ticks position
    #     # ax.yaxis.set_major_formatter(matplotlib.ticker.NullFormatter())   # remove the major ticks
    #     ax.yaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(fcm.ticks_format))  #add the custom ticks

    # stars_proxy = matplotlib.lines.Line2D([], [], linewidth=0, marker='*', markersize=10.0, color='gold')
    # pts_proxy = matplotlib.lines.Line2D([], [], linewidth=0, marker='+', markersize=5.0, color='black')
    # legend_info.append( (stars_proxy, 'Sig. results') )
    # legend_info.append( (pts_proxy, 'Replicates') )
    # diffs_fig.suptitle('2015/10/15 - Mean biological replicate fold signal over TEP 0.0 conc. (IPTG 1mm) (mean of replicate means of gated distributions)', y=1.04)
    # diffs_fig.tight_layout()
    # diffs_fig.legend([t[0] for t in legend_info], [t[1] for t in legend_info], loc = 'lower center', ncol=4)
    # # diffs_fig.tight_layout()
    # diffs_fig.set_size_inches(11.0*len(mean_cis)/3.0, 6.0)
    # diffs_fig.savefig(os.path.join(fig_dir, 'diffs.pdf'), dpi=300,  bbox_inches='tight', pad_inches=0.6)
    # diffs_fig.clf()
    # plt.close(diffs_fig)
    # del diffs_fig
    # plt.clf()
    # plt.cla()
    # gc.collect()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        plot_gate_value()
