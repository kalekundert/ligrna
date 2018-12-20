#!/usr/bin/env python3

import RNA as vrna
import sgrna_sensor
from math import exp

sgrna = sgrna_sensor.mhf(30)

fc = vrna.fold_compound(sgrna.rna)

designs = [
        'mhf 30',
        'w30 63',
        'w30 63/2',
        'w30 64',
        'w30 64/1',
        'w30 65',
        'w30 65/1',
        'w30 77',
        'w30 77/1',
        'w30 77/2',
        'w30 78',
        'w30 78/1',
        'w30 78/2',
        'w30 79',
        'w30 79/1',
        'w30 80',
        'w30 80/1',
]
prefolded = '............................................................(.........................).........................'

print(' ' * (9 + 1 + 6 + 3) + prefolded)
for name in designs:
    sgrna = sgrna_sensor.from_name(name)
    struct = vrna.fold_compound(sgrna.rna)
    q_tot = struct.pf()[1]

    struct.constraints_add(prefolded, vrna.CONSTRAINT_DB_DEFAULT)
    fold_prefolded, q_prefolded = struct.pf()

    rt_37 = 1.987203611e-3 * 310  # RT in kcal/mol at 37°C
    f_prefolded = exp(-(q_prefolded - q_tot) / rt_37)

    print(f"{sgrna.slash_name:9s} {100 * f_prefolded:6.3f}%  {fold_prefolded}")
