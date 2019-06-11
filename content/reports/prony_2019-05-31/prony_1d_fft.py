import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import toeplitz, lstsq, hankel

N = 100
n = np.arange(N)
# omega = np.array((4, 5, 8.5))
omega = np.array((4,),)
y = np.sum(np.e**(1j * 2 * np.pi * omega[np.newaxis, :] * n[:, np.newaxis] / N), axis=1)

y_hat = y[:-1]
b_hat = -y[len(omega):]

# FIXME
# assert 2 * len(y_hat) > len(omega), "Not enough samples for Prony's method recovery"
def zeropad(x, padded_size):
    """zeropad 1D array x to size padded_size"""

    return np.pad(x, (0, padded_size - len(x)), mode='constant')


padded_size = len(y_hat) + len(b_hat) - 1
h_hat = np.fft.ifft(
    np.fft.fft(zeropad(b_hat, padded_size)) / np.fft.fft(zeropad(y_hat, padded_size))
)

h = np.insert(h_hat[:len(omega)], 0, 1)

omega_reconstructed = np.log(np.roots(h)) / (1j * 2 * np.pi / 100)

# plt.subplot(3, 1, 1)
# plt.title('y')
# plt.plot(y)

# plt.subplot(3, 1, 2)
# plt.title('y DFT')
# plt.plot(np.abs(np.fft.fft(y)))

# plt.subplot(3, 1, 3)
# plt.title('prony estimate')
# y_reconstructed = np.zeros(N * 100)  # 100X resolution
# y_reconstructed[omega_reconstructed.real.astype(int) * 100] = 1
# plt.plot(np.linspace(0, N, N * 100), y_reconstructed)

# plt.tight_layout()
# plt.show()
