#!/usr/bin/env python3

from pylab import *

g = lambda L, N, p=1: 1 - ((L-1)/L)**(N*p)
f = lambda L, N, p=1: L * g(L, N, p)
p = logspace(-3, 0)

print(f(1e7, 5e7, 0.5) / 1e7)
print(f(f(1e7, 5e7), 5e7) / 1e7)
print(g(1e7, 5e7))

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
