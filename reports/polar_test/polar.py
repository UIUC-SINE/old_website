import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import rotate, geometric_transform
from skimage.transform import resize
from mas.forward_model import size_equalizer, downsample, crop, add_noise
from mas.tracking import reproject_image_into_polar
from skimage.feature import register_translation
# from mas.data import strands as data_strands
from mas.strand_generator import strands

scale = 0.75
rotation = -10

# ----- -----

source = strands(
    image_width=1600,
    thickness=int(22 * 1024 / 1600),
    num_strands=int(100 * 1600 / 1024)
)

image_width = 1024
s_center = np.array(source.shape) // 2
original = crop(image=source, center=s_center, width=image_width)
original = add_noise(original, model='poisson', max_count=10)

a = resize(
    source,
    (np.array(source.shape) * scale).astype(int)
)
b = rotate(a, rotation)
r_center = np.array(b.shape) // 2
rotated = crop(image=b, center=r_center, width=image_width)
rotated = add_noise(rotated, model='poisson', max_count=10)

# ---- edge effects -----

# original = strands(image_width=1024)
# r = int(np.linalg.norm(original.shape)) + 1
# original = size_equalizer(original, (r, r))
# rotated = size_equalizer(
#     rotate(
#         resize(
#             original,
#             (np.array(original.shape) * scale).astype(int)
#         ),
#         rotation),
#     (r, r)
# )

center = np.array(original.shape) // 2
original_polar, _, _ = reproject_image_into_polar(original, origin=center, log=True)[:680]
rotated_polar, _, _ = reproject_image_into_polar(rotated, origin=center, log=True)

rotated_polar = rotated_polar[:680]
original_polar = original_polar[:680]

plt.subplot(2, 2, 1)
plt.imshow(original, cmap='gist_heat')
plt.axis('off')
plt.subplot(2, 2, 2)
plt.imshow(rotated, cmap='gist_heat')
plt.axis('off')
plt.subplot(2, 2, 3)
plt.imshow(original_polar, cmap='gist_heat')
plt.axis('off')
plt.subplot(2, 2, 4)
plt.imshow(rotated_polar, cmap='gist_heat')
plt.axis('off')

plt.show()

a, b = register_translation(original_polar, rotated_polar, 100)[0]

scale_estimate = 1 - np.log2((a + 1)**(1/20))
rotation_estimate = b / image_width * 360

print('scale_estimate:', scale_estimate)
print('rotation_estimate:', rotation_estimate)
print('scale err:', np.abs(scale - scale_estimate) / scale)
print('rotation err:', np.abs(rotation - rotation_estimate) / rotation)

s.append(scale_estimate)
r.append(rotation_estimate)
