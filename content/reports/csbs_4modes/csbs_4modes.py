#!/bin/env python3

from mas.data import strands
from mas.forward_model import add_noise, get_measurements, get_contributions
from mas.psf_generator import PhotonSieve, PSFs
from mas.plotting import plotter4d
from mas.deconvolution import tikhonov
from mas.csbs import csbs
from mas import sse_cost
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import compare_ssim, compare_psnr

ps = PhotonSieve()
wavelengths = np.array([33.4, 33.5]) * 1e-9
sources = strands[0:2]
recons = np.zeros((1, 4) + sources.shape)

# %% csbs_grid -----

psfs = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=10,
    num_copies=10
)

csbs(psfs, sse_cost, 10, lam=1e-2, order=0)

measured = get_measurements(sources=sources, real=True, psfs=psfs)
measured_noisy = add_noise(measured, max_count=100, model='Poisson')
recons[0, 0] = tikhonov(
    sources=sources,
    measurements=measured_noisy,
    psfs=psfs,
    tikhonov_lam=5e-2,
    tikhonov_order=1
)

# %% csbs_focus -----

psfs = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=10
)

csbs(psfs, sse_cost, 10, lam=1e-2, order=0)

measured = get_measurements(sources=sources, real=True, psfs=psfs)
measured_noisy = add_noise(measured, max_count=100, model='Poisson')
recons[0, 1] = tikhonov(
    sources=sources,
    measurements=measured_noisy,
    psfs=psfs,
    tikhonov_lam=5e-2,
    tikhonov_order=1
)


# %% naive_grid -----

psfs = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=10
)
psfs.copies = np.ones(10)

measured = get_measurements(sources=sources, real=True, psfs=psfs)
measured_noisy = add_noise(measured, max_count=100, model='Poisson')
recons[0, 2] = tikhonov(
    sources=sources,
    measurements=measured_noisy,
    psfs=psfs,
    tikhonov_lam=5e-2,
    tikhonov_order=1
)

# %% naive_focus -----

psfs = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=5
)

measured = get_measurements(sources=sources, real=True, psfs=psfs)
measured_noisy = add_noise(measured, max_count=100, model='Poisson')
recons[0, 3] = tikhonov(
    sources=sources,
    measurements=measured_noisy,
    psfs=psfs,
    tikhonov_lam=5e-2,
    tikhonov_order=1
)


# %% plot -----
def get_ssim(source, recon):
    return compare_ssim(recon, source,
        data_range=np.max(recon) - np.min(recon)
    )
get_ssim = np.vectorize(get_ssim, signature='(a,b),(c,d)->()')

plotter4d(recons[:, :, 0], cmap='gist_heat')
ssims = get_ssim(sources, recons)
