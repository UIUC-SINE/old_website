#!/bin/env python3
# Ulas Kamaci - 2019-11-13
# image drift implementation on photon sieve forward model

import numpy as np
import copy
from skimage.transform import rescale, resize
from scipy.stats import poisson
from skimage.draw import line, line_aa
from mas.strand_generator import strands, strand_video
from mas.psf_generator import PSFs, PhotonSieve, circ_incoherent_psf
from mas.forward_model import get_measurements, add_noise, size_equalizer, rectangle_adder
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from skimage.feature import register_translation
from scipy.ndimage import fourier_shift
from scipy.ndimage.filters import gaussian_filter
from scipy.signal import convolve2d
from mas.deconvolution import tikhonov, admm
from mas.deconvolution.admm import bm3d_pnp
from functools import partial

# %% forward

exp_time=10 # s
drift_angle=np.deg2rad(10) # radians
drift_velocity=0.2e-3 # meters / s
max_count=20
wavelengths=np.array([30.4e-9])
# CCD parameters
frame_rate=8 # Hz
ccd_size=(750, 750)
start=(400,0)
pixel_size=14e-6 # meters
# simulation subpixel parameters
resolution_ratio=2 # CCD pixel_size / simulation pixel_size
fov_ratio=2 # simulated FOV / CCD FOV
# sieve parameters
diameter=75e-3 # meters
smallest_hole_diameter=17e-6 # meters

frames, frames_clean, scene, topleft_coords = strand_video(
        # experiment parameters
        exp_time=exp_time, # s
        drift_angle=drift_angle, # radians
        drift_velocity=drift_velocity, # meters / s
        max_count=max_count,
        wavelengths=wavelengths,
        # CCD parameters
        frame_rate=frame_rate, # Hz
        ccd_size=ccd_size,
        start=start,
        pixel_size=pixel_size, # meters
        # simulation subpixel parameters
        resolution_ratio=resolution_ratio, # CCD pixel_size / simulation pixel_size
        fov_ratio=fov_ratio, # simulated FOV / CCD FOV
        # sieve parameters
        diameter=diameter, # meters
        smallest_hole_diameter=smallest_hole_diameter # meters
)

# ps = PhotonSieve(diameter=diameter, smallest_hole_diameter=smallest_hole_diameter)
#
# # generate psfs
# psfs = PSFs(
#     ps,
#     sampling_interval=pixel_size/resolution_ratio,
#     measurement_wavelengths=wavelengths,
#     source_wavelengths=wavelengths,
#     psf_generator=circ_incoherent_psf,
#     cropped_width=101,
#     num_copies=1
# )
#
# # convolve the high resolution scene with the photon sieve PSF
# # FIXME convolve this additionally with a Gaussian to simulate S/C jitter
# convolved = get_measurements(sources=scene[np.newaxis,:,:], mode='circular', psfs=psfs)[0]
#
# [r0, c0] = (400,0) # pick the topleft point for the initial frame
# topleft_coords = [ # calculate the topleft points for all frames
#     (
#         int(r0 - k/frame_rate*drift_velocity*np.sin(drift_angle)/pixel_size*resolution_ratio),
#         int(c0 + k/frame_rate*drift_velocity*np.cos(drift_angle)/pixel_size*resolution_ratio)
#     )
#     for k in range(num_frames+1)
# ]
#
# frames_clean = np.zeros((num_frames, ccd_size[0], ccd_size[1])) # initialize the frame images
#
# # calculate each frame by integrating high resolution image along the drift
# # direction
# for frame in range(num_frames):
#     temp = np.zeros((ccd_size[0]*resolution_ratio, ccd_size[1]*resolution_ratio))
#     # calculate topleft coordinates for the shortest line connecting the
#     # topleft coordinates of the consecutive frames
#     path_rows, path_cols = line(
#         topleft_coords[frame][0],
#         topleft_coords[frame][1],
#         topleft_coords[frame+1][0],
#         topleft_coords[frame+1][1]
#     )
#     if len(path_rows) > 1:
#         path_rows, path_cols = path_rows[:-1], path_cols[:-1]
#     for row,col in zip(path_rows, path_cols):
#         temp += convolved[row:row+temp.shape[0], col:col+temp.shape[1]]
#     frames_clean[frame] = rescale(temp, 1/resolution_ratio, anti_aliasing=False)
#
# # add noise to the frames
# if nonoise is False:
#     frames = poisson.rvs(
#         frames_clean / frames_clean.max() * (max_count_rate / frame_rate) +
#         (dark_current + background_noise) / frame_rate
#     )
#     frames = np.random.normal(loc=frames, scale=read_noise)
#     # set the negative values to zero
#     frames[frames < 0] = 0

