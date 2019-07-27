---
date: 2019-07-15
title: Weekly Report
author: Evan
template: project.j2
---

[TOC]

This week, I set out to prove some of statements in [Sarvaiya, Patnaik, Kothari 2012](http://www.jprr.org/index.php/jprr/article/view/355).  As I mentioned in the previous report, this paper glosses over the details of how the Log-Polar transform affects scaled/rotated images and simply states that they manifest as translations in the Log-Polar domain.  This analysis wasn't strictly necessary for the paper review, but I found it helpful nonetheless for truly understanding the effects of the Log-Polar transform.  The final analytical result may also be useful for showing how the Log-Polar transform introduces conditioning problems.  This is mentioned and accounted for in the paper, but again is not proven with much rigor.

Also after working through the proofs, I made some minor refinements to my chosen mathematical notation.

### Log-Polar transform of scaled, rotated and shifted images

[Previously](https://uiuc-sine.github.io/reports/2019-07-08/index.html#Foroosh), I showed the Fourier transform of a scaled, rotated and shifted image is a scaled and rotated version of the image's Fourier transform modulated by a complex exponential.

i.e.

$$
\mathcal{F}\left[ i(R_{\theta_0}S_{s_0} \bm{x} - \bm{c}) \right](\bm{\omega}) = \frac{1}{s_0^2} e^{-j \langle S_{s_0}^{-1}R_{\theta_0} \bm{\omega},\, \bm{c} \rangle} I(S_{s_0}^{-1} R_{\theta_0} \bm{\omega})
$$

where

$$S_{s_0} = \begin{bmatrix} s_0 & 0 \\ 0 & s_0 \end{bmatrix} \tag*{scaling}$$

$$R_{\theta_0} = \begin{bmatrix}\cos \theta_0 & -\sin \theta_0 \\ \sin \theta_0 & \cos \theta_0 \end{bmatrix} \tag*{rotation}$$

$$\bm{c} = \begin{bmatrix} x_0 & y_0 \end{bmatrix}^T \tag*{translation}$$

$$\bm{x} = \begin{bmatrix} x & y \end{bmatrix}^T \tag*{spatial coordinate vector}$$

$$\bm{\omega} = \begin{bmatrix} u & v \end{bmatrix}^T \tag*{frequency coordinate vector}$$

Next I will show that the Log-Polar transform of a scaled, rotated image is a translated version of the image's Log-Polar transform.

i.e.

$$
\mathcal{LP}\left[ i(R_{\theta_0}S_{s_0}\bm{x}) \right](\rho, \theta) = \mathcal{LP} \left[ i(\bm{x}) \right](\rho + \ln s_0, \theta + \theta_0)
$$

<br>

$$
\begin{aligned}
\mathcal{LP} \left[i(R_{\theta_0} S_{s_0} \bm{x}) \right](\rho, \theta) &= \mathcal{LP} \left[ i(s_0(x \cos \theta_0 - y \sin \theta_0), s_0(x \sin \theta_0 + y \cos \theta_0) \right](\rho, \theta) \\
&= \mathcal{LP} \left[ i(e^{\ln s_0}(x \cos \theta_0 - y \sin \theta_0), e^{\ln s_0}(x \sin \theta_0 + y \cos \theta_0) \right](\rho, \theta) \\ 
& \text{Substitute \((x, y) = (e^{\rho} \cos \theta, e^{\rho} \sin \theta)\)} \\
&= i(e^{\ln s_0}(e^{\rho} \cos \theta \cos \theta_0 - e^{\rho} \sin \theta \sin \theta_0), e^{\ln s_0}(e^{\rho} \cos \theta \sin \theta_0 + e^{\rho} \sin \theta \cos \theta_0) \\
& \text{Apply angle sum identities} \\
&= i(e^{\rho + \ln s_0} \cos (\theta + \theta_0), e^{\rho + \ln s_0} \sin (\theta + \theta_0)) \\
&= \mathcal{LP} \left[ i(x) \right](\rho + \ln s_0, \theta + \theta_0)
\end{aligned}
$$

So when we apply Log-Polar transform to a scaled and rotated image, we can simply apply these substitutions

$$
\begin{aligned}
s_0(x \cos \theta_0 - y \sin \theta_0) &= e^{\rho + \ln s_0} \cos(\theta + \theta_0) \\
s_0(x \sin \theta_0 + y \cos \theta_0) &= e^{\rho + \ln s_0} \sin(\theta + \theta_0)
\end{aligned}
$$

First we define the Log-Polar transform of $I$.

$$
I_{LP}(\rho, \theta) = I(e^{\rho} \cos \theta, e^{\rho} \sin \theta)
$$

$$
\begin{aligned}
& \frac{1}{s_0^2} e^{j \langle S^{-1} R \omega,\, \bm{c} \rangle} I(S^{-1} R \bm{\omega}) \\ 
&= \frac{1}{s_0^2} e^{-j \left(\frac{1}{s_0} \left[ u \cos \theta_0 - v \sin \theta_0, u \sin \theta_0 + v \cos \theta_0 \right]^T \bm{c}\right)} I(\frac{1}{s_0} \left[ u \cos \theta_0 - v \sin \theta_0, u \sin \theta_0 + v \cos \theta_0 \right]^T) \\
&= \frac{1}{s_0^2} \text{exp} \left[ -j\left(\frac{1}{s_0} \left[ x_0 (u \cos \theta_0 - v \sin \theta_0) + y_0 (u \sin \theta_0 + v \cos \theta_0 v)\right]\right) \right] I\left(\frac{1}{s_0} (u \cos \theta_0 - v \sin \theta_0), \frac{1}{s_0} (u \sin \theta_0 + v \cos \theta_0) \right) \\
&= \frac{1}{s_0^2} \text{exp} \left[ -j\left(x_0 \frac{1}{s_0} (u \cos \theta_0 - v \sin \theta_0) + y_0 \frac{1}{s_0} (u \sin \theta_0 + v \cos \theta_0 v)\right) \right] I\left(\frac{1}{s_0} (u \cos \theta_0 - v \sin \theta_0), \frac{1}{s_0} (u \sin \theta_0 + v \cos \theta_0) \right) \\
& \text{Apply Log-Polar transform} \\
&= \frac{1}{s_0^2} \text{exp} \left[ -j\left(x_0 e^{\rho + \ln \frac{1}{s_0}} \cos(\theta + \theta_0) + y_0 e^{\rho + \ln \frac{1}{s_0}} \sin(\theta + \theta_0)\right) \right] I\left(e^{\rho + \ln \frac{1}{s_0}} \cos(\theta + \theta_0), e^{\rho + \ln \frac{1}{s_0}} \sin(\theta + \theta_0) \right) \\
& \text{Apply definition of \(I_{LP}\)} \\
&= \frac{1}{s_0^2} \text{exp} \left[ -j\left(x_0 e^{\rho + \ln \frac{1}{s_0}} \cos(\theta + \theta_0) + y_0 e^{\rho + \ln \frac{1}{s_0}} \sin(\theta + \theta_0)\right) \right] I_{LP}\left(\rho + \ln \frac{1}{s_0}, \theta + \theta_0 \right) \\
\end{aligned}
$$

The important result here is that after taking the Log-Polar transform, the effects of $R_{\theta_0}$ and $S_{s_0}$ are simply translations.  We can now use the standard phase-correlation method for calculating $\ln\frac{1}{s_0}$ and $\theta_0$ to recover scale and rotation.
<!-- \text{substitute } (x, y) \rightarrow (e^{\rho} \cos \theta, e^{\rho} \sin \theta) \\ -->

### Summary

* Added section on Log-Polar method to thesis introduction.
* Explicitly wrote out effects of Log-Polar transform on scaled/rotated/shifted images.
* Toyed with potential application of Prony's method idea
