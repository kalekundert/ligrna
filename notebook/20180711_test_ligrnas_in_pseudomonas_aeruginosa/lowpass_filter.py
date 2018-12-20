#!/usr/bin/env python3

# Play around with filtering schemes to get rid of high-frequency noise.

import sys
import numpy as np
import matplotlib.pyplot as plt
from plot_tmp_mic import load_data

def load_noisy_data():
    #df = load_data('data/20181108_pseudomonas_mic_8x_clean.toml')
    df = load_data('data/20181110_pseudomonas_mic_6x_clean.toml')
    df.set_index(['well'], inplace=True)
    #df.sort_index(inplace=True)

    # ABCDEFGH
    # 9    11
    #   10    12
    df = df.loc[sys.argv[1]]
    return df['minutes'] / 60, df['read']

def apply_butterworth_lowpass_filter(x, y):
    # This filter doesn't completely get rid of noise, and distorts the rest of 
    # the curve.  This code was copied from Stack Overflow:
    #   https://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units

    import numpy as np
    from scipy.signal import butter, lfilter, freqz

    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    # Filter requirements.
    order = 6
    fs = 1/300       # sample rate, Hz
    cutoff = 1/1200  # desired cutoff frequency of the filter, Hz

    # Get the filter coefficients so we can check its frequency response.
    b, a = butter_lowpass(cutoff, fs, order)
    z = butter_lowpass_filter(y, cutoff, fs, order)

    plt.plot(x, z, label="Butterworth")

def apply_lowess_filter(x, y):
    # The difference between lowess and loess seems pretty subtle, and possibly 
    # more by convention that anything else.
    from statsmodels.nonparametric.smoothers_lowess import lowess

    z = lowess(y, x, is_sorted=True, frac=0.025, it=0)
    plt.plot(z[:,0], z[:,1], label="LOWESS")

def apply_savitzky_golay_filter(x, y):
    from scipy.signal import savgol_filter

    z = savgol_filter(y, 11, 2)

    d = y - z
    i = d < 0.03

    plt.plot(x, d)
    #plt.plot(x[i], y[i], label="Savitzky-Golay Diff")
    plt.plot(x, z, label="Savitzky-Golay")

def apply_custom_filter(x, y):
    import numpy as np

    n = 30
    x = np.array(x)
    y = np.array(y)
    z = np.copy(y)

    ii = np.zeros(y.shape, dtype=int)
    ii[:n] = np.arange(len(y))[:n]
    j = n

    ds = []

    for i in range(n, len(z)):

        i_n = ii[j-n:j]
        x_n = x[i_n]
        z_n = z[i_n]

        p, r, _, _, _ = np.polyfit(x_n, z_n, 2, full=True)

        err = np.sqrt(r / n)

        z_exp = np.polyval(p, x[i])
        z_real = z[i]
        d = z_real - z_exp
        di = i - j

        #print('i      =', i)
        #print('j      =', j)
        #print('di     =', di)
        #print('i_n    =', i_n)
        #print('x_n    =', repr(x_n))
        #print('z_n    =', repr(z_n))
        #print('b, m   =', repr(p))
        #print('err    =', err)
        #print('x[i]   =', x[i])
        #print('z_exp  =', z_exp)
        #print('z_real =', z_real)
        #print('d      =', d)
        #print()
        if d < max(5 * err, 0.005):
            ii[j] = i
            j += 1
        else:
            pass
            #print(f"Dropping point {i}; Δ={d}")

    print(ii)

    
    print("Dropped {}/{} data points.".format(len(ii) - j, len(ii)))
    ii = ii[:j]
    plt.plot(x[ii], z[ii])

def apply_one_frame_filter(x, y):
    d = np.diff(y)

    dd = np.zeros(x.shape)
    dd[1:-1] = d[:-1] - d[1:]

    i = dd < 0.1

    plt.plot(x[i], y[i])


import pandas as pd
pd.set_option("display.max_rows",10001)

if __name__ == '__main__':
    x, y = load_noisy_data()
    plt.plot(x, y)

    #apply_butterworth_lowpass_filter(x, y)
    #apply_lowess_filter(x, y)
    #apply_savitzky_golay_filter(x, y)
    #apply_custom_filter(x, y)
    #apply_one_frame_filter(x, y)

    plt.legend(loc='best')
    plt.show()

