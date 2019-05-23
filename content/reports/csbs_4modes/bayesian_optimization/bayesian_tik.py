from mas.psf_generator import PhotonSieve, PSFs
from mas.forward_model import add_noise, get_measurements
from mas.data import strands
from mas import sse_cost
from mas.csbs import csbs
from mas.measure import compare_ssim
from bayes_opt import BayesianOptimization
from mas.deconvolution import tikhonov
import numpy as np
from matplotlib import pyplot as plt

truth = strands[0:2]
ps = PhotonSieve()

wavelengths = np.array([33.4e-9, 33.5e-9])

psfs = PSFs(
    ps,
    source_wavelengths=wavelengths,
    # naive_focus
    # measurement_wavelengths=wavelengths,
    # num_copies=6,
    # csbs_grid
    measurement_wavelengths=10,
    num_copies=12
    # csbs_focus
    # measurement_wavelengths=wavelengths,
    # num_copies=12
    # naive_grid
    # measurement_wavelengths=10,
    # num_copies=1
)


# Bounded region of parameter space
pbounds = {'tikhonov_lam_exp': (-4, 1), 'csbs_lam_exp': (-4, 1)}

# def cost(tikhonov_lam_exp):
def cost(tikhonov_lam_exp, csbs_lam_exp):

    # csbs_grid
    psfs.copies = np.repeat(12, 12)
    # csbs_focus
    # psfs.copies = np.repeat(12, 2)
    csbs(psfs, sse_cost, 12, lam=10**csbs_lam_exp, order=1)
    measured = get_measurements(psfs=psfs, sources=truth, real=True)
    measured_noisy = add_noise(measured, model='poisson', max_count=500)
    recon = tikhonov(
            sources=measured,
            psfs=psfs,
            measurements=measured_noisy,
            tikhonov_lam=10**tikhonov_lam_exp
    )

    plt.imshow(recon[0])
    plt.show()
    plt.pause(.05)
    return compare_ssim(truth[0], recon[0]) + compare_ssim(truth[1], recon[1])

optimizer = BayesianOptimization(
    cost,
    pbounds=pbounds,
    random_state=1,
)

# %% optimize -----

np.seterr(all='ignore')
optimizer.maximize(
    acq='ei',
    xi=1e-4,
    init_points=10,
    n_iter=40,
)

# ----- 1D plot -----
# searched = np.array([
#     [
#             x['params']['tikhonov_lam_exp'],
#             x['target']
#     ] for x in optimizer.res
# ])
# plt.plot(searched[:, 0], searched[:, 1], 'o')

# ----- 2D contour plot -----
# searched = np.array([
#     [
#             x['params']['tikhonov_lam_exp'],
#             x['params']['csbs_lam_exp'],
#             x['target']
#     ] for x in optimizer.res
# ])
# plt.tricontourf(searched[:, 0], searched[:, 1], searched[:, 2])
# plt.plot(searched[:, 0], searched[:, 1], 'ko')

