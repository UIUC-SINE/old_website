#!/usr/bin/env python

from imageio import imwrite
from mas.strand_generator import StrandVideo
import numpy as np
import imageio

# %% generate

frame = StrandVideo().frames[0]

# scale to 16 bits
dtype = 'uint16'
frame = np.iinfo(dtype).max * (frame - frame.min()) / (frame.max() - frame.min())

imageio.imwrite('out.png', frame.astype(dtype))

# %%
