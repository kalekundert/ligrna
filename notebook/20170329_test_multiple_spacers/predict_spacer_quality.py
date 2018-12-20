#!/usr/bin/env python3

"""\
Usage:
   predict_spacer_quality.py [options]
   predict_spacer_quality.py <spacer> <design> [options]

Arguments:
    <spacer>
        One of the spacers understood by the ``sgrna_sensor`` command, e.g. g1, 
        r1, d1, fol1, etc.

    <design>
        One of the following design names:
            - rxb 11,1
            - mhf 30
            - 3mx rxb 11,1
            - 3mx mhf 30

Options:
    -o --output <path>
        Write the plot the given path.  The image format (e.g. SVG, PNG, PDF, 
        etc) will be deduced from the path extension.
        
    -a --algorithm <name>     [default: mfe]
        Use the given algorithm to score the interaction between the spacer and 
        the aptamer.  Valid options are:

        mfe:
            Calculate the minimum free energy (MFE), only considering intra- 
            chain base-pairs.
        mfe-dimer:
            Calculate the minimum free energy (MFE), considering intra- and 
            inter-chain base-pairs.
        pf-dimer:
            Calculate the partition function normalized free energy (MFE), 
            considering intra- and inter-chain base-pairs.

    -m --max-change
        Plot the maximum change in cleavage, rather than the average change.  
        The maximum change might better reflect the true activity of the 
        sensors, because the assay is very sensitive to conditions (the age of 
        the Cas9 in particular).  So the maximum represents the most ideal 
        conditions.

    -A --aptamer-only
        Only consider interactions between the spacer and the aptamer, exclude 
        the linker sequences that were found during screening.

    -s --species NAME   [default: sp]
        Which species of Cas9 the spacer is for.
"""

import sys
import docopt
import RNA
import sgrna_sensor
import numpy as np
import matplotlib.pyplot as plt

from sgrna_sensor import densiometry
from scipy.stats import linregress
from color_me import ucsf

args = docopt.docopt(__doc__)

if args['--aptamer-only']:
    inserts = {
            'rxb 11,1':     'AUACCAGCCGAAAGGCCCUUGGCAG',
            'mhf 30':       'AUACCAGCCGAAAGGCCCUUGGCAG',
            '3mx rxb 11,1': 'AUACCAGCCGAAAGGCCAUUGGCAG',
            '3mx mhf 30':   'AUACCAGCCGAAAGGCCAUUGGCAG',
    }
else:
    inserts = {
            'rxb 11,1':     'GUGGGAUACCAGCCGAAAGGCCCUUGGCAGCCUAC',
            'mhf 30':        'GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC',
            '3mx rxb 11,1': 'GUGGGAUACCAGCCGAAAGGCCAUUGGCAGCCUAC',
            '3mx mhf 30':    'GCCGAUACCAGCCGAAAGGCCAUUGGCAGCGAC',
    }

def calc_energy(spacer, insert):
    if args['--algorithm'] == 'mfe':
        duplex = RNA.duplexfold(spacer, insert)
        return duplex.energy
    elif args['--algorithm'] == 'mfe-dimer':
        fc = RNA.fold_compound(f'{spacer}&{insert}')
        return fc.mfe_dimer()[1]
    elif args['--algorithm'] == 'pf-dimer':
        fc = RNA.fold_compound(f'{spacer}&{insert}')
        return fc.pf_dimer()[1]
    else:
        raise ValueError(f"unknown algorithm: '{args['--algorithm']}'")

def calc_energy_from_row(row):
    spacer = sgrna_sensor.spacer(row.spacer).seq
    insert = inserts[row.design]
    return calc_energy(spacer, insert)


if args['<spacer>'] and args['<design>']:
    spacer = sgrna_sensor.spacer(args['<spacer>'], species=args['--species']).rna
    insert = inserts[args['<design>']]
    print(f"Spacer: {spacer}")
    print(f"Insert: {insert}")
    print(f"ΔG:     {calc_energy(spacer, insert)}")

else:
    df = densiometry.load_cleavage_data_from_xlsx_dir('densiometry')
    df = densiometry.calc_mean_change(df)

    # Drop all the controls
    df = df[df.design.isin(inserts.keys())]


    # Calculate the minimum free energy (MFE) for binding between the spacer 
    # and the aptamer insert.
    df['binding_energy'] = df.apply(calc_energy_from_row, axis='columns')

    def plot_design(design, label, color): #
        i = df.design == design
        x = 100 * abs(df[i].max_change if args['--max-change'] else df[i].mean_change)
        y = df[i].binding_energy
        m, b, R, p, err = linregress(x, y)

        X = np.linspace(0, 100)
        Y = m * X + b

        plt.plot(x, y, 'o', color=color, label='_nolegend_')
        plt.plot(X, Y, '-', color=color, label=f'{label} (R={R:.3f})')

    plot_design('mhf 30', 'ligRNA⁺', ucsf.teal[0])
    plot_design('rxb 11,1', 'ligRNA⁻', ucsf.navy[0])
    plt.xlabel('Δ cleavage (%)')
    plt.ylabel('ΔG (kcal/mol)')
    plt.legend()
    plt.savefig(args.get('--output', 'predict_spacer_quality.svg'))

    if args['--output'] is None:
        plt.title(' '.join(sys.argv))
        plt.show()
