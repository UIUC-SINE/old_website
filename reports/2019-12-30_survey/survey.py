from mas.tracking import (
    guizar_multiframe2,
    ulas_multiframe2, ulas_multiframe3,
    correlate_and_sum2, correlate_and_sum3
)

from mas.strand_generator import StrandVideo
from mas.misc import combination_experiment
import numpy as np
import seaborn as sns; sns.set()


# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.melt.html
# https://seaborn.pydata.org/tutorial/axis_grids.html
# https://seaborn.pydata.org/generated/seaborn.lineplot.html


def experiment(*, max_count, drift_velocity, drift_angle, **kwargs):

    sv = StrandVideo(
        max_count=max_count,
        drift_velocity=drift_velocity,
        drift_angle=drift_angle
    )

    corr_sum = correlate_and_sum3(sv.frames)

    guizar_drift, d = guizar_multiframe2(corr_sum, start=10, end=30)
    ulas_drift1, ulas_drift2 = ulas_multiframe3(corr_sum)

    return {
        'guizar_error': np.linalg.norm(sv.true_drift - guizar_drift),
        'guizar_drift': guizar_drift,
        'ulas_error1': np.linalg.norm(sv.true_drift - ulas_drift1),
        'ulas_error2': np.linalg.norm(sv.true_drift - ulas_drift2),
        'ulas_drift1': ulas_drift1,
        'ulas_drift2': ulas_drift2,
        'd': np.linalg.norm(sv.true_drift - d, axis=1),
        'true_drift': sv.true_drift
    }

# %% result

result = combination_experiment(
    experiment,
    max_count=[20],
    # drift_velocity=[0.01e-3, 0.05e-3, 0.2e-3],
    drift_velocity=[0.2e-3],
    drift_angle=np.linspace(0, -90, 20),
    repetition=np.arange(5)
)

result.to_pickle('result.pkl')