# %% plot
pixel_arcsec = 72e-3
fig, ax = plt.subplots(1,2, figsize=(10.1,4.6))
ax[0].imshow(scene, cmap='gist_heat')
# ax[0].set_xticklabels([np.round(i*pixel_arcsec/resolution_ratio, decimals=1) for i in ax[0].get_xticks()])
# ax[0].set_yticklabels([np.round(i*pixel_arcsec/resolution_ratio, decimals=1) for i in ax[0].get_yticks()])
aa, bb = ccd_size[0] * resolution_ratio, ccd_size[1] * resolution_ratio
topleft = [list(topleft_coords[0]), list(topleft_coords[-1])]
topright = copy.deepcopy(topleft); topright[0][1] += bb; topright[1][1] += bb
botright = copy.deepcopy(topright); botright[0][0] += aa; botright[1][0] += aa
botleft = copy.deepcopy(botright); botleft[0][1] -= bb; botleft[1][1] -= bb
ax[0].plot([topleft[0][1], botleft[0][1]], [topleft[0][0], botleft[0][0]], 'b--', lw=2)
ax[0].plot([topright[1][1], botright[1][1]], [topright[1][0], botright[1][0]], 'b--', lw=2)
if np.sin(drift_angle) >= 0:
    ax[0].plot([topleft[0][1], topleft[1][1]], [topleft[0][0], topleft[1][0]], 'b--', lw=2)
    ax[0].plot([botright[0][1], botright[1][1]], [botright[0][0], botright[1][0]], 'b--', lw=2)
    ax[0].plot([botleft[0][1], botright[0][1]], [botleft[0][0], botright[0][0]], 'b--', lw=2)
    ax[0].plot([topleft[1][1], topright[1][1]], [topleft[1][0], topright[1][0]], 'b--', lw=2)
else:
    ax[0].plot([botleft[0][1], botleft[1][1]], [botleft[0][0], botleft[1][0]], 'b--', lw=2)
    ax[0].plot([topright[0][1], topright[1][1]], [topright[0][0], topright[1][0]], 'b--', lw=2)
    ax[0].plot([topleft[0][1], topright[0][1]], [topleft[0][0], topright[0][0]], 'b--', lw=2)
    ax[0].plot([botleft[1][1], botright[1][1]], [botleft[1][0], botright[1][0]], 'b--', lw=2)
for i in range(len(frames)):
    ax[1].imshow(frames[i], cmap='gist_heat')
    # ax[1].set_xticklabels([np.round(i*pixel_arcsec, decimals=1) for i in ax[1].get_xticks()])
    # ax[1].set_yticklabels([np.round(i*pixel_arcsec, decimals=1) for i in ax[1].get_yticks()])
    patch = Rectangle((topleft_coords[i][1],topleft_coords[i][0]),aa,bb,color='blue',alpha=0.4)
    ax[0].add_patch(patch)
    plt.pause(0.05)
    patch.remove()
    if i is not len(frames) - 1:
        plt.cla()


# %% register --------------------------------------------------------------
num_frames = frames.shape[0]
true_shift = drift_velocity / frame_rate * np.array([
    np.cos(drift_angle),
    np.sin(drift_angle)
]) / pixel_size # true drift from one to the next frame. notation: (x,y)

print('true_shift:({},{})'.format(true_shift[0],true_shift[1]))

