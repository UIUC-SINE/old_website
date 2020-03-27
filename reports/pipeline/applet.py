#!/bin/env python3
# Evan Widloski - 2020-03-27
# Generate applet showing single noisy frame under different conditions

from skimage.transform import resize
from mas.strand_generator import StrandVideo, get_visors_noise
from mas.tracking import guizar_multiframe, correlate_and_sum, shift_and_sum
from mas.misc import combination_experiment
from html_slider.html_slider import render_pandas
import numpy as np

scene = StrandVideo(noise_model=None).scene

def experiment(*, max_count, background_noise, drift_velocity, frame_rate):

    # noise
    noise_model = get_visors_noise(background=background_noise)
    sv = StrandVideo(
        scene=scene,
        max_count=max_count,
        noise_model=noise_model,
        drift_velocity=drift_velocity * 1e-3,
        frame_rate=frame_rate
    )

    # register
    corr_sum = correlate_and_sum(sv.frames)
    drift, _ = guizar_multiframe(corr_sum)

    # reconstruct
    coadded = shift_and_sum(sv.frames, drift, mode='crop')
    coadded = resize(coadded, (300, 300))

    frame = resize(sv.frames[0], (300, 300))

    return {
        'coadded': coadded,
        'frame': frame,
        'est_drift': drift,
        'true_drift': sv.true_drift,
    }


# %% experiment

results = combination_experiment(
    experiment,
    max_count=[20, 40, 80],
    background_noise=[25, 50, 100, 200],
    drift_velocity=[0.05, 0.1, 0.2, 0.4],
    frame_rate=[4, 6, 8]
)

results.to_pickle('results.pkl')

# %% slider

render_pandas(
    results,
    output='coadded',
    slider_cols=['max_count', 'background_noise', 'drift_velocity', 'frame_rate'],
    slider_defaults=[0, 2, 2, 0],
    indicator_cols=['true_drift', 'est_drift'],
    im_col='coadded'
)

render_pandas(
    results,
    output='noisy_frame',
    slider_cols=['max_count', 'background_noise', 'drift_velocity', 'frame_rate'],
    slider_defaults=[0, 2, 2, 0],
    indicator_cols=['true_drift', 'est_drift'],
    im_col='frame'
)
