#!/usr/bin/env python3

import re
from color_me import ucsf, tango
from matplotlib.ticker import MaxNLocator

class FoldChangeLocator(MaxNLocator):

    def __init__(self, max_ticks=6):
        super().__init__(
            nbins=max_ticks - 1,
            #steps=[0.5, 1, 2, 5, 10, 50, 100],
            steps=[1, 2, 5, 10],
        )

    def tick_values(self, vmin, vmax):
        ticks = set(super().tick_values(vmin, vmax))
        ticks.add(1);
        ticks.discard(0)
        return sorted(ticks)

def pick_color(label, lightness=0):
    """
    Pick a color for the given experiment.

    The return value is a hex string suitable for use with matplotlib.
    """
    family = pick_color_family(label)
    return pick_ucsf_color(family, lightness)

def pick_color_family(label):
    p = r'(%s)(\b|[(])'
    control = re.compile(p % r'[w]?(on|off|wt|dead|null|pos|neg|pa14|control)')
    upper_stem = re.compile(p % r'us|.u.?|#3|#24|#25')
    lower_stem = re.compile(p % r'ls|.l.?')
    bulge = re.compile(p % r'.b.?')
    nexus = re.compile(p % r'nx|.x.?|[wm]11|#61')
    hairpin = re.compile(p % r'.h.?|[wm]30|#80|#85')

    label = label.lower()

    if control.search(label):
        return 'control'
    elif nexus.search(label):
        return 'nexus'
    elif hairpin.search(label):
        return 'hairpin'
    elif lower_stem.search(label):
        return 'lower stem'
    elif upper_stem.search(label):
        return 'upper stem'
    elif bulge.search(label):
        return 'bulge'
    elif 'rfp' in label:
        return 'rfp'
    elif 'gfp' in label:
        return 'gfp'
    else:
        return 'default'

def pick_tango_color(family, lightness=0):
    """
    Pick a color from the Tango color scheme for the given experiment.

    The Tango color scheme is best known for being the basis of GTK icons, 
    which are used heavily on Linux systems.  The colors are bright, and the 
    scheme includes a few tints of each color.
    """
    i = lambda x: max(x - lightness, 0)

    if family == 'control':
        return tango.grey[i(4)]
    elif family == 'lower stem':
        return tango.purple[i(1)]
    elif family == 'nexus':
        return tango.red[i(1)]
    elif family == 'hairpin':
        return tango.orange[i(1)]
    elif family == 'upper stem':
        return tango.blue[i(1)]
    elif family == 'bulge':
        return tango.green[i(1)]
    elif family == 'rfp':
        return tango.red[i(1)]
    elif family == 'gfp':
        return tango.green[i(2)]
    elif family == 'default':
        return tango.brown[i(2)]
    else:
        return family if lightness == 0 else '#dddddd'

def pick_ucsf_color(family, lightness=0):
    """
    Pick a color from the official UCSF color scheme for the given experiment.

    The UCSF color scheme is based on primary teal and navy colors and is 
    accented by a variety of bright -- but still somewhat subdued -- colors.  
    The scheme includes tints of every color, but not shades.
    """
    i = lambda x: min(x + lightness, 3)

    if family == 'control':
        return ucsf.light_grey[i(0)]
    elif family == 'lower stem':
        return ucsf.olive[i(0)]
    elif family == 'nexus':
        return ucsf.navy[i(0)]
    elif family == 'hairpin':
        return ucsf.teal[i(0)]
    elif family == 'upper stem':
        return ucsf.blue[i(0)]
    elif family == 'bulge':
        return ucsf.blue[i(0)]
    elif family == 'rfp':
        return ucsf.red[i(0)]
    elif family == 'gfp':
        return ucsf.olive[i(0)]
    elif family == 'default':
        return ucsf.dark_grey[i(0)]
    else:
        return family if lightness == 0 else '#dddddd'

def pick_linestyle(theo_mM, standard=1):
    morse_code = {
            '0': '-----',
            '1': '.----',
            '2': '..---',
            '3': '...--',
            '4': '....-',
            '5': '.....',
            '6': '-....',
            '7': '--...',
            '8': '---..',
            '9': '----.',
    }

    def morse_from_float(x):
        return ''.join(
                morse_code.get(xx, '') 
                for xx in str(x)
        )

    def dashes_from_morse(morse):
        dashes = []
        lengths = {
                '.': [2, 2],
                '-': [5, 2],
        }

        for dot_dash in morse:
            dashes += lengths[dot_dash]

        return dashes

    if theo_mM == standard:
        return {'linestyle': '-'}
    elif theo_mM == 0:
        return {'linestyle': '--'}
    else:
        return {'dashes': dashes_from_morse(morse_from_float(theo_mM))}

def pick_style(label, theo_mM, standard_mM=1, color_controls=False):
    # apo behind holo, and controls behind everything else.
    zorder = theo_mM if pick_color_family(label) != 'control' else theo_mM - 10
    use_color = color_controls and pick_color_family(label) == 'control'
    return {
            'color': pick_color(label) if theo_mM or use_color else 'black',
            'linewidth': 1,
            'zorder': zorder,
            **pick_linestyle(theo_mM, standard_mM),
    }

def pick_data_style(label, theo_mM, standard_mM=1, color_controls=False):
    # apo behind holo, and controls behind everything else.
    zorder = theo_mM if pick_color_family(label) != 'control' else theo_mM - 10
    use_color = color_controls and pick_color_family(label) == 'control'
    return {
            'color': pick_color(label) if theo_mM or use_color else 'black',
            'linestyle': 'none',
            'marker': '+',
            'zorder': zorder,
    }

