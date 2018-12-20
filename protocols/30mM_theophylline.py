#!/usr/bin/env python3

"""\
Prepare a stock solution of 30 mM theophylline.

Usage:
    30mM_theophylline.py [options]

Options:
    -v --volume <mL>    [default: 40]
        Roughly how much stock solution you want to prepare.

    -c --conc <mM>      [default: 30]
        The concentration of theophylline you want to prepare.

Note that theophylline is a drug, and as such it is fairly toxic.  Be careful 
not to inhale or ingest it and read the MSDS for more information.
"""

import docopt
import dirty_water

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
volume = eval(args['--volume'])
conc = eval(args['--conc'])
mw = 180.16

mg_theo = volume * conc * mw / 1000
mL_water = 1000 / mw / conc

protocol += """\
Measure approximately {mg_theo:.1f} mg theophylline 
into a glass bottle with a stir bar."""

protocol += """\
Add {mL_water:.4f} mL water for each mg theophyline."""

protocol += """\
Stir on a ≈90°C hot plate for 15 min."""

print(protocol)
