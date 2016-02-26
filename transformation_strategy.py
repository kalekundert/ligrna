#!/usr/bin/env python3

import os
if os.fork():
    raise SystemExit

from pylab import *

g = lambda L, N, p=1: 1 - ((L-1)/L)**(N*p)
f = lambda L, N, p=1: L * g(L, N, p)
p = logspace(-3, 0)

plot(p, f(6e7, 5e7, p) / 6e7, 'k', label='MG1655 directly')
plot(p, f(f(6e7, 1e7, p), 5e7) / 6e7, 'k:', label='Top10 (1e7), then MG1655')
plot(p, f(f(6e7, 1e8, p), 5e7) / 6e7, 'k-.', label='Top10 (1e8), then MG1655')
plot(p, f(f(6e7, 1e9, p), 5e7) / 6e7, 'k--', label='Top10 (1e9), then MG1655')
xscale('log')
yscale('log')
legend(loc='lower right')
ylabel('Fraction of library transformed')
xlabel('Transformation penalty for ligation product')
#savefig('transformation_strategy.pdf')
show()
