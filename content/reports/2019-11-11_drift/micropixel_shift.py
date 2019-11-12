#!/bin/env python3
# Evan Widloski - 2019-11-11
# image drift implementation

from skimage.draw import line
import numpy as np
import matplotlib.pyplot as plt
from mas.plotting import plotter4d
from mas.forward_model import size_equalizer

image_width = 100
ccd_width = 2
# number of micropixels inside a ccd pixel (along a single dimension)
micropixel_scale = 10

# assert ccd smaller than high resolution grid
assert ccd_width * micropixel_scale < image_width

# generate 4D identity matrix representing CCD
ccd = np.eye(ccd_width**2).reshape(ccd_width, ccd_width, ccd_width, ccd_width)
# upsample CCD matrix according to micropixel_scale
ccd = np.repeat(
    np.repeat(
        ccd,
        repeats=micropixel_scale,
        axis=2
    ),
    repeats=micropixel_scale,
    axis=3
)
# embed ccd in (image_width, image_width) matrix
ccd = size_equalizer(ccd, (image_width, image_width))

# convolve CCD matrix with drift path
points = np.array(line(20, 20, 40, 40)).T - (image_width // 2, image_width // 2)
sense_vec = np.zeros((ccd_width, ccd_width, image_width, image_width))
for point in points:
    sense_vec += np.roll(ccd, point, axis=(2,3))

plotter4d(sense_vec)
