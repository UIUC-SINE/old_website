import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
from itertools import product

# https://seaborn.pydata.org/generated/seaborn.lineplot.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.melt.html
# https://seaborn.pydata.org/tutorial/axis_grids.html

# %% load

result = pd.read_pickle('results.pkl')

# %% plot


result_long =  result.melt(
    id_vars=['max_count', 'drift_velocity', 'drift_angle', 'repetition'],
    value_vars=['error_old', 'error_new1', 'error_new2'],
    value_name='pixel_err',
    var_name='method'
)

# result_long = result_long.query('drift_velocity == 5e-5 or drift_velocity == 2e-4')

plt.close()
grid = sns.FacetGrid(result_long, row='drift_angle', col='max_count', margin_titles=True)
grid.map(sns.lineplot, 'drift_velocity', 'pixel_err', 'method', data=result_long)
grid.add_legend()
plt.show()
