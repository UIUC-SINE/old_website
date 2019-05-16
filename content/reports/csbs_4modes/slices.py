#!/bin/env python3

from mas.data import strands as sources
from mas.forward_model import add_noise, get_measurements, get_contributions
from mas.psf_generator import PhotonSieve, PSFs
import numpy as np
import matplotlib.pyplot as plt

# %% generate -----

ps = PhotonSieve()
wavelengths = np.array([33.4, 33.5]) * 1e-9
sources = sources[0:-1:7].reshape((3, 1, 160, 160))
psfs = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=300,
    num_copies=1,
    image_width=301
)

# %% plot -----


# fig = plt.figure(figsize=(12, 12))
# ax = fig.add_subplot(111, projection='3d')
plt.figure(figsize=(10, 5))

dft_mag1 = np.fft.fftshift(np.abs(psfs.psf_dfts[:, 0, 0, :]), axes=1).T
dft_mag2 = np.fft.fftshift(np.abs(psfs.psf_dfts[:, 1, 0, :]), axes=1).T

spatial_extent = (-psfs.psfs.shape[-1] // 2, psfs.psfs.shape[-1] // 2)
wavelength_extent = (psfs.measurement_wavelengths[0], psfs.measurement_wavelengths[-1])

plt.subplot(2, 1, 1)
plt.imshow(dft_mag1, extent=wavelength_extent + spatial_extent, aspect='auto')
plt.title('PSF DFT slices - 33.4 nm source')
plt.ylabel('spatial frequency')
plt.subplot(2, 1, 2)
plt.imshow(dft_mag2, extent=wavelength_extent + spatial_extent, aspect='auto')
plt.title('PSF DFT slices - 33.5 nm source')
plt.ylabel('spatial frequency')
plt.xlabel('measurement wavelength')

plt.tight_layout()
plt.savefig('slices.png', dpi=300)

plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
freqs = (0, 5, 10, 25, 50, 100)
for freq in freqs:
    plt.plot(psfs.measurement_wavelengths, dft_mag1[150 + freq, :])
plt.legend(freqs)
plt.title('PSF DFT mags at selected spatial frequencies - 33.4 nm source')
plt.ylabel('DFT mag')
plt.xlabel('measurement wavelength')
plt.margins(x=0)

plt.subplot(2, 1, 2)
for freq in freqs:
    plt.plot(psfs.measurement_wavelengths, dft_mag2[150 + freq, :])
plt.legend(freqs)
plt.title('PSF DFT mags at selected spatial frequencies - 33.5 nm source')
plt.ylabel('DFT mag')
plt.xlabel('measurement wavelength')
plt.margins(x=0)

plt.tight_layout()
plt.savefig('sample_slices.png', dpi=300)

# X, Y = np.meshgrid(
#     np.arange(dft_mag.shape[1]), np.arange(dft_mag.shape[0]
#     )
# )
# ax.plot_surface(X, Y, dft_mag, rstride=1, cstride=1)
