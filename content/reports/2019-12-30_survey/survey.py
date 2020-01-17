from mas.tracking import correlate_and_sum2, guizar_multiframe2, ulas_multiframe2
from mas.strand_generator import StrandVideo
from mas.misc import combination_experiment
import numpy as np
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.melt.html
# https://seaborn.pydata.org/tutorial/axis_grids.html
# https://seaborn.pydata.org/generated/seaborn.lineplot.html


def experiment(*, max_count, drift_velocity, drift_angle, **kwargs):

    sv = StrandVideo()

    corr_sum = correlate_and_sum2(sv.frames, mode='CC')
    guizar_drift = guizar_multiframe2(sv.frames)

    ulas_drift1, ulas_drift2 = ulas_multiframe2(sv.frames)

    return {
        'guizar_error': np.linalg.norm(sv.true_drift - guizar_drift),
        'ulas_error1': np.linalg.norm(sv.true_drift - ulas_drift1),
        'ulas_error2': np.linalg.norm(sv.true_drift - ulas_drift2)
    }

# %% result

result = combination_experiment(
    experiment,
    max_count=[20, 40, 80],
    drift_velocity=np.array((0.05, 0.1, 0.2, 0.4)) * 1e-3,
    drift_angle=np.linspace(0, 90, 20),
    repetition=np.arange(20)
    # max_count=[20],
    # drift_velocity=np.array([0.2]) * 1e-3,
    # drift_angle=np.linspace(0, 90, 2),
    # repetition=np.arange(1)
)

result.to_pickle('result.pkl')
