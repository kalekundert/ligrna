#!/usr/bin/python

blank_datafile = '/home/kyleb/Dropbox/UCSF/cas9/FCS/150916-3.1/kyleb/150916-rfp-cas9/96 Well - Flat bottom_002/Specimen_001_F1_F01_046.fcs'
sample_directory = '/home/kyleb/Dropbox/UCSF/cas9/FCS/150916-3.1/kyleb/150916-rfp-cas9/96 Well - Flat bottom_002'
script_output_dir = 'script_output'

row_chars = 'ABCDEFGH'

from FlowCytometryTools import FCMeasurement, ThresholdGate
from FlowCytometryTools.core.gates import CompositeGate
import os, FlowCytometryTools
import pylab as P
import numpy as np

class PlatePos:
    def __init__ (self, plate_position_str):
        self.row = plate_position_str[0]
        assert( self.row in row_chars )
        self.col = int(plate_position_str[1:])

    @property
    def __repr__(self):
        return self.plate_row + '%02d' % self.plate_col

    def __lt__ (self, other):
        return str(self) < str(other)

class PlateRange:
    def __init__ (self, plate_position_str):
        pass

# experiment_definitions = {
#     'TEP_conc' : {
#         0.0 : PlateRange(['A1-E3']),
#         1.0e-3 : PlateRange(['A4-E6']), # 1mM
#         10.0e-3 : PlateRange(['A7-E9']), # 10 mM
#     },
#     'ATC_conc' : {
#         0.0 : PlateRange(['A1-E1','A4-E4','A7-E7']),
#         2.0e-6 : PlateRange(['A2-E2','A5-E5','A8-E8']), # 2uM
#         1.0e-6 : PlateRange(['A3-E3','A6-E6','A9-E9']), # 1uM
#     },
#     'blank_media' : PlateRange(['F1']),
# }

class FCSFile:
    def __init__ (self, filepath, plate_position_str):
        self.filepath = filepath
        self.plate_position_obj = PlatePos(plate_position_str)

    @property
    def plate_position(self):
        return str( self.plate_position_obj )

    @property
    def plate_row(self):
        return self.plate_position_obj.row

    @property
    def plate_col(self):
        return self.plate_position_obj.col

    def __lt__ (self, other):
        return self.plate_position < other.plate_position
    
    def __repr__(self):
        return self.plate_position

def find_fcs_files(sample_directory):
    fcs_files = []
    for filename in os.listdir(sample_directory):
        if filename.endswith('.fcs'):
            full_filename = os.path.join(sample_directory, filename)
            fcs_files.append( (PlatePos(filename.split('_')[2]), full_filename) )
    fcs_files.sort()
    return fcs_files

def process_experiment():
    pass

def output_medians_and_sums():
    fsc_gate = ThresholdGate(10000.0, 'FSC-A', region='above')
    ssc_gate = ThresholdGate(9000.0, 'SSC-A', region='above')
    fsc_ssc_gate = CompositeGate(fsc_gate, 'and', ssc_gate)

    # Load blank data
    blank_sample = FCMeasurement(ID='blank', datafile=blank_datafile).gate(fsc_gate)

    fcs_files = find_fcs_files(sample_directory)
    
    channel_medians = {channel_name : {} for channel_name in blank_sample.channel_names}
    channel_sums = {channel_name : {} for channel_name in blank_sample.channel_names}
    for plate_pos, filepath in fcs_files:
        sample = FCMeasurement(ID='sample', datafile=filepath).gate(fsc_gate)
        for channel_name in sample.channel_names:
            if plate_pos.row not in channel_medians[channel_name]:
                channel_medians[channel_name][plate_pos.row] = {}
                channel_sums[channel_name][plate_pos.row] = {}
            assert( plate_pos.col not in channel_medians[channel_name][plate_pos.row] )
            channel_medians[channel_name][plate_pos.row][plate_pos.col] =  sample.data[channel_name].median()
            channel_sums[channel_name][plate_pos.row][plate_pos.col] =  np.sum(sample.data[channel_name])
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

if __name__ == '__main__':
    output_medians_and_sums()
    process_experiment()
