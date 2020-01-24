#!/bin/env python3

import numpy as np
from mas.strand_generator import strand_video
from matplotlib import pyplot as plt
from mas.deconvolution import tikhonov
# from mas.tracking import multi_register
from mas.tracking import multi_register_cupy as multi_register
from mas.decorators import _vectorize


# %% forward

exp_time=10 # s
drift_angle=np.deg2rad(-45) # radians
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
true_drift = drift_velocity / frame_rate * np.array([
    np.cos(drift_angle),
    -np.sin(drift_angle)
]) / pixel_size # true drift from one to the next frame. notation: (x,y)

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
    smallest_hole_diameter=smallest_hole_diameter, # meters
    noise_model=None
)

argmaxes, phase_correlations, separations = multi_register(frames)

# %% register

def center_of_mass(image):
    """Compute circular center of mass of an image"""

    # sum columns, rows
    xs, ys = image.sum(axis=0), image.sum(axis=1)

    # compute circular distance
    dist_xs = np.roll(
        np.abs(np.arange(-len(xs) // 2 + 1, len(xs) // 2 + 1)),
        -len(xs) // 2 + 1
    )
    dist_ys = np.roll(
        np.abs(np.arange(-len(ys) // 2 + 1, len(ys) // 2 + 1)),
        -len(ys) // 2 + 1
    )

    # compute circular center of masses
    com_x = np.argmin(np.fft.ifftn(np.fft.fft(xs) * np.fft.fft(dist_xs)).real)
    com_y = np.argmin(np.fft.ifftn(np.fft.fft(ys) * np.fft.fft(dist_ys)).real)

    return np.array((com_x, com_y))

    # # %% test

    # # test circle
    # image = np.zeros((300, 300))
    # xx, yy = np.meshgrid(np.arange(300), np.arange(300))
    # # image[np.linalg.norm(np.array((149, 149)) - np.stack((xx, yy), axis=2), axis=2) < 50] = 1
    # image[np.linalg.norm(np.array((10, 10)) - np.stack((xx, yy), axis=2), axis=2) < 50] = 1
    # image[np.linalg.norm(np.array((10, 310)) - np.stack((xx, yy), axis=2), axis=2) < 50] = 1
    # image[np.linalg.norm(np.array((310, 10)) - np.stack((xx, yy), axis=2), axis=2) < 50] = 1
    # image[np.linalg.norm(np.array((310, 310)) - np.stack((xx, yy), axis=2), axis=2) < 50] = 1

def maximum(image):

    return np.unravel_index(np.argmax(image), image.shape)

def roll(x, shift):
    shift = np.round(shift).astype(int)
    return np.roll(
        np.roll(
            x,
            shift[1],
            axis=0
        ),
        shift[0],
        axis=1
    )

def shift_and_sum(phase_correlations, shift):
    summation = np.zeros(frames[0].shape, dtype='complex128')

    for time_diff, phase_correlation in enumerate(phase_correlations):
        time_diff += 1 # enumerate starts at 0
        integer_shift = np.round(np.array(shift) * (time_diff)).astype(int)
        shifted = roll(phase_correlation, integer_shift)
        summation += shifted

    return summation.real


shift_est = np.array((0, 0))
for _ in range(10):
    image = shift_and_sum(phase_correlations, -shift_est)
    shift_est += center_of_mass(image)
    shift_est %= np.array(image.shape)

    print('shift_est:', shift_est)
    plt.imshow(image.real)
    plt.show()

    input()

print(center_of_mass(image))
