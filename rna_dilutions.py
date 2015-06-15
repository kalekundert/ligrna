#!/usr/bin/env python3


def show(table, suffix=''):
    for k in ('wt', 'dead', 'nx0', 'nx1', 'nx2', 'nx3'):
        if k in table:
            print('{:<4} {:.2f} {}'.format(k, table[k], suffix))


ng_uL = {
        'wt': 6712,
        'dead': 5381,
        'nx0': 8699,
        'nx1': 6744,
        'nx2': 5012,
        'nx3': 6669,
}
mw = {
        'wt': 41647.2,
        'dead': 41567.1,
        'nx0': 49360.8,
        'nx1': 49360.8,
        'nx2': 49360.8,
        'nx3': 49360.8,
}
nM = {
        x: 1e6 * ng_uL[x] / mw[x]
        for x in mw
}

show(nM)
print()

# Dilute each reaction to the same concentration
# ==============================================
# 1. Find the reaction with the lowest yield.

min_yield = min(ng_uL, key=lambda k: ng_uL[k])
vol_rna = 26

dilution = {
        x: nM[x] * vol_rna / nM[min_yield] - vol_rna
        for x in nM
}

del dilution[min_yield]
nM = nM[min_yield]

print('Add the following amount of water to {} μL of sgRNA to dilute each construct to {:.0f} nM:'.format(vol_rna, nM))
show(dilution, 'μL water')
print()

# Calculate how to dilute the RNA to 120 nM in 6 steps
# ====================================================

steps = 6
f = (120 / nM) ** (1 / (steps - 1))

leave = 7.5
take = leave * f / (1 - f)

print('Perform a serial dilution using the following parameters:')
print('1. Put {:.2f} μL RNA in the first tube.'.format(take + leave))
print('2. Add {:.2f} μL water in the remaining tubes.'.format(leave))
print('3. Perform a serial dilution, taking {:.2f} μL each time.'.format(take))
print()

# Make sure the calculation pass the smell test
# =============================================

print('Final sgRNA concentrations in 30 μL Cas9 reaction:')
for n in range(steps):
    print('{:.2f} nM'.format(leave * nM * f ** n / 30))

