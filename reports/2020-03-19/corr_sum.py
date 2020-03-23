from mas.strand_generator import StrandVideo
from html_slider import html_slider
from mas.tracking import correlate_and_sum
import numpy as np
from skimage.transform import resize

sv = StrandVideo()

# %% corr

corr_sum = abs(correlate_and_sum(sv.frames))
corr_sum = np.fft.fftshift(corr_sum, axes=(1, 2))
corr_sum = [resize(abs(cs), (300, 300)) for cs in corr_sum]
corr_sum = np.array(corr_sum)

# %% slider

html_slider(corr_sum, output='corr_sum', labels=['correlation sum'])

