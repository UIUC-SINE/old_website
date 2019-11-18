#!/bin/env python3
# Ulas Kamaci - 2019-11-13
# image drift implementation on photon sieve forward model

import numpy as np
import copy
from skimage.transform import rescale
from scipy.stats import poisson
from skimage.draw import line
from mas.strand_generator import strands
from mas.psf_generator import PSFs, PhotonSieve, circ_incoherent_psf
from mas.forward_model import get_measurements, add_noise, size_equalizer, rectangle_adder
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from skimage.feature import register_translation

# %% scene
resolution_ratio = 5 # resolution_ratio = ccd_pixel_size / simulated_scene_pixel_size
fov_ratio = 2 # fov_ratio = simulated_imge_fov / ccd_fov
scene = strands(num_strands=100*fov_ratio, thickness=22*resolution_ratio, min_angle=-20, max_angle=20,
            image_width=160*resolution_ratio*fov_ratio, initial_width=512*resolution_ratio*fov_ratio)

plt.imshow(scene, cmap='gist_heat')
plt.show()

# %% params
# exposure parameters
total_exp_time = 10 # in seconds
frame_rate = 4 # in Hz
num_frames = int(total_exp_time*frame_rate)

# drift parameters
drift_angle = 10 * (2*np.pi/360) # in radians
drift_velocity = 0.2e-3 # in meter/second
# drift_velocity = 0 # in meter/second

# signal & noise parameters
max_count_rate = 20 # count/second/pixel
read_noise = 10 # std deviation for count/read/pixel
dark_current = 8 # in count/second/pixel
background_noise = 2 # in count/second/pixel
nonoise = False # test parameter to simulate noise-free frames

# ccd parameters
ccd_size = [160,160] # number of (rows,columns) in the photodetector array
pixel_size = 14e-6 # in meters

# sieve parameters
diameter = 75e-3 # in meters
smallest_hole_diameter = 17e-6 # in meters

# %% forward
ps = PhotonSieve(diameter=diameter, smallest_hole_diameter=smallest_hole_diameter)

# generate psfs
psfs = PSFs(
    ps,
    sampling_interval=pixel_size/resolution_ratio,
    measurement_wavelengths=np.array([30.4e-9]),
    source_wavelengths=np.array([30.4e-9]),
    psf_generator=circ_incoherent_psf,
    cropped_width=101,
    num_copies=1
)

# convolve the high resolution scene with the photon sieve PSF
# FIXME convolve this additionally with a Gaussian to simulate S/C jitter
convolved = get_measurements(sources=scene[np.newaxis,:,:], mode='circular', psfs=psfs)[0]

[r0, c0] = (400,0) # pick the topleft point for the initial frame
topleft_coords = [ # calculate the topleft points for all frames
    (
        int(r0 - k/frame_rate*drift_velocity*np.sin(drift_angle)/pixel_size*resolution_ratio),
        int(c0 + k/frame_rate*drift_velocity*np.cos(drift_angle)/pixel_size*resolution_ratio)
    )
    for k in range(num_frames+1)
]

frames = np.zeros((num_frames, ccd_size[0], ccd_size[1])) # initialize the frame images

# calculate each frame by integrating high resolution image along the drift
# direction
for frame in range(num_frames):
    temp = np.zeros((ccd_size[0]*resolution_ratio, ccd_size[1]*resolution_ratio))
    # calculate topleft coordinates for the shortest line connecting the
    # topleft coordinates of the consecutive frames
    path_rows, path_cols = line(
        topleft_coords[frame][0],
        topleft_coords[frame][1],
        topleft_coords[frame+1][0],
        topleft_coords[frame+1][1]
    )
    if len(path_rows) > 1:
        path_rows, path_cols = path_rows[:-1], path_cols[:-1]
    for row,col in zip(path_rows, path_cols):
        temp += convolved[row:row+temp.shape[0], col:col+temp.shape[1]]
    frames[frame] = rescale(temp, 1/resolution_ratio, anti_aliasing=False)

# add noise to the frames
if nonoise is False:
    frames = poisson.rvs(
        frames / frames.max() * (max_count_rate / frame_rate) +
        (dark_current + background_noise) / frame_rate
    )
    frames = np.random.normal(loc=frames, scale=read_noise)

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


# %% registration --------------------------------------------------------------
true_pixel_drift = drift_velocity / frame_rate * np.array([
    np.cos(drift_angle),
    np.sin(drift_angle)
]) / pixel_size # true drift from one to the next frame. notation: (x,y)

# form the array that will hold all the estimated pairwise shifts between the frames
est_pixel_drift = np.zeros((int(num_frames * (num_frames-1) / 2), 2)) # notation: (rows,cols) (-y,x)
counter = 0
for i in range(num_frames-1):
    for j in np.arange(i+1, num_frames):
        est_pixel_drift[counter], _, _ = register_translation(frames[i], frames[j])
        est_pixel_drift[counter] = est_pixel_drift[counter] / (j-i)
        counter += 1

est_pixel_drift_refined = copy.deepcopy(est_pixel_drift)
plt.figure()
plt.scatter(est_pixel_drift_refined[:,1], -est_pixel_drift_refined[:,0], s=3) # notation: plt.scatter(x,y)
for i in range(10):
    est_pixel_drift_refined = est_pixel_drift_refined[np.linalg.norm(
        est_pixel_drift_refined - np.mean(est_pixel_drift_refined, axis=0),
        axis=1
    ) < 40 * 2**(-i)
    ]
    plt.scatter(est_pixel_drift_refined[:,1], -est_pixel_drift_refined[:,0], s=3)
    print(np.mean(est_pixel_drift_refined, axis=0))

registered = np.zeros_like(frames[0])
for i in range(num_frames):
    registered += np.fft.ifft2(fourier_shift(np.fft.fft2(frames[i]), i*np.mean(est_pixel_drift_refined, axis=0))).real

plt.figure()
plt.imshow(registered, cmap='gist_heat')
plt.title('Registered Image')
