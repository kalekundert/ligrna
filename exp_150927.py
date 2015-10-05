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
channel_name = 'B-A'

plate_1 = Plate([
    PlateInfo('TEP_conc', 0.0, ['A1-E3']),
    PlateInfo('TEP_conc', 100.0e-6, ['A4-E6']), # 100 uM
    PlateInfo('TEP_conc', 1.0e-3, ['A7-E9']), # 1 mM

    PlateInfo('ATC_conc', 0.0, ['A1-E1','A4-E4','A7-E7']),
    PlateInfo('ATC_conc', 2.0e-6, ['A2-E2','A5-E5','A8-E8']), # 2uM
    PlateInfo('ATC_conc', 1.0e-6, ['A3-E3','A6-E6','A9-E9']), # 1uM

    PlateInfo('Control-Pos', None, 'A1-A9'),
    PlateInfo('Control-Neg', None, 'B1-B9'),
    PlateInfo('NX-0', None, 'C1-C9'),
    PlateInfo('US-0,0', None, 'D1-D9'),
    PlateInfo('NX2', None, 'E1-E9'),
    PlateInfo('Control-Blank', None, 'C12'),
], sample_dir = '/kortemmelab/data/kyleb/cas9/FCS/150927-3.1/150927-rfp-cas9_002-5.30pm/Plate1and2',
    name = 'replicate_1',
)

# Plate 2 was originally the same layout as plates 1 and 3,
# but was transferred to the extra space on plate 1 for ease of reading
plate_2 = Plate([
    PlateInfo('TEP_conc', 0.0, ['F1-H3', 'A10-C11']),
    PlateInfo('TEP_conc', 100.0e-6, ['F4-H6', 'D10-F11']), # 100 uM
    PlateInfo('TEP_conc', 1.0e-3, ['F7-H9', 'G10-H11', 'A12-B12']), # 1 mM

    PlateInfo('ATC_conc', 0.0, ['F1-H1', 'F4-H4', 'F7-H7', 'A10-A11', 'D10-D11', 'G10-G11']),
    PlateInfo('ATC_conc', 2.0e-6, ['F2-H2', 'F5-H5', 'F8-H8', 'B10-B11', 'E10-E11', 'H10-H11']), # 2uM
    PlateInfo('ATC_conc', 1.0e-6, ['F3-H3', 'F6-H6', 'F9-H9', 'C10-C11', 'F10-F11', 'A12-B12']), # 1uM

    PlateInfo('Control-Pos', None, 'F1-F9'),
    PlateInfo('Control-Neg', None, 'G1-G9'),
    PlateInfo('NX-0', None, 'H1-H9'),
    PlateInfo('US-0,0', None, ['A10-H10', 'A12']),
    PlateInfo('NX2', None, ['A11-H11', 'B12']),
    PlateInfo('Control-Blank', None, 'C12'),
], sample_dir = '/kortemmelab/data/kyleb/cas9/FCS/150927-3.1/150927-rfp-cas9_002-5.30pm/Plate1and2',
    name = 'replicate_2',
)

plate_3 = Plate([
    PlateInfo('TEP_conc', 0.0, ['A1-E3']),
    PlateInfo('TEP_conc', 100.0e-6, ['A4-E6']), # 100 uM
    PlateInfo('TEP_conc', 1.0e-3, ['A7-E9']), # 1 mM

    PlateInfo('ATC_conc', 0.0, ['A1-E1','A4-E4','A7-E7']),
    PlateInfo('ATC_conc', 2.0e-6, ['A2-E2','A5-E5','A8-E8']), # 2uM
    PlateInfo('ATC_conc', 1.0e-6, ['A3-E3','A6-E6','A9-E9']), # 1uM

    PlateInfo('Control-Pos', None, 'A1-A9'),
    PlateInfo('Control-Neg', None, 'B1-B9'),
    PlateInfo('NX-0', None, 'C1-C9'),
    PlateInfo('US-0,0', None, 'D1-D9'),
    PlateInfo('NX2', None, 'E1-E9'),
    PlateInfo('Control-Blank', None, 'F1'),
], sample_dir = '/kortemmelab/data/kyleb/cas9/FCS/150927-3.1/150927-rfp-cas9_002-5.30pm/Plate3',
    name = 'replicate_3',
)

all_plates = [plate_1, plate_2, plate_3]

exp_tep_concs = [
    (0.0, '0'),
    (100.0e-6, '100uM'),
    (1.0e-3, '1mM'),
]


def points_above_line(x_data, y_data, m, b):
    # Calculate y-intercepts for all points given slope m
    comp_bs = np.subtract(y_data, np.multiply(x_data, m))
    # Return number of points whose y intercept is above passed in b
    return np.count_nonzero(comp_bs > b)

def find_perpendicular_gating_line(x_data, y_data, threshold):
    # Returns the line parameters which give you a certain percentage (threshold) of population
    # above the line
    x_data = np.sort( x_data  )
    y_data = np.sort( y_data  )
    x_max = np.amax(x_data)
    y_max = np.amax(y_data)
    # y = mx + b
    m, b, r, p, stderr = scipy.stats.linregress(x_data, y_data)
    inv_m = -1.0 / m
    inv_b = y_max
    percent_above_line = points_above_line(x_data, y_data, inv_m, inv_b) / float(len(x_data))
    desired_points_above_line = int(threshold * len(x_data))
    def obj_helper(calc_b):
        return abs(points_above_line(x_data, y_data, inv_m, calc_b) - desired_points_above_line)
    res = scipy.optimize.minimize(obj_helper, inv_b, method='nelder-mead', options={'disp': False, 'maxiter': 1000})
    inv_b = res.x[0]
    return (inv_m, inv_b)

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h

