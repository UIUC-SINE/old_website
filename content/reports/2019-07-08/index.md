---
author: Evan
date: 2019-07-08
title: Weekly Report
template: project.j2
---

I've spent the last few days going over two phase correlation papers that I mentioned in previous reports (De Castro/Morandi and Foroosh) and translating them to use my notation.

# De Castro/Morandi

Translating the paper by De Castro and Morandi was fairly straightforward (the result of which can be found [here](http://uiuc-sine.github.io/thesis/intro.html#de-castro-morandi-method)), but I ran into some minor problems that still need to be addressed.  For example, take the following excerpt from the paper (translated into my notation)

$$
\theta \text{ may thus be determined by varying } \hat{\theta} \text{ until the shape of } \\
\mathcal{F}^{-1} \left[ \frac{I_2(\omega)}{I_1(R_{\hat{\theta}} \omega)}\right] \text{ gives the closest approximation of a unity pulse.}
$$

The authors give no insight as to how they measure closeness to an impulse function. In my writeup I left a placeholder for this hypothetical measure and suggested one that might suffice, but there are many others that might work.

Another issue that cropped up relates to the use of the quotient $\frac{I_2(\omega)}{I_1(R_{\theta} \hat{\omega})}$ for finding rotation angle $\theta$.  As a reminder, as the angle being tested $\hat{\theta}$ approaches the true angle, the quotient yields an exponential.

i.e. when $\hat{\theta} \approx \theta$, we get

$$
\mathcal{F}^{-1} \left[ \frac{I_2(\omega)}{I_1(R_{\theta} \omega)}\right](x) = \mathcal{F}^{-1} \left[ e^{-j \langle \omega, c \rangle} \right](x) = \delta(x - c)
$$

While this works for finding $\theta$, the authors explicitly state that using CPSD (which also yields an exponential when $\hat{\theta} = \theta$) is a more robust option.  However, when I tried to validate this mathematically I got the following result

$$
CPSD(\hat{I_1}, I_2) = \frac{I_1(R_{\hat{\theta}}^{-1} \omega) \overline{I_2(\omega)}}{\left| I_1(R_{\hat{\theta}}^{-1} \omega) \overline{I_2(\omega)} \right|} = 
\frac{I_1(R_{\hat{\theta}}^{-1} \omega) \overline{I_1(R_{\theta} \omega)}}{\left| I_1(R_{\hat{\theta}}^{-1} \omega) \overline{I_1(R_{\theta} \omega)} \right|} e^{j \langle \omega, c \rangle} = e^{j \langle \omega, c \rangle}
$$

In other words, CPSD will yield a complex exponential regardless of $\hat{\theta}$.

# Foroosh

The Foroosh paper is more challenging to adapt to my notation because of its use of the Log-Polar/Fourier-Mellin transform.  One of my goals is rewrite the authors' more qualitative arguments for how the Log-Polar transform turns rotation/scaling into translation into a more mathematical one.  To that end, I sketched out a straightforward proof of how rotation, scaling and translation in the spatial domain affect the Fourier domain.

$$
\begin{aligned}
\mathcal{F}\left[ i(R_{\theta}S_s x - c) \right](\omega) &= \int i(R_{\theta}S_sx - c) e^{-j \langle \omega,\, x \rangle} dx \\
&= \frac{1}{s^2} \int i(y) e^{-j \langle \omega,\, S_s^{-1}R_{\theta}^{-1} y \rangle} e^{-j \langle \omega,\,  S_s^{-1} R_{\theta}^{-1} c \rangle} dy \\
&= \frac{1}{s^2} \int i(y) e^{-j \langle S_s^{-1}R_{\theta} \omega,\, y \rangle} e^{-j \langle S_s^{-1}R_{\theta} \omega,\, c \rangle} dy \\
&= \frac{1}{s^2} e^{-j \langle S_s^{-1}R_{\theta} \omega,\, c \rangle} \int i(y) e^{-j \langle S_s^{-1}R_{\theta} \omega,\, y \rangle} dy \\
&= \frac{1}{s^2} e^{-j \langle S_s^{-1}R_{\theta} \omega,\, c \rangle} I(S_s^{-1}R_{\theta} \omega)
\end{aligned}
$$

The next step is to show that after applying the log-polar transform to $I(S_s^{-1} R_{\theta} \omega)$, $S_s^{-1}$ and $R_{\theta}$ manifest as translations.

# Summary
- One step of the De Castro/Morandi paper is to measure how close a function is to an impulse, but the authors don't say how.
- De Castro/Morandi recommends using CPSD for finding the rotation angle, but this doesn't seem to work out mathematically.
- I wrote a brief proof of how to express the scaled, rotated, and translated image $i(R_{\theta}S_s x - c)$ in the Fourier domain.  Essentially just a combined proof of the Fourier shift, Fourier rotation, and Fourier scale theorems in 2D.
