#!/usr/bin/env python3

import numpy as np
import itertools

def unclump_points(y, yerr, x=0, dx=1):
    """
    Return x values such that the given points can be plotted (with error bars) 
    without any overlaps.  
    """

    # Determine which points are clashing with each other.
    n = len(y)
    clashes = np.zeros((n,n))

    for i, j in itertools.combinations(range(n), 2):
        i_min = y[i] - yerr[i]
        i_max = y[i] + yerr[i]
        j_min = y[j] - yerr[j]
        j_max = y[j] + yerr[j]

        clashes[i,j] = clashes[j,i] = \
                (i_min <= j_min <= i_max) or (i_min <= j_max <= i_max) or \
                (j_min <= i_min <= j_max) or (j_min <= i_max <= j_max)

    # Create groups of non-clashing points using a greedy algorithm.
    labels = {}
    next_label = 0
    sorted_indices = list(np.argsort(y))
    unlabeled_indices = lambda: (
            i for i in sorted_indices if i not in labels)

    for i in unlabeled_indices():
        group = [i]

        for j in unlabeled_indices():
            for ii in group:
                if clashes[j,ii]: break
            else:
                group.append(j)

        for ii in group:
            labels[ii] = next_label

        next_label += 1

    # Calculate an x-coordinate for each group.
    def label_to_offset(ii): #
        sign = 1 if ii % 2 else -1
        factor = (ii + 1) // 2
        return x + sign * factor * dx

    return np.array([label_to_offset(labels[i]) for i in range(n)])



