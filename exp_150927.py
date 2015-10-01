#!/usr/bin/python

from FlowCytometryTools import FCMeasurement, ThresholdGate
from FlowCytometryTools.core.gates import CompositeGate
import os, FlowCytometryTools
import pylab as P
import numpy as np
from fcm import Plate, PlateInfo
import sys

channel_name = 'B-A'

plate_1 = Plate([
    PlateInfo('TEP_conc', 0.0, ['A1-E3']),
    PlateInfo('TEP_conc', 100.0e-6, ['A4-E6']), # 100 uM
    PlateInfo('TEP_conc', 1.0e-3, ['A7-E9']), # 1 mM
    
    PlateInfo('ATC_conc', 0.0, ['A1-E1','A4-E4','A7-E7']),
    PlateInfo('ATC_conc', 2.0e-6, ['A2-E2','A5-E5','A8-E8']), # 2uM
    PlateInfo('ATC_conc', 1.0e-6, ['A3-E3','A6-E6','A9-E9']), # 1uM

    PlateInfo('Control-Pos', None, 'A1-A9'),
    PlateInfo('Control-Neg', None, 'B1-B9'),
    PlateInfo('NX-0', None, 'C1-C9'),
    PlateInfo('US-0,0', None, 'D1-D9'),
    PlateInfo('NX2', None, 'E1-E9'),
    PlateInfo('Control-Blank', None, 'C12'),
], sample_dir = '/kortemmelab/data/kyleb/cas9/FCS/150927-3.1/150927-rfp-cas9_002-5.30pm/Plate1and2',
    name = 'replicate_1',
)

# Plate 2 was originally the same layout as plates 1 and 3,
# but was transferred to the extra space on plate 1 for ease of reading
plate_2 = Plate([
    PlateInfo('TEP_conc', 0.0, ['F1-H3', 'A10-C11']),
    PlateInfo('TEP_conc', 100.0e-6, ['F4-H6', 'D10-F11']), # 100 uM
    PlateInfo('TEP_conc', 1.0e-3, ['F7-H9', 'G10-H11', 'A12-B12']), # 1 mM
    
    PlateInfo('ATC_conc', 0.0, ['F1-H1', 'F4-H4', 'F7-H7', 'A10-A11', 'D10-D11', 'G10-G11']),
    PlateInfo('ATC_conc', 2.0e-6, ['F2-H2', 'F5-H5', 'F8-H8', 'B10-B11', 'E10-E11', 'H10-H11']), # 2uM
    PlateInfo('ATC_conc', 1.0e-6, ['F3-H3', 'F6-H6', 'F9-H9', 'C10-C11', 'F10-F11', 'A12-B12']), # 1uM

    PlateInfo('Control-Pos', None, 'F1-F9'),
    PlateInfo('Control-Neg', None, 'G1-G9'),
    PlateInfo('NX-0', None, 'H1-H9'),
    PlateInfo('US-0,0', None, ['A10-H10', 'A12']),
    PlateInfo('NX2', None, ['A11-H11', 'B12']),
    PlateInfo('Control-Blank', None, 'C12'),
], sample_dir = '/kortemmelab/data/kyleb/cas9/FCS/150927-3.1/150927-rfp-cas9_002-5.30pm/Plate1and2',
    name = 'replicate_2',
)

plate_3 = Plate([
    PlateInfo('TEP_conc', 0.0, ['A1-E3']),
    PlateInfo('TEP_conc', 100.0e-6, ['A4-E6']), # 100 uM
    PlateInfo('TEP_conc', 1.0e-3, ['A7-E9']), # 1 mM
    
    PlateInfo('ATC_conc', 0.0, ['A1-E1','A4-E4','A7-E7']),
    PlateInfo('ATC_conc', 2.0e-6, ['A2-E2','A5-E5','A8-E8']), # 2uM
    PlateInfo('ATC_conc', 1.0e-6, ['A3-E3','A6-E6','A9-E9']), # 1uM

    PlateInfo('Control-Pos', None, 'A1-A9'),
    PlateInfo('Control-Neg', None, 'B1-B9'),
    PlateInfo('NX-0', None, 'C1-C9'),
    PlateInfo('US-0,0', None, 'D1-D9'),
    PlateInfo('NX2', None, 'E1-E9'),
    PlateInfo('Control-Blank', None, 'F1'),
], sample_dir = '/kortemmelab/data/kyleb/cas9/FCS/150927-3.1/150927-rfp-cas9_002-5.30pm/Plate3',
    name = 'replicate_3',
)

