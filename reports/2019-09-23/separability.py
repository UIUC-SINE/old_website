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
from itertools import product

# %% psfs

ps = PhotonSieve()

psfs_separated = PSFs(
    ps,
    source_wavelengths=np.array([33.4e-9, 33.5e-9]),
)
psfs_close = PSFs(
    ps,
    source_wavelengths=np.array([33.4e-9, 33.402e-9]),
)

# %% compute

prod_separated = np.array(list(product(psfs_separated.psfs, psfs_separated.psfs)))
energy_separated = np.sum(
    np.linalg.norm(prod_separated, axis=(3, 4))**2,
    axis=(1, 2)
).reshape((32, 32))
separability_separated = np.linalg.norm(
    prod_separated[:, 0, 0] * prod_separated[:, 1, 1] - prod_separated[:, 0, 1] * prod_separated[:, 1, 0],
    axis=(1, 2)
).reshape((32, 32)) / energy_separated
product_separated = energy_separated * separability_separated

prod_close = np.array(list(product(psfs_close.psfs, psfs_close.psfs)))
energy_close = np.sum(
    np.linalg.norm(prod_close, axis=(3, 4))**2,
    axis=(1, 2)
).reshape((32, 32))
separability_close = np.linalg.norm(
    prod_close[:, 0, 0] * prod_close[:, 1, 1] - prod_close[:, 0, 1] * prod_close[:, 1, 0],
    axis=(1, 2)
).reshape((32, 32)) / energy_close
product_close = energy_close * separability_close

plt.figure()
plt.title('energy_separated')
plt.imshow(energy_separated)
plt.figure()
plt.title('separability_separated')
plt.imshow(separability_separated)
plt.figure()
plt.title('product_separated')
plt.imshow(product_separated)
plt.figure()
plt.title('energy_close')
plt.imshow(energy_close)
plt.figure()
plt.title('separability_close')
plt.imshow(separability_close)
plt.figure()
plt.title('product_close')
plt.imshow(product_close)
