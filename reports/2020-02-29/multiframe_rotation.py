from skimage import data
from skimage.feature import register_translation
from skimage.transform import rescale, warp_polar, rotate
from skimage.util import img_as_float
from mas.tracking import roll
import matplotlib.pyplot as plt
import numpy as np

# radius must be large enough to capture useful info in larger image
radius = 1500
angle = 53.7
scale = 2.2
image = data.retina()
image = img_as_float(image)
rotated = rotate(image, angle)
rescaled = rescale(rotated, scale, multichannel=True)
image_polar = warp_polar(
    image, radius=radius,
    scaling='log', multichannel=True
)
rescaled_polar = warp_polar(
    rescaled, radius=radius,
    scaling='log', multichannel=True
)
rescaled_polar = roll(rescaled_polar, (10, 10))

fig, axes = plt.subplots(2, 2, figsize=(8, 8))
ax = axes.ravel()
ax[0].set_title("Original")
ax[0].imshow(image)
ax[1].set_title("Rotated and Rescaled")
ax[1].imshow(rescaled)
ax[2].set_title("Log-Polar-Transformed Original")
ax[2].imshow(image_polar)
ax[3].set_title("Log-Polar-Transformed Rotated and Rescaled")
ax[3].imshow(rescaled_polar)
plt.show()

# setting `upsample_factor` can increase precision
tparams = register_translation(image_polar, rescaled_polar, upsample_factor=20)
shifts, error, phasediff = tparams
shiftr, shiftc = shifts[:2]

# Calculate scale factor from translation
klog = radius / np.log(radius)
shift_scale = 1 / (np.exp(shiftc / klog))

print(f"Expected value for cc rotation in degrees: {angle}")
print(f"Recovered value for cc rotation: {shiftr}")
print()
print(f"Expected value for scaling difference: {scale}")
print(f"Recovered value for scaling difference: {shift_scale}")
