#!/usr/bin/env python3

"""\
Plot activities measured in the β-galactosidase assay.

Usage:
    miller_units.py [<layout.toml>...] [-o PREFIX] [-PFbB] [--figure-mode]

Arguments:
    <layout.toml>
        One or more TOML-formatted configuration files defining how each well 
        in a particular plate should be interpreted.  See the 'Configuration' 
        section below for more details.  By default, the newest layout file in 
        the plate reader directory will be used.
        
Options:
    -o --output PREFIX
        Path name to use to prefix the output plots.  For example, if you give 
        `--output bgal`, the following files would be created: `bgal_fits.svg`, 
        `bgal_miller.svg`, and `bgal_fold.svg`.
        
    -P --parse-only
        Load the given config file and print it out, then exit.

    -F --fits-only
        Only show the linear fits.  This is useful when fine-tuning the 
        parameters for each fit.

    -b --subtract-intercept
        When plotting the fits, adjust the data so that all of the linear fits 
        go through zero.  This is sometimes helpful for displaying data from 
        different days on the same plots.

    -B --bars-only
        Only show the bar plots.  This is useful if you already know that all 
        the fits make sense.

    --figure-mode
        Tweak a number of visual parameters to get a plot suitable for the 
        paper.

Configuration:
    Below is a list of the keys that are understood in the configuration file:

    'xlsx_path' [string]
        The path to the XLSX file containing the plate reader data, relative to 
        the configuration file itself.  If not specified, this script will look 
        for a file with the same name as the configuration file, but the 
        '.xlsx' extension, e.g. 'abc.xlsx' if the config file is 'abc.toml'.

    'template' [string]
        The path to another TOML file that should be interpreted as containing 
        default values for all possible settings.

    'notes' [string]
        A string that will be printed every time the file is visualized.  This 
        is meant to reminder the user of any details relating to this 
        particular experiment (e.g. mistakes) that might affect interpretation 
        of the data.

    'primary_key' [string, default: 'sgrna']
        The primary variable being manipulated in the experiments.  This is 
        used to organize the "fits" and "fold" plots.  It can be one of the 
        keys mentioned below, or a custom key specific to the file in question.  

    'secondary_key' [string, default: 'spacer']
        The secondary variable being manipulated in the experiments.  This is 
        used to organize the "fits" and "fold" plots.  It can be one of the 
        keys mentioned below, or a custom key specific to the file in question.  

    'dead_time_min' [number]
        The amount of time (in minutes) that elapsed between when the reaction 
        was started and the plate reader measurements began.  This is only 
        there for the sake of record-keeping; it's not used in any of the 
        analysis.

    The following keys relate to particular wells.  Each of these keys can be 
    specified in any of four kinds of block: [well.A1], [row.A], [col.1], and 
    [plate].  The [well] block allows values to be set for individual wells ('A1' 
    in this example).  The [row] and [col] blocks allow values to be set for 
    whole rows and columns ('A' and '1' in these examples).  The [plate] block 
    allows values to be set for the whole plate.  The same value can be set 
    multiple times, in which case the value from the most specific block will 
    take precedence.

    'sgrna' [string]
        The name of the sgRNA, e.g. 'on', 'off', 'rxb 11,1', 'mhf 30', etc.

    'spacer' [string]
        The name of the target sequence, e.g. 'lz', 'li', 'la', 'lo', 'lp'.

    'ligand' [bool]
        Whether or not theophylline was present in the reaction.

    'blank' [string]
        The name of the well (e.g. 'A1') to use as a blank.  All of the 
        absorbance values for this well (e.g. OD600 and A420) will have the 
        corresponding values from their blank well subtracted from them.  You 
        can also specify just a row ('A') or just a column ('1'), in which case 
        the unspecified value will be taken from the well itself (e.g. putting 
        "blank = 'A'" in the [row.B] block would cause A1 to blank B1, A2 to 
        blank B2, and so on).

    'od600_blank' [string]
        Like 'blank', but only for OD600.

    'a420_blank' [string]
        Like 'blank', but only for A420.

    'min_time' [number, default: 0]
        When making linear fits, ignore any data points before the given time 
        (in minutes).  This is necessary because the early data points can be 
        non-linear as the lysis reaction proceeds.

    'max_time' [number]
        When making linear fits, ignore any data points after the given time 
        (in minutes).  It's usually better to use 'max_a420' (see below), but 
        sometimes this is more convenient.

    'max_a420' [number, default: 1.9]
        When making linear fits, ignore any data points with A420 values larger 
        than the given maximum.  This is necessary because ONPG becomes 
        limiting once the reaction has progressed far enough.

    'culture_volume_uL' [number, default: 100]
        The volume of cells (in µL) added to the reaction.
"""

