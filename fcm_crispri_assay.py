#!/usr/bin/env python3

"""\
Usage:
    fcm_crispri_assay.py <num_designs>
"""

import docopt
import dirty_water

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
num_designs = int(eval(args['<num_designs>']))
num_cultures = num_designs + 2
lb_vol = int(1.1 * num_cultures)

protocol += """\
Make enough LBCC for 2 controls and {num_designs} designs:

- {lb_vol} mL LB
- {lb_vol} μL 100 mg/mL (1000x) Carb
- {lb_vol} μL 35 mg/mL (1000x) Chlor"""

protocol += """\
Grow overnight cultures:

- Inoculate 1 mL LBCC with either picked colonies 
  or glycerol stocks for each of the controls and 
  the designs.

- Grow overnight at 37°C."""

lb_vol = 2 * lb_vol
atc_vol = 10 * lb_vol
lbcca_vol = lb_vol // 2
theo_vol = lbcca_vol / 30

protocol += """\
Make enough LBCCA and LBCCAT for {num_cultures} cultures:

LBCCA:
- {lb_vol} mL LB
- {lb_vol} μL 100 mg/mL (1000x) Carb
- {lb_vol} μL 35 mg/mL (1000x) Chlor
- {atc_vol} μL 100 μg/mL (100x) ATC

LBCCAT:
- {lbcca_vol} mL LBCCA
- {theo_vol:.2f} 30 mM (30x) theophylline"""

protocol += """\
Grow the cultures with and without theophylline, 
while inducing Cas9:

- Subculture 4 μL of each overnight into 1 mL 
  LBCCA and 1 mL LBCCAT.

- Grow at 37°C for at least 9h.
"""

protocol += """\
Dilute 1 μL of each culture into 199 μL PBS.
"""

protocol += """\
Analyze the cells via flow cytometry."""

print(protocol)

# vim: tw=50
