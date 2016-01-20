#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')
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
colors = [(0,0,1,0.3), (0,1,0,0.3), (1,0,0,0.3)]

master_sample_dir = '/kortemmelab/data/kyleb/cas9/151211_pam/55hour'

plate_1 = Plate([
    PlateInfo('cas9-design33v2', None, ['A1-A2']),
    PlateInfo('cas9-design580', None, ['A3-A4']),
    PlateInfo('cas9-design182', None, ['A5-A6']),
    PlateInfo('cas9-design223', None, ['A9-A10']),
    PlateInfo('cas9-wt', None, ['D1-D2']),

    PlateInfo('sgRNA-NAA', None, ['A2', 'A4', 'A6', 'A10']),
    PlateInfo('sgRNA-NGG', None, ['D2']),
    PlateInfo('sgRNA-empty', None, ['A1', 'A3', 'A5', 'A9', 'D1']),
], sample_dir = master_sample_dir,
    name = 'replicate_1',
)

plate_2 = Plate([
    PlateInfo('cas9-design33v2', None, ['B1-B2']),
    PlateInfo('cas9-design580', None, ['B3-B4']),
    PlateInfo('cas9-design182', None, ['B5-B6']),
    PlateInfo('cas9-design223', None, ['B9-B10']),
    PlateInfo('cas9-wt', None, ['E1-E2']),

    PlateInfo('sgRNA-NAA', None, ['B2', 'B4', 'B6', 'B10']),
    PlateInfo('sgRNA-NGG', None, ['E2']),
    PlateInfo('sgRNA-empty', None, ['B1', 'B3', 'B5', 'B9', 'E1']),
], sample_dir = master_sample_dir,
    name = 'replicate_2',
)

plate_3 = Plate([
    PlateInfo('cas9-design33v2', None, ['C1-C2']),
    PlateInfo('cas9-design580', None, ['C3-C4']),
    PlateInfo('cas9-design182', None, ['C5-C6']),
    PlateInfo('cas9-design223', None, ['C9-C10']),
    PlateInfo('cas9-wt', None, ['F1-F2']),

    PlateInfo('sgRNA-NAA', None, ['C2', 'C4', 'C6', 'C10']),
    PlateInfo('sgRNA-NGG', None, ['F2']),
    PlateInfo('sgRNA-empty', None, ['C1', 'C3', 'C5', 'C9', 'F1']),
], sample_dir = master_sample_dir,
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
    gated_plates = [make_individual_gating_fig(p, gate_val, gate_name, fig_dir, fast_run = fast_run, florescence_channel = channel_name, title = os.path.basename(__file__)) for p in all_plates]

    for exp in gated_plates:
        cas9_names = set()
        sgrna_names = set()
        for p in exp.experimental_parameters:
            if p.startswith('cas9-'):
                cas9_names.add(p)
            elif p.startswith('sgRNA-'):
              sgrna_names.add(p)
        cas9_names = sorted( x for x in cas9_names )
        sgrna_names = sorted( x for x in sgrna_names )

        plots_per_row = 4
        plot_cols = min(plots_per_row, len(cas9_names))
        plot_rows = len(cas9_names) / plots_per_row + 1
        current_plot_col = 1
        plate_fig = plt.figure(figsize=(22.0*plot_cols/3.0, 17.0*plot_rows/3.0), dpi=300)
        plot_num = 1
        plate_fig.suptitle(exp.name, fontsize=12)
        for cas9_name_i, cas9_name in enumerate(cas9_names):
            xlabel = True
            if current_plot_col == 1:
                ylabel = True
            else:
                ylabel = False
            ax = plate_fig.add_subplot(plot_rows, plot_cols, plot_num)
            plot_num += 1
            if current_plot_col == plot_cols:
                current_plot_col = 1
            else:
                current_plot_col += 1
            ax.grid(True)
            if xlabel:
                ax.set_xlabel('%s' % (cas9_name), size=18)
            if ylabel:
                ax.set_ylabel('Counts', size=18)
            hist_output = {}
            well_means = {}
            xmax = float('inf')
            xmin = float('-inf')
            for sgrna_name_i, sgrna_name in enumerate(sgrna_names):
                # print cas9_name, exp.well_set(cas9_name)
                # print sgrna_name, exp.well_set(sgrna_name)
                well_set = exp.well_set(cas9_name).intersection(exp.well_set(sgrna_name))
                if len(well_set) == 0:
                    continue
                well = exp.single_well_from_set(well_set)
                color = colors[sgrna_name_i % len(colors)]
                well_mean = well.data[channel_name].mean()
                channel_data = well.data[channel_name].as_matrix()
                
                if len(channel_data) == 0:
                    channel_data = [0.0000001]

                # Add pos/neg signal fold diff to mean diffs
                # Fast way to make code work and not bootstrap
                if True:
                    well_mean_low, well_mean_high = (well_mean, well_mean)
                else:
                    # Slow bootstrapping
                    try:
                        well_mean_low, well_mean_high = bootstrap.ci(channel_data, statfunction=np.average, method='pi')
                    except Exception:
                        well_mean_low, well_mean_high = (well_mean, well_mean)

                well_means[(cas9_name, sgrna_name)] = (well_mean, well_mean_low, well_mean_high)
                hist_output[(cas9_name, sgrna_name)] = well.plot(channel_name, bins=500, fc=color, lw=1, ax=ax, autolabel=False, stacked=True, label='%s %d' % (sgrna_name, int(well_mean)) )
                print exp.name, cas9_name + '-' + sgrna_name, len(channel_data), channel_data
                # Find 99th percentile limits
                this_xmax = np.max(channel_data)
                if this_xmax < xmax:
                    xmax = this_xmax
                this_xmin = np.min(channel_data)
                if this_xmin > xmin:
                    xmin = this_xmin
            ax.set_xlim( (xmin, min(10000, xmax) ) )

            ylim = ax.get_ylim()
            xlim = ax.get_xlim()
            for sgrna_name_i, sgrna_name in enumerate(sgrna_names):
                well_set = exp.well_set(cas9_name).intersection(exp.well_set(sgrna_name))
                if len(well_set) == 0:
                    continue
                well = exp.single_well_from_set(well_set)
                color = colors[sgrna_name_i % len(colors)]
                if (cas9_name, sgrna_name) in hist_output and hist_output[(cas9_name, sgrna_name)]:
                    n, bins, patches = hist_output[(cas9_name, sgrna_name)]
                    ax.plot((well_means[(cas9_name, sgrna_name)][0], well_means[(cas9_name, sgrna_name)][0]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='-', linewidth=2)
                    if well_means[(cas9_name, sgrna_name)][0] != well_means[(cas9_name, sgrna_name)][1] and well_means[(cas9_name, sgrna_name)][0] != well_means[(cas9_name, sgrna_name)][2]:
                        ax.plot((well_means[(cas9_name, sgrna_name)][1], well_means[(cas9_name, sgrna_name)][1]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='--', linewidth=1)
                        ax.plot((well_means[(cas9_name, sgrna_name)][2], well_means[(cas9_name, sgrna_name)][2]), (ylim[0], ylim[1]), color=(color[0], color[1], color[2], 1.0), linestyle='--', linewidth=1)

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

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        plot_gate_value()
