import numpy as np
import pandas as pd

x = np.random.random((3, 3))

open('result1.html', 'w').write(pd.DataFrame(x).to_html(border=1))
