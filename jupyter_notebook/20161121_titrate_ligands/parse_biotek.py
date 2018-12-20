#!/usr/bin/env python3

import re
from datetime import datetime
from pprint import pprint

class BiotekData:

    def __init__(self):
        self.timepoints = []
        self.trajectories = {}

    @property
    def dt(self):
        return self.timepoints

    @property
    def traj(self):
        return self.trajectories


def parse_biotek(txt_path):
    # Biotek's exported *.txt files contain degree signs (°) encoded in latin1.
    # This really is an awful file format to work with.
    with open(txt_path, encoding='latin1') as file:
        lines = file.readlines()

    data = BiotekData()

    for line in lines:
        tokens = line.split('\t')

        # The header will begin with the work 'Time' and will contain a token 
        # labeling each well being measured.  Save this mapping and use it to 
        # initialize the trajectory data structure.
        if tokens[0] == 'Time' and len(tokens) > 2:
            labels = tokens[2:]
            for label in labels:
                data.trajectories[label] = []

        # Data lines will begin with a time expressed as HOURS:MINS:SECS.  
        # Ignore lines that do not match this format.
        try:
            hours, mins, secs = tokens[0].split(':')
            dt = int(hours) + int(mins)/60 + int(secs)/3600
        except:
            continue

        # Ignore lines that don't have data (these will exist if the run was 
        # aborted early for some reason).
        if sum(1 for _ in filter(str.strip, tokens)) <= 1:
            continue

        data.timepoints.append(dt)
        for label, value in zip(labels, tokens[2:]):
            data.trajectories[label].append(float(value))

    return data

