import numpy as np
from matplotlib import pyplot as plt
from skimage.data import camera, moon
from mas.forward_model import add_noise

c = camera().astype(float)
m = moon().astype(float)
y1 = c + m
y2 = np.roll(c, (-10, -15), (0, 1)) + np.roll(m, (20, 25), (0, 1))
y1 = add_noise(y1, dbsnr=30, model='gaussian')
y2 = add_noise(y2, dbsnr=30, model='gaussian')
# y1 = c
# y2 = np.roll(c, (-10, -15), (0, 1))



def exp_2d(m_0, n_0, shape=y1.shape):
    # m, n = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]))
    # return np.e**(
    #     1j * 2 * np.pi * (m_0 * m / shape[0] + n_0 * n / shape[1])
    # ) / (shape[0] * shape[1])
    z = np.zeros(shape)
    z[m_0, n_0] = 1
    return np.fft.ifftn(z) * shape[0] * shape[1]

# %% 1source

# y1_1 = camera()
# y2_1 = np.roll(y1_1d, (-10, -15), (0, 1))
# plt.imshow(np.fft.ifftn(np.fft.fftn(y2_1) / exp_2d(10, 15, shape=(512, 512))).real)
# plt.colorbar()
# plt.figure()
# plt.imshow(y1_1)
# plt.colorbar()
# plt.show()

# %% foo


def pinv(A):
    """pinv on first two-dimensions of 4D array"""
    a_flip = np.moveaxis(A, (0, 1, 2, 3), (2, 3, 0, 1))
    a_inv = np.linalg.pinv(a_flip)
    return np.moveaxis(a_inv, (2, 3, 0, 1), (0, 1, 2, 3))


A = np.array(
    (
        (np.ones(y1.shape), np.ones(y1.shape)),
        (exp_2d(10, 15), exp_2d(-20, -25))
    )
)
# A = np.array(
#     (
#         np.ones(y1.shape),
#         exp_2d(10, 15)
#     )
# )[:, np.newaxis]

A_inv = pinv(A)
Y = np.array((np.fft.fftn(y1), np.fft.fftn(y2)))
result = np.einsum('abcd,bcd->acd', A_inv, Y)
