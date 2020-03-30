#!/bin/env python3
# Evan Widloski - 2020-03-28
# test registration on upscaled AIA data

from skimage.transform import resize
from mas.strand_generator import StrandVideo, get_visors_noise
from mas.tracking import guizar_multiframe, correlate_and_sum, shift_and_sum, guizar_upsample
from mas.misc import combination_experiment
from html_slider.html_slider import render_pandas
import numpy as np
from imageio import imread

resolution_ratio = 2
fov_ratio = 2
scene = imread('scene.bmp')
size = np.array((750, 750))
scene = resize(scene, size * resolution_ratio * fov_ratio)

def experiment(*, max_count, background_noise, drift_velocity, frame_rate):

    # noise
    noise_model = get_visors_noise(background=background_noise)
    sv = StrandVideo(
        ccd_size=size,
        start=((1400, 1300)),
        scene=scene,
        max_count=max_count,
        noise_model=noise_model,
        drift_velocity=drift_velocity * 1e-3,
        resolution_ratio=resolution_ratio,
        fov_ratio=fov_ratio,
        frame_rate=frame_rate
    )

    # register
    corr_sum = correlate_and_sum(sv.frames)
    drift, _ = guizar_multiframe(corr_sum)
    # drift_u, _ = guizar_upsample(corr_sum)

    # reconstruct
    coadded = shift_and_sum(sv.frames, drift, mode='crop')
    coadded = resize(coadded, (300, 300))

    frame = resize(sv.frames[0], (300, 300))

    return {
        'coadded': coadded,
        'frame': frame,
        'est_drift': drift,
        # 'est_drift_u': drift_u,
        'true_drift': sv.true_drift,
        # 'd': d
    }


# %% experiment

results = combination_experiment(
    experiment,
    # max_count=[20, 40, 80],
    # background_noise=[25, 50, 100, 200],
    # drift_velocity=[0.05, 0.1, 0.2, 0.4],
    # frame_rate=[4, 6, 8]
    max_count=[80],
    background_noise=[100],
    drift_velocity=[0.2],
    frame_rate=[4]
)

# results.to_pickle('results.pkl')

# %% slider

render_pandas(
    results,
    output='noisy_frame',
    slider_cols=['max_count', 'background_noise', 'drift_velocity', 'frame_rate'],
    slider_defaults=[0, 2, 2, 0],
    im_col='frame'
)

render_pandas(
    results,
    output='coadded',
    slider_cols=['max_count', 'background_noise', 'drift_velocity', 'frame_rate'],
    slider_defaults=[0, 2, 2, 0],
    indicator_cols=['true_drift', 'est_drift'],
    im_col='coadded'
)
