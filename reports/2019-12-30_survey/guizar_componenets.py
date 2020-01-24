# compare error in drift estimates in guizar method under different drift velocities

from mas.strand_generator import StrandVideo
from mas.tracking import guizar_multiframe2, correlate_and_sum3
from mas.misc import combination_experiment
import numpy as np
import pandas as pd

def experiment(*, drift_velocity, drift_angle, max_count):
    sv = StrandVideo(
        drift_velocity=drift_velocity,
        max_count=max_count,
        drift_angle=drift_angle
    )

    corr_sum = correlate_and_sum3(sv.frames)
    gm, d = guizar_multiframe2(corr_sum, start=1, end=39)

    return {
        'component_errors': np.linalg.norm(sv.true_drift - d, axis=1)
    }

result = combination_experiment(
    experiment,
    drift_velocity=np.linspace(0.01e-3, 1e-3, 10),
    drift_angle=[-75],
    max_count=[80]
)


# %% plot

import seaborn as sns; sns.set()

# https://www.mikulskibartosz.name/how-to-split-a-list-inside-a-dataframe-cell-into-rows-in-pandas/
result_flat = result.component_errors.apply(pd.Series).merge(
    result,
    left_index=True,
    right_index=True
).drop(['component_errors'], axis=1).melt(
    id_vars=['drift_velocity', 'drift_angle', 'max_count'],
    var_name='time',
    value_name='component_error'
)

sns.lineplot(
    x='time',
    y='component_error',
    hue='drift_velocity',
    data=result_flat
)
plt.show()
