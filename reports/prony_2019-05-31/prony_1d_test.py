# Verify that Prony's method works for 1d phase correlation

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import toeplitz, lstsq, hankel
from scipy.misc import face
from scipy.ndimage import rotate
from mas.tracking import phase_correlate
from mas.forward_model import add_noise

# %% measure

x0 = face(gray=True)[200, 100:100 + 512]
x0 = add_noise(x0, model='gaussian', dbsnr=30, signature='(m)->(m)')
# x1 = face(gray=True)[200, 200:200 + 512]
x1 = np.roll(x0, -100)
x1 = add_noise(x1, model='gaussian', dbsnr=30, signature='(m)->(m)')

num_peaks = 1
y = np.fft.ifft(phase_correlate(x0, x1))
N = len(y)

# %% estimate

y_hat = hankel(y[:N - num_peaks], y[N - num_peaks - 1:N - 1])
b_hat = -y[num_peaks:]

# FIXME
# assert 2 * len(y_hat) > num_peaks, "Not enough samples for Prony's method recovery"

h_hat = np.linalg.pinv(y_hat) @ b_hat

h = np.insert(np.flip(h_hat), 0, 1)

omega_reconstructed = np.log(np.roots(h)) / (1j * 2 * np.pi / N)

# %% plot

plt.subplot(2, 1, 1)
plt.title('Original and Shifted')
plt.hold(True)
plt.plot(x0)
plt.plot(x1)

plt.subplot(2, 1, 2)
plt.title('Offset - Prony estimate')
y_reconstructed = np.zeros(N * 1000)  # 1000X plotting resolution
y_reconstructed[omega_reconstructed.real.astype(int) * 1000] = 1
plt.plot(np.linspace(0, N, N * 1000), y_reconstructed)

plt.tight_layout()
plt.show()
