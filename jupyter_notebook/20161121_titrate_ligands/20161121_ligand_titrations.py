#!/usr/bin/env python3

import sys, numpy as np
import matplotlib.pyplot as plt
from parse_biotek import parse_biotek
from pprint import pprint


data = parse_biotek('20161121_ligand_titrations.txt')
concentrations = {
        'amm': 2000/2**np.arange(10),
        '3mx': 2000/2**np.arange(10),
        'add': 2000/2**np.arange(10),
        'thi': 2000/2**np.arange(10),
}
ligands = {
        'amm': [
            ['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11'],
            ['B11', 'B10', 'B9', 'B8', 'B7', 'B6', 'B5', 'B4', 'B3', 'B2'],
        ],
        '3mx': [
            ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11'],
            ['D11', 'D10', 'D9', 'D8', 'D7', 'D6', 'D5', 'D4', 'D3', 'D2'],
        ],
        'add': [
            ['E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11'],
            ['F11', 'F10', 'F9', 'F8', 'F7', 'F6', 'F5', 'F4', 'F3', 'F2'],
        ],
        'thi': [
            ['G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11'],
            ['H11', 'H10', 'H9', 'H8', 'H7', 'H6', 'H5', 'H4', 'H3', 'H2'],
        ],
}
full_ligand_names = {
        'amm': 'Ammeline',
        '3mx': '3-Methylxanthine',
        'add': 'Adenine',
        'thi': 'Thiamine',
}

def smooth_growth(data, well):
    from scipy.interpolate import splrep, splev
    x = data.timepoints
    y = data.trajectories[well]
    f = splrep(x, y)
    return splev(x, f)

def growth_rate(data, well):
    return np.gradient(data.trajectories[well])

def smooth_growth_rate(data, well):
    return np.gradient(smooth_growth(data, well))

def time_to_peak_growth(data, well):
    max_rate_i = np.argmax(growth_rate(data, well))
    return data.timepoints[max_rate_i]

def plot_peak_growth_vs_ligand(data, ligand):
    for replicate in ligands[ligand]:
        t = [time_to_peak_growth(data, well) for well in replicate]
        plt.semilogx(concentrations[ligand], t)

    plt.title('{}'.format(full_ligand_names[ligand]))
    plt.xlabel('[{}] (μM)'.format(full_ligand_names[ligand].lower()))
    plt.ylabel('time to peak growth rate (hours)')

def plot_growth(data, ligand, i):
    colors = 'blue', 'green'
    for j, replicate in enumerate(ligands[ligand]):
        # Black: No ligand
        well = replicate[-1]
        plt.plot(data.timepoints, data.trajectories[well], 'k--')
        k = np.argmax(growth_rate(data, well))
        plt.plot(data.timepoints[k], data.trajectories[well][k], 'ko')

        # Blue/green: Ligand titration
        c = colors[j]
        well = replicate[i]
        plt.plot(data.timepoints, data.trajectories[well], color=c, label=well)
        k = np.argmax(growth_rate(data, well))
        plt.plot(data.timepoints[k], data.trajectories[well][k], 'o', color=c)

    plt.title('[{}] = {} μM'.format(
        full_ligand_names[ligand].lower(), concentrations[ligand][i]))
    plt.xlabel('time (hours)')
    plt.ylabel('OD600')
    plt.ylim(0, 1)

def plot_growth_rate(data, ligand, i):
    colors = 'blue', 'green'
    for j, replicate in enumerate(ligands[ligand]):
        well = replicate[-1]
        plt.plot(data.timepoints, growth_rate(data, well), 'k--')

        c = colors[j]
        well = replicate[i]
        plt.plot(data.timepoints, growth_rate(data, well), label=well, color=c)

    plt.title('[{}] = {} μM'.format(
        full_ligand_names[ligand].lower(), concentrations[ligand][i]))
    #plt.legend(loc='best')
    plt.xlabel('time (hours)')
    plt.ylabel('OD600/hour')
    plt.ylim(-0.01, 0.05)

if __name__ == '__main__':
    #plt.subplot(311); plot_peak_growth_vs_ligand(data, sys.argv[1])
    #plt.subplot(312); plot_growth(data, sys.argv[1], int(sys.argv[2]))
    #plt.subplot(313); plot_growth_rate(data, sys.argv[1], int(sys.argv[2]))

    #plot_peak_growth_vs_ligand(data, sys.argv[1])
    #plt.figure()
    for i in range(10):
        plt.subplot(2, 10, i+1); plot_growth(data, sys.argv[1], i)
        plt.subplot(2, 10, i+11); plot_growth_rate(data, sys.argv[1], i)

    plt.gcf().canvas.mpl_connect('resize_event', lambda x: plt.tight_layout())
    plt.show()
