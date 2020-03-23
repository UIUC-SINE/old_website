#!/bin/env python3
# Evan Widloski - 2020-03-21
# Reimplementing _upsampled_dft

import numpy as np
import matplotlib.pyplot as plt
from register_translation import _upsampled_dft


argmax = np.array([20, 20])

x = np.zeros((100, 100))
x[argmax] = 1

upsample_factor = 100
upsample_window_size = 1.5 * upsample_factor
upsample_window_offset = argmax * upsample_factor - upsample_window_size // 2

res = _upsampled_dft(x, upsample_window_size, upsample_factor)
# w1, w2 = np.meshgrid(*[np.arange(upsample_window_size)]*2)

