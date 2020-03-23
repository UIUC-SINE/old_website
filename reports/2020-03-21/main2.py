from skimage.transform import resize
from mas.strand_generator import StrandVideo, get_visors_noise
from mas.tracking import guizar_multiframe, correlate_and_sum, shift_and_sum
from mas.misc import combination_experiment
from html_slider.html_slider import render_pandas
import numpy as np

sv = StrandVideo(noise_model=None)

def experiment(*, max_count, background_noise):

    # generate
    frames_clean = np.copy(sv.frames_clean)
    frames_clean *= max_count / np.max(sv.frames_clean)

    # noise
    noise_model = get_visors_noise(background=background_noise)
    frames = noise_model(frames_clean, sv.frame_rate)
    noise = frames - frames_clean

    # register
    corr_sum = correlate_and_sum(frames)
    drift, _ = guizar_multiframe(corr_sum)

    # reconstruct
    recon = shift_and_sum(frames, drift)
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
        'recon': recon,
        'noise_recon': noise_recon,
        'fc': frames_clean[0],
        'f': frames[0],
        'noise': noise[0],
    }

# %% experiment

results = combination_experiment(
    experiment,
    max_count=[20],
    background_noise=[8]

)

# %% slider

render_pandas(
    results,
    slider_cols=['max_count', 'background_noise'],
    indicator_cols=['snr_db', 'true_drift', 'est_drift'],
    im_col='result'
)
