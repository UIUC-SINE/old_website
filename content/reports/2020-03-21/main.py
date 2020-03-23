from skimage.transform import resize
from mas.strand_generator import StrandVideo, get_visors_noise
from mas.tracking import guizar_multiframe, correlate_and_sum, shift_and_sum
from mas.misc import combination_experiment
from html_slider.html_slider import render_pandas
import numpy as np

scene = StrandVideo(noise_model=None).scene

def experiment(*, max_count, background_noise, drift_velocity):

    # noise
    noise_model = get_visors_noise(background=background_noise)
    sv = StrandVideo(
        scene=scene,
        max_count=max_count,
        noise_model=noise_model,
        drift_velocity=drift_velocity * 1e-3,
    )
    noise = sv.frames - sv.frames_clean

    # register
    corr_sum = correlate_and_sum(sv.frames)
    drift, _ = guizar_multiframe(corr_sum)

    # reconstruct
    recon = shift_and_sum(sv.frames, drift)
    noise_recon = shift_and_sum(noise, drift)

    result = resize(recon, (300, 300))

    snr_db = 10 * np.log10(
        np.sum((recon - noise_recon)**2) / np.sum(noise_recon**2)
    )

    return {
        'result': result,
        'est_drift': drift,
        'true_drift': sv.true_drift,
        'snr_db': snr_db,
    }

# %% experiment

results = combination_experiment(
    experiment,
    max_count=[20, 40, 80],
    background_noise=[0, 2, 4, 8, 16],
    drift_velocity=[0.05, 0.1, 0.2, 0.4]
    # max_count=[20],
    # background_noise=[8],
    # drift_velocity=[0.2],
)

# results.to_pickle('results.pkl')

# %% slider

render_pandas(
    results,
    slider_cols=['max_count', 'background_noise', 'drift_velocity'],
    slider_defaults=[0, 3, 2],
    indicator_cols=['snr_db', 'true_drift', 'est_drift'],
    im_col='result'
)
