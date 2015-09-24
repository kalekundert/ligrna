#!/usr/bin/python

blank_datafile = '/home/kyleb/Dropbox/UCSF/cas9/FCS/150916-3.1/kyleb/150916-rfp-cas9/96 Well - Flat bottom_002/Specimen_001_F1_F01_046.fcs'
sample_directory = '/home/kyleb/Dropbox/UCSF/cas9/FCS/150916-3.1/kyleb/150916-rfp-cas9/96 Well - Flat bottom_002'
script_output_dir = 'script_output'

from FlowCytometryTools import FCMeasurement, ThresholdGate
from FlowCytometryTools.core.gates import CompositeGate
import os, FlowCytometryTools
import pylab as P
import numpy as np

sample_filenames = []
for filename in os.listdir(sample_directory):
    if filename.endswith('.fcs'):
        plate_position = filename.split('_')[2]
        plate_row = plate_position[0]
        assert( plate_row in 'ABCDEFGH' )
        plate_col = int(plate_position[1:])
        full_filename = os.path.join(sample_directory, filename)
        sample_filenames.append( (full_filename, plate_row, plate_col) )
sample_filenames.sort()

fsc_gate = ThresholdGate(10000.0, 'FSC-A', region='above')
ssc_gate = ThresholdGate(9000.0, 'SSC-A', region='above')
fsc_ssc_gate = CompositeGate(fsc_gate, 'and', ssc_gate)

# Load blank data
blank_sample = FCMeasurement(ID='blank', datafile=blank_datafile).gate(fsc_gate)

channel_medians = {channel_name : {} for channel_name in blank_sample.channel_names}
channel_sums = {channel_name : {} for channel_name in blank_sample.channel_names}
for filename, plate_row, plate_col in sample_filenames:
    sample = FCMeasurement(ID='sample', datafile=filename).gate(fsc_gate)
    for channel_name in sample.channel_names:
        if plate_row not in channel_medians[channel_name]:
            channel_medians[channel_name][plate_row] = {}
            channel_sums[channel_name][plate_row] = {}
        assert( plate_col not in channel_medians[channel_name][plate_row] )
        channel_medians[channel_name][plate_row][plate_col] =  sample.data[channel_name].median()
        channel_sums[channel_name][plate_row][plate_col] =  np.sum(sample.data[channel_name])
    #     if channel_name in ['B-A', 'A-A']:
    #         print filename, channel_name
    #         sample.plot(channel_name, bins=100, alpha=0.9, color='green');
    #         blank_sample.plot(channel_name, bins=100, alpha=0.9, color='blue');
    #         P.grid(True)
    #         P.show() # <-- Uncomment when running as a script.

if not os.path.isdir(script_output_dir):
    os.makedirs(script_output_dir)

rows = [char for char in 'ABCDEFGH']
cols = range(1, 13)
for channel, data_type in [(channel_medians, 'medians'), (channel_sums, 'sums')]:
    for channel_name in channel:
        filename = os.path.join(script_output_dir, '%s_%s.csv' % (channel_name, data_type))
        with open(filename, 'w') as f:
            for col in cols:
                for row in rows:
                    if row in channel[channel_name] and col in channel[channel_name][row]:
                        f.write('%.2f,' % channel[channel_name][row][col])
                    else:
                        f.write('NA,')
                f.write('\n')
