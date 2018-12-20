import numpy as np

def percent_gaussian(n):
    s = max(np.random.normal() for i in range(n))
    x = np.linspace(-4, 4, 1000)
    g = np.exp(-x**2)

    Z = np.trapz(g,x)
    f = np.trapz(g[x > s], x[x > s])

    return f / Z

print(np.percentile([percent_gaussian(1) for i in range(10000)], 100))
print(np.percentile([percent_gaussian(10) for i in range(10000)], 100))
print(np.percentile([percent_gaussian(100) for i in range(10000)], 100))
print(np.percentile([percent_gaussian(1000) for i in range(10000)], 100))


