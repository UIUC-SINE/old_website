---
date: 2020-03-21
author: Evan Widloski
title: Noise Experiments
template: project.j2
description: Reconstructions at various noise levels
---

Here are some image reconstructions using our current best image registration algorithm.  Below are the steps used to generate the observations and subsequent reconstruction.

1. Generate high-resolution scene
2. Generate lower-resolution video frames as observed through photon sieve of linearly translating spacecraft
3. Scale video frames and add noise
4. [Estimate drift](https://uiuc-sine.github.io/reports/2019-12-30_survey/index.html)
5. Coadd registered frames

For simplicity, a few steps in the reconstruction process are not included here that would replace step 5:

5. Motion blur removal
6. Tikhonov regularization
7. Super resolution

<figure style="text-align: center">
<iframe src="out.html" height=550 width=350></iframe>
</figure>

The observation model used for generating each observed frame $y_k$ is

$$x_k = \text{blur}_k\left(\frac{s}{\max(s)} * m, \, v\right)$$

$$y_k = \mathcal{N}\left( \text{Pois}(x_k + (n_d + n_b) / f), \sqrt{n_r}\right)$$

with parameters:

- input scene: $s$
- max photon count: $m$
- drift velocity (mm/s): $v$
- background noise: $n_b$
- dark current: $n_d=8$
- read noise: $n_r=10$
- frame rate: $f=4$

Operator $\text{blur}_k(\cdot, v)$ selects a region from the high resolution scene $s$ corresponding to the spacecraft field of view at frame $k$ and applies appropriate motion blur.
