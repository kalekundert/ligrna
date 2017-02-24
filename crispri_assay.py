#!/usr/bin/env python3

"""\
Usage:
    crispri_assay.py [--time <hours>] [--time-course] [--verbose]

Options:
    -t --time <hours>  [default: 9]
        The number of hours to grow the cells for.

    -T --time-course
        Take time-points every hour.

    -v --verbose
        Print out the more pedantic details about the protocol, namely 
        cytometer settings and things like that.
"""

import docopt
import dirty_water

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
hours = eval(args['--time'])

protocol += """\
Make 1 mL overnight cultures of the designs you 
want to test."""

protocol += f"""\
Grow each culture with and without ligand, 
while inducing Cas9:

- Subculture 4 μL of each overnight into 1 mL 
  apo media and 1 mL holo media.

- Grow at 37°C for {hours}
"""

if args['--time-course']:
    protocol += """\
Take a time point every hour, starting at 6h:

- Prepare plates with 200 μL PBS + Sp.  Keep at 
  4°C.

- If the cultures are totally transparent, dilute 
  2 μL into the PBS + Sp.

- If the cultures are visibly cloudy, but not 
  saturated, dilute 1 μL into the PBS + Sp.

- If the cultures are saturated, dilute 0.5 μL 
  into the PBS + Sp.
"""

protocol += """\
Dilute 0.5 μL of each culture into 200 μL PBS.
"""

protocol += """\
Measure the GFP and RFP fluorescence of each 
culture by flow cytometry.
"""

print(protocol)

if args['--verbose']:
    print("""\

Below are the excitation and emission maxima for 
the fluorescent proteins used in this assay:

Fluorophore  Excitation  Emission  Reference
──────────────────────────────────────────────────
sfGFP               485       510  Pédelacq (2006)
mRFP                557       592  Campbell (2002)

Below are the laser settings I use on the Lim Lab 
BD LSRII.  They don't really match the fluorescent 
proteins that well, so it might make sense to use 
different settings on different cytometers:

Channel  Excitation  Emission  Voltage  Threshold
─────────────────────────────────────────────────
FSC                                400
SSC                                250
GFP             488    530/30      600       5000
RFP             532    610/10      500        500

Below are the loader settings I use on the Lim Lab 
BD LSRII.  I use the lowest flow rate possible 
because my cultures are usually pretty saturated, 
and I want to be as accurate as possible.  I use a 
relatively high sample volume because I want to be 
sure of recording 10,000 events, even for cultures 
that didn't grow well for some reason.  The two 
100 μL mixes at 180 μL/sec are enough that I don't 
need to mix the cells when diluting them into PBS.  
I use the highest possible wash volume, but it 
doesn't help anything as far as I can tell.

Loader Setting       Value
──────────────────────────
Flow rate       0.5 μL/sec
Sample volume        60 μL
Mixing volume       100 μL
Mixing speed    180 μL/sec
Num mixes                2
Wash volume         800 μL""")

# vim: tw=50
