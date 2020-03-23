#!/bin/env python3
# Evan Widloski - 2020-03-19
# Guizar-Sicairos registration simultaneously utilizing all frames

import numpy as np
from skimage._shared.fft import fftmodule as fft


def _upsampled_dft(data, upsampled_region_size,
                   upsample_factor=1, axis_offsets=None):
    """
    Upsampled DFT by matrix multiplication.

    This code is intended to provide the same result as if the following
    operations were performed:
        - Embed the array "data" in an array that is ``upsample_factor`` times
          larger in each dimension.  ifftshift to bring the center of the
          image to (1,1).
        - Take the FFT of the larger array.
        - Extract an ``[upsampled_region_size]`` region of the result, starting
          with the ``[axis_offsets+1]`` element.

    It achieves this result by computing the DFT in the output array without
    the need to zeropad. Much faster and memory efficient than the zero-padded
    FFT approach if ``upsampled_region_size`` is much smaller than
    ``data.size * upsample_factor``.

    Parameters
    ----------
    data : array
        The input data array (DFT of original data) to upsample.
    upsampled_region_size : integer or tuple of integers, optional
        The size of the region to be sampled.  If one integer is provided, it
        is duplicated up to the dimensionality of ``data``.
    upsample_factor : integer, optional
        The upsampling factor.  Defaults to 1.
    axis_offsets : tuple of integers, optional
        The offsets of the region to be sampled.  Defaults to None (uses
        image center)

    Returns
    -------
    output : ndarray
            The upsampled DFT of the specified region.
    """
    # if people pass in an integer, expand it to a list of equal-sized sections
    if not hasattr(upsampled_region_size, "__iter__"):
        upsampled_region_size = [upsampled_region_size, ] * data.ndim
    else:
        if len(upsampled_region_size) != data.ndim:
            raise ValueError("shape of upsampled region sizes must be equal "
                             "to input data's number of dimensions.")

    if axis_offsets is None:
        axis_offsets = [0, ] * data.ndim
    else:
        if len(axis_offsets) != data.ndim:
            raise ValueError("number of axis offsets must be equal to input "
                             "data's number of dimensions.")

    im2pi = 1j * 2 * np.pi

    dim_properties = list(zip(data.shape, upsampled_region_size, axis_offsets))


    for (n_items, ups_size, ax_offset) in dim_properties[::-1]:
        kernel = ((np.arange(ups_size) + ax_offset)[:, None]
                  * fft.fftfreq(n_items, upsample_factor))
        # import ipdb
        # ipdb.set_trace()
        kernel = np.exp(-im2pi * kernel)

        # Equivalent to:
        #   data[i, j, k] = kernel[i, :] @ data[j, k].T
        data = np.tensordot(kernel, data, axes=(1, -1))
    return data


def guizar_multiframe(corr_sum, upsample_factor=100, start=10, end=30):
    """
    Efficient subpixel image translation registration by cross-correlation.
    Modified and simplified version of register_translation from skimage

    Args:
        corr_sum (ndarray): correlated and summed input frame groups
        upsample_factor (int): Upsampling factor

    Returns:
        shifts : ndarray
    """

    shape = np.array(corr_sum[0].shape)

    d = []
    for time_diff, cross_correlation in enumerate(corr_sum[start - 1:end - 1]):

        time_diff += start

        # coarse maxima
        maxima = np.unravel_index(
            np.argmax(np.abs(cross_correlation)),
            shape
        )

        # switch maxima coordinates from [(0, 0), (M, N)] to [(-M/2, -N/2), (M/2, N/2)]
        midpoints = shape // 2
        shifts = np.array(maxima, dtype=np.float64)
        shifts[shifts > midpoints] -= np.array(shape)[shifts > midpoints]

        # Initial shift estimate in upsampled grid

        # cast cupy.ndarray -> int
        upsampled_region_size = int(np.ceil(upsample_factor * 1.5))
        # Center of output array at dftshift + 1
        dftshift = upsampled_region_size // 2
        # upsample_factor = np.array(upsample_factor, dtype=np.float64)
        # normalization = (src_freq.size * upsample_factor ** 2)
        # Matrix multiply DFT around the current shift estimate
        sample_region_offset = shifts*upsample_factor - dftshift
        print(upsampled_region_size, upsample_factor, sample_region_offset, shifts)
        # import ipdb
        # ipdb.set_trace()
        cross_correlation = _upsampled_dft(
            # image_product.conj(),
            np.fft.ifftn(cross_correlation).conj(),
            upsampled_region_size,
            upsample_factor,
            sample_region_offset
        ).conj()
        # cross_correlation /= normalization
        # Locate maximum and map back to original pixel grid
        maxima = np.unravel_index(
            np.argmax(np.abs(cross_correlation)),
            cross_correlation.shape
        )
        CCmax = cross_correlation[maxima]

        maxima = np.array(maxima, dtype=np.float64) - dftshift

        shifts = shifts + maxima / upsample_factor

        d.append(np.array((shifts[1], -shifts[0])) / time_diff)
    d = np.array(d)
    guizar_error = np.mean(d, axis=0)

    return guizar_error, d
