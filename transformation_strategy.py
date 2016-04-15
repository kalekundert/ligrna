#!/usr/bin/env python3
# encoding: utf-8

import pylab; pylab.rcParams['font.family'] = 'DejaVu Sans'
from pylab import *
from matplotlib import cm
from pprint import pprint

# L: library size
# N: sampling capacity
g = lambda L, N, p=1: 1 - ((L-1)/L)**(N*p)
f = lambda L, N, p=1: L * g(L, N, p)
p = logspace(-3, 0)

# Number of live cells that can be sorted in the given time in hours.
h = lambda t: t * (6e7 / 6.5) * (60 / 100) / 60
t = linspace(0, 100, 500)

lib = 3 * 4**12 + 2 * 4**11 + 1 * 4**10
tfm = f(4**12, 16.14e7) + f(4**11, 1.47e7) + f(4**10, 1.58e7) + \
      f(4**12, 16.10e7) + f(4**11, 1.65e7) + f(4**12, 3.08e7)
xtfm = [f(tfm, n * 5e7) for n in range(0, 7)]

print('rb')
print(g(9.48e6, 34511092 * (60 / 100)))
rb = f(9.48e6, 34511092 * (60 / 100))
print(rb)
print('%.2e'%f(.213*rb, 7.35e6))
print('%.2e'%f(.050*rb, 1.74e6))
print('%.2e'%f(.092*rb, 3.16e6))
print('rb_theo')
print(g(9.48e6, 36456613 * (60 / 100)))
print(f(9.48e6, 36456613 * (60 / 100)))
rb_theo = f(9.48e6, 36456613 * (60 / 100))
print('%.2e'%g(.271*rb_theo, 9.88e6))
print('%.2e'%g(.075*rb_theo, 2.75e6))
print('%.2e'%g(.120*rb_theo, 4.39e6))

print()
print(f(3e6, h(t))[100])
print(g(3e6, h(t))[100])
print(h(t)[100])
print(t[100])


plot(t, f(3e6, h(t)) / 3e6, 'k:', label='Round 2 (N=%.2f×10⁷)' % (1e6/1e7))
plot(t, f(7e5, h(t)) / 7e5, 'k:', label='Round 2 (N=%.2f×10⁷)' % (1e6/1e7))
plot(t, f(1e6, h(t)) / 1e6, 'k:', label='Round 2 (N=%.2f×10⁷)' % (1e6/1e7))
#plot(t, f(lib, h(t)) / lib, 'k:', label='Theoretical library (N=%.2f×10⁷)' % (lib/1e7))
#plot(t, f(tfm, h(t)) / lib, 'k', label='Constructed library (N=%.2f×10⁷)' % (tfm/1e7))
#for n in reversed(range(1, 5)):
    #plot(t, f(xtfm[n], h(t)) / lib, color=cm.gray(1/2-(n-2)/(5-2)/2), label='%dx MG1655 transformations (N=%.2f×10⁷)' % (n, xtfm[n]/1e7))
#plot(t, f(9.48e6, h(t)) / lib, 'k', label='Transformed library (N=0.95×10⁷)')
#legend(loc='lower right', fontsize=13)
ylabel('Fraction of theoretical library sorted')
xlabel('Sort time (h)')
#savefig('sorting_throughput.pdf')
show()

raise SystemExit
#print(f(1e7, 5e7, 0.5) / 1e7)
#print(f(f(1e7, 5e7), 5e7) / 1e7)
#print(g(1e7, 5e7))

import os
if os.fork():
    raise SystemExit

plot(p, f(6e7, 5e7, p) / 6e7, 'k', label='MG1655 directly')
plot(p, f(f(6e7, 5e7, p), 5e7) / 6e7, 'k:', label='Top10 (1e7), then MG1655')
xscale('log')
yscale('log')
legend(loc='lower right')
ylabel('Fraction of library transformed')
xlabel('Transformation penalty for ligation product')
#savefig('transformation_strategy.pdf')
show()
