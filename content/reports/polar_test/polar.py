import numpy as np
from matplotlib import pyplot as plt
from scipy.misc import face
from scipy.ndimage import rotate, geometric_transform
from mas.forward_model import size_equalizer, downsample
from mas.tracking import reproject_image_into_polar
from skimage.feature import register_translation


# center images in square region
original = face(gray=True)
r = int(np.linalg.norm(original.shape)) + 1
original = size_equalizer(original, (r, r))
rotated = size_equalizer(rotate(downsample(original), 35), (r, r))

center = np.array(original.shape) // 2
original_polar, _, _ = reproject_image_into_polar(original, origin=center, log=True)
rotated_polar, _, _ = reproject_image_into_polar(rotated, origin=center, log=True)

plt.subplot(2, 2, 1)
plt.imshow(original)
plt.subplot(2, 2, 2)
plt.imshow(rotated)
plt.subplot(2, 2, 3)
plt.imshow(original_polar)
plt.subplot(2, 2, 4)
plt.imshow(rotated_polar)

plt.figure()
# plt.imshow(np.abs(register_translation(original_polar, rotated_polar, 10)))
plt.show()
