#!/bin/env python3
# Evan Widloski - 2020-03-18
# Show error from each correlation sum

import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import circulant
from mas.tracking import correlate_and_sum

N = 100

# signal
x = np.random.random((100, 1))

# noise
noise_var = 1


# generate frames
frames_clean = circulant(x).T[:, :, np.newaxis]
frames_noise = np.random.normal(
    size=frames_clean.shape,
    scale=np.sqrt(noise_var)
)
frames = frames_clean + frames_noise

corr_sum_clean = correlate_and_sum(frames_clean)
corr_sum_noise = correlate_and_sum(frames_noise)
corr_sum = correlate_and_sum(frames)

