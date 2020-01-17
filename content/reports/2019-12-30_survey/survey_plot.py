import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
from itertools import product

# https://seaborn.pydata.org/generated/seaborn.lineplot.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.melt.html
# https://seaborn.pydata.org/tutorial/axis_grids.html

# %% load

result = pd.read_pickle('result.pkl')

# %% plot

result =  result.melt(
    id_vars=['max_count', 'drift_velocity', 'drift_angle', 'repetition'],
    value_vars=['guizar_error', 'ulas_error1', 'ulas_error2'],
    value_name='pixel_err',
    var_name='method'
)

plt.close()
grid = sns.FacetGrid(result, row='drift_velocity', col='max_count', margin_titles=True)
grid.map(sns.lineplot, 'drift_angle', 'pixel_err', 'method', data=result)
plt.show()
