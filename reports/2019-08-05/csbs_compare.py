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

ps = PhotonSieve()
wavelengths = np.array([33.4e-9, 33.402e-9])

psfs_focus = PSFs(
    ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=6
)

psfs_csbs = PSFs(
    ps,
    source_wavelengths=wavelengths,
    num_copies=10
)
csbs(psfs_csbs, sse_cost, 12, lam=10**-4.5, order=1)

# %% measure

sources = strands[:2]

meas_focus = get_measurements(sources=sources, mode='circular', psfs=psfs_focus, real=True)
meas_csbs = get_measurements(sources=sources, mode='circular', psfs=psfs_csbs, real=True)

# meas_focus = add_noise(meas_focus, model='gaussian', dbsnr=15)
# meas_csbs = add_noise(meas_csbs, model='gaussian', dbsnr=15)
meas_focus = add_noise(meas_focus, model='poisson', max_count=20)
meas_csbs = add_noise(meas_csbs, model='poisson', max_count=20)

recon_focus = tikhonov(psfs=psfs_focus, measurements=meas_focus, tikhonov_lam=1e-3)
recon_csbs = tikhonov(psfs=psfs_csbs, measurements=meas_csbs, tikhonov_lam=1e-3)

recon_focus -= np.mean(recon_focus, axis=(1, 2))[:, np.newaxis, np.newaxis]
recon_csbs -= np.mean(recon_csbs, axis=(1, 2))[:, np.newaxis, np.newaxis]
sources_comp = sources - np.mean(sources, axis=(1, 2))[:, np.newaxis, np.newaxis]

result_focus = np.sum(compare_ssim(sources_comp, recon_focus))
result_csbs = np.sum(compare_ssim(sources_comp, recon_csbs))

print('focused SSIM sum:', result_focus)
print('csbs SSIM sum:', result_csbs)

plotter4d(recon_focus)
plotter4d(recon_csbs)

# plt.imsave('meas_focus0.png', meas_focus[0], cmap='gist_heat')
# plt.imsave('meas_focus1.png', meas_focus[1], cmap='gist_heat')

# plt.imsave('meas_csbs0.png', meas_csbs[0], cmap='gist_heat')
# plt.imsave('meas_csbs1.png', meas_csbs[1], cmap='gist_heat')

# plt.imsave('recon_focus0.png', recon_focus[0], cmap='gist_heat')
# plt.imsave('recon_focus1.png', recon_focus[1], cmap='gist_heat')

# plt.imsave('recon_csbs0.png', recon_csbs[0], cmap='gist_heat')
# plt.imsave('recon_csbs1.png', recon_csbs[1], cmap='gist_heat')
