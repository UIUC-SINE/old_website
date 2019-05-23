---
title: CSBS vs Naive plane selection
author: Evan Widloski
date: 2019-04-30
template: project.j2
---
![Measurement contributions from each source.  Off-focus contributions are nearly DC](contributions.png)

![Each column of pixels is a 'slice' through the center of the DFT of a PSF measured at a particular distance from the sieve.](slices.png){ .figure style=max-width:100% }

![1D view of the above plot at some selected spatial frequencies.  Notice the DFT magnitude is always maximized at the focal plane for each spatial frequency.](sample_slices.png){ .figure style=max-width:100% }

![Reconstructions with various methods, max count 10](reconstructions_10.png)
![Reconstructions SSIMs, max count 10](ssim_comparison_10.png)

![Reconstructions with various methods, max count 500](reconstructions_500.png)
![Reconstructions SSIMs, max count 500](ssim_comparison_500.png)


#### Bayesian Optimization

The reconstruction parameters for the above section were all found using bayesian optimization, which is a common tool for searching hyperparameters.  Bayesian optimization is particularly well-suited to optimizing black box functions which are expensive to evaluate.  

In our case, the naive focus and naive grid methods both have a single \\(\lambda_{tik}\\) parameter for Tikhonov regularization, while CSBS grid and CSBS focus had both a Tikhonov \\(\lambda_{tik}\\) and a \\(\lambda_{csbs}\\) used during plane selection.  It's worth noting that for CSBS grid and CSBS focus \\(\lambda_{tik}\\) and \\(\lambda_{csbs}\\) should be the same, but we found that the reconstruction were much better when these were allowed to be optimized separately.

For posterity, the hyperparameter surfaces for each mode are included below.

![](bayesian_optimization/bayesian_tik_csbs_grid_10_split.png)
![](bayesian_optimization/bayesian_tik_csbs_focus_10_split.png)
![](bayesian_optimization/bayesian_tik_naive_grid_10.png)
![](bayesian_optimization/bayesian_tik_naive_focus_10.png)
![](bayesian_optimization/bayesian_tik_csbs_grid_500_split.png)
![](bayesian_optimization/bayesian_tik_csbs_focus_500_split.png)
![](bayesian_optimization/bayesian_tik_naive_grid_500.png)
![](bayesian_optimization/bayesian_tik_naive_focus_500.png)
