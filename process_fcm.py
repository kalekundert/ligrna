#!/usr/bin/python

datafile = '/home/kyleb/Dropbox/UCSF/cas9/FCS/150916-3.1/kyleb/150916-rfp-cas9/96 Well - Flat bottom_002/Specimen_001_A1_A01_001.fcs'

from FlowCytometryTools import FCMeasurement, ThresholdGate
import os, FlowCytometryTools
from pylab import *

# Locate sample data included with this package
# datadir = os.path.join(FlowCytometryTools.__path__[0], 'tests', 'data', 'Plate01')
# datafile = os.path.join(datadir, 'RFP_Well_A3.fcs')

# Load data
sample = FCMeasurement(ID='A1', datafile=datafile)

#tsample = tsample.transform('hlog', channels=['Y2-A', 'B1-A', 'V2-A'], b=500.0)

# Plot
for channel_name
#tsample.plot('Y2-A', bins=100, alpha=0.9, color='green');
#grid(True)

# show() # <-- Uncomment when running as a script.
