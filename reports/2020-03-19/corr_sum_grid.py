from mas.strand_generator import StrandVideo
from html_slider import html_slider
from mas.tracking import correlate_and_sum
import numpy as np
from skimage.transform import resize

sv = StrandVideo()

# %% corr

corr_sum = abs(correlate_and_sum(sv.frames))
corr_sum = np.fft.fftshift(corr_sum, axes=(1, 2))

center = np.array(corr_sum.shape[1:]).astype(int) // 2

for n, cs in enumerate(corr_sum, 1):
    m = np.max(cs)
    cs[
        np.arange(
            center[0] - n // 2 - 10*n,
            center[0] - n // 2 + 10*n,
            step=n
        ),
        # center[0] - n // 2,
        :
    ] = m
    cs[
        :,
        np.arange(
            center[1] - n // 2 - 10*n,
            center[1] - n // 2 + 10*n,
            step=n
        ),
        # center[1] - n // 2
    ] = m

corr_sum = corr_sum[:, center[0]-50:center[0]+50, center[1]-50:center[1]+50]

# corr_sum = [resize(abs(cs), (300, 300)) for cs in corr_sum]
# corr_sum = np.array(corr_sum)

# %% slider

html_slider(corr_sum[5:18], output='corr_sum', labels=['correlation sum'])

