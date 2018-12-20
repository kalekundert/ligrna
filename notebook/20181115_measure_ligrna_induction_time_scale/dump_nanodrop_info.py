#!/usr/bin/env python3

import pandas as pd
from pathlib import Path

nanodrop = Path(__file__).resolve().parents[2] / 'data/nanodrop'
df_from_tsv = lambda path: pd.read_csv(path, sep='\t', header=0)

df = pd.concat([
        df_from_tsv(nanodrop/'20181130_mhf_30_timecourse.tsv'),
        df_from_tsv(nanodrop/'20181203_rxb_11_1_timecourse.tsv'),
]).dropna('columns', 'all')

print(f"""\
ng/µL
  mean   = {df['Nucleic Acid(ng/uL)'].mean():.2f}
  median = {df['Nucleic Acid(ng/uL)'].median():.2f}
  min    = {df['Nucleic Acid(ng/uL)'].min():.2f}
  25%    = {df['Nucleic Acid(ng/uL)'].quantile(0.25):.2f}
  75%    = {df['Nucleic Acid(ng/uL)'].quantile(0.75):.2f}
  max    = {df['Nucleic Acid(ng/uL)'].max():.2f}
  std    = {df['Nucleic Acid(ng/uL)'].std():.2f}

A260/A280
  mean   = {df['A260/A280'].mean():.2f}
  std    = {df['A260/A280'].std():.2f}
""")

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

x = df['Nucleic Acid(ng/uL)']
f = gaussian_kde(x)
y = np.linspace(0, 1600, 500)

plt.plot(y, f(y))
plt.xlabel('ng/µL')
plt.ylabel('density')
plt.title('Distribution of RNA yields')
plt.show()

