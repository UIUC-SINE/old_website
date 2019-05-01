---
author: Evan Widloski
title: Initial ISTA nanoflare reconstructions
date: 2019-04-25
template: project.j2
---

These are ISTA reconstructions of nanoflares images with Poisson noise.  The sparsifying transform used in the algorithm was the Radon transform restricted to \\(\theta = \[-30, 30]\\).

![ISTA reconstruction with highest SSIM](ista_reconstruction2.png){ style=max-width:100%}

![Best looking ISTA reconstruction](ista_reconstruction.png){ style=max-width:100%}

![ISTA reconstructions for various \\(\lambda\\), time_step.  Max photon count is 10](ista_grid.png){ style=max-width:100%}
