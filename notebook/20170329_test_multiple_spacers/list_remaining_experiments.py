#!/usr/bin/env python3

from sgrna_sensor import densiometry

df = densiometry.load_cleavage_data_from_xlsx_dir('densiometry')

pc = densiometry.calc_percent_cut(df)
pd = densiometry.calc_percent_change(df)
md = densiometry.calc_mean_change(df)
expts = md[md.design.isin(['rxb 11,1', 'mhf 30'])]

print("<3  replicates:")
print(expts.query('num_replicates < 3'))
print()

print(">4% change in controls:")
controls = pd[pd.design.isin(['on', 'off'])]
print(controls[abs(controls.percent_change) > 0.04])
print()

print(">10% stdev:")
print(expts[(expts.std_change > 0.1) & (expts.mean_change > 0.1)])
