#!/bin/env python3
# Evan Widloski - 2019-10-21
# compare 1D motion estimate accuracy for one long integration vs
#    many smaller noisy ones

import numpy as np
import matplotlib.pyplot as plt
from mas.misc import experiment

def exp(x, num_frames, shift, noise):
    """Run correlation experiment for single noise realization
    Args:
        x: input image
        num_frames: number of integrations/frames
        shift: drift ground truth for error computation
        noise: noise function which takes x and num_frames
    """

    x_repeat = [x] * num_frames
    x_shift = [np.roll(x, shift * (frame + 1)) for frame in range(num_frames)]

    # poisson noise
    y = noise(x_shift, num_frames)

    # correlate all signals using fft

    correlations = np.fft.ifft(
        np.fft.fft(x_repeat, axis=1).conj() *
        np.fft.fft(y, axis=1),
        axis=1
    )

    correlation_sum = np.zeros(len(x), dtype='complex128')
    for m, correlation in enumerate(correlations):
        correlation_sum += np.roll(correlation, -m)

    shift_est = np.argmax(correlation_sum)
    err = min(abs(shift_est - shift), abs(shift - shift_est))

    return {'correlation': correlation, 'sq_err': err**2, 'shift_est': shift_est, 'err': err}


# randomly generated image
x = [16, 20, 8, 13, 7, 13, 14, 4, 5, 14]

def noise(x, num_frames):
    return (
        np.random.poisson(
            (np.array(x) + 8 + 2) / num_frames
        ) +
        np.random.normal(0, scale=10)
    )


oneframe = experiment(
    exp,
    iterations=10000,
    x=x,
    num_frames=1,
    shift=1,
    noise=noise
)

print()
multframe = experiment(
    exp,
    iterations=10000,
    x=x,
    num_frames=10,
    shift=1,
    noise=noise
)

print('oneframe:', oneframe.err.mean())
print('multframe:', multframe.err.mean())

# oneframe: 0.31341400
# multframe: 0.312758
