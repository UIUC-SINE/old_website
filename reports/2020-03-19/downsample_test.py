#!/bin/env python3
# Evan Widloski - 2020-03-21
# compare default downsampler with shifted version

from mas.strand_generator import StrandVideo
from mas.tracking import correlate_and_sum
from mas.forward_model import upsample, downsample, downsample2, size_equalizer
import numpy as np
from html_slider import html_slider
import matplotlib.pyplot as plt

# %% begin

sv = StrandVideo(angle_velocity=0)
cs = correlate_and_sum(sv.frames_clean)

# %% draw_patches

plt.imshow(abs(cs[35]))
for line in np.arange(18, cs.shape[1], step=36):
    plt.axhline(line, color='red')
for line in np.arange(18, cs.shape[2], step=36):
    plt.axvline(line, color='red')
plt.savefig('newgrid.png')

plt.close()

plt.imshow(abs(cs[35]))
for line in np.arange(cs.shape[1], step=36):
    plt.axhline(line, color='red')
for line in np.arange(cs.shape[2], step=36):
    plt.axvline(line, color='red')
plt.savefig('oldgrid.png')

# %% downsample

# maximum downsample so image is 20 x 20
maximum_factor = cs.shape[1] // 20

downsampled = [downsample(cs[n], n+1)[:19, :19] for n in range(maximum_factor)]
downsampled2 = [downsample2(cs[n], n+1)[:19, :19] for n in range(maximum_factor)]

x = np.stack((downsampled, downsampled2), axis=0)

html_slider(x, labels=['ds. method', 'ds. factor'], output='downsample')
