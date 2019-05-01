#!/bin/env python3

from mas.data import strands as sources
from mas.forward_model import add_noise, get_measurements, get_contributions
from mas.psf_generator import PhotonSieve, PSFs
from mas.plotting import plotter4d
import numpy as np
import matplotlib.pyplot as plt

ps = PhotonSieve()
wavelengths = np.array([33.4, 33.5]) * 1e-9
sources = sources[0:-1:10].reshape((2, 1, 160, 160))
psfs = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=1
)


contributions = get_contributions(sources=sources[:, 0, :, :], psfs=psfs, real=True)
plt = plotter4d(
    contributions,
    title='measurement contributions',
    column_labels=wavelengths,
    sup_xlabel='source wavelengths',
    row_labels=wavelengths,
    sup_ylabel='measurement wavelengths',
    scale=True
)
plt.savefig('contributions.png')
plt.show()

# measurements = get_measurements(sources=sources, psfs=psfs, real=True)
# measurements = add_noise(measurements, maxcount=10, model='poisson')
