#!/usr/bin/env python3

import sgrna_sensor

def show(table, suffix=''):
    for k in ('wt', 'dead', 'nx_0', 'nx_1', 'nx_2', 'nx_3'):
        if k in table:
            print('{:<4} {:.2f} {}'.format(k, table[k], suffix))


ng_uL = {
        #'nx_0': 1684,
        #'nx_1': 2121,
        #'nx_2': 2771,
        #'nx_3': 5531,
        'us/0/0': 52.88,
}
#ng_uL = {
#        'nx_2': 330.7,
#}
mw = { 
        x: sgrna_sensor.molecular_weight(x)
        for x in ng_uL
}
nM = {
        x: 1e6 * ng_uL[x] / mw[x]
        for x in mw
}


print("Initial sgRNA concentrations (ng/μL):")
show(ng_uL, 'ng/μL')
print()
print("Initial sgRNA concentrations (nM):")
show(nM, 'nM')
print()

# Dilute each reaction to the same concentration
# ==============================================
# 1. Find the reaction with the lowest yield.

min_yield = min(ng_uL, key=lambda k: ng_uL[k])
vol_rna = 15

dilution = {
        x: nM[x] * vol_rna / nM[min_yield] - vol_rna
        for x in nM
}

del dilution[min_yield]
nM = nM[min_yield]

if len(mw) > 1:
    print('Add the following amount of water to {} μL of sgRNA to\n'
          'dilute each construct to {:.0f} nM:'.format(vol_rna, nM))
    show(dilution, 'μL water')
    print()

# Calculate how to dilute the RNA to 120 nM in 6 steps
# ====================================================

steps = 3
#target_conc = 120
#target_conc = 45
target_conc = 300
f = (target_conc / nM) ** (1 / (steps - 1))

#leave = 7.5
leave = 15
take = leave * f / (1 - f)
print(f)

print('Perform a serial dilution using the following parameters:')
print('1. Put {:.2f} μL RNA in the first tube.'.format(take + leave))
print('2. Add {:.2f} μL water in the remaining tubes.'.format(leave))
print('3. Perform a serial dilution, taking {:.2f} μL each time.'.format(take))
print()

# Make sure the calculation pass the smell test
# =============================================

print("Final sgRNA concentrations after diluting 10-fold:")
for n in range(steps):
    print('{:>7.2f} nM'.format(nM * f ** n / 10))

