# Evan Widloski - 2019-04-18
# Subpixel registration test with various levels of poisson noise, circular shift
# based on https://scikit-image.org/docs/dev/auto_examples/transform/plot_register_translation.html

import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.feature import register_translation
from skimage.feature.register_translation import _upsampled_dft
from mas.plotting import plotter4d
from mas.forward_model import get_measurements
from mas.psf_generator import PhotonSieve, PSFs
from mas.decorators import vectorize
from scipy.ndimage.interpolation import shift
from mas.data import strands
# from scipy.ndimage import fourier_shift

original = strands[0]
offset = (25, 25)
# shifted = np.fft.ifft2(fourier_shift(np.fft.fft2(original), offset))
shifted = shift(original, shift=offset, mode='wrap')

# %% psfs -----

ps = PhotonSieve(diameter=10e-2)
wavelengths = np.array([33.4e-9])
psfs = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=1
)

# %% measure -----

measured_original = get_measurements(
    sources=original[np.newaxis, :, :],
    psfs=psfs,
    real=True
)[0]

measured_shifted = get_measurements(
    sources=shifted[np.newaxis, :, :],
    psfs=psfs,
    real=True
)[0]