# initialize the array that holds fourier transforms of the correlations between frame pairs
correlations_f = np.zeros((num_frames-1, frames.shape[1], frames.shape[2])).astype(np.complex128)

for i in range(num_frames-1):
    for j in np.arange(i+1, num_frames):
        # k^th element of correlations_f is the sum of all correlations between
        # frame pairs that are k frame apart from each other.
        correlations_f[j-i-1] += np.fft.fftn(frames[i]) * np.fft.fftn(frames[j]).conj()

correlations = np.fft.ifft2(correlations_f).real

for i in range(len(correlations)):
    # convolve the correlations with a gaussian to eliminate outlier peaks
    correlations[i] = gaussian_filter(correlations[i], sigma=1, mode='wrap')

shifts = np.zeros((correlations.shape[0], 2))

for i in range(correlations.shape[0]):
    # find the argmax points, which give the estimated shift
    shifts[i] = np.unravel_index(np.argmax(correlations[i]), correlations[i].shape)

# bring the shift values from [0,N] to [-N/2, N/2] format
shifts[shifts>np.fix(frames[0].shape[0]/2)] -= frames[0].shape[0]

# normalize the shifts to per frame shift
shifts = shifts / np.tile(np.arange(1,shifts.shape[0]+1), (2,1)).T

# determine what proportion of the shift estimates to use in the final shift estimation
# if `proportion` < 1, then we are not using the correlations of frame pairs that
# are very far from each other, the reason being that further apart frames have
# less overlap, where the nonoverlapping parts contribute to the correlation as
# 'noise', and reduce the accuracy.
proportion = 0.4

# estimate the shift using the first `proportion` of the shift array
shift_est = np.mean(shifts[:int(proportion * shifts.shape[0])], axis=0)
print('shift_est:({},{})'.format(shift_est[1],-shift_est[0]))


# initialize the array that will take the fourier transform of the correlations of correlations
correlations_f2 = np.zeros((num_frames-2, frames.shape[1], frames.shape[2])).astype(np.complex128)

for i in range(num_frames-2):
    for j in np.arange(i+1, num_frames-1):
        # compute the correlations between correlations to get a more refined estimate of drift
        correlations_f2[j-i-1] += np.fft.fftn(correlations[i]) * np.fft.fftn(correlations[j]).conj()

correlations2 = np.fft.ifft2(correlations_f2).real

for i in range(len(correlations2)):
    # convolve the correlations with a gaussian to eliminate outlier peaks
    correlations2[i] = gaussian_filter(correlations2[i], sigma=1, mode='wrap')

shifts2 = np.zeros((correlations2.shape[0], 2))

for i in range(correlations2.shape[0]):
    shifts2[i] = np.unravel_index(np.argmax(correlations2[i]), correlations2[i].shape)

shifts2[shifts2>np.fix(frames[0].shape[0]/2)] -= frames[0].shape[0]
shifts2 = shifts2 / np.tile(np.arange(1,shifts2.shape[0]+1), (2,1)).T

shift_est2 = -np.mean(shifts2[:int(proportion * shifts2.shape[0])], axis=0)
print('shift_est2:({},{})'.format(shift_est2[1],-shift_est2[0]))

registered = np.zeros_like(frames[0])
for i in range(num_frames):
    registered += np.fft.ifft2(fourier_shift(np.fft.fft2(frames[i]), i*shift_est2)).real

plt.figure()
plt.imshow(registered, cmap='gist_heat')
plt.title('Registered Image')
plt.show()


# %% deblur --------------------------------------------------------------
# first create a motion blur kernel on a grid with 1 um pixel size
pixel_size_um = pixel_size * 1e6

# width of the final motion blur kernel with CCD pixel size
kernel_size = 11
(x,y) = (pixel_size_um * shift_est2[1], -pixel_size_um * shift_est2[0])
N = int(np.ceil(np.max((abs(x),abs(y)))))

# set the shape of the initial kernel with 1 um pixels based on the estimated drift
kernel_um = np.zeros((2*N+1, 2*N+1))

