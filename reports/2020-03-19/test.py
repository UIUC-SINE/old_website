#!/bin/env python3
# Evan Widloski - 2020-03-19
# Guizar-Sicairos registration simultaneously utilizing all frames

import numpy as np
import matplotlib.pyplot as plt
from mas.strand_generator import StrandVideo
from mas.tracking import correlate_and_sum
from register_translation import guizar_multiframe
from mas.forward_model import size_equalizer, downsample
from downsample_test import downsample2
from skimage.transform import rescale

# %% generate

sv = StrandVideo(angle_velocity=0)

corr_sum = correlate_and_sum(sv.frames)

# %% coarse

max_scale = len(corr_sum)
scale_factor = np.array(corr_sum[0].shape) // len(corr_sum)

coarse_list = []
for n, cs in enumerate(corr_sum, 1):
    coarse_list.append(
        downsample2(
            cs[:scale_factor[0] * n, :scale_factor[1] * n],
            n
        )
    )

coarse = abs(np.array(coarse_list).sum(axis=0))

coarse_est = np.unravel_index(np.argmax(coarse), coarse.shape)

# %% fine

fine_list = []
fine_argmaxes = []
# FIXME - corr_sum must be real for rescale()
corr_sum = abs(corr_sum)
for n, cs in enumerate(corr_sum, 1):
    print(n)
    sfx, sfy = scale_factor
    rescaled = rescale(
        cs[:sfx * n, :sfy * n],
        float(max_scale) / n)[
            :sfx * max_scale,
            :sfy * max_scale
        ]
    fine_list.append(rescaled)
    fine_argmaxes.append(np.unravel_index(np.argmax(rescaled), rescaled.shape))

fine = np.array(fine_list)

weights = np.arange(1, max_scale + 1)**2
weights = weights / weights.sum()
weights[-2:] = 0

result = np.sum(weights[:, np.newaxis, np.newaxis] * fine, axis=0)

fine_est = np.array(np.unravel_index(np.argmax(result), result.shape)) / max_scale
