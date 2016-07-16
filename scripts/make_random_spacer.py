#!/usr/bin/env python3

import random, string, yaml

random.seed(0)
num_spacers = 20
random_spacer = lambda: \
        ''.join(random.choice('ACGU') for x in range(20))
spacers = {
        string.ascii_lowercase[i]: [random_spacer(), '']
        for i in range(num_spacers)}

with open('with_random_spacers.yml', 'w') as file:
    yaml.dump({'contexts': spacers}, file)

