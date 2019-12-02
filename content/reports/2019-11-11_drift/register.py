#!/bin/env python3
# Evan Widloski - 2019-11-18
# Test averaged registration method

from itertools import combinations
import numpy as np
from skimage.feature import register_translation
from scipy.ndimage.measurements import center_of_mass
import matplotlib.pyplot as plt

from mas.strand_generator import strand_video
from mas.tracking import phase_correlate

# %% setup - compute frames and correlations

pixel_size = 14e-6
frame_rate = 8
drift_angle = np.deg2rad(-45)
drift_velocity = 0.1e-3

frames = strand_video(
    frame_rate=frame_rate,
    drift_angle=drift_angle,
    drift_velocity=drift_velocity,
    pixel_size=pixel_size,
    noise_model=None
)

def corr(a, b):
    return np.abs(
        np.fft.ifftn(
            np.fft.fftn(a) * np.fft.fftn(b).conj()
        )
    )

phase_correlations = []
time_diffs = []
for i, j in combinations(range(len(frames)), 2):
    phase_correlations.append(corr(frames[i], frames[j]))
    time_diffs.append(j - i)
phase_correlations = np.array(phase_correlations)
time_diffs = np.array(time_diffs)


true_pixel_drift = drift_velocity / frame_rate * np.array([
    np.cos(drift_angle),
    np.sin(drift_angle)
]) / pixel_size # true drift from one to the next frame. notation: (x,y)

# %% register

# ests = []
# for n, phase_correlations_n in enumerate(phase_correlations):
#     for phase_correlation in phase_correlations_n:
#         ests.append(np.unravel_index(np.argmax(np.abs(phase_correlation)), (160, 160)))
# ests = np.array(ests)

# pos = 0
# for n in reversed(range(len(frames - 1))):
#     print(n)
#     pos += n
#     plt.scatter(ests[pos:pos + n, 0], ests[pos:pos + n, 1])

# initial registration estimate
# ests = []
# for n, phase_correlations_n in enumerate(phase_correlations):
#     phase_correlation_n = np.zeros(frames[0].shape)
#     for phase_correlation in phase_correlations_n:
#         phase_correlation_n += phase_correlation
#     ests.append(np.unravel_index(np.argmax(np.abs(phase_correlation_n)), (160, 160)))
# ests = np.array(ests)

# %% shift_sum

from mas.decorators import _vectorize

def roll(x, shift):
    return np.roll(
        np.roll(
            x,
            shift[1],
            axis=0
        ),
        shift[0],
        axis=1
    )

# @_vectorize(signature='(i)->(j,k)', included=['shift'])
@_vectorize(signature='(i)->(j,k)', included=[2])
def shift_and_sum(phase_correlations, time_diffs, shift):
    print(shift)
    summation = np.zeros(frames[0].shape)

    for phase_correlation, time_diff in zip(phase_correlations, time_diffs):
        integer_shift = np.round(shift * time_diff).astype(int)
        shifted = roll(phase_correlation, integer_shift)
        summation += shifted

    return summation

# %% iterate

true_pixel_drift = drift_velocity / frame_rate * np.array([
    np.cos(drift_angle),
    np.sin(drift_angle)
]) / pixel_size # true drift from one to the next frame. notation: (x,y)

def dumb_estimate(phase_correlations, time_diffs):
    ests = []
    for time_diff in range(1, len(frames)):
        pcs = phase_correlations[np.where(time_diffs == time_diff)]
        est = np.array(
            np.unravel_index(
                np.argmax(
                    roll(np.sum(pcs, axis=0), (80, 80))
                ),
                frames[0].shape
            )
        ) - (80, 80)
        est = est / time_diff
        ests.append(est)

    return ests
