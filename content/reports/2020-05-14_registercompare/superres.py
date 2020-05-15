# Evan Widloski - 2020-05-14
# Comparing Cross Correlation and Phase Correlation

import numpy as np

from mas.strand_generator import StrandVideo
from mas.misc import combination_experiment
from mas.forward_model import upsample
from mas.tracking.tracking import (
    guizar_multiframe, correlate_and_sum, shift_and_sum
)

sv = StrandVideo()

corr_sum = correlate_and_sum(sv.frames, mode='PC')
est_drift, _ = guizar_multiframe(corr_sum)

upsampled = upsample(sv.frames, factor=10)

recon = shift_and_sum(sv.frames, est_drift)

