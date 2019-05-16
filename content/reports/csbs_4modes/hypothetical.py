# Evan Widloski - 2019-05-01
# Testing CSBS on a hypothetical imaging element

from mas.psf_generator import PhotonSieve, PSFs
from mas.csbs import csbs
from mas import sse_cost
from skimage.draw import circle, rectangle
from mas.plotting import fourier_slices
import numpy as np


N = 49
image_width = 301
ps = PhotonSieve()
wavelengths = np.array([33.4, 33.5]) * 1e-9
psfs = PSFs(
    sieve=ps,
    source_wavelengths=wavelengths,
    measurement_wavelengths=N,
    num_copies=5,
    image_width=image_width
)

# %% annulus -----

# def annulus(radius, width, amplitude=1, image_width=301):

#     annulus = np.zeros((image_width, image_width))

#     x1, y1 = circle(
#         image_width / 2,
#         image_width / 2,
#         radius + width / 2,
#         shape=(image_width, image_width)
#     )
#     x2, y2 = circle(
#         image_width / 2,
#         image_width / 2,
#         radius - width / 2,
#         shape=(image_width, image_width)
#     )

#     annulus[x1, y1] = 1
#     annulus[x2, y2] = 0
#     annulus *= amplitude

#     return annulus

# annulus = np.vectorize(annulus, signature='(),(),()->(i,j)')

# n = np.arange(N)
# radii1 = 3 * np.abs(n - 15) + 3
# radii2 = 3* np.abs(n - 35) + 3
# widths1 = widths2 = np.repeat(5, N)
# amplitudes1 = 2.**(-np.abs(n - 15))
# amplitudes2 = 2.**(-np.abs(n - 35))

# dfts1 = annulus(radii1, widths1, amplitudes1)[:, np.newaxis, :, :]
# dfts2 = annulus(radii2, widths2, amplitudes2)[:, np.newaxis, :, :]
# dfts1 = np.fft.fftshift(dfts1, axes=(2, 3))
# dfts2 = np.fft.fftshift(dfts2, axes=(2, 3))

# dfts = np.concatenate((dfts1, dfts2), axis=1)

# psfs.psf_dfts = dfts
# psfs.psfs = dfts

# csbs(psfs, sse_cost, 10, lam=1e-2, order=0)
# fourier_slices(psfs)

# %% square -----

def square(top, left, width, amplitude=1, image_width=301):

    square = np.zeros((image_width, image_width))
    xx, yy = rectangle(
        (top, left),
        (top + width - 1, left + width - 1),
        shape=(image_width, image_width)
    )

    square[xx.astype(int), yy.astype(int)] = amplitude
    return square

square = np.vectorize(square, signature='(),(),()->(i,j)')

n = np.arange(N)
tops = (n // np.sqrt(N)) * (image_width / np.sqrt(N))
lefts = (n % np.sqrt(N)) * (image_width / np.sqrt(N))
widths = np.repeat(image_width / np.sqrt(N), N)

dfts = square(tops, lefts, widths)[:, np.newaxis, :, :]

psfs.psf_dfts = dfts
psfs.psfs = np.fft.ifft2(psfs.psf_dfts)

# csbs(psfs, sse_cost, 10, lam=1e-9, order=1)
csbs(psfs, sse_cost, 10, lam=1e0, order=1)
plt, _ = fourier_slices(psfs)
plt.show()
