from mas.tracking import guizar_multiframe, correlate_and_sum, guizar_upsample
from mas.strand_generator import StrandVideo
from mas.misc import combination_experiment
import numpy as np
import seaborn as sns; sns.set()

# MAS commit a8b7bebc

def experiment(*, max_count, drift_velocity, drift_angle, **kwargs):

    sv = StrandVideo(angle_velocity=0)
    N = len(sv.frames)

    corr_sum = correlate_and_sum(sv.frames)

    drift_new1, d = guizar_multiframe(corr_sum, start=1, end=N)
    drift_old = np.mean(d[9:29], axis=0)

    drift_new2 = guizar_upsample(corr_sum)[0]

    # import ipdb
    # ipdb.set_trace()

    return {
        'error_old': np.linalg.norm(sv.true_drift - drift_old),
        'error_new1': np.linalg.norm(sv.true_drift - drift_new1),
        'error_new2': np.linalg.norm(sv.true_drift - drift_new2),
        'drift_old': drift_old,
        'drift_new1': drift_new1,
        'drift_new2': drift_new2,
        'errorv_old': sv.true_drift - drift_old,
        'errorv_new1': sv.true_drift - drift_new1,
        'errorv_new2': sv.true_drift - drift_new2,
        'd': d,
        'd_err': np.linalg.norm(sv.true_drift - d, axis=1),
        'true_drift': sv.true_drift
    }

# %% result

results = combination_experiment(
    experiment,
    # max_count=[20, 40, 80],
    # drift_velocity=[0.01e-3, 0.05e-3, 0.2e-3],
    # drift_angle=np.linspace(0, -90, 4),
    max_count=[20],
    drift_velocity=[0.2e-3],
    drift_angle=[-45],
    repetition=np.arange(50)
)
