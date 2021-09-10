#!/usr/bin/env python
# Evan Widloski - 2021-03-13
# Compare phase correlation vs cross correlation accuracy for circular
# cross correlation problem with Gaussian noise and no signal prior.
# Expect cross-correlation to outperform phase-correlation since it is ML sol.

import numpy as np
import matplotlib.pyplot as plt
from mas.misc import experiment


def cc(a, b):
    """compute cross-correlogram of a, b"""
    return np.fft.ifft(np.fft.fft(a) * np.fft.fft(b).conj()).real


def pc(a, b):
    """compute phase-correlogram of a, b"""
    return np.fft.ifft(np.angle(np.fft.fft(a)) * np.angle(np.fft.fft(b)).conj()).real

def circular_diff(b, a, N):
    """compute difference (b - a) taking shortest path on circle of N points"""
    return (b - a + (N / 2)) % N - (N / 2)


def corr_exp(*, correlator, c, N, sigma):
    """Run a single correlation experiment
    Args:
        correlator (function): correlogram function
        c (int): circular shift amount
        N (int): length of vector
        sigma (float): gaussian noise std. dev.
    """
    # known ground truth
    mu = np.random.random(N)
    MU = np.fft.fft(mu)
    MU[20:] = 0
    mu = np.fft.ifft(MU).real

    # noisy observation
    x = np.random.normal(np.roll(mu, c), sigma**2)

    c_est = np.argmax(cc(x, mu))

    return {
        'err': circular_diff(c_est, c, N),
        'c_est': c_est,
        'abserr': np.abs(circular_diff(c_est, c, N)),
    }

result_cc = experiment(
    corr_exp,
    iterations=100000,
    correlator=cc,
    c=20,
    N=100,
    sigma=.9
)
print('cc:', (float(result_cc.err.mean())), float(result_cc.err.std()))

result_pc = experiment(
    corr_exp,
    iterations=100000,
    correlator=pc,
    c=20,
    N=100,
    sigma=.9
)
print('pc:', (float(result_pc.err.mean())), float(result_pc.err.std()))