all_plates = [plate_1, plate_2, plate_3]

tep_concs = [
    (0.0, '0'),
    (100.0e-6, '100uM'),
    (1.0e-3, '1mM'),
]

if __name__ == '__main__':
    fsc_gate_above = 16000.0
    fsc_gate = ThresholdGate(fsc_gate_above, 'FSC-A', region='above')
    ssc_gate = ThresholdGate(9000.0, 'SSC-A', region='above')
    fsc_ssc_gate = CompositeGate(fsc_gate, 'and', ssc_gate)
    fsc_ssc_axis_limits = (-50000, 100000)

    for exp in all_plates:
        blank_samples = list(exp.well_set('Control-Blank'))
        assert( len(blank_samples) == 1 )
        blank_sample = exp.samples[blank_samples[0]]
        nonblank_samples = list(exp.all_position_set.difference(exp.well_set('Control-Blank')))
        P.title('%s - FSC/SSC gating' % (exp.name))
        for i, nonblank_sample in enumerate(nonblank_samples):
            exp.samples[nonblank_sample].plot(['FSC-A', 'SSC-A'], kind='scatter', color=np.random.rand(3,1), s=1, alpha=0.1)
        blank_sample.plot(['FSC-A', 'SSC-A'], kind='scatter', color='red', s=2, alpha=1.0, label='Blank media')
        P.ylim(fsc_ssc_axis_limits)
        P.xlim(fsc_ssc_axis_limits)
        P.plot((fsc_gate_above, fsc_gate_above), (fsc_ssc_axis_limits[0], fsc_ssc_axis_limits[1]), color='black', linestyle='--', linewidth=2, label='FSC gate')
        P.grid(True)
        P.legend()
        P.show()
        
        exp.gate(fsc_ssc_gate)
        tep_wells = {}
        for tep_conc, tep_conc_name in tep_concs:
            tep_wells[tep_conc] = exp.well_set('TEP_conc', tep_conc)
    
        for atc_conc in exp.parameter_values('ATC_conc'):
            atc_wells = exp.well_set('ATC_conc', atc_conc)
            for name in exp.experimental_parameters:
                P.title('%s - %s - ATC conc %.1E M' % (exp.name, name, atc_conc))
                exp_wells = exp.well_set(name).intersection(atc_wells)
                exp_tep_wells = {}
                for tep_conc, tep_conc_name in tep_concs:
                    exp_tep_wells[tep_conc] = list(tep_wells[tep_conc].intersection(exp_wells))
                    assert( len(exp_tep_wells[tep_conc]) == 1 )
                    exp_tep_wells[tep_conc] = exp_tep_wells[tep_conc][0]
                tep_medians = {}
                count = 0
                colors = [(0,0,1,1), (0,1,0,1), (1,0,0,1)]
                for tep_conc, tep_conc_name in tep_concs:
                    tep_medians[tep_conc] = exp.samples[exp_tep_wells[tep_conc]].data[channel_name].median()
                    exp.samples[exp_tep_wells[tep_conc]].plot(channel_name, bins=100, fc=colors[count%len(colors)], lw=1, label='%s TEP - median %.0f' % (tep_conc_name, tep_medians[tep_conc]) )
                    count += 1
                # blank_sample.plot(channel_name, bins=100, alpha=0.1, color='black', label='blank media')
                P.legend()
                P.grid(True)
                P.show()