# calculate the line representing the motion blur
rr, cc, val = line_aa(
    N + np.round((y/2)).astype(int),
    N - np.round((x/2)).astype(int),
    N - np.round((y/2)).astype(int),
    N + np.round((x/2)).astype(int),
)

# update the kernel with the calculated line
kernel_um[rr,cc] = val

# resize the initial 1 um kernel to the given pixel size
kernel = resize(size_equalizer(kernel_um, [int(pixel_size_um)*kernel_size]*2), [kernel_size]*2, anti_aliasing=True)

# compute the analytical photon sieve PSF with the given pixel size
psfs = PSFs(
    ps,
    sampling_interval=pixel_size,
    measurement_wavelengths=wavelengths,
    source_wavelengths=wavelengths,
    psf_generator=circ_incoherent_psf,
    cropped_width=kernel_size,
    num_copies=1
)

psf_orig = copy.deepcopy(psfs.psfs[0,0])

# convolve the photon sieve PSF with the motion blur kernel to find the "effective blurring kernel"
psfs.psfs[0,0] = convolve2d(psfs.psfs[0,0], kernel, mode='same')

# normalize the kernel
psfs.psfs[0,0] /= psfs.psfs[0,0].sum()

# normalize the registered image (doesn't change anything but helps choosing regularization parameter consistently)
registered /= registered.max()

# do a tikhonov regularized deblurring on the registered image to remove the
# in-frame blur with the calculated "effective blurring kernel"
recon_tik = tikhonov(
    measurements=registered[np.newaxis,:,:],
    psfs=psfs,
    tikhonov_lam=1e1,
    tikhonov_order=1
)
plt.figure()
plt.imshow(recon_tik[0], cmap='gist_heat')
plt.title('Deblurred Tikhonov')
plt.show()

# do a Plug and Play with BM3D reconstruction with tikhonov initialization
recon = admm(
    measurements=registered[np.newaxis,:,:],
    psfs=psfs,
    regularizer=partial(bm3d_pnp),
    recon_init=recon_tik,
    iternum=5,
    periter=1,
    nu=10**0.0,
    lam=[10**-0.5]
)

plt.figure()
plt.imshow(recon[0], cmap='gist_heat')
plt.title('Deblurred')
plt.show()


# This commented out part is my (Ulas') first registration implementation that
# is based on taking the mean of the argmaxes.
# ----------------------------------------------------------------------------
# # form the array that will hold all the estimated pairwise shifts between the frames
# est_pixel_drift = np.zeros((int(num_frames * (num_frames-1) / 2), 2)) # notation: (rows,cols) (-y,x)
# counter = 0
# for i in range(num_frames-1):
#     for j in np.arange(i+1, num_frames):
#         est_pixel_drift[counter], _, _ = register_translation(frames[i], frames[j], upsample_factor=20)
#         est_pixel_drift[counter] = est_pixel_drift[counter] / (j-i)
#         counter += 1
#
# est_pixel_drift_refined = copy.deepcopy(est_pixel_drift)
# plt.figure()
# plt.scatter(est_pixel_drift_refined[:,1], -est_pixel_drift_refined[:,0], s=3) # notation: plt.scatter(x,y)
# for i in range(10):
#     shrinked_list = est_pixel_drift_refined[np.linalg.norm(
#         est_pixel_drift_refined - np.mean(est_pixel_drift_refined, axis=0),
#         axis=1
#     ) < 40 * 2**(-i)
#     ]
#     if shrinked_list.shape[0] > 0:
#         est_pixel_drift_refined = shrinked_list
#     else:
#         break
#     plt.scatter(est_pixel_drift_refined[:,1], -est_pixel_drift_refined[:,0], s=3)
#     print(np.mean(est_pixel_drift_refined, axis=0))
#
# registered = np.zeros_like(frames[0])
# for i in range(num_frames):
#     registered += np.fft.ifft2(fourier_shift(np.fft.fft2(frames[i]), i*np.mean(est_pixel_drift_refined, axis=0))).real
#
# plt.figure()
# plt.imshow(registered, cmap='gist_heat')
# plt.title('Registered Image')
