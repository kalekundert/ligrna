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

# master_sample_dir = '/kortemmelab/data/kyleb/cas9/151118/kyleb/1511018-5hour/96_well_flat_bottom'
master_sample_dir = '/dbscratch/kyleb/96_well_flat_bottom'

plate_1 = Plate([
    PlateInfo('cas9-design01', None, ['A1', 'B1']),
    PlateInfo('cas9-design02', None, ['A2', 'B2']),
    PlateInfo('cas9-design03', None, ['A3', 'B3']),
    PlateInfo('cas9-design04', None, ['A4', 'B4']),
    PlateInfo('cas9-design05', None, ['A5', 'B5']),
    PlateInfo('cas9-design06', None, ['A6', 'B6']),
    
    PlateInfo('cas9-design07', None, ['C1', 'D1', 'F6']),
    PlateInfo('cas9-design08', None, ['C2', 'D2']),
    PlateInfo('cas9-design09', None, ['C3', 'D3']),
    PlateInfo('cas9-design10', None, ['C4', 'D4']),
    PlateInfo('cas9-design11', None, ['C5', 'D5']),
    PlateInfo('cas9-design12', None, ['C6', 'D6']),

    PlateInfo('cas9-design13', None, ['E1', 'F1']),
    PlateInfo('cas9-design14', None, ['E2', 'F2']),
    PlateInfo('cas9-design15', None, ['E4', 'F4']),
    PlateInfo('cas9-wt', None, ['E5', 'F5', 'E6']),

    PlateInfo('sgRNA-NAA', None, ['A1-A6', 'C1-C6', 'E1', 'E2', 'E4', 'E6']),
    PlateInfo('sgRNA-NGG', None, ['E5', 'F6']),
    PlateInfo('sgRNA-empty', None, ['B1-B6', 'D1-D6', 'F1', 'F2', 'F4', 'F5']),
], sample_dir = master_sample_dir,
    name = 'replicate_1',
)

plate_2 = Plate([
    PlateInfo('cas9-design01', None, ['A7', 'B7']),
    PlateInfo('cas9-design02', None, ['A8', 'B8']),
    PlateInfo('cas9-design03', None, ['A9', 'B9']),
    PlateInfo('cas9-design04', None, ['A10', 'B10']),
    PlateInfo('cas9-design05', None, ['A11', 'B11']),
    PlateInfo('cas9-design06', None, ['A12', 'B12']),

    PlateInfo('cas9-design07', None, ['C7', 'D7', 'F11']),
    PlateInfo('cas9-design08', None, ['C8', 'D8']),
    PlateInfo('cas9-design09', None, ['C9', 'D9']),
    PlateInfo('cas9-design10', None, ['C10', 'D10']),
    PlateInfo('cas9-design11', None, ['C11', 'D11']),
    PlateInfo('cas9-design12', None, ['C12', 'D12']),

    PlateInfo('cas9-design13', None, ['E7', 'F7']),
    PlateInfo('cas9-design14', None, ['E8', 'F8']),
    PlateInfo('cas9-design15', None, ['E9', 'F9']),
    PlateInfo('cas9-wt', None, ['E10', 'F10', 'E11']),

    PlateInfo('sgRNA-NAA', None, ['A7-A12', 'C7-C12', 'E7', 'E8', 'E9', 'E11']),
    PlateInfo('sgRNA-NGG', None, ['E10', 'F11']),
    PlateInfo('sgRNA-empty', None, ['B7-B12', 'D7-D12', 'F7', 'F8', 'F9', 'F10']),
], sample_dir = master_sample_dir,
    name = 'replicate_2',
)

all_plates = [plate_1, plate_2]

def main():
    outer_fig_dir = os.path.join('script_output', os.path.basename(__file__).split('.')[0])
    gate_val = 0.6
    gate_name = 'poly_0.6'
    fig_dir = os.path.join(outer_fig_dir, gate_name)
    if not os.path.isdir(fig_dir):
        os.makedirs(fig_dir)
    gated_plates = make_gating_fig(all_plates, gate_val, gate_name, fig_dir, fast_run=True, plot_one_sample=True)

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
                if fast_run:
                    well_mean_low, well_mean_high = (well_mean, well_mean)
                else:
                    # Slow bootstrapping
                    try:
                        well_mean_low, well_mean_high = bootstrap.ci(channel_data, statfunction=np.average, method='pi')
                    except Exception:
                        well_mean_low, well_mean_high = (well_mean, well_mean)

                well_means[(cas9_name, sgrna_name)] = (well_mean, well_mean_low, well_mean_high)
                hist_output[(cas9_name, sgrna_name)] = well.plot(channel_name, bins=500, fc=color, lw=1, ax=ax, autolabel=False, stacked=True, label='%s' % (sgrna_name) )
                print exp.name, cas9_name + '-' + sgrna_name, len(channel_data), channel_data
                # Find 99th percentile limits
                this_xmax = np.max(channel_data)
                if this_xmax < xmax:
                    xmax = this_xmax
                this_xmin = np.min(channel_data)
                if this_xmin > xmin:
                    xmin = this_xmin
            ax.set_xlim( (xmin, min(xmax, 5000)) )

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
