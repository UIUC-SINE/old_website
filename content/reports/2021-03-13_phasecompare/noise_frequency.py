#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

mu = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
MU = np.fft.fft(mu)

sigma = .2
x = np.random.normal(np.tile(mu, (300, 1)), sigma**2)
X = np.fft.fft(x)

# X2 = (
#     np.random.normal(np.tile(np.fft.fft(mu).real, (500, 1)), sigma**2 * 2) +
#     1j * np.random.normal(np.tile(np.fft.fft(mu).imag, (500, 1)), sigma**2 * 2)
# )



# plt.subplot(2, 1, 1)
plt.plot(MU.real, MU.imag, 'o-')
plt.plot(X.real, X.imag, 'o')
# plt.subplot(2, 1, 2)
# plt.plot(X2.real, X2.imag, 'o')
plt.gca().set_aspect('equal')
plt.show()