import re
import sys
import docopt
import toml
import itertools
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import sgrna_sensor

from pathlib import Path
from color_me import ucsf
from sgrna_sensor.plate_reader import BiotekExperiment
from sgrna_sensor.style import pick_color, pick_style, FoldChangeLocator
from nonstdlib import inf, nan

pd.set_option('display.max_rows', 500)

class Reaction:

    def __init__(self, expt, well):
        self.expt = expt
        self.meta = expt['well'][well]
        self.well = well
        self.sgrna = self.meta['sgrna']
        self.spacer = self.meta['spacer']
        self.ligand = self.meta['ligand']
        self.apo_holo = 'holo' if self.ligand else 'apo'
        self.keys = (
                expt.get('primary_key', 'spacer'),
                expt.get('secondary_key', 'sgrna'),
        )
        self.key = tuple(self.meta[x] for x in self.keys)
        self.label = self.meta.get('label', 
                ' '.join(self.meta[x] for x in self.keys))

        df = expt['data'].kinetic[420]\
                .query('well == @well').reset_index(drop=True)
        self.t_min = self.raw_t_min = df['minutes']
        self.a420 = self.raw_a420 = df['read']
        self.od600 = self.raw_od600 = expt['data'].reads[600][well]
        self.vol_mL = self.meta['culture_volume_uL'] / 1000

        # If a blank well was given, subtract it from the absorbance 
        # measurements.
        self.a420_blank_well = self._blank_well('a420')
        self.od600_blank_well = self._blank_well('od600')
        self.a420_blank = np.zeros(len(self.a420))
        self.od600_blank = 0

        if self.a420_blank_well:
            self.a420_blank = df[self.a420_blank_well]
            self.a420 -= self.a420_blank
        if self.od600_blank_well:
            self.od600_blank = expt['data'].reads[600][self.od600_blank_well]
            self.od600 -= self.od600_blank

        self.i_min = i = self._first_timepoint()
        self.i_max = j = self._last_timepoint()
        self.fit_t_min = self.t_min[i:j]
        self.fit_a420 = self.a420[i:j]

        try:
            self.miller, self.fit = miller_units(
                    self.fit_t_min,
                    self.fit_a420,
                    self.od600,
                    self.vol_mL,
            )
        except Exception as e:
            print(f"Failed to fit line for well {well}: i_min={i}; i_max={j}")
            self.miller, self.fit = nan, (nan, nan)

    def __repr__(self):
        return f'<Reaction well={self.well} miller={self.miller:.1f} date={self.expt["data"].date.strftime("%Y-%m-%d")}>'

    def __str__(self):
        from pprint import pformat

        class TruncatedRepr:

            def __init__(self, a):
                self.a = a

            def __repr__(self):
                a = np.asarray(self.a)
                return f'[{a[0]} {a[1]} {a[2]} ... {a[-3]} {a[-2]} {a[-1]}]'

        return pformat(dict(
                well=self.well,
                sgrna=self.sgrna,
                ligand=self.ligand,
                t_min=TruncatedRepr(self.t_min),
                a420=TruncatedRepr(self.a420),
                od600=self.od600,
                vol_mL=self.vol_mL,
                i_min=self.i_min,
                i_max=self.i_max,
                miller=self.miller,
                fit=self.fit,
        ))

    def _first_timepoint(self):
        # Some traces curve upwards in the early timepoints, perhaps as cell 
        # lysis continues.  Here we decide the first timepoint to include.
        min_time = self.meta['min_time']
        return abs(self.t_min - min_time).idxmin()

    def _last_timepoint(self):
        # Some traces curve downwards once A420 gets too high, presumably as 
        # the substrate begins to be limiting.  The user can also specify the 
        # latest timepoint they want to include.

        i = self.i_min  # Don't count points before the time cutoff.
        max_a420 = self.meta['max_a420']
        max_t = self.meta.get('max_time', self.t_min.iloc[-1])
        return max(i+2, min(
                abs( self.a420.iloc[i:] - max_a420).idxmin(),
                abs(self.t_min.iloc[i:] - max_t   ).idxmin(),
        ))

    def _blank_well(self, channel):
        blank_well = self.meta.get(f'{channel}_blank', self.meta.get('blank'))

        if blank_well is None:
            return None

        row_col_pat = re.compile('^([A-H])?([0-9]{1,2})?$')
        blank_match = row_col_pat.match(blank_well)
        well_match = row_col_pat.match(self.well)

        if not blank_match:
            raise ValueError(f"blank well '{blank_well}' doesn't seem like a well.")
        if not well_match:
            raise ValueError(f"well '{self.well}' doesn't seem like a well.")

        blank_row, blank_col = blank_match.groups()
        well_row, well_col = well_match.groups()

        if blank_row and blank_col:
            return blank_row + blank_col

        elif blank_row and not blank_col:
            return blank_row + well_col

        elif not blank_row and blank_col:
            return well_row + blank_col

        else:
            raise AssertionError()

    def linear_fit(self, x):
        return np.polyval(self.fit, x)

