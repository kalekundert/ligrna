#!/usr/bin/env python3

import numpy as np

def sum_to_n(n):
    return n * (n+1) / 2

def pick_timepoints(start, stop, steps, inc):
    n_incs = sum_to_n(steps - 1)
    stop_corr = stop - inc * n_incs

    step = (stop_corr - start) / (steps - 1)

    x = start + step * np.arange(steps)
    x += sum_to_n(np.arange(steps)) * inc

    return x

assert list(pick_timepoints(5, 30, 6, 0)) == [5, 10, 15, 20, 25, 30]
assert list(pick_timepoints(5, 45, 6, 1)) == [5, 11, 18, 26, 35, 45]

np.set_printoptions(precision=2)
cat = np.concatenate

schedules = [
        pick_timepoints(0, 30, 11, 0),
        pick_timepoints(0, 30, 10, 1/3),
        pick_timepoints(0, 30, 10, 1/2),
        cat(([0], pick_timepoints(2, 30, 9, 1/2))),
        cat(([0], pick_timepoints(2, 30, 8, 1/3))),
        cat(([0], pick_timepoints(2, 30, 8, 1/2))),
]

for schedule in schedules:
    print(' '.join(f'{t:6.2f}' for t in schedule))
