#!/usr/bin/env python3
# Ulas Kamaci 2018-10-27

import numpy as np
from matplotlib import pyplot as plt
from mas.forward_model import get_measurements, add_noise, size_equalizer
from mas.psf_generator import PSFs, PhotonSieve, circ_incoherent_psf
from mas.deconvolution import tikhonov, admm
from mas.deconvolution.admm import bm3d_pnp
from mas.plotting import plotter4d
from mas.data import strands_ext
from functools import partial
from skimage.measure import compare_ssim as ssim

# %% meas ------------------------

source_wavelengths = np.array([33.4e-9, 33.5e-9])
num_sources = len(source_wavelengths)
meas_size = [160,160]
sources = strands_ext[0:num_sources]
sources_ref = size_equalizer(sources, ref_size=meas_size)
ps = PhotonSieve(diameter=16e-2, smallest_hole_diameter=7e-6)

# generate psfs
psfs = PSFs(
    ps,
    sampling_interval=3.5e-6,
    measurement_wavelengths=source_wavelengths,
    source_wavelengths=source_wavelengths,
    psf_generator=circ_incoherent_psf,
    # image_width=psf_width,
    num_copies=1
)

# ############## INVERSE CRIME ##############
# measured = get_measurements(
#     sources=sources,
#     mode='circular',
#     meas_size=meas_size,
#     psfs=psfs
# )
#
# nu=10**-1.5
# lam=[10**-3.8]*num_sources


# ############## GAUSSIAN CONVOLUTION ##############
# measured = get_measurements(
#     sources=sources,
#     mode='circular',
#     meas_size=meas_size,
#     psfs=psfs,
#     blur_sigma=5
# )
# nu=10**-1.5
# lam=[10**-3.8]*num_sources

############## DRIFT ##############
measured = get_measurements(
    sources=sources,
    mode='circular',
    meas_size=meas_size,
    psfs=psfs,
    # blur_sigma=1,
    drift_amount=15
)

# ############## CONVOLUTION AND DRIFT ##############
# measured = get_measurements(
#     sources=sources,
#     mode='circular',
#     meas_size=meas_size,
#     psfs=psfs,
#     blur_sigma=1,
#     drift_amount=5
# )

measured_noisy = add_noise(measured, max_count=100, model='Poisson')

# %% recon ---------------------------------

recon = tikhonov(
    measurements=measured_noisy,
    psfs=psfs,
    tikhonov_lam=2e-2,
    tikhonov_order=1
)
recon = admm(
    sources=sources_ref,
    measurements=measured_noisy,
    psfs=psfs,
    regularizer=partial(
        # patch_based
        # TV
        bm3d_pnp
        # dncnn_pnp, model=model
        ),
    recon_init=recon,
    iternum=20,
    periter=5,
    nu=10**-1.5,
    lam=[10**-3.8]*num_sources,
)

ssim_ = np.zeros(num_sources)
mse_ = np.mean((sources_ref - recon)**2, axis=(1, 2))
psnr_ = 20 * np.log10(np.max(sources_ref, axis=(1,2))/np.sqrt(mse_))
for i in range(num_sources):
    ssim_[i] = ssim(sources_ref[i], recon[i],
        data_range=np.max(recon[i])-np.min(recon[i]))

plotter4d(recon,
    cmap='gist_heat',
    figsize=(5.6,8),
    title='Recon. SSIM={}\n Recon. PSNR={}'.format(ssim_, psnr_)
)

plotter4d(sources_ref,
    cmap='gist_heat',
    figsize=(5.6,8),
    title='Original'
)
