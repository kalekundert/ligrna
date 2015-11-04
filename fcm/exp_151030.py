#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')
import multiprocessing as mp
from fcm import Plate, PlateInfo
import fcm
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
    PlateInfo('TEP_conc', 0.0, ['A1', 'A4', 'A7', 'A10']),
    PlateInfo('TEP_conc', 1.0e-3, ['B1', 'B4', 'B7', 'B10']), # 1 mM

    PlateInfo('IPTG_conc', 1.0e-3, ['A1', 'B1', 'A4', 'B4', 'A7', 'B7', 'A10', 'B10']), # 1 mM

    PlateInfo('ATC_conc', 1.0e-6, ['A1', 'B1', 'A4', 'B4', 'A7', 'B7', 'A10', 'B10']), # 1uM

    PlateInfo('Control-Pos', None, ['A1', 'B1']),
    PlateInfo('Control-Neg', None, ['A4', 'B4']),
    PlateInfo('NX-0', None, ['A7', 'B7']),
    PlateInfo('US-0,0', None, ['A10', 'B10']),
], sample_dir = '/kortemmelab/data/kyleb/cas9/151030/kyleb/151030-4,3a,45pm_001/96 Well - Flat bottom',
    name = 'replicate_1',
)

plate_2 = Plate([
    PlateInfo('TEP_conc', 0.0, ['A2', 'A5', 'A8', 'A11']),
    PlateInfo('TEP_conc', 1.0e-3, ['B2', 'B5', 'B8', 'B11']), # 1 mM

    PlateInfo('IPTG_conc', 1.0e-3, ['A2', 'B2', 'A5', 'B5', 'A8', 'B8', 'A11', 'B11']), # 1 mM

    PlateInfo('ATC_conc', 1.0e-6, ['A2', 'B2', 'A5', 'B5', 'A8', 'B8', 'A11', 'B11']), # 1uM

    PlateInfo('Control-Pos', None, ['A2', 'B2']),
    PlateInfo('Control-Neg', None, ['A5', 'B5']),
    PlateInfo('NX-0', None, ['A8', 'B8']),
    PlateInfo('US-0,0', None, ['A11', 'B11']),
], sample_dir = '/kortemmelab/data/kyleb/cas9/151030/kyleb/151030-4,3a,45pm_001/96 Well - Flat bottom',
    name = 'replicate_2',
)

plate_3 = Plate([
    PlateInfo('TEP_conc', 0.0, ['A3', 'A6', 'A9', 'A12']),
    PlateInfo('TEP_conc', 1.0e-3, ['B3', 'B6', 'B9', 'B12']), # 1 mM

    PlateInfo('IPTG_conc', 1.0e-3, ['A3', 'B3', 'A6', 'B6', 'A9', 'B9', 'A12', 'B12']), # 1 mM

    PlateInfo('ATC_conc', 1.0e-6, ['A3', 'B3', 'A6', 'B6', 'A9', 'B9', 'A12', 'B12']), # 1uM

    PlateInfo('Control-Pos', None, ['A3', 'B3']),
    PlateInfo('Control-Neg', None, ['A6', 'B6']),
    PlateInfo('NX-0', None, ['A9', 'B9']),
    PlateInfo('US-0,0', None, ['A12', 'B12']),
], sample_dir = '/kortemmelab/data/kyleb/cas9/151030/kyleb/151030-4,3a,45pm_001/96 Well - Flat bottom',
    name = 'replicate_3',
)

all_plates = [plate_1, plate_2, plate_3]

exp_tep_concs = [
    (0.0, '0'),
    (1.0e-3, '1mM'),
]

