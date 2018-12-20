#!/usr/bin/env python3

import os, sys, csv, numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from more_itertools import chunked
from pprint import pprint
from datetime import datetime

def parse_epc(epc_path):
    # Read the header of the file to figure out how the data is formatted, i.e.  
    # how many time-points there are and how many rows and columns make up each 
    # time-point.

    with open(epc_path) as epc_file:
        epc_reader = csv.reader(epc_file)

        header = next(epc_reader)
        plate_rows = int(header[1])
        plate_cols = int(header[2])
        num_timepoints = int(header[3])

        data = list(epc_reader)

    # Discard the first three time-points.  I don't know what these rows are 
    # supposed to mean, but they seem like nothing but a bunch of useless 
    # punctuation characters.

    data = data[3*plate_rows:]
    timepoints = list(chunked(data, plate_rows))[:num_timepoints]
    trajectories = np.empty((plate_rows, plate_cols, num_timepoints))

    for k, tp in enumerate(timepoints):
        for i, row in enumerate(tp):
            for j, od in enumerate(row):
                trajectories[i,j,k] = float(od)

    times = [
            datetime.strptime(row[0], '%Y/%m/%d %H:%M:%S')
            for row in data[plate_rows * num_timepoints:]
    ]
    hours = [(x - times[0]).total_seconds() / 3600 for x in times]

    return trajectories, hours