def load_expt(toml_path):

    def recursive_merge(expt, defaults, overwrite=False):
        for key, default in defaults.items():
            if isinstance(default, dict):
                expt.setdefault(key, {})
                recursive_merge(expt[key], default)
            else:
                if overwrite or key not in expt:
                    expt[key] = default

    def do_load_paths(toml_path):
        toml_path = Path(toml_path).resolve()
        expt = toml.load(str(toml_path))
        expt['toml_path'] = toml_path

        # Resolve the path the actual data.
        if 'xlsx_path' in expt:
            expt['xlsx_path'] = toml_path.parent / expt['xlsx_path']
        else:
            default_xlsx = toml_path.parent / f'{toml_path.stem}.xlsx'
            if default_xlsx.exists():
                expt['xlsx_path'] = default_xlsx

        if 'xlsx_path' in expt:
            expt['data'] = BiotekExperiment(str(expt['xlsx_path']))

        # Include a remote file if one is specified.  
        if 'template' in expt:
            expt['template'] = toml_path.parent / expt['template']
            template = do_load_paths(expt['template'])
            recursive_merge(expt, template)

        return expt

    expt = do_load_paths(toml_path)

    # Complain if `xlsx_path` isn't defined.

    # It's ok for individual files to not include `xlsx_path`, because it might 
    # be filled in by default, or implied from a template file.  But by the 
    # time we get here, we need to know where the data is.

    if 'xlsx_path' not in expt:
        raise ValueError(f"no xlsx path specified or inferred in '{toml_path}'")

    # Apply any row or column defaults.
    if 'well' not in expt:
        expt['well'] = {}

    rows = expt.get('row', {})
    cols = expt.get('col', {})

        # Create new wells implied by the 'row' and 'col' blocks.
    for row, col in itertools.product(rows, cols):
        expt['well'].setdefault(f'{row}{col}', {})

        # Update any existing wells.
    for well in expt.get('well', {}):
        row, col = well[:1], well[1:]
        recursive_merge(expt['well'][well], rows.get(row, {}))
        recursive_merge(expt['well'][well], cols.get(col, {}))

    # Apply any plate-wide defaults.
    recursive_merge(
            expt.setdefault('plate', {}),
            dict(
                culture_volume_uL=100,
                min_time=0,
                max_a420=1.9,
            )
    )
    for well in expt.get('well', {}):
        recursive_merge(expt['well'][well], expt['plate'])

    # If the experiment has any notes, print them out.
    if 'notes' in expt:
        print(toml_path)
        print(expt['notes'].strip())
        print()

    return expt

