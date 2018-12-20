#!/usr/bin/env python3

"""\
Usage:
    show_titrations.py <ligand> [<channel>] [options]

Options:
    -t --time-limit <hours>   [default: 12]
        How many hours of the growth curves to show.

    -T --top-only
        Only show the traces from the top half of the plate (rows B-D).

    -B --bottom-only
        Only show the traces from the bottom half of the plate (rows E-G).

    -m --media-controls
        Plot the media-only (i.e. no cell) controls.

    -o --output <path>
"""

import re, os
import docopt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from debugtools import p, pp, pv
from collections import OrderedDict

class BiotekData:

    def __init__(self, path):
        self.times = {}
        self.trajectories = {}

        with open(path) as file:
            lines = file.readlines()

        mode = None
        well_name_pattern = re.compile('[A-H](1|2|3|4|5|6|7|8|9|10|11|12)')

        for line in lines:
            if not line.strip():
                continue

            header, *tokens = line.split()

            # Looks for cues about what data is to follow.
            if header.startswith('OD600'):
                mode = 'OD600'
            if header.startswith('RFP'):
                mode = 'RFP'
            if header.startswith('GFP'):
                mode = 'GFP'
            if header.startswith('Results'):
                break

            if not mode:
                continue

            if header == 'Time':
                self.times[mode] = np.array([str_to_secs(x) for x in tokens])

            if well_name_pattern.match(header):
                trajectory = np.array([float(x) for x in tokens])
                self.trajectories.setdefault(header, {})[mode] = trajectory


def parse_biotek(path):
    return BiotekData(path)

def str_to_secs(hour_min_sec_str):
    h, m, s = hour_min_sec_str.split(':')
    return 3600 * int(h) + 60 * int(m) + int(s)

def row_to_wells(letter):
    return [letter + str(i + 1) for i in range(0, 12)]


titrations = {
        'add': zip(
            row_to_wells('B'),
            reversed(row_to_wells('E')),
        ),
        'gua': zip(
            row_to_wells('C'),
            reversed(row_to_wells('F')),
        ),
        'add+gua': zip(
            row_to_wells('D'),
            reversed(row_to_wells('G')),
        ),
}


def plot_titration(data, ligand, channel='OD600', time_limit=12, 
        top_only=False, bottom_only=False, show_media=False):

    if isinstance(data, str):
        data = parse_biotek(data)

    t = data.times[channel] / 3600
    n = np.argmax(t > time_limit)

    labels = []
    gradient = mpl.cm.ScalarMappable(
            mpl.colors.Normalize(0, 10),
            mpl.cm.viridis_r,
    )

    for i, wells in enumerate(titrations[ligand]):
        if i in (0, 11):
            if not show_media:
                continue
            style = dict(
                    color='black',
                    linestyle=':',
            )
            bottom_style = style
        else:
            style = dict(
                    color=gradient.to_rgba(i-1)
            )
            if bottom_only:
                bottom_style = style
            else:
                bottom_style = dict(
                        linestyle='--',
                        dashes=(3,2),
                        **style
                )

        wells_shown = []
        if not bottom_only:
            plt.plot(t[:n], data.trajectories[wells[0]][channel][:n], **style)
            wells_shown.append(wells[0])
        if not top_only:
            plt.plot(t[:n], data.trajectories[wells[1]][channel][:n], **bottom_style)
            wells_shown.append(wells[1])

        if i == 0:
            label = 'holo media'
        elif i == 11:
            label = 'apo media'
        elif i == 10:
            label = '0.00 μM'
        else:
            label=f'{2000/2**(i-1):.2f} μM'

        label += f' [{",".join(wells_shown)}]'
        labels.append(mpl.lines.Line2D([], [], label=label, **style))

    plt.title(ligand)
    plt.legend(handles=labels, loc='upper left', prop={'size': 8})
    plt.xlim(0, time_limit)
    plt.xlabel('Time (h)')
    plt.ylabel(channel)


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    data = parse_biotek('20170214_test_add_gua_toxicity.txt')

    if os.fork():
        raise SystemExit

    plot_titration(
            data,
            ligand=args['<ligand>'],
            channel=args['<channel>'] or 'OD600',
            time_limit=float(args['--time-limit']),
            top_only=args['--top-only'],
            bottom_only=args['--bottom-only'],
            show_media=args['--media-controls'],
    )

    if args['--output']:
        plt.savefig(args['--output'].replace('$', '20170214_test_add_gua_toxicity'))
    plt.show()




