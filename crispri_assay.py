#!/usr/bin/env python3

"""\
Usage:
    crispri_assay.py [--lb] [--rfp] [--verbose]

Options:
    --lb
        Use LB to grow the induced cells with and with theophylline before 
        sorting.  The default media is EZ, which is more expensive but 
        generally gives better signal.

    --rfp
        Measure red fluorescence rather than green.  This changes some of the 
        flow cytometry parameters.

    -v --verbose
        Print out the more pedantic details about the protocol, including 
        recipes for the medias, product numbers 
        for some reagents, and things like that.
"""

import docopt
import dirty_water

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
media = 'LB' if args['--lb'] else 'EZ'
channel = 'RFP' if args['--rfp'] else 'GFP'
gfp_threshold = '5000' if args['--rfp'] else ''
rfp_threshold = '' if args['--rfp'] else '500'

if args['--verbose']:
    if args['--lb']:
        protocol += """\
Prepare the following reagents:

Reagent  Description
─────────────────────────────────────────────────
LBCC     LB, 100 μg/mL carbenicillin, 35 μg/mL 
         chloramphenicol
LBCCA    LBCC, 1 μg/mL anhydrotetracycline
LBCCAT   LBCCA, 1 mM theophylline
"""
    else:
        protocol += """\
Prepare the following reagents:

Reagent  Description
─────────────────────────────────────────────────
LBCC     LB, 100 μg/mL carbenicillin, 35 μg/mL 
         chloramphenicol
EZCCA    MOPS EZ rich defined media (Teknova 
         M2105), 0.1% glucose, 100 μg/mL 
         carbenicillin, 35 μg/mL chloramphenicol, 
         1 μg/mL anhydrotetracycline
EZCCAT   EZCCA, 1 mM theophylline
"""

protocol += """\
Make overnight cultures of the designs you want to 
test in LBCC."""

protocol += """\
Grow each culture with and without theophylline, 
while inducing Cas9:

- Subculture 4 μL of each overnight into 1 mL 
  {media}CCA and 1 mL {media}CCAT.

- Grow at 37°C for at least 9h.
"""

protocol += """\
Dilute 1 μL of each culture into 199 μL PBS.
"""

protocol += """\
Measure the {channel} fluorescence of each culture on 
the BD LSRII flow cytometer.

Loader Setting       Value    Laser         Voltage  Threshold
──────────────────────────    ────────────────────────────────
Flow rate       0.5 μL/sec    FSC               400
Sample volume        60 μL    SSC               250
Mixing volume       100 μL    FITC              600  {gfp_threshold:>9s}
Mixing speed    180 μL/sec    PE-Texas Red      500  {rfp_threshold:>9s}
Num mixes                2
Wash volume         800 μL"""

print(protocol)

# vim: tw=50
