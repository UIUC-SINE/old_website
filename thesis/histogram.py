import numpy as np
from scipy.misc import face
import matplotlib.pyplot as plt

f = face(gray=True)

y, x = np.histogram(f, bins=256, range=(0, 255))

xx = (x[:-1] + x[1:]) / 2

plt.figure(figsize=(8, 3))
plt.subplot(1, 2, 1)
plt.axis('off')
plt.imshow(f, cmap='gray')

plt.subplot(1, 2, 2)
plt.plot(xx, y / np.product(f.shape))
plt.xlabel('Intensity')
plt.grid(True)
plt.tight_layout()

plt.show()
