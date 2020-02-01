from mas.psf_generator import PSFs, PhotonSieve
from mas.forward_model import add_noise, get_measurements
from mas.deconvolution import tikhonov
from mas.data import strands
from matplotlib import pyplot as plt
import seaborn as sns; sns.set()
from mas.plotting import plotter4d
from mas.measure import compare_ssim
from mas import sse_cost
from mas.csbs import csbs
from mas.misc import experiment
import numpy as np
import pandas as pd

# evaluate CSBS reconstruction improvement for many sieve diameters and many separations

sources = strands[:2]

def get_psfs(*, separation, diameter):
    ps = PhotonSieve(diameter=diameter)
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

    return psfs_focus, psfs_csbs

# %% measure

result = pd.DataFrame()
# for diameter in np.logspace(-2, -1, 20):
for diameter in np.logspace(-1, -1, 1):
    for separation in np.logspace(-12, -10, 20):

        psfs_focus, psfs_csbs = get_psfs(separation=separation, diameter=diameter)

        def measure_reconstruct():

            noise = 15 # dB SNR

            meas_focus = get_measurements(sources=sources, mode='circular', psfs=psfs_focus, real=True)
            meas_csbs = get_measurements(sources=sources, mode='circular', psfs=psfs_csbs, real=True)

            meas_focus = add_noise(meas_focus, model='gaussian', dbsnr=noise)
            meas_csbs = add_noise(meas_csbs, model='gaussian', dbsnr=noise)

            recon_focus = tikhonov(psfs=psfs_focus, measurements=meas_focus, tikhonov_lam=1e-3)
            recon_csbs = tikhonov(psfs=psfs_csbs, measurements=meas_csbs, tikhonov_lam=1e-3)
            result_focus = np.sum(compare_ssim(truth=sources, estimate=recon_focus))
            result_csbs = np.sum(compare_ssim(truth=sources, estimate=recon_csbs))

            ratio = result_csbs / result_focus

            return dict(**locals())

        exp_result = experiment(measure_reconstruct, iterations=20)
        exp_result['separation'] = separation
        exp_result['diameter'] = diameter
        result = result.append(
            exp_result[['separation', 'ratio', 'diameter']]
        )
        print(
            'separation:{:.3E}\tratio_mean:{:.3E}\tratio_std:{:.3E}'.format(
                separation,
                np.mean(exp_result.ratio),
                np.std(exp_result.ratio)
            )
        )

# %% plot

ax = sns.lineplot(x='separation', y='ratio', hue='diameter', data=result)
ax.set(xscale='log')
plt.show()
plt.savefig('test.png')
