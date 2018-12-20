#!/usr/bin/env python3

import numpy as np
from sklearn.cluster import AffinityPropagation
from pprint import pprint

clashes = 100 * np.array([
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 0],
    [1, 1, 0, 0],
])

kernel = AffinityPropagation(affinity='precomputed')
labels = kernel.fit_predict(clashes)

print(labels)

y = [1,2,3,4,5]
y_std = [0.1, 0.1, 2, 2, 0.1]
