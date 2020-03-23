#!/bin/env python3
# Evan Widloski - 2020-03-18
# Show error from each correlation sum

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

results = pd.read_pickle('results50.pkl')
results = results.query('drift_velocity == 0.2e-3')

# this is so ugly, never do this again
w = results.query('max_count == 20')
x = (np.stack(w.d, axis=-1) - np.stack(w.true_drift, axis=-1))
y = np.moveaxis(x, (2, 0, 1), (0, 1, 2))
z = np.linalg.norm(y, axis=2)
plt.plot(z.mean(axis=0), label='max_count=20')

w = results.query('max_count == 40')
x = (np.stack(w.d, axis=-1) - np.stack(w.true_drift, axis=-1))
y = np.moveaxis(x, (2, 0, 1), (0, 1, 2))
z = np.linalg.norm(y, axis=2)
plt.plot(z.mean(axis=0), label='max_count=40')

w = results.query('max_count == 80')
x = (np.stack(w.d, axis=-1) - np.stack(w.true_drift, axis=-1))
y = np.moveaxis(x, (2, 0, 1), (0, 1, 2))
z = np.linalg.norm(y, axis=2)
plt.plot(z.mean(axis=0), label='max_count=80')

plt.legend()

plt.show()
plt.savefig('cs_error.png')
