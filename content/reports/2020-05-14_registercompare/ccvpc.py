# Evan Widloski - 2020-05-14
# Comparing Cross Correlation and Phase Correlation

import numpy as np

from mas.strand_generator import StrandVideo
from mas.misc import combination_experiment
from mas.tracking.tracking import guizar_multiframe, correlate_and_sum

scene = StrandVideo().scene

# %% monte

def experiment(*, method, drift_velocity, max_count, repetition):
    sv = StrandVideo(scene=scene, max_count=max_count)

    corr_sum = correlate_and_sum(sv.frames, mode=method)
    est_drift, _ = guizar_multiframe(corr_sum)

    return {
        'err': np.linalg.norm(sv.true_drift - est_drift),
        'true_drift': sv.true_drift,
        'est_drift': est_drift
    }

result = combination_experiment(
    experiment,
    method=['PC', 'CC'],
    drift_velocity=[1e-5, 5e-5, 25e-5],
    max_count=[20, 40, 80],
    repetition=np.arange(20)
)

# %% plot

import seaborn as sns
sns.set()

grid = sns.FacetGrid(result, col='max_count', margin_titles=True)
grid.map(sns.lineplot, 'drift_velocity', 'err', 'method', data=result)
plt.legend()

