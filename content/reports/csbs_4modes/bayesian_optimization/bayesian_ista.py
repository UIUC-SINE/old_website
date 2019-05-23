from mas.psf_generator import PhotonSieve, PSFs
from mas.forward_model import add_noise, get_measurements
from mas.data import strands
from mas.measure import compare_ssim
from bayes_opt import BayesianOptimization
from mas.deconvolution import ista
import numpy as np
from matplotlib import pyplot as plt

# %% problem -----

truth = strands[0:1]
ps = PhotonSieve()

wavelengths = np.array([33.4e-9, 40e-9])

psfs = PSFs(
    ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=10
)
measured = get_measurements(psfs=psfs, sources=truth, real=True)
measured = add_noise(measured, model='poisson', max_count=10)

def cost(lam_exp, time_step_exp):

    recon = ista(
        psfs=psfs,
        measurements=measured,
        lam=10**lam_exp,
        time_step=10**time_step_exp,
        iterations=100
    )[0]

    cost = compare_ssim(
        truth[0],
        recon
    )

    plt.subplot(1, 3, 3)
    plt.title('Reconstruction - SSIM {:.3f}'.format(cost))
    plt.imshow(recon)
    plt.axis('off')
    plt.xlabel('lam_exp={:.3f}\ntime_step_exp={:.3f}')
    plt.show()
    plt.pause(.05)

    return cost if cost > 0 else 0

# %% optimization -----


# Bounded region of parameter space
pbounds = {'lam_exp': (-6, -3), 'time_step_exp':(-5, -2)}
optimizer = BayesianOptimization(
    cost,
    pbounds=pbounds,
    random_state=1,
)

# %% optimize -----

plt.figure(figsize=(8,3))
plt.subplot(1, 3, 1)
plt.title('Truth')
plt.imshow(truth[0])
plt.axis('off')
plt.subplot(1, 3, 2)
plt.title('Measured')
plt.imshow(measured[0])
plt.axis('off')
plt.pause(.05)

try:
    np.seterr(all='ignore')
    optimizer.maximize(
        acq='ei',
        # kappa=0.1,
        init_points=10,
        n_iter=25,
    )

# plot scatterplot of previous trials on keyboard interrupt
except KeyboardInterrupt:
    pass

plt.figtext(0.02, 0.02, str(optimizer.max), fontsize='xx-small')
plt.savefig('ista_best.png', dpi=300)

plt.figure()
searched = np.array([
    [
            x['params']['lam_exp'],
            x['params']['time_step_exp'],
            x['target']
    ] for x in optimizer.res
])
plt.tricontourf(searched[:, 0], searched[:, 1], searched[:, 2])
plt.plot(searched[:, 0], searched[:, 1], 'ko', ms=3)
plt.xlabel('lam_exp')
plt.ylabel('time_step_exp')
plt.tight_layout()

plt.savefig('ista_search.png', dpi=300)