def load_reactions(expts):
    from natsort import natsorted
    rxns = []

    for expt in expts:
        for well in natsorted(expt['well']):
            rxn = Reaction(expt, well)
            rxns.append(rxn)

    return rxns

def load_keys(rxns):
    primary_keys, secondary_keys = {}, {}

    for _, rxn in iter_reactions(rxns):
        primary_key, secondary_key = rxn.keys

        attr_1 = rxn.meta[primary_key]
        if attr_1 not in primary_keys:
            primary_keys[attr_1] = len(primary_keys)

        attr_2 = rxn.meta[secondary_key]
        if attr_2 not in secondary_keys:
            secondary_keys[attr_2] = len(secondary_keys)

    return primary_keys, secondary_keys

def iter_reactions(rxns):
    yield from enumerate(rxns)

def miller_units(t_min, a420, od600, vol_mL):
    m, b = np.polyfit(t_min, a420, 1)
    path_cm = 0.25
    return 1000 * m * path_cm / (od600 * vol_mL), (m, b)

def plot_fits(rxns, stem, subtract_intercept=False, figure_mode=False):
    rows, cols = load_keys(rxns)

    if figure_mode:
        subtract_intercept = True

    size_in = 1.5 if figure_mode else 3.0
    fig_size_in = size_in * len(cols), size_in * len(rows)
    fig, axes = plt.subplots(
            len(rows), len(cols),
            figsize=fig_size_in,
            squeeze=False,
            sharex=True,
            sharey=figure_mode,
    )
    max_t = 0
    min_a420 = {x: inf for x in itertools.product(rows.values(), cols.values())}
    max_a420 = {x: -inf for x in itertools.product(rows.values(), cols.values())}

    for _, rxn in iter_reactions(rxns):
        b = rxn.fit[1] if subtract_intercept else 0
        t, y = rxn.t_min, rxn.a420 - b
        i, j = rxn.i_min, rxn.i_max

        fit_style = pick_style(rxn.sgrna, not rxn.ligand)
        fit_style['label'] = rxn.well
        data_style = fit_style.copy(); data_style.pop('dashes', None)
        data_style.update(marker='+', linestyle='none', label='_nolabel_')
        trim_style = data_style.copy()
        trim_style.update(marker='_', markerfacecolor='none')

        row_key, col_key = rxn.keys
        row = rows[rxn.meta[row_key]]
        col = cols[rxn.meta[col_key]]
        ax = axes[row,col]

        ax.plot(t.iloc[:i], y.iloc[:i], **trim_style)
        ax.plot(t.iloc[i:j], y.iloc[i:j], **data_style)
        ax.plot(t.iloc[j:], y.iloc[j:], **trim_style)

        if rxn.miller != nan:
            ax.plot(t, rxn.linear_fit(t) - b, **fit_style)

        if figure_mode:
            min_a420[row,col] = 0
            max_a420[row,col] = 1
        else:
            min_a420[row,col] = min(min_a420[row,col], min(rxn.a420 - b))
            max_a420[row,col] = max(max_a420[row,col], max(rxn.a420 - b))

        if figure_mode:
            max_t = 20
        else:
            max_t = max(max_t, max(rxn.t_min))

        label = '\n'.join(textwrap.wrap(
            f'{rxn.meta[row_key]} {rxn.meta[col_key]}',
            width=9, break_long_words=False,
        ))
        if not figure_mode:
            ax.legend(title=label, loc='upper left')

    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            ax.set_ylim(min_a420[i,j], max_a420[i,j])

    for ax in axes[-1,:]:
        ax.set_xlabel('time (min)')
    for ax in axes[:,-1 if figure_mode else 0]:
        box = dict(facecolor='yellow')
        ax.set_ylabel('ΔA420' if subtract_intercept else 'A420')
    for ax in axes.flat:
        ax.set_xlim(0, max_t)

    if figure_mode:
        for ax in axes.flat:
            ax.yaxis.set_tick_params(left=False, labelleft=False)
        for ax in axes[:,-1]:
            ax.yaxis.set_tick_params(right=True, labelright=True)
            ax.yaxis.set_label_position("right")

    finalize_plot(fig, stem, 'fits')

