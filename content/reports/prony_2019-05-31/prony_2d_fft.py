import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import toeplitz, lstsq, hankel
from scipy.signal import convolve2d
from mas.forward_model import add_noise

N = 100
m, n = np.arange(N), np.arange(N)
omega_m = np.array((4.00001,))
omega_n = np.array((8.00002,))
y = np.sum(
    np.e**(
        1j * 2 * np.pi *
        (
            omega_m[np.newaxis, np.newaxis, :, np.newaxis] *
            m[:, np.newaxis, np.newaxis, np.newaxis] +
            omega_n[np.newaxis, np.newaxis, np.newaxis, :] *
            n[np.newaxis, :, np.newaxis, np.newaxis]
        ) / N
    ), axis=(2, 3)
)

n_filt = np.repeat(
    np.array(((1, -np.e**(1j * 2 * np.pi * omega_n[0] / N)),)),
    1,
    axis=0
)
m_filt = np.repeat(
    np.array(((1, -np.e**(1j * 2 * np.pi * omega_m[0] / N)),)),
    1,
    axis=0
).T
correct_h = convolve2d(m_filt, n_filt)

y_hat_m = y[:-1, :]
b_hat_m = -y[len(omega_m):, :]
y_hat_n = y[:, :-1]
b_hat_n = -y[:, len(omega_m):]

# FIXME
# assert 2 * len(y_hat) > len(omega), "Not enough samples for Prony's method recovery"
def zeropad(x, padded_size):
    """zeropad 1D array x to size padded_size"""

    return np.pad(x, [(0, padded_size - x.shape[0]), (0, padded_size - x.shape[1])], mode='constant')


padded_size = len(y_hat_m) + len(b_hat_m) - 1
h_hat_m = np.fft.ifft2(
    np.fft.fft2(zeropad(b_hat_m, padded_size)) / np.fft.fft2(zeropad(y_hat_m, padded_size))
)
h_m = [1, h_hat_m[0, 0]]

padded_size = len(y_hat_n) + len(b_hat_n) - 1
h_hat_n = np.fft.ifft2(
    np.fft.fft2(zeropad(b_hat_n, padded_size)) / np.fft.fft2(zeropad(y_hat_n, padded_size))
)
h_n = [1, h_hat_n[0, 0]]


omega_m_reconstructed = np.log(np.roots(h_m)) / (1j * 2 * np.pi / 100)
omega_n_reconstructed = np.log(np.roots(h_n)) / (1j * 2 * np.pi / 100)

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
