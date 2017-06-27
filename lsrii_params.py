"""\
Below are the excitation and emission maxima for the 
fluorescent proteins used in this assay:

Fluorophore  Excitation  Emission  Reference
──────────────────────────────────────────────────
sfGFP               485       510  Pédelacq (2006)
mRFP                557       592  Campbell (2002)

Below are the laser settings I use on the Lim Lab BD 
LSRII:

Channel  Laser  Filter  Voltage  Threshold
───────────────────────────────────────────
FSC        488              400
SSC        488  488/10      250
GFP        488  530/30      600       5000
RFP        561  610/10      500        500

Below are the loader settings I use on the Lim Lab BD 
LSRII.  I use the lowest flow rate possible because 
my cultures are usually pretty saturated, and I want 
to be as accurate as possible.  I use a relatively 
high sample volume because I want to be sure of 
recording 10,000 events, even for cultures that 
didn't grow well for some reason.  The two 100 μL 
mixes at 180 μL/sec are enough that I don't need to 
mix the cells when diluting them into PBS.  I use the 
highest possible wash volume, but it doesn't help 
anything as far as I can tell.

Loader Setting       Value
──────────────────────────
Flow rate       0.5 μL/sec
Sample volume        60 μL
Mixing volume       100 μL
Mixing speed    180 μL/sec
Num mixes                2
Wash volume         800 μL"""

# vim: tw=53

