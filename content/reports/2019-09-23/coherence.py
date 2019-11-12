from mas.psf_generator import PSFs, PhotonSieve
from mas.forward_model import add_noise, get_measurements
from mas.deconvolution import tikhonov
from mas.data import strands
import numpy as np
from matplotlib import pyplot as plt
from mas.plotting import plotter4d
from mas.measure import compare_ssim
from mas import sse_cost
from mas.csbs import csbs
from itertools import product

# %% psfs

ps = PhotonSieve()
wavelengths = np.array([33.4e-9, 33.402e-9])

psfs = PSFs(ps, source_wavelengths=wavelengths)

# %% plot

plt.plot(
    psfs.measurement_wavelengths,
    1 / np.sum((psfs.psfs[:, 0] * psfs.psfs[:, 1]), axis=(1,2))
)

plt.axvline(wavelengths[0], color='red')
plt.axvline(wavelengths[1], color='red')
plt.title('Incoherence of PSF pairs')
plt.ylabel('Incoherence')
plt.xlabel('Meas. wavelength')

plt.show()
