from mas.data import strands as sources
from mas.forward_model import add_noise, get_measurements, get_contributions
from mas.psf_generator import PhotonSieve, PSFs
from mas.plotting import plotter4d
from mas.csbs import csbs
from mas import sse_cost
import numpy as np
import matplotlib.pyplot as plt

# %% psfs -----

ps = PhotonSieve()
wavelengths = np.array([33.4, 33.5]) * 1e-9
sources = sources[np.array((0, 1))].reshape((2, 1, 160, 160))
psfs = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=wavelengths,
    num_copies=1
)

# %% contributions -----

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