def main():
    outer_fig_dir = os.path.join('script_output', os.path.basename(__file__).split('.')[0])

    if fast_run:
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

        pool = mp.Pool(1)
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
    gating_fig = plt.figure(figsize=(len(all_plates)*9, 11), dpi=600)
    gating_axes = []
    mean_diffs = {}
    for plate_num, exp in enumerate(all_plates):
        blank_samples = list(exp.well_set('Control-Blank'))
        nonblank_samples = list(exp.all_position_set.difference(exp.well_set('Control-Blank')))
        if len(gating_axes) >= 1:
            ax = gating_fig.add_subplot(1, len(all_plates), plate_num+1, sharey=gating_axes[0])
        else:
            ax = gating_fig.add_subplot(1, len(all_plates), plate_num+1)
        gating_axes.append(ax)
        ax.set_title(exp.name)

        if gate_name.startswith('fsc'):
            gate = ThresholdGate(gate_val, 'FSC-A', region='above')
        elif gate_name.startswith('poly'):
            all_exp_data_fsc = []
            all_exp_data_ssc = []
            for i, nonblank_sample in enumerate(nonblank_samples):
                if not fast_run:
                    exp.samples[nonblank_sample].plot(['FSC-A', 'SSC-A'], kind='scatter', color=np.random.rand(3,1), s=1, alpha=0.1, ax=ax)
                all_exp_data_fsc.append( exp.samples[nonblank_sample].data['FSC-A'] )
                all_exp_data_ssc.append( exp.samples[nonblank_sample].data['SSC-A'] )

            gate_m, gate_b = fcm.find_perpendicular_gating_line( np.concatenate(all_exp_data_fsc), np.concatenate(all_exp_data_ssc), gate_val)

            fsc_ssc_axis_limits = (-50000, 100000)

            x_max = np.amax(np.concatenate(all_exp_data_fsc))
            x_min = np.amin(np.concatenate(all_exp_data_fsc))
            y_max = np.amax(np.concatenate(all_exp_data_ssc))
            y_min = np.amin(np.concatenate(all_exp_data_ssc))
            ax.set_ylim(fsc_ssc_axis_limits)
            ax.set_xlim(fsc_ssc_axis_limits)
            fudge = 1.0
            polygon_xs = [x_min-fudge, x_min-fudge, (y_min-gate_b)/float(gate_m), x_max+fudge, x_max+fudge]
            polygon_ys = [y_max+fudge, gate_m*x_min+gate_b, y_min-fudge, y_min-fudge, y_max+fudge]
            gate = PolyGate(np.array([[x,y] for x, y in zip(polygon_xs, polygon_ys)]), ['FSC-A', 'SSC-A'], region='in', name='polygate')

        for i, blank_sample in enumerate(blank_samples):
            if i == 0:
                exp.samples[blank_sample].plot(['FSC-A', 'SSC-A'], kind='scatter', color='red', s=2, alpha=1.0/float(len(blank_samples)), gates=[gate], label='Blank media', ax=ax)
            else:
                if not fast_run:
                    exp.samples[blank_sample].plot(['FSC-A', 'SSC-A'], kind='scatter', color='red', s=2, alpha=1.0/float(len(blank_samples)), gates=[gate], ax=ax)
        exp.gate(gate)

        ax.grid(True)
        if len(blank_samples) > 0:
            ax.legend()

        tep_wells = {}
        for tep_conc, tep_conc_name in exp_tep_concs:
            tep_wells[tep_conc] = exp.well_set('TEP_conc', tep_conc)

        plot_rows = len(exp.parameter_values('ATC_conc')) * len(exp.parameter_values('IPTG_conc'))
        plot_cols = len(exp.experimental_parameters)
        plate_fig = plt.figure(figsize=(22.0*len(exp.experimental_parameters)/3.0, 17.0*len(exp.parameter_values('ATC_conc'))/3.0), dpi=300)
        plot_num = 1
        plate_fig.suptitle(exp.name, fontsize=12)
        for atc_conc_count, atc_conc in enumerate(exp.parameter_values('ATC_conc')):
            atc_wells = exp.well_set('ATC_conc', atc_conc)
            for iptg_conc_count, iptg_conc in enumerate(exp.parameter_values('IPTG_conc')):
                iptg_wells = exp.well_set('IPTG_conc', iptg_conc)
                for name_count, name in enumerate(sorted(exp.experimental_parameters)):
                    if name_count == 0:
                        ylabel = True
                    else:
                        ylabel = False
                    if atc_conc_count + 1 == len(exp.parameter_values('ATC_conc')):
                        xlabel = True
                    else:
                        xlabel = False
                    ax = plate_fig.add_subplot(plot_rows, plot_cols, plot_num)
                    ax.grid(True)
                    if xlabel:
                        ax.set_xlabel('%s - %s' % (channel_name, name), size=18)
                    if ylabel:
                        ax.set_ylabel('ATC Conc. %s\nIPTG Conc. %.0e' % (atc_conc, iptg_conc), size=18)
                    plot_num += 1
                    exp_wells = exp.well_set(name).intersection(atc_wells).intersection(iptg_wells)
                    exp_tep_wells = {}
                    for tep_conc, tep_conc_name in exp_tep_concs:
                        exp_tep_wells[tep_conc] = list(tep_wells[tep_conc].intersection(exp_wells))
                        assert( len(exp_tep_wells[tep_conc]) == 1 )
                        exp_tep_wells[tep_conc] = exp_tep_wells[tep_conc][0]
                    tep_means = {}
                    hist_output = {}
                    count = 0
                    colors = [(0,0,1,0.3), (0,1,0,0.3), (1,0,0,0.3)]
                    xmax = float('inf')
                    xmin = float('-inf')
                    for tep_conc, tep_conc_name in exp_tep_concs:
                        color = colors[count % len(colors)]
                        tep_mean = exp.samples[exp_tep_wells[tep_conc]].data[channel_name].mean()
                        channel_data = exp.samples[exp_tep_wells[tep_conc]].data[channel_name].as_matrix()
                        # Fast way to make code work and not bootstrap
                        if fast_run:
                            tep_mean_low, tep_mean_high = (tep_mean, tep_mean)
                        else:
                            # Slow bootstrapping
                            try:
                                tep_mean_low, tep_mean_high = bootstrap.ci(channel_data, statfunction=np.average, method='bca', n_samples=15000)
                            except Exception:
                                tep_mean_low, tep_mean_high = (tep_mean, tep_mean)

                        tep_means[tep_conc] = (tep_mean, tep_mean_low, tep_mean_high)
                        hist_output[tep_conc] = exp.samples[exp_tep_wells[tep_conc]].plot(channel_name, bins=120, fc=color, lw=1, ax=ax, autolabel=False, stacked=True, label='%s TEP - %.0f (%.0f-%.0f)' % (tep_conc_name, tep_mean, tep_mean_low, tep_mean_high) )
                        # Find 99th percentile limits
                        this_xmax = np.max(channel_data)
                        if this_xmax < xmax:
                            xmax = this_xmax
                        this_xmin = np.min(channel_data)
                        if this_xmin > xmin:
                            xmin = this_xmin
                        count += 1
                    ax.set_xlim( (xmin, xmax) )

                    # blank_sample.plot(channel_name, bins=100, alpha=0.1, color='black', label='blank media', ax=ax)
                    ylim = ax.get_ylim()
                    xlim = ax.get_xlim()
                    count = 0
                    for tep_conc, tep_conc_name in exp_tep_concs:
                        if tep_conc != 0.0 and iptg_conc == 1.0e-3:
                            if name not in mean_diffs:
                                mean_diffs[name] = {}
                            if atc_conc not in mean_diffs[name]:
                                mean_diffs[name][atc_conc] = {}
                            if tep_conc not in mean_diffs[name][atc_conc]:
                                mean_diffs[name][atc_conc][tep_conc] = {}

                            assert( exp.name not in mean_diffs[name][atc_conc][tep_conc] )
                            mean_diffs[name][atc_conc][tep_conc][exp.name] = tep_means[tep_conc][0] / tep_means[0.0][0]
                        color = colors[count % len(colors)]
                        n, bins, patches = hist_output[tep_conc]
                        ax.plot((tep_means[tep_conc][1], tep_means[tep_conc][1]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='--', linewidth=1)
                        ax.plot((tep_means[tep_conc][0], tep_means[tep_conc][0]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='-', linewidth=2)
                        ax.plot((tep_means[tep_conc][2], tep_means[tep_conc][2]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='--', linewidth=1)

                        mu, std = scipy.stats.norm.fit(exp.samples[exp_tep_wells[tep_conc]].data[channel_name]) # distribution fitting
                        # now, mu and std are the mean and
                        # the standard deviation of the fitted distribution
                        # fitted distribution

                        # Plot normalized distibution
                        # Normal normal distribution is scaled to area of 1, so multiply by actual
                        # area of histogram (np.sum(n * np.diff(bins)))
                        pdf_fitted = scipy.stats.norm.pdf(bins, loc=mu, scale=std) * np.sum(n * np.diff(bins))
                        ax.plot(bins, pdf_fitted, color=(color[0], color[1], color[2], 1.0), linewidth=2)
                        count += 1

                    ax.legend()
        plate_fig.savefig(os.path.join(fig_dir, 'plate-%s.pdf' % exp.name))
        plate_fig.clf()
        plt.close(plate_fig)
        del plate_fig
        # plate_fig.tight_layout()
    gating_fig.savefig(os.path.join(fig_dir, 'gates.png'))
    gating_fig.clf()
    plt.close(gating_fig)
    del gating_fig

    # Prepare mean diffs figure
    mean_cis = copy.deepcopy(mean_diffs)
    sig_results = {}
    for name in mean_cis:
        sig_results[name] = 0
        for atc_conc in mean_cis[name]:
            for tep_conc in mean_cis[name][atc_conc]:
                mean, mean_low, mean_high = fcm.mean_confidence_interval( mean_cis[name][atc_conc][tep_conc].values() )
                mean_cis[name][atc_conc][tep_conc] = (mean, mean_low, mean_high, mean_cis[name][atc_conc][tep_conc].values() )
                if mean_low > 1.0 or mean_high < 1.0:
                    sig_results[name] += 1
    with open(os.path.join(fig_dir, 'sig_results.txt'), 'w') as f:
        f.write('Significant results:\n')
        f.write( str(sig_results) )
        f.write('\n')

    diffs_fig = plt.figure()
    axes = []
    colors = [(0,1,0,0.3), (1,0,0,0.3)]
    legend_info = []
    for name_count, name in enumerate(sorted(mean_cis)):
        if len(axes) == 0:
            ax = diffs_fig.add_subplot(1, len(mean_cis), name_count+1)
        else:
            ax = diffs_fig.add_subplot(1, len(mean_cis), name_count+1, sharey=axes[0])
        axes.append(ax)
        ax.set_ylim( (0.1, 10.0) )

        atc_concs = sorted( mean_cis[name].keys() )
        tep_concs = set()
        for atc_conc in atc_concs:
            for tep_conc in mean_cis[name][atc_conc]:
                tep_concs.add(tep_conc)
        tep_concs = sorted([x for x in tep_concs])

        ind = np.arange(len(atc_concs))  # the x locations for the groups
        width = 0.9 / len(tep_concs) # the width of the bars

        group_centers = [[] for x in xrange(len(atc_concs))]
        for tep_conc_count, tep_conc in enumerate(tep_concs):
            data = [mean_cis[name][atc_conc][tep_conc][0] for atc_conc in atc_concs]
            yerr = [
                mean_cis[name][atc_conc][tep_conc][0]-mean_cis[name][atc_conc][tep_conc][1]
                for atc_conc in atc_concs
            ]
            rects = ax.bar(ind + width*tep_conc_count + width/2.0, data, width, color=colors[tep_conc_count % len(colors)])
            bar_centers = [r.get_x()+r.get_width()/2.0 for r in rects]
            for i, center in enumerate(bar_centers):
                group_centers[i].append(center)
            color = colors[tep_conc_count % len(colors)]
            ax.errorbar(bar_centers, data, yerr=yerr,
                        # zorder = 4,
                        linewidth = 1, capthick = 1,
                        # lolims=True, uplims=True,
                        fmt='none', ecolor=(color[0], color[1], color[2], 1.0))

            # Plot all points
            y_pts = []
            x_pts = []
            for i, atc_conc in enumerate(atc_concs):
                for y_pt in mean_cis[name][atc_conc][tep_conc][3]:
                    x_pts.append(bar_centers[i])
                    y_pts.append(y_pt)
            rep_line = ax.plot(x_pts, y_pts, linewidth=0, marker='+', markersize=5.0, color='black')
            if name_count == 0:
                legend_info.append( (rects, 'TEP %.1E' % tep_conc) )

            # Plot stars for significant values
            star_xs = []
            star_ys = []
            for x, tup in zip(bar_centers, [mean_cis[name][atc_conc][tep_conc] for atc_conc in atc_concs]):
                y, y_min, y_max, y_pts = tup
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
            ax.set_ylabel('Fold signal over TEP 0')
        ax.set_title(name)
        ax.set_xticks(group_centers)
        ax.set_xticklabels( atc_concs )
        ax.set_xlabel( 'ATC conc. (M)' )

        subs = [2.0, 4.0, 6.0, 8.0]  # ticks to show per decade
        ax.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(subs=subs)) #set the ticks position
        # ax.yaxis.set_major_formatter(matplotlib.ticker.NullFormatter())   # remove the major ticks
        ax.yaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(fcm.ticks_format))  #add the custom ticks

    stars_proxy = matplotlib.lines.Line2D([], [], linewidth=0, marker='*', markersize=10.0, color='gold')
    pts_proxy = matplotlib.lines.Line2D([], [], linewidth=0, marker='+', markersize=5.0, color='black')
    legend_info.append( (stars_proxy, 'Sig. results') )
    legend_info.append( (pts_proxy, 'Replicates') )
    diffs_fig.suptitle('2015/10/15 - Mean biological replicate fold signal over TEP 0.0 conc. (IPTG 1mm) (mean of replicate means of gated distributions)', y=1.04)
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