def plot_miller_units(rxns, stem, figure_mode=False):
    if figure_mode:
        return

    num_spacers = len({rxn.spacer for i, rxn in iter_reactions(rxns)})
    fig, axes = plt.subplots(4, 1, figsize=(1 + 3 * num_spacers, 8))
    style = dict(linewidth=5)
    xticks = []

    for i, rxn in iter_reactions(rxns):
        style = dict(
                linewidth=5,
                color=pick_color(rxn.sgrna),
        )
        raw_style = dict(
                linewidth=5,
                color=pick_color(rxn.sgrna, lightness=2),
        )
        x = [i, i]
        ys = [
                (0, [0, rxn.fit[0]],    style),
                (1, [0, rxn.raw_od600], raw_style),
                (1, [0, rxn.od600],     style),
                (2, [0, rxn.vol_mL],    style),
                (3, [0, rxn.miller],    style),
        ]
        xticks.append((i, f'{rxn.apo_holo} {rxn.label}'))

        for j, y, style in ys:
            axes[j].plot(x, y, **style)


    xticks, xticklabels = zip(*xticks)
    axes[3].set_xticklabels(xticklabels, rotation='vertical')

    for ax in axes:
        ax.set_ylim(0, ax.get_ylim()[1])
        ax.set_xlim(xticks[0] - 0.5, xticks[-1] + 0.5)
        ax.set_xticks(xticks)
        if ax is not axes[3]:
            ax.tick_params(labelbottom=False)

    axes[0].set_ylabel('d[A420]/dt')
    axes[1].set_ylabel('OD600')
    axes[2].set_ylabel('volume (mL)')
    axes[3].set_ylabel('Miller units')

    finalize_plot(fig, stem, 'miller')

def plot_miller_units(rxns, stem, figure_mode=False):
    primary_keys, secondary_keys = load_keys(rxns)
    n1, n2 = len(primary_keys), len(secondary_keys)

    fig, ax = plt.subplots(figsize=(1 + 1 * len(primary_keys), 3))
    style = dict(linewidth=5)
    xticks = []

    apos = {}
    holos = {}
    miller_units = {False: [], True: []}
    fold_changes = {}

    replicates = {}
    colors = {}
    
    for i, rxn in iter_reactions(rxns):
        colors[rxn.key] = pick_color(rxn.sgrna)
        replicates.setdefault(rxn.key, {})\
                  .setdefault(rxn.ligand, [])\
                  .append(rxn)

    for key in replicates:
        apos = np.array([x.miller for x in replicates[key][False]])
        holos = np.array([x.miller for x in replicates[key][True]])

        i = primary_keys[key[0]]
        j = secondary_keys[key[1]]

        x = i * (len(primary_keys) + 1) + j
        x_apo = 2 * x
        x_holo = 2 * x + 1

        xticks.append((x_apo, ' '.join(key + ('apo',))))
        xticks.append((x_holo, ' '.join(key + ('holo',))))

        y_apo = np.mean(apos)
        y_apo_err = np.std(apos)
        y_holo = np.mean(holos)
        y_holo_err = np.std(holos)

        ax.plot([x_apo,x_apo], [0,y_apo], color=colors[key], **style)
        ax.plot([x_holo,x_holo], [0,y_holo], color=colors[key], **style)

        ax.errorbar([x_apo], [y_apo], y_apo_err, color=colors[key])
        ax.errorbar([x_holo], [y_holo], y_holo_err, color=colors[key])

    xticks, xticklabels = zip(*xticks)
    ax.set_xlim(xticks[0] - 0.5, xticks[-1] + 0.5)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation='vertical')
    ax.set_ylabel('Miller Units')
    ax.set_ylim(0, ax.get_ylim()[1])
    ax.yaxis.set_major_locator(FoldChangeLocator(6))
    ax.yaxis.grid()

    fig.tight_layout()
    finalize_plot(fig, stem, 'miller')

