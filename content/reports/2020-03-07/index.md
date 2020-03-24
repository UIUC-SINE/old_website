---
date: 2020-03-07
author: Evan Widloski
title: ML Solution to Registration
template: project.j2
---

# Deriving ML Solution to Multiframe Cross Correlation

In this section, I attempt to justify why my extension of Guizar's registration method uses phase correlations of all possible pairs of frames and not just adjacent frame pairs or correlations between the first and Nth frame.

First I derive the ML solution for the two-frame case then extend it to multiple frames.

#### Two Frames

Assumptions:

- Original image $\mu$ is known
- Image is circularly shifted rather than linearly

Let $\mu = \left[ \mu_1, ..., \mu_N \right]^T$ be an image.

Let $C_k(\cdot)$ be a circular shift operator by $k$ positions.

Let $Y = \left[Y_1, ..., Y_N\right]^T \sim \mathcal{N}(C_k(\mu), \sigma^2)$ be a noisy observation of $\mu$ shifted by $k$.

The likelihood of $Y$ is

$$P(Y | k) = \prod_{n=1}^N P(Y_n | k) = \prod_{n=1}^N \phi \left( \frac{Y_n - C_k(\mu)_n}{\sigma} \right)$$

And the ML solution for $k$ is

$$
\begin{aligned} \hat{k}_{ML} &= \arg \max_k \ln P(Y | k) = \arg \max_k \sum_{n=1}^N \ln \text{exp} \left[- \frac{(Y_n - C_k(\mu)_n)^2}{\sigma^2} \right] \\
&= \arg \min \sum_{n=1}^N \left[Y_n - C_k(\mu)_n\right]^2 \\
&= \arg \min_k \sum_{n=1}^N Y_n^2 - 2\sum_{n=1}^N Y_n C_k(\mu)_n + \sum_{n=1}^N \mu_n^2 \\
&= \arg \max_k \underbrace{\sum_{n=1}^N Y_n C_k(\mu)_n}_{\text{cross correlation}}
= \arg \max_k (Y \ast \mu)[k]
\end{aligned}
$$

Conclusion: **The ML solution for the two frame case is argmax of the cross correlation.**

#### Multiple Frames

Assumptions:

- Original image $\mu$ is known
- Image is circularly shifted rather than linearly

Let $\mu = \left[ \mu_1, ..., \mu_N \right]^T$ be an image.

Let $C_k(\cdot)$ be a circular shift operator by $k$ positions. $k$ represents the drift velocity.

Let $Y_m = \left[Y_1, ..., Y_N\right]^T \sim \mathcal{N}(C_k(\mu), \sigma^2)$ be the mth noisy observation of $\mu$ shifted by $km$ in a sequence of $M$ frames.

The likelihood of $Y_1, ..., Y_M$ is

$$
\begin{aligned}
P(Y_1, ..., Y_M | k) &= \prod_{m=1}^M P(Y_m | k) = \prod_{m=1}^M \prod_{n=1}^N P(Y_{m,n} | k) \\
&= \prod_{m=1}^M \prod_{n=1}^N \phi \left(\frac{Y_{m,n} - C_{km}(\mu)_n}{\sigma} \right)
\end{aligned}
$$

And the ML solution for $k$ is

$$
\begin{aligned}
\hat{k}_{ML} &= \arg \max \ln P(Y_1, ..., Y_m | k) \\
&= \arg \max_k \sum_{m=1}^M \sum_{n=1}^N \ln \text{exp} \left[- \frac{(Y_{m,n} - C_{km}(\mu)_n)^2}{\sigma^2} \right] \\
&= \arg \min_k \sum_{m=1}^M \sum_{n=1}^N \left[ Y_{m,n} - C_{km}(\mu)_n \right]^2 \\
&= \arg \min_k \sum_{m=1}^M \sum_{n=1}^N Y_{m,n}^2 - 2Y_{m,n}C_{km}(\mu)_n + \mu_n^2 \\
&= \arg \max_k \sum_{m=1}^M \underbrace{\sum_{n=1}^N Y_{m,n}C_{km}(\mu)_n}_{\text{cross corr. of }Y_m\text{ and }\mu}
\end{aligned}
$$

According to this expression, the maximum likelihood solution is an argmax of the sum of cross correlations of all $Y_m$ with $\mu$.

We can't apply this formula directly since $\mu$ is not known.  However, we can substitute an estimator, such as

$$\hat{\mu} = \text{mean}\left[C_{-1k}(Y_1), C_{-2k}(Y_2), ..., C_{-Mk}(Y_M)\right]$$.

Substituting this for $\mu$, we see that the solution involves a cross correlation of each observation with all other observations.

Conclusion: **The ML solution for the multi-frame case involves cross-correlating all possible pairs ** $(Y_{m_1}, Y_{m_2}), m_1 < m_2$.
