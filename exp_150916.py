#!/usr/bin/python

from FlowCytometryTools import FCMeasurement, ThresholdGate
from FlowCytometryTools.core.gates import CompositeGate
import os, FlowCytometryTools
import pylab as P
import numpy as np
from fcm import Plate, PlateInfo

sample_directory = '/home/kyleb/Dropbox/UCSF/cas9/FCS/150916-3.1/kyleb/150916-rfp-cas9/96 Well - Flat bottom_002'
channel_name = 'B-A'

exp = Plate([
    PlateInfo('TEP_conc', 0.0, ['A1-E3']),
    PlateInfo('TEP_conc', 1.0e-3, ['A4-E6']), # 1mM
    PlateInfo('TEP_conc', 10.0e-3, ['A7-E9']), # 10 mM
    
    PlateInfo('ATC_conc', 0.0, ['A1-E1','A4-E4','A7-E7']),
    PlateInfo('ATC_conc', 2.0e-6, ['A2-E2','A5-E5','A8-E8']), # 2uM
    PlateInfo('ATC_conc', 1.0e-6, ['A3-E3','A6-E6','A9-E9']), # 1uM

    PlateInfo('Control-Pos', None, 'A1-A9'),
    PlateInfo('Control-Neg', None, 'B1-B9'),
    PlateInfo('NX-0', None, 'C1-C9'),
    PlateInfo('NX-2', None, 'D1-D9'),
    PlateInfo('US-0,0', None, 'E1-E9'),
    PlateInfo('Control-Blank', None, 'F1'),
])

if __name__ == '__main__':
    fsc_gate = ThresholdGate(10000.0, 'FSC-A', region='above')
    ssc_gate = ThresholdGate(9000.0, 'SSC-A', region='above')
    fsc_ssc_gate = CompositeGate(fsc_gate, 'and', ssc_gate)

    exp.load_fcs_dir(sample_directory, verbose=True)
    exp.gate(fsc_gate)

    tep_0_wells = exp.well_set('TEP_conc', 0.0)
    tep_1_wells = exp.well_set('TEP_conc', 1.0e-3)
    tep_10_wells = exp.well_set('TEP_conc', 10.0e-3)
    blank_sample = exp.samples[list(exp.well_set('Control-Blank'))[0]]
    
    for atc_conc in exp.parameter_values('ATC_conc'):
        atc_wells = exp.well_set('ATC_conc', atc_conc)
        for name in ['Control-Pos', 'Control-Neg', 'NX-2']:
            P.title('%s - ATC conc %.1E' % (name, atc_conc))
            exp_wells = exp.well_set(name).intersection(atc_wells)
            exp_tep_0_wells = list(tep_0_wells.intersection(exp_wells))
            exp_tep_1_wells = list(tep_1_wells.intersection(exp_wells))
            exp_tep_10_wells = list(tep_10_wells.intersection(exp_wells))
            assert( len(exp_tep_0_wells) == 1 )
            assert( len(exp_tep_1_wells) == 1 )
            assert( len(exp_tep_10_wells) == 1 )
            tep_0_median = exp.samples[exp_tep_0_wells[0]].data[channel_name].median()
            tep_1_median = exp.samples[exp_tep_1_wells[0]].data[channel_name].median()
            tep_10_median = exp.samples[exp_tep_10_wells[0]].data[channel_name].median()
            exp.samples[exp_tep_0_wells[0]].plot(channel_name, bins=100, alpha=0.5, color='blue', label='0mM TEP - median %.0f' % tep_0_median )
            exp.samples[exp_tep_1_wells[0]].plot(channel_name, bins=100, alpha=0.5, color='green', label='1mM TEP - median %.0f - %.1fx' % (tep_1_median, tep_1_median/tep_0_median) )
            exp.samples[exp_tep_10_wells[0]].plot(channel_name, bins=100, alpha=0.5, color='red', label='10mM TEP - median %.0f - %.1fx' % (tep_10_median, tep_10_median/tep_0_median) )
            blank_sample.plot(channel_name, bins=100, alpha=1.0, color='black', label='blank media')
            P.legend()
            P.grid(True)
            P.show()
