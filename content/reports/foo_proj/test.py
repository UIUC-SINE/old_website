import numpy as np
import pandas as pd

def fib():
    a, b = 0, 1
    while 1:
        yield a
        a, b = b, a + b

x = fib()
next(x)

x = np.random.random((3, 3))

open('result1.html', 'w').write(pd.DataFrame(x).to_html(border=1))
