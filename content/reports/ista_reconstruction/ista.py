import numpy as np
import pywt
from mas.strand_generator import strands
from mas.forward_model import add_noise
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from skimage.transform import radon, iradon
from mas.data import strand as truth
import time

# %% load -----

# dictionary = np.load('dictionary.npy')
# dict_adjoint = lambda x: np.einsum('ab,txab->tx', x, dictionary)
# dict_forward = lambda x: np.einsum('tx,txab->ab', x, dictionary)

# %% measure -----

# truth = strands(numstrands=10)
measurement = add_noise(truth, maxcount=10, model='poisson')

theta = np.linspace(-30., 30., max(measurement.shape), endpoint=False)
# theta = np.linspace(-30., 30., 20, endpoint=False)
def radon_forward(x):
    return radon(x, theta=theta, circle=False)
def radon_adjoint(x):
    return iradon(x, theta=theta, circle=False, filter=None)

plt.subplot(1, 3, 1)
plt.imshow(truth)
plt.subplot(1, 3, 2)
plt.imshow(measurement)
plt.show()
plt.pause(.05)


# %% ista -----

def ista(*, lam, time_step, iterations, rescale=False):
    x = radon_forward(measurement)
    results = []
    for n in range(iterations):
        print(f'iteration {n}')

        im = radon_adjoint(x)
        if rescale:
            im -= np.min(im)
            im /= np.max(im)

        x = pywt.threshold(
            x + time_step * radon_forward(measurement - im),
            lam
        )

        if n % 10 == 0:
            plt.subplot(1, 3, 3)
            plt.imshow(radon_adjoint(x))
            plt.show()
            plt.pause(.05)
            # input()

    return radon_adjoint(x)

# %% plot -----

# iterations = np.linspace(50, 200, 4, dtype=int)
iterations = 100
time_steps = np.logspace(-4, -3, 4)
lams = np.logspace(-2, -1, 4)

ii, tt, ll = np.meshgrid(iterations, time_steps, lams)
# results = np.vectorize(ista, otypes=[object])(iterations=ii, time_step=tt, lam=ll)

reconstruction = ista(lam=.025, time_step=0.0005, iterations=110, rescale=True)
# reconstruction= ista(lam=.3, time_step=0.0005, iterations=110)
# reconstruction= ista(lam=.045, time_step=0.0005, iterations=200)

# plt.subplot(1, 3, 3)
# plt.imshow(reconstruction)
