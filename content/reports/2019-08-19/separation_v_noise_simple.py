from mas.psf_generator import PSFs, PhotonSieve
from mas.forward_model import add_noise, get_measurements
from mas.deconvolution import tikhonov
from mas.data import strands
from matplotlib import pyplot as plt
from mas.plotting import plotter4d
from mas.measure import compare_ssim
from mas import sse_cost
from mas.csbs import csbs
import numpy as np

separation = .04e-9 # m

ps = PhotonSieve()
wavelengths = np.array([33.4e-9, 33.4e-9 + separation])

psfs_focus = PSFs(
    ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=6,
    image_width=303
)


psfs_csbs = PSFs(
    ps,
    source_wavelengths=wavelengths,
    num_copies=10,
    image_width=303
)
csbs(psfs_csbs, sse_cost, 12, lam=10**-4.5, order=1)

sources = strands[:2]

# %% measure

noise = 15 # dB SNR

meas_focus = get_measurements(sources=sources, mode='circular', psfs=psfs_focus, real=True)
meas_csbs = get_measurements(sources=sources, mode='circular', psfs=psfs_csbs, real=True)

meas_focus = add_noise(meas_focus, model='gaussian', dbsnr=noise)
meas_csbs = add_noise(meas_csbs, model='gaussian', dbsnr=noise)

recon_focus = tikhonov(psfs=psfs_focus, measurements=meas_focus, tikhonov_lam=1e-3)
recon_csbs = tikhonov(psfs=psfs_csbs, measurements=meas_csbs, tikhonov_lam=1e-3)
result_focus = np.sum(compare_ssim(sources, recon_focus))
result_csbs = np.sum(compare_ssim(sources, recon_csbs))

print(result_csbs / result_focus, result_focus)

# print('focused SSIM:', result_focus)
# print('csbs SSIM:', result_csbs)

# recon_focus_mean = recon_focus - np.mean(recon_focus, axis=(1, 2))[:, np.newaxis, np.newaxis]
# recon_csbs_mean = recon_csbs - np.mean(recon_csbs, axis=(1, 2))[:, np.newaxis, np.newaxis]
# sources_mean = sources - np.mean(sources, axis=(1, 2))[:, np.newaxis, np.newaxis]

# result_focus_mean = np.sum(compare_ssim(sources_mean, recon_focus_mean))
# result_csbs_mean = np.sum(compare_ssim(sources_mean, recon_csbs_mean))

# print('focused SSIM, mean:', result_focus_mean)
# print('csbs SSIM, mean:', result_csbs_mean)
