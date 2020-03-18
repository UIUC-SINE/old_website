from mas.tracking import guizar_multiframe, correlate_and_sum
from mas.strand_generator import StrandVideo
from mas.misc import combination_experiment
import numpy as np
import seaborn as sns; sns.set()

# MAS commit a8b7bebc

def experiment(*, max_count, drift_velocity, drift_angle, **kwargs):

    sv = StrandVideo(angle_velocity=0)
    N = len(sv.frames)

    corr_sum = correlate_and_sum(sv.frames)

    _, d = guizar_multiframe(corr_sum, start=1, end=N)
    drift_old = np.mean(d[9:29], axis=0)

    n = np.arange(1, N)
    weights1 = n
    weights2 = n * (N - n)**2 / (n + (N - n)**2)

    # FIXME - why is [-1] so bad sometimes? single frame correlation?
    #         shouldnt [-2] be half as bad?
    weights1[-2:] = 0

    weights1 = weights1 / np.sum(weights1)
    weights2 = weights2 / np.sum(weights2)

    drift_new1 = np.sum(d * weights1[:, np.newaxis], axis=0)
    drift_new2 = np.sum(d * weights2[:, np.newaxis], axis=0)

    # import ipdb
    # ipdb.set_trace()

    return {
        'error_old': np.linalg.norm(sv.true_drift - drift_old),
        'error_new1': np.linalg.norm(sv.true_drift - drift_new1),
        'error_new2': np.linalg.norm(sv.true_drift - drift_new2),
        'drift_old': drift_old,
        'drift_new1': drift_new1,
        'drift_new2': drift_new1,
        'errorv_old': sv.true_drift - drift_old,
        'errorv_new1': sv.true_drift - drift_new1,
        'errorv_new2': sv.true_drift - drift_new2,
        'weights1': weights1,
        'weights2': weights1,
        'd': d,
        'd_err': np.linalg.norm(sv.true_drift - d, axis=1),
        'true_drift': sv.true_drift
    }

# %% result

results = combination_experiment(
    experiment,
    max_count=[20, 40, 80],
    drift_velocity=[0.01e-3, 0.05e-3, 0.2e-3],
    drift_angle=np.linspace(0, -90, 4),
    # max_count=[20],
    # drift_velocity=[0.2e-3],
    # drift_angle=[-45],
    repetition=np.arange(30)
)