def plot_fold_changes(rxns, stem, figure_mode=False):
    primary_keys, secondary_keys = load_keys(rxns)
    n1, n2 = len(primary_keys), len(secondary_keys)

    # 1.739: To get same axes height at TMP MIC panel.
    wh = (3.325, 1.739) if figure_mode else (1 + 1* len(primary_keys), 3)
    fig, ax = plt.subplots(figsize=wh)
    style = dict(linewidth=5)
    xticks = []

    apos = {}
    holos = {}
    miller_units = {False: [], True: []}
    fold_changes = {}

    replicates = {}
    colors = {}
    
    for i, rxn in iter_reactions(rxns):
        colors[rxn.key] = pick_color(rxn.sgrna)
        replicates.setdefault(rxn.key, {})\
                  .setdefault(rxn.ligand, [])\
                  .append(rxn)

    for key in replicates:
        apos = np.array([x.miller for x in replicates[key][False]])
        holos = np.array([x.miller for x in replicates[key][True]])
        fold_changes = holos / apos

        #i = primary_keys[key[0]]
        #j = secondary_keys[key[1]]
        #x0 = i * (len(primary_keys) + 1) + j
        #n = len(fold_changes)

        #for k, fold_change in enumerate(fold_changes):
        #    x = [x0*n + k, x0*n + k]
        #    y = [0, fold_change if fold_change > 1 else 1/fold_change]
        #    xticks.append((x[0], ' '.join(key)))
        #    ax.plot(x, y, color=colors[key], **style)

        i = primary_keys[key[0]]
        j = secondary_keys[key[1]]
        x = i * (len(primary_keys) + 1) + j
        xticks.append((x, ' '.join(key)))

        # For visualization purposes, I always want the fold_change to be 
        # greater than one.  But I don't want to enforce this until after the 
        # mean fold change has been calculated.
        if np.mean(fold_changes) < 1:
            fold_changes = 1 / fold_changes

        y = np.mean(fold_changes)
        yerr = np.std(fold_changes)

        ax.plot([x,x], [0,y], color=colors[key], **style)
        ax.errorbar([x], [y], yerr, color=colors[key])

    xticks, xticklabels = zip(*xticks)
    ax.set_xlim(xticks[0] - 0.5, xticks[-1] + 0.5)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation='vertical')
    ax.set_ylabel('Fold change')
    ax.set_ylim(0, ax.get_ylim()[1])
    ax.yaxis.set_major_locator(FoldChangeLocator(6))
    ax.yaxis.grid()

    finalize_plot(fig, stem, 'fold')

def finalize_plot(fig, stem, suffix):
    #fig.tight_layout()

    def px_from_top(dy):
        y_disp, _ = fig.transFigure.transform((1,0)) - dy
        y_fig, _ = fig.transFigure.inverted().transform((y_disp, 0))
        return y_fig

    fig.subplots_adjust(top=px_from_top(35))
    fig.suptitle(stem, y=px_from_top(5))
    fig.savefig(f'plots/{stem}_{suffix}.svg')


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    if args['<layout.toml>']:
        toml_paths = args['<layout.toml>']
    else:
        all_toml_paths = Path('plate_reader').glob('*.toml')
        toml_paths = [sorted(all_toml_paths)[-1]]
        print(toml_paths[0])

    expts = [load_expt(x) for x in toml_paths]

    if args['--parse-only']:
        pprint(expts)
        sys.exit()

    if args['--output']:
        out = args['--output']
    elif len(expts) == 1:
        out = expts[0]['toml_path'].stem
    else:
        print("Error: need to specify --output if there are multiple inputs.")
        sys.exit(1)

    rxns = load_reactions(expts)

    if not args['--bars-only']:
        plot_fits(rxns, out, args['--subtract-intercept'], args['--figure-mode'])
    if not args['--fits-only']:
        plot_miller_units(rxns, out, args['--figure-mode'])
        plot_fold_changes(rxns, out, args['--figure-mode'])

    try: plt.show()
    except KeyboardInterrupt: print()


