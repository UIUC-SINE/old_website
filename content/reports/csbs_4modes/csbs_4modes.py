#!/bin/env python3

from mas.data import strands
from mas.forward_model import add_noise, get_measurements, get_contributions
from mas.psf_generator import PhotonSieve, PSFs
from mas.plotting import plotter4d
from mas.deconvolution import tikhonov, ista
from mas.csbs import csbs
from mas.decorators import _vectorize
from mas import sse_cost
import numpy as np
import matplotlib.pyplot as plt
from mas.measure import compare_ssim
import pandas as pd
import seaborn as sns
import copy

ps = PhotonSieve()
wavelengths = np.array([33.4, 33.5]) * 1e-9
sources = strands[0:len(wavelengths)]
noise_copies = 100
recons = np.zeros((5, noise_copies) + sources.shape)
psfs = np.zeros((4), dtype=object)
max_count = 500

vec_tikhonov = _vectorize(
    signature='(a,b,c)->(d,e,f)',
    included=['measurements']
)(tikhonov)

def vec_add_noise(x, **kwargs):
    x = np.repeat(x[np.newaxis], noise_copies, axis=0)
    return add_noise(x, **kwargs)

# %% csbs_grid -----
print('csbs_grid')

psfs[0] = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=10,
    num_copies=12
)

# csbs(psfs[0], sse_cost, 12, lam=10**-3.75, order=1) # 10 counts
csbs(psfs[0], sse_cost, 12, lam=10**-3.5, order=1) # 500 counts

measured = get_measurements(sources=sources, real=True, psfs=psfs[0])
measured_noisy = vec_add_noise(measured, max_count=max_count, model='Poisson')
recons[0] = vec_tikhonov(
    sources=sources,
    measurements=measured_noisy,
    psfs=psfs[0],
    # tikhonov_lam=10**-0.75, # 10 counts
    tikhonov_lam=10**-1.75, # 500 counts
    tikhonov_order=1
)

# %% csbs_focus -----
print('csbs_focus')

psfs[1] = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=12
)

# csbs(psfs[1], sse_cost, 12, lam=10**-3.75, order=1) # 10 counts
csbs(psfs[1], sse_cost, 12, lam=10**-3.25, order=1) # 500 counts

measured = get_measurements(sources=sources, real=True, psfs=psfs[1])
measured_noisy = vec_add_noise(measured, max_count=max_count, model='Poisson')
recons[1] = vec_tikhonov(
    sources=sources,
    measurements=measured_noisy,
    psfs=psfs[1],
    # tikhonov_lam=10**-0.75, # 10 counts
    tikhonov_lam=10**-1.75, # 500 counts
    tikhonov_order=1
)


# %% naive_grid -----
print('naive_grid')

psfs[2] = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=10,
    num_copies=1
)

measured = get_measurements(sources=sources, real=True, psfs=psfs[2])
measured_noisy = vec_add_noise(measured, max_count=max_count, model='Poisson')
recons[2] = vec_tikhonov(
    sources=sources,
    measurements=measured_noisy,
    psfs=psfs[2],
    # tikhonov_lam=10**-1, # 10 counts
    tikhonov_lam=10**-2, # 500 counts
    tikhonov_order=1
)

# %% naive_focus -----
print('naive_focus')

psfs[3] = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=6
)

measured = get_measurements(sources=sources, real=True, psfs=psfs[3])
measured_noisy = vec_add_noise(measured, max_count=max_count, model='Poisson')
recons[3] = vec_tikhonov(
    sources=sources,
    measurements=measured_noisy,
    psfs=psfs[3],
    # tikhonov_lam=10**-0.8, # 10 counts
    tikhonov_lam=10**-1.75, # 500 counts
    tikhonov_order=1
)


# %% plot -----

def get_ssim(source, recon):
    return compare_ssim(recon, source)
get_ssim = np.vectorize(get_ssim, signature='(a,b),(c,d)->()')

csbs_modes = ['CSBS grid', 'CSBS focus', 'Naive grid', 'Naive focus', 'Original']

recons[4] = sources


plotter4d(
    recons[:, 0],
    cmap='gist_heat',
    scale=True,
    row_labels=csbs_modes,
    column_labels=['33.4nm', '33.5nm'],
    sup_xlabel='Source',
    sup_ylabel='CSBS mode',
    figsize=(5, 6)
)
plt.savefig('reconstructions.png', dpi=300)

plt.close()

# ssims = np.mean(get_ssim(sources, recons), axis=(1, 2))
ssims = np.mean(get_ssim(sources, recons), axis=(1, 2))
plt.plot(ssims, 'o')
plt.grid(True)
plt.xticks(np.arange(len(ssims)), csbs_modes)
plt.savefig('ssim_comparison.png', dpi=300)
plt.show()