def main():
    outer_fig_dir = os.path.join('script_output', 'exp_150927')

    if fast_run:
        plot_gate_value('poly_0.6', 0.6, outer_fig_dir)
    else:
        func_args = []
        # Append fsc threshold gates
        fsc_gate_above = -20000.0
        while fsc_gate_above <= 60000.0:
            break
            fsc_gate_above += 10000.0
            func_args.append( ('fsc_%d'% int(fsc_gate_above), fsc_gate_above, outer_fig_dir) )
        # Append poly gates
        for gate_val in np.arange(0.1,1.0,0.1):
            if gate_val != 0.6:
                continue
            func_args.append( ('poly_%.1f' % gate_val, gate_val, outer_fig_dir) )

        for arg_tup in func_args:
            run_subprocess

        pool = mp.Pool()
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
        assert( len(blank_samples) == 1 )
        blank_sample = exp.samples[blank_samples[0]]
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

            gate_m, gate_b = find_perpendicular_gating_line( np.concatenate(all_exp_data_fsc), np.concatenate(all_exp_data_ssc), gate_val)

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


        exp.gate(gate)
        blank_sample.plot(['FSC-A', 'SSC-A'], kind='scatter', color='red', s=2, alpha=1.0, gates=[gate], label='Blank media', ax=ax)
        ax.grid(True)
        ax.legend()

        tep_wells = {}
        for tep_conc, tep_conc_name in exp_tep_concs:
            tep_wells[tep_conc] = exp.well_set('TEP_conc', tep_conc)

        plot_rows = len(exp.parameter_values('ATC_conc'))
        plot_cols = len(exp.experimental_parameters)
        plate_fig = plt.figure(figsize=(22.0*len(exp.experimental_parameters)/3.0, 17.0*len(exp.parameter_values('ATC_conc'))/3.0), dpi=300)
        plot_num = 1
        plate_fig.suptitle(exp.name, fontsize=12)
        for atc_conc_count, atc_conc in enumerate(exp.parameter_values('ATC_conc')):
            atc_wells = exp.well_set('ATC_conc', atc_conc)
            for name_count, name in enumerate(exp.experimental_parameters):
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
                    ax.set_ylabel('%s - ATC Conc. %s' % ('Count', atc_conc), size=18)
                plot_num += 1
                exp_wells = exp.well_set(name).intersection(atc_wells)
                exp_tep_wells = {}
                for tep_conc, tep_conc_name in exp_tep_concs:
                    exp_tep_wells[tep_conc] = list(tep_wells[tep_conc].intersection(exp_wells))
                    assert( len(exp_tep_wells[tep_conc]) == 1 )
                    exp_tep_wells[tep_conc] = exp_tep_wells[tep_conc][0]
                tep_means = {}
                hist_output = {}
                count = 0
                colors = [(0,0,1,0.3), (0,1,0,0.3), (1,0,0,0.3)]
                for tep_conc, tep_conc_name in exp_tep_concs:
                    color = colors[count % len(colors)]
                    tep_mean = exp.samples[exp_tep_wells[tep_conc]].data[channel_name].mean()

                    # Fast way to make code work and not bootstrap
                    if fast_run:
                        tep_mean_low, tep_mean_high = (tep_mean, tep_mean)
                    else:
                        # Slow bootstrapping
                        try:
                            tep_mean_low, tep_mean_high = bootstrap.ci(exp.samples[exp_tep_wells[tep_conc]].data[channel_name].as_matrix(), statfunction=np.average, method='bca', n_samples=15000)
                        except Exception:
                            tep_mean_low, tep_mean_high = (tep_mean, tep_mean)

                    tep_means[tep_conc] = (tep_mean, tep_mean_low, tep_mean_high)
                    hist_output[tep_conc] = exp.samples[exp_tep_wells[tep_conc]].plot(channel_name, bins=40, fc=color, lw=1, ax=ax, autolabel=False, stacked=True, label='%s TEP - %.0f (%.0f-%.0f)' % (tep_conc_name, tep_mean, tep_mean_low, tep_mean_high) )
                    count += 1

                # blank_sample.plot(channel_name, bins=100, alpha=0.1, color='black', label='blank media', ax=ax)
                ylim = ax.get_ylim()
                xlim = ax.get_xlim()
                count = 0
                for tep_conc, tep_conc_name in exp_tep_concs:
                    if tep_conc != 0.0:
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
                mean, mean_low, mean_high = mean_confidence_interval( mean_cis[name][atc_conc][tep_conc].values() )
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
    for name_count, name in enumerate(mean_cis):
        if len(axes) == 0:
            ax = diffs_fig.add_subplot(1, len(mean_cis), name_count+1)
        else:
            ax = diffs_fig.add_subplot(1, len(mean_cis), name_count+1, sharey=axes[0])
        axes.append(ax)
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

        ax.set_ylim( (0.0, 10.0) )
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
    diffs_fig.suptitle('Experiment %s - Mean biological replicate fold signal over TEP 0.0 conc. (mean of replicate means of gated distributions)' % exp.name, y=1.04)
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
