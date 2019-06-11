#!/bin/env python3
# Evan Widloski - 2019-06-01
# Testing FFT-based deconvolution

import numpy as np

def zeropad(x, padded_size):
    """zeropad 1D array x to size padded_size"""

    return np.pad(x, (0, padded_size - len(x)), mode='constant')

def fft_deconvolve(a, b, mode='full'):
    max_size = np.max((len(a), len(b)))
    padded_size = max_size
    A = np.fft.fft(zeropad(a, padded_size))
    B = np.fft.fft(zeropad(b, padded_size))
    # import ipdb
    # ipdb.set_trace()

    if mode == 'full':
        return np.fft.ifft(A / B)
    elif mode == 'valid':
        min_size = np.min((len(a), len(b)))
        return np.fft.ifft(A / B)[:max_size - min_size + 1]

np.random.seed(1)
a = np.random.random(7)
b = np.random.random(4)
min_length = np.min((len(a), len(b)))

# do full convolution in frequency domain (a ★ b = c)
A = np.fft.fft(zeropad(a, len(a) + len(b) - 1))
B = np.fft.fft(zeropad(b, len(a) + len(b) - 1))
C = A * B
c_full = np.fft.ifft(C)
c_valid = c_full[min_length - 1:-(min_length - 1)]

print('------ full convolve -------')
print(np.convolve(a, b, mode='full') - c_full)
print('------ valid convolve -------')
print(np.convolve(a, b, mode='valid') - c_valid)

print('------ full deconvolve -------')
print(np.fft.ifft(C / A) - zeropad(b, 10))
print('------ valid deconvolve -------')
print(np.fft.ifft(C / A)[:len(b)] - b)

print('------ full deconvolve, func -------')
print(fft_deconvolve(c_full, a, mode='full') - zeropad(b, 10))
print('------ valid deconvolve, func -------')
print(fft_deconvolve(c_full, a, mode='valid') - b)
