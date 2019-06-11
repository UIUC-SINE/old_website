# Verify that Prony's method works for synthesized 1D signals

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import toeplitz, lstsq, hankel

N = 100
n = np.arange(N)
omega = np.array((4, 5, 8.5))
y = np.sum(np.e**(1j * 2 * np.pi * omega[np.newaxis, :] * n[:, np.newaxis] / N), axis=1)
# y = n

y_hat = hankel(y[:N - len(omega)], y[N - len(omega) - 1:N - 1])
b_hat = -y[len(omega):]

# FIXME
# assert 2 * len(y_hat) > len(omega), "Not enough samples for Prony's method recovery"

h_hat = np.linalg.pinv(y_hat) @ b_hat

h = np.insert(np.flip(h_hat), 0, 1)

omega_reconstructed = np.log(np.roots(h)) / (1j * 2 * np.pi / N)

plt.subplot(3, 1, 1)
plt.title('y')
plt.plot(y)

plt.subplot(3, 1, 2)
plt.title('y DFT')
plt.plot(np.abs(np.fft.fft(y)))

plt.subplot(3, 1, 3)
plt.title('prony estimate')
y_reconstructed = np.zeros(N * 1000)  # 1000X plotting resolution
y_reconstructed[omega_reconstructed.real.astype(int) * 1000] = 1
plt.plot(np.linspace(0, N, N * 1000), y_reconstructed)

plt.tight_layout()
plt.show()
