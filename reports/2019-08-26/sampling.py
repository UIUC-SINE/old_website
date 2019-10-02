import numpy as np
from itertools import product
import matplotlib.pyplot as plt

image_width = 1000
rot_grid_spacing = 20

# rot_angle = np.pi / 3
def grid_points(*, width, spacing, angle):
    rot_matrix = np.array(
        ((np.cos(angle), -np.sin(angle)),
        (np.sin(angle), np.cos(angle)))
    )

    x = np.array(
        list(product(
            np.arange(-width * np.sqrt(2), width * np.sqrt(2), spacing),
            np.arange(-width * np.sqrt(2), width * np.sqrt(2), spacing)
        ))
    )

    # rotate and center coordinates
    rot_points = (x @ rot_matrix) + (width / 2, width / 2)
    rot_points = rot_points.astype(int)
    # remove coordinates outside window
    rot_points = rot_points[
        (rot_points[:, 0] >=0) *
        (rot_points[:, 0] < width) *
        (rot_points[:, 1] >= 0) *
        (rot_points[:, 1] < width)
    ]
    # reshape coordinate matrix
    rot_points = np.array((rot_points[:, 0], rot_points[:, 1]))

    return rot_points

im = np.zeros((image_width, image_width))
rot_points = grid_points(width=image_width, spacing=rot_grid_spacing, angle=0)
im[tuple(rot_points)] = 1
rot_points = grid_points(width=image_width, spacing=rot_grid_spacing, angle=np.pi / 3)
im[tuple(rot_points)] = 1

plt.subplot(2, 1, 1)
plt.imshow(im)
plt.subplot(2, 1, 2)
plt.imshow(np.abs(np.fft.fft2(im)))
plt.show()
