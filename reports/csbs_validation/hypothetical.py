# Evan Widloski - 2019-05-01
# Testing CSBS on a hypothetical imaging element

from mas.psf_generator import PhotonSieve, PSFs
from mas.csbs import csbs
from mas import sse_cost
from skimage.draw import circle, rectangle
from mas.plotting import fourier_slices
import numpy as np
from mas.plotting import plotter4d


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

# %% ps -----

wavelengths = np.array([33.4e-9])
ps = PhotonSieve()
psfs_ps = PSFs(ps, source_wavelengths=wavelengths, measurement_wavelengths=49, num_copies=5)

plotter4d(
    np.fft.fftshift(
        np.abs(psfs.psf_dfts.reshape(7, 7, 301, 301)),
        axes=(2, 3),
    ),
    figsize=(5, 5),
    scale=True
)
plt.savefig('photonsieve_dfts.png', dpi=300)

# %% sq -----

wavelengths = np.array([33.4e-9])
ps = PhotonSieve()
psfs_sq = PSFs(ps, source_wavelengths=wavelengths, measurement_wavelengths=49, num_copies=5)

def square(top, left, width, image_width=301, amplitude=1):

    square = np.zeros((image_width, image_width))
    xx, yy = rectangle(
        (top, left),
        (top + width - 1, left + width - 1),
        shape=(image_width, image_width)
    )

    square[xx.astype(int), yy.astype(int)] = amplitude
    return square

square = np.vectorize(square, signature='(),(),()->(i,j)', excluded=['image_width'])

image_width=301
N = 49
n = np.arange(N)
tops = (n // np.sqrt(N)) * (image_width / np.sqrt(N))
lefts = (n % np.sqrt(N)) * (image_width / np.sqrt(N))
widths = np.repeat(image_width / np.sqrt(N), N)

dfts = square(tops, lefts, widths, image_width=image_width)[:, np.newaxis, :, :]
# PSF DFTs have DC in upper-left
dfts = np.fft.fftshift(dfts, axes=(2, 3))

psfs_sq.psf_dfts = dfts
psfs_sq.psfs = np.fft.ifft2(psfs_sq.psf_dfts)

plotter4d(
    np.fft.fftshift(
        np.abs(psfs_sq.psf_dfts.reshape(7, 7, 301, 301)),
        axes=(2, 3),
    ),
    figsize=(5, 5),
    scale=True
)
plt.savefig('square_dfts.png', dpi=300)

# %% csbs_ps -----

csbs(psfs_ps, sse_cost, 10, lam=1e0, order=1)
fourier_slices(psfs_ps)
plt.savefig('photonsieve_csbs.png', dpi=300)

# %% csbs_sq -----

plt.cla()
plt.close()

csbs(psfs_sq, sse_cost, 10, lam=1e0, order=1)
plt.imshow(psfs_sq.copies.reshape(7, 7), cmap='magma')
plt.figtext(
    0.98, 0.98, str(psfs_sq.csbs_params),
    horizontalalignment='right',
    rotation='vertical', fontsize='xx-small'
)
plt.axis('off')
cbar = plt.colorbar()
cbar.set_label('Copies')
plt.savefig('square_csbs_order1.png', dpi=300)

plt.cla()
plt.close()

psfs_sq.copies = np.repeat(5, 49)
csbs(psfs_sq, sse_cost, 10, lam=1e0, order=0)
plt.imshow(psfs_sq.copies.reshape(7, 7), cmap='magma')
plt.figtext(
    0.98, 0.98, str(psfs_sq.csbs_params),
    horizontalalignment='right',
    rotation='vertical', fontsize='xx-small'
)
plt.axis('off')
cbar = plt.colorbar()
cbar.set_label('Copies')
plt.savefig('square_csbs_order0.png', dpi=300)
