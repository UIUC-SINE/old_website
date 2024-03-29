---
template: project.j2
date: 2019-06-16
title: Thesis
---
<style>
c { 
    color: gray;
} 
header h1 {
    border: none;
}
h1 {
    /* border-bottom: 1px solid black; */
    border: 1px solid black;
    padding: 1em;
    text-align: center;
}
h2 {
    /* text-decoration: underline; */
    border-bottom: 1px solid black;
    font-size: 1.25em;
}
h3 {
    font-size: 1em;
}
</style>

[TOC]

# Introduction

<!--
- fields where imaging is used
  - remote sensing
    - change detection
    - image mosaicing
    - super resolution
  - medicine
    - combining CT and MRI data
    - overlaying patient data on anatomical references

-->

*Image registration* is the process of transforming multiple snapshots so that subjects or features common to two or more snapshots are aligned.
The images may be stitched into a composite image to get a wider field of view, higher resolution, reduced noise, or may be simply be aligned as in the case of video stabilization.  Depending on the problem, registration algorithms often need to contend with changes in the scene being imaged (due to elapsed time between snapshots), perspective changes (changes in camera position), and illumination changes (from different imaging equipment). [^brown]

*Motion estimation*, a related field, is the process of identifying motion captured in a series of images (usually frames of a video).  This motion may be due to motion of the camera which causes the whole scene to appear to move (*apparent motion*), or individual objects moving independently within the frame.  In motion fields, a velocity vector is associated with each pixel in a particular region of the image (*local* motion estimation) or the image as a whole (*global* motion estimation).  These motion vectors usually represent 2D motion across the image, but may also be 3D to capture movement in 3D space.  When a motion field for individual pixels has been computed it is common to group motion vectors that belong to the same moving object, a process known as *motion segmentation*. [^1]

Registration is an important step in the image processing pipeline for countless fields.  For example, in remote sensing applications registration is used in change detection, image mosaicing, and super resolution.  In medical imaging applications, registration is used for overlaying patient images from multiple channels, such as CT and MRI, which the caregiver can cross-reference for diagnoses, and to compare patient data to physiological atlases.

In the next sections, I mathematically describe the problem of image registration, provide a categorization framework for registration methods, and explain the motivating problem of this thesis.


## Registration Problem Model

Let $i_1$ and $i_2$ be two images captured of a scene.  These are often called the *reference* and *sensed* images.  In image registration, we want to find a mapping from regions in the sensed image to regions in the reference image.  More formally, we want to find $f$ such that

$$
i_2(\bm{x}) = g(i_1(f(\bm{x})), \bm{x}) \,\, \forall \bm{x} \in X
$$

where $\bm{x}$ is a coordinate vector in the image overlap region $X$, $f$ is some unknown coordinate transform, and $g$ is an unknown intensity mapping function.  $g$ is often assumed to be unitary, but can be a very complicated function in multimodal applications like medical imaging where $i_1$ and $i_2$ are captured from different instruments.  For the rest of this paper, I assume $i_1$ and $i_2$ are 2D vectors containing image data.

<!-- X is intersection region for SR, fusion -->
<!-- X is union for stitching -->

## Categorizing Registration Methods

While there is a wide variety of approaches to the problem of image registration, many algorithms can be broken down into 4 steps which aids in their classification. [^zitova].

1. **Feature detection** - Distinct features (points, edges, closed regions, intersections, corners, etc.) are detected in both images.  These features may be represented by coordinates (intersections, corners, etc.), coordinate pairs (edges) or a more complex parameterization.  This step is omitted in non-feature based registration methods.
2. **Feature Matching** - Correspondence is established between features detected in the images.  Feature similarity measures or feature positions within the images may be used to do this.  This step is omitted in non-feature-based registration methods.
3. **Transform model estimation** - In feature-based methods, the parameters of the coordinate mapping function $f$ are computed using the previously matched features.  In non-feature-based methods, model parameters can be estimated from image statistics, iterative cost minimization, or image spectra, to name a few.  This step is where most variability between registration methods lies.
4. **Image transformation** - The sensed image is transformed using the estimated parameters and optionally fused with the reference image.  Interpolation may be necessary if the mapping function contains non-integer coordinates.

The registration algorithms reviewed later in this manuscript perform a single pass of these steps to arrive at the registered result, but some other algorithms, especially those used in the process of super-resolution, repeat steps through several iterations and only stop when some criterion is met. [^farsiu2004]

<!-- In the next section, I highlight some classical and/or popular contemporary image registration methods and the domains in which they are applied. -->

## A Comment on Notation

This document contains many types of variables which can represent transform parameters, <!-- placeholder variables inside optimizations, --> 1D vectors of parameters and 2D images.   I try to follow these guidelines for easier reading:

* bold for variables which represent 1D vectors.  For example $\bm{x}$ is a coordinate vector representing position within an image
* superscript $*$ for ground truth parameters of coordinate transform $f$.  For example $s^*$ and $\theta^*$ are parameters controlling scaling and rotation
* hat $\,\hat{}\,$ for algorithmic estimates of ground truth parameters. For example $\hat{\theta}$ represents the estimates for $\theta^*$ found by a particular algorithm
<!-- * hat $\,\hat{}\,$ for placeholder variables in maximization or minimization problems. For example $\hat{\theta}$ may represent the current value under test in an iterative algorithm searching for $\theta_0$ -->
<!-- * superscript $*$ for final parameter estimates obtained by registration methods. For example $\theta^*$ is a best estimate for the true $\theta_0$ -->


## Types of Image Transforms

The coordinate transform is a fundamental component of any registration algorithm.  Most registration algorithms describe a specific class of coordinate transforms which can be completely described by a handful of parameters that are searched over during the *transform model estimation* step .  In this section, I describe a few of the most common classes of coordinate transforms, their parameters, and give some examples of where they are used.

### Translation

The simplest and most common type of coordinate transform is translation

$$f(\bm{x}) = \bm{x} - \bm{c}$$

<!-- FIXME citation -->

where $\bm{c}$ is a length 2 vector whose elements correspond to the shift in each dimension.  Some of the oldest registration methods operate over this class of transforms. 

### Rotation

Another type of registration method is rotation, in which the sensed image is rotated about some point.

$$f(\bm{x}) = R_{\theta}\bm{x}$$

where $R_{\theta}$ is known as a *rotation matrix*.  $R_{\theta}$ has orthogonal columns and can be entirely parameterized by $\theta$, the rotation angle.

$$
R_{\theta} = \begin{bmatrix} \cos \theta & - \sin \theta \\ \sin \theta & \cos \theta \end{bmatrix}
$$

These two transform classes might be used together when stitching images from a digital microscope to get a larger field of view where the specimen slide is allowed to translate or rotate in a fixed plane.

### Scaling

A third type of coordinate transform is scaling, where the sensed image origin and orientation remain fixed, but coordinates are scaled.

$$f(\bm{x}) = S_s \bm{x}$$

where $S_s$ is a scaling matrix parameterized by the scaling factor $s$.

$$S_s = \begin{bmatrix} s & 0 \\ 0 & s \end{bmatrix}$$

These three coordinate transforms taken together are often called an *similarity transform*.  Similarity transforms are rigid, meaning they do not change the shape of features in the reference image, parallel lines remain parallel, and angles and lengths are preserved.  For example, a triangle in the sensed image will map to a similar triangle in the reference image.

Similarity transforms can be written generally as

$$f(\bm{x}) = R_{\theta} S_s \bm{x} - \bm{c}$$

Some authors allow for the first or second column of $R_{\theta}$ to be negated which corresponds to a geometric reflection, though this is less useful in registration settings.

### Affine

A generalization of the similarity transform is the *affine transform*, where the rotation matrix is replaced by a matrix with no orthogonality constraint and the scaling factor is incorporated.

$$f(\bm{x}) = \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix} \bm{x} - \bm{c}$$

This transform can also account geometric skew, where angles and lengths are no longer preserved but parallel lines remain parallel.

<!-- ### Perspective -->

<!-- Another coordinate transform is *perspective projection*, which is used when $\bm{x}$ corresponds to a point in 3D space and the entire 3D scene is projected to a 2D plane in a nonlinear fashion. -->

<!-- ![](perspective.jpg){: style=width:500px} -->

### Elastic

When the type of transform is unknown or more complicated, elastic transforms can be used to correct for misalignment.  This can arise in situations where a 3D scene is projected through an optical system onto a 2D plane, but unlike perspective projection, there are large depth variations which occlude parts of the scene.  Objects which appear in one image may be completely obscured in the other, which is increasingly difficult to account for as the number of occlusions increases.  In these settings, a more general coordinate transform which can map more arbitrary distortions is preferred.

Elastic methods can either operate over the image as a whole (global), or apply different transforms to regions of the image separately (local).

An example of a global elastic method is the *bivariate polynomial* transform, in which the x and y coordinates are fed through a pair of polynomial functions.

$$u = \sum_{l=0}^m \sum_{j=0}^i a_{ij} x^l y^{j - l}$$

$$v = \sum_{l=0}^m \sum_{j=0}^i b_{ij} x^l y^{j - l}$$

where $\[x\,y\]$ are the original coordinates, $\[u,\,v\]$ the transformed coordinates, and $a_{ij}$ and $b_{ij}$ are constant parameters controlling the transform.

Local methods are more general than global methods and can handle distortions that global methods cannot, such as deformable objects, complex 3D surfaces, and object motion within the scene.  While these methods are more powerful, there is a tradeoff with computational complexity as the number of parameters increases.  An example of a local elastic coordinate transform is piecewise spline interpolation.

Below is a diagram which illustrates examples of some of these transform classes.

![](transforms.png){: style=width:300px}

<!-- | Transform   | Properties                                | Applications | -->
<!-- |-------------|-------------------------------------------|--------------| -->
<!-- | Similarity  | Preserves angles, lengths, parallel lines |              | -->
<!-- | Affine      | Preserves parallel lines                  |              | -->
<!-- | Perspective |                                           |              | -->
<!-- | Projective  |                                           |              | -->
<!-- | Elastic     |                                           |              | -->


## VISORS Mission

The VIrtual Super-resolution Optics with Reconfigurable Swarms (VISORS) mission, due to be launched by NASA in 2023, is a heliophysics CubeSat mission designed to study the Sun's corona at a finer scale than has been achieved in previous missions in order to shine light on the processes which drive heating in the corona.

VISORS consists of two 3U spacecraft known as the Optics Spacecraft (OSC) and Detector Spacecraft (DSC), which carry instrumentation for taking measurements in extreme ultraviolet (EUV) range.  These two spacecraft will fly in formation 40 meters apart aligned along an axis pointed at the region of interest on the Sun during science mode.  The OSC focuses incoming light using a novel diffractive element known as a photon sieve while simultaneously using its solar panels to block off-axis light from entering the DSC.  The DSC will be positioned on the focal plane corresponding to He II emission line at 30.4nm.  In particular, the OSC uses a diffractive optical element known as a photon sieve, which can outperform equivalent reflective optics due to tighter manufacturing tolerances. [^oktem]

VISORS is what is known as a *virtual* telescope.  In contrast to other non-virtual space telescopes such as Hubble (visible light) and the Solar Dynamic Observatory (EUV), the focusing optics and detector fly on separate spacecraft which allows the design to support large focal lengths without significantly increasing spacecraft volume and to reconfigure the wavelength after launch by adjusting spacecraft separation.

In addition to its contributions to heliophysics, VISORS will serve as a technology demonstration of diffractive, distributed telescopy and precision satellite formation flying.

![](satellite.png)

## Paper Outline

Chapter 2 introduces classes of image registration and describes popular registration methods from each class.
Chapter 3 introduces the idea of subpixel registration, its uses, and gives a summary of a fast subpixel registration algorithm which is used to derive a new fast multi-frame subpixel algorithm, described in chapter 4.
Chapter 5 contains numerical registration experiments under various settings, a description of the pipeline used to generate the test images, and some tests involving other classes of images unrelated to the VISORS project.

# Review of Registration Methods

There are two overarching categories of image registration algorithms, feature-based and area-based.  These registration classes vary primarily in the steps leading up to transform estimation, while the image transformation step is generally unchanged for a given motion model.  In feature-based methods, structures such as lines, regions or points, known as *features*, are detected in the reference and sensed images during the feature detection and feature estimation steps, while in area-based methods these steps are omitted entirely.

In this chapter, I focus primarily on the steps involved up estimating the image transform, namely feature detection, feature matching, and transform model estimation.

<!-- This simplicity can sometimes come at a performance cost in certain situations, however.  If a target scene has smooth regions with few salient features to register on, an area-based method may perform more poorly than a feature-based method which can ignore the smooth parts of the scene that contain little alignment information. -->

## Feature-Based Methods

Feature-based methods involve a preprocessing step known as *feature detection*, where notable structures in both images are located.  These structures can come in a variety of forms and can correspond to different kinds of objects depending on the context.  For example, images being registered in a remote sensing context could contain features such as amorphous regions (forests, lakes, fields), line segments (roads, buildings), or single points (street intersections, region corners).  There are many algorithms capable of extracting these features and the optimal choice of algorithm is highly dependent on the target scene.  In general, a desirable property of these algorithms is that the same features can be detected in both images and that these features are robust against corruption introduced by intensity mapping function $g$ or noise. [^zitova]

Some features in the sensed image may not having a matching counterpart in the reference image due to occlusions or because their counterpart is outside of the field of view. A desirable property of the feature matching algorithm is that incorrect matches are eliminated or assigned a low probability so that parameter estimates in the later transform estimation step are not skewed. [^zitova]

### Harris Corner Detection and RANSAC


## Area-Based Methods


### Cross Correlation

<!-- FIXME i_2(f) not well defined -->

The most straightforward of all methods, direct correlation, is conceptually simple and works for many classes of transforms.

Note that the normalization here is crucial so that the intensities of $i_1$ and $i_2$ do not influence the maximum.  We call this measure normalized cross correlation (NCC). [^brown]

<!-- only works when $f$ is a simple linear translation, $f(\bm{x}) = \bm{x} - \bm{c}^*$. -->

$$
\begin{aligned}
\hat{f} &= \arg \max_{f \in F} \text{NCC}(i_1, i_2(f)) \\
&= \arg \max_{f \in F} \frac{\sum_{\bm{x} \in X} i_1(\bm{x})i_2(f(\bm{x}))}{\sqrt{\sum_{\bm{x} \in X} i_1(\bm{x})^2}}
\end{aligned}
$$

where $F$ is the set of all linear translations.  Practically, the time required to search the space of all possible transforms for a given application makes this approach infeasible, so $F$ is often restricted to translations.

$$
\hat{c} = \arg \max_{\bm{c}} \frac{\sum_{\bm{x} \in X} i_1(\bm{x})i_2(\bm{x} - \bm{c})}{\sqrt{\sum_{\bm{x} \in X} i_1(\bm{x})^2}}
$$


<!-- $$ f^* = \arg \max_{\hat{f}} \sum_x i_1(x)i_2(\hat{f}(x)) = \arg \min_{\hat{f}} \sum_x e(x)^2 $$ --> 

Related similarity measures which are sometimes used in place of normalized cross correlation are sum of squared error (SSE)

$$
\text{SSE}(i_1, i_2(f)) = \sum_{\bm{x} \in X} (i_1(\bm{x}) - i_2(f(\bm{x})))^2
$$

and correlation coefficient

$$
\text{Corr}(i_1, i_2(f)) = \frac{\text{cov}(i_1, i_2(f))}{\sigma_1 \sigma_2} = \frac{\sum_{\bm{x} \in X} (i_1(\bm{x}) - \mu_1)(i_2(f(\bm{x})) - \mu_2)}{\sqrt{\sum_{\bm{x} \in X} (i_1(\bm{x}) - \mu_1)^2 \sum_{\bm{x} \in X}(i_2(f(\bm{x})) - \mu_2)^2}}
$$

where $\mu_1$, $\mu_2$, $\sigma_1$, $\sigma_2$ are the means and variances of $i_1$ and $i_2$ over $X$.

While cross correlation methods are very old, they continue to see widespread use because of ease of implementation in hardware (NCC can be efficiently implemented using multiply-accumulate hardware) and because limiting $f$ to translations isn't significantly restrictive for many scenarios.

In practice though, cross correlation is still successful in the presence of slight rotation, scaling or even non-affine transforms. <!-- need to find citation -->

### Generalized Iterative Cross Correlation

### Selective Similary Detection Algorithm (SSDA)

In standard correlation methods, the sum over $X$ for each candidate $f$ must be computed in full before a maximum is found.  Barnea, Silverman [^4] propose a class alternative schemes which greatly improve computation time in two ways.  The paper calls these algorithms selective similarity detection algorithms (SSDAs), of which one is presented here.

First, the paper uses absolute sum of errors (ASE) as a similarity measure, which requires no costly multiplications unlike NCC or SSE.

$$
ASE(i_1, i_2(f)) = \sum_{\bm{x} \in X} |i_1(\bm{x}) - i_2(\bm{x} - \bm{c})|
$$

The second optimization uses early stopping and requires that the sum over $X$ be implemented sequentially (e.g. as an iterative software loop).  For a particular candidate $\bm{c}$, the current value of the sum is compared to a threshold parameter $T$ after each iteration.  If the ASE surpasses this threshold, the number of iterations is recorded and the algorithm moves on to the next candidate.  If an candidate computation never exceeds $T$, then the final ASE is recorded instead.

Finally, the candidate with the lowest ASE is selected.  If all candidates surpassed the threshold, then the candidate with the most number of iterations before passing the threshold is selected.

![Error accumulation curves for candidates $\bm{c}_1$, $\bm{c}_2$, $\bm{c}_3$ and $\bm{c}_4$.  Error computation for $\bm{c}_1$ and $\bm{c}_2$ terminated early at 7 and 9 iterations.  $\bm{c}_4$ is the best estimate for offset, followed by $\bm{c}_3$, $\bm{c}_2$ and $\bm{c}_1$.](ssda.png)

This algorithm offers potentially orders of magnitude speed improvements over direct cross-correlation because of early stopping, but requires selection of parameter $T$.  A choice of $T$ too high limits efficiency gains while a choice of $T$ too low can lead to suboptimal results.

### NMSRE Conjugate Descent

<!-- FIXME assumes linear shift, but this section is about high dimensional f -->

The first method, presented by Guizar-Sicairos, Thurman, Fienup [^6],  is a form of conjugate descent on the normalized root mean squared error (NRMSE), which is a translation-invariant measure of error between an image $f$ and a copy $g$ shifted by $(x_0^{\ast}, y_0^*)$.

$$
f^*_{NMSRE} = \min_{\hat{f}} \frac{\sum_{x} |i_2(\hat{f}(x)) - i_1(x)|^2}{\sum_{x}|i_1(x)|^2}
$$

By minimizing the NMSRE over $f$, the true parameters of $f$ can be found.

Rewriting the above definition into a maximization problem and assuming $f$ is a linear shift by $[x_0, y_0]$, we can achieve a more useful formulation.

$$
NMSRE^2 = 1 - \frac{\max_{x_0, y_0} |r(x_0, y_0)|^2}{\sum_{x, y}|i_1(x, y)|^2 \sum_{x, y}|i_2(x, y)|^2} \\
$$

$$
\begin{aligned}
r(x_0, y_0) &= \sum_{x, y}I_2(x - x_0, y - y_0)I_1^*(x, y) \\
&= \sum_{u, v} \tilde{I_1}(u, v)\tilde{I_2}^*(u, v) \text{exp}\left[ j 2 \pi \left( u \frac{x_0}{M} + v \frac{y_0}{N} \right) \right]
\end{aligned}
$$

where $r$ is cross correlation and $\tilde{I_1}$ and $\tilde{I_2}$ are the image DFTs of size $M \times N$.

Since all other terms are constant, we need only minimize $|r(x_0, y_0)|^2$.

$$
\frac{d(r(x_0, y_0))}{dx_0} = 2 \text{Im} \left(r(x_0, y_0) \sum_{u, v} \frac{2 \pi u}{M} \tilde{I_1}^*(u, v) \times \tilde{I_2}(u, v) \text{exp} \left[-j 2 \pi \left( u \frac{x_0}{M} + v \frac{y_0}{N} \right) \right] \right) $$

With this partial derivative (and a similar for $y_0$) we can use standard conjugate descent to solve for $(x_0^{\ast}, y_0^*)$.

## Frequency-Based Methods

If an acceleration over correlation-based methods is needed or the images were acquired under frequency dependent noise, Fourier methods are often preferred.  These methods exploit the Fourier representation of images in the frequency domain and have shown better robustness against illumination differences between $i_1$ and $i_2$.

### Phase Correlation

Phase correlation was originally proposed for registering linearly translated images.  It takes advantage of the Fourier Shift theorem, which states that translating an image and taking its Fourier transform is equivalent to multiplying the Fourier transform of the original untranslated image by a complex exponential.

Computing the cross-power spectral density (CPSD) we can directly obtain this complex exponential.

$$
i_2(\bm{x}) = i_1(\bm{x} - \bm{c}^*)
$$

$$
CPSD(i_1, i_2)(\bm{\omega}) = \frac{I_1(\bm{\omega}) \overline{I_2(\bm{\omega})}}{|I_1(\bm{\omega}) \overline{I_2(\bm{\omega})}|} =
\frac{I_1(\bm{\omega}) \overline{I_1(\bm{\omega}) e^{-j \langle \bm{\omega}, \bm{c}^* \rangle}}}{|I_1(\bm{\omega}) \overline{I_1(\bm{\omega}) e^{-j \langle \bm{\omega}, \bm{c}^* \rangle}}|} = e^{j \langle \bm{\omega},  \bm{c}^* \rangle}
$$

Where $I_1$ and $I_2$ are the Fourier transforms of $i_1$ and $i_2$.  The final estimate for $\bm{c}_0$ is obtained by a final inverse Fourier transform of the CPSD, yielding a delta at location $\bm{c}_0$.

$$
PC(i_1, i_2)(\bm{x}) = \mathcal{F}^{-1}\left[ CPSD(i_1, i_2) \right](\bm{x}) = \delta(\bm{x} - \bm{c}^*) \\
\hat{c} = \arg \max_{\bm{x}} PC(i_1, i_2)(\bm{x})
$$

An important consideration here is that the Fourier Shift theorem only holds when translation is circular.  In practice, the phase correlation method still works if the region of overlap is sufficiently large.  Foroosh, Zerubia, Berthod [^7] propose a prefilter which can be applied to both images before phase correlation to reduce these effects.

### De Castro, Morandi Method

De Castro, Morandi [^5] introduced an extension of the phase correlation method which applies to images that are translated and rotated. This method is similar in spirit to the Generalized Iterative Cross Correlation method in that it amounts to repeatedly detransforming $i_2$ with different parameters, testing alignment with $i_1$ using some similarity measure and repeating this process until the correct parameters are found.  Like the standard phase correlation method, this technique claims robustness against frequency dependent noise and non-uniform illumination differences between the images.

Let $i_2$ be a translated and rotated copy of $i_1$.  Then

$$
i_2(\bm{x}) = i_1(R_{\theta^*} (\bm{x} - \bm{c^*}))
$$

where 

$$
R_{\theta^*} = \begin{bmatrix} \cos \theta^* & - \sin \theta^* \\ \sin \theta^* & \cos \theta^* \end{bmatrix}
$$

is a rotation operator of angle $\theta^*$.

From the Fourier shift theorem, we know that a shift by $\bm{c}^*$ in the spatial domain results in a multiplication by a complex exponential in the frequency domain.  Additionally, the Fourier rotation theorem tells us that a rotation in the spatial domain is a rotation by the same angle in the frequency domain.  Therefore, the relation between $I_1$ and $I_2$ can be written

$$
I_2(\bm{\omega}) = e^{-j \langle \bm{\omega}, \bm{c}^* \rangle} I_1(R_{\theta^*} \bm{\omega})
$$

<!-- $$ -->
<!-- CPSD(I_1, \hat{I_2})(\omega) = \frac{I_1(\omega) \overline{I_2(R^{-1}_{\hat{\theta}}\omega)}}{|I_1(\omega) \overline{I_2(R^{-1}_{\hat{\theta}}\omega)}|} = -->
<!-- \frac{I_1(\omega) \overline{I_1(R^{-1}_{\hat{\theta}} R_{\theta} \omega)}}{|I_1(\omega) \overline{I_1(R^{-1}_{\hat{\theta}} R_{\theta} \omega)}|} = -->
<!-- \frac{I_1(\omega) \overline{I_1(R_{\theta - \hat{\theta}} \omega)}}{|I_1(\omega) \overline{I_1(R_{\theta - \hat{\theta}} \omega)}|} = -->
<!-- $$ -->

To find $\theta^*$, the authors consider the expression

$$
\mathcal{F}^{-1} \left[ \frac{I_2(\bm{\omega})}{I_1(R_{\theta} \bm{\omega})} \right]
$$

When $\theta = \theta^*$, we get

$$
\mathcal{F}^{-1} \left[ \frac{I_2(\bm{\omega})}{I_1(R_{\theta} \bm{\omega})} \right] =
\mathcal{F}^{-1} \left[ \frac{e^{-j \langle \bm{\omega}, \bm{c}^* \rangle}I_1(R_{\theta^*}\bm{\omega})}{I_1(R_{\theta^*} \bm{\omega})} \right]  = \mathcal{F}^{-1} \left[ e^{-j \langle \bm{\omega}, \bm{c}^* \rangle} \right] = \delta(\bm{x} - \bm{c}^*)
$$

By testing a range of values for $\theta$ for which results in the closest to an impulse in the above expression, an approximate for the true $\theta^*$ can be found.

Formally, this is the minimization problem

$$
\hat{\theta} = \arg \min_{\theta} \left\Vert \mathcal{F}^{-1} \left[ 
\frac{I_2(\bm{\omega})}{I_1(R_{\theta}\bm{\omega})}
\right] \right\Vert_N
$$

where $\left\Vert \right\Vert_N$ is a placeholder for a measure which is large for unit impulses.  For example

$$
\left\Vert f \right\Vert_N = \left\Vert f - \delta(\bm{x} - \arg \max_{\hat{\bm{x}}} f(\hat{\bm{x}})) \right\Vert_2
$$

When $\hat{\theta}$ has been found, the offset can be obtained directly from the impulse function

$$
\hat{\bm{c}} = \arg \max_\bm{x} \mathcal{F}^{-1} \left[ \frac{I_2(\bm{\omega})}{I_1(R_{\hat{\theta}} \bm{\omega})} \right](\bm{x})
$$

Note that the denominator $I_1(R_{\hat{\theta}} \bm{\omega})$ must be evaluated using interpolation, as $R_{\hat{\theta}} \bm{\omega}$ will not coincide with the sample nodes of $I_1$ in general.

<!-- FIXME author somehow use window to eliminate edge effects? -->

<!-- FIXME need a notational correction here, there are continuous and discrete versions of I in both time and frequency that need to be expressed -->
<!-- \tilde{I}(\omega_x, \omega_y) = \int_X I(x, y) e^{-j(x \omega_x + y \omega_y)} dx\, dy \approx \Delta x \Delta y \tilde{I}(\omega_x, \omega_y) -->


### Phase Correlation - Rotation/Scale Extension

Phase correlation in its original form is an elegant method of registering translated images.  The method introduced by De Castro and Morandi provides a way to detect and correct for rotation in images before applying phase correlation.  However, another common transform in imaging systems is scaling, which can occur when the target scene moves closer to the imaging device or if the imager has zoom capabilities.  Like rotation, scaling by a factor $s_0$ can also be written as a matrix operator like so

$$
S_{s^*} = \begin{bmatrix}s^* & 0 \\ 0 & s^*\end{bmatrix}
$$

Sarvaiya, Patnaik, Kothari [^8] introduced a new method which is capable of registering images that have been translated, rotated and scaled.  They make use of the Fourier scale, Fourier shift and Fourier rotation properties and also the Log-Polar transform (also known as Fourier-Mellin transform), where rotation and scaling in the original domain manifest as translation in the Log-Polar domain.  Their approach is broken into two applications of the phase correlation method, where the first application is used to recover scale and rotation, and the second, translation.

If $i_2$ is a scaled, rotated and shifted copy of $i_1$,

$$
i_2(\bm{x}) = i_1(R_{\theta^*} S_{s^*} \bm{x} - \bm{c}_0)
$$

$$
\begin{aligned}
&PC \left( \left| \mathcal{LP} \left[ \mathcal{F} \left[ i_1 \right] \right] \right| , \left| \mathcal{LP} \left[ \mathcal{F} \left[ i_2 \right]\right] \right| \right)(x, y) \\
= &PC \left( \left| \mathcal{LP} \left[ \mathcal{F} \left[ i_1 \right] \right] \right| , \left| \mathcal{LP} \left[ \mathcal{F} \left[ i_1(R_{\theta^*} S_{s^*} \bm{x} - \bm{c}_0) \right] \right] \right| \right)(x, y)  \\
&\text{Apply Fourier shift, scale, rotation properties} \\
= &PC \left( \left| \mathcal{LP} \left[ I_1(\bm{\omega}) \right] \right| , \left| \mathcal{LP} \left[ \frac{1}{s^{*2}} e^{-j \langle S_{s^*}^{-1} R_{\theta^*} \bm{\omega}, \bm{c}_0 \rangle} I_1(S_{s^*}^{-1} R_{\theta^*} \bm{\omega}) \right] \right| \right)(x, y) \\
= &PC \left( \left| \mathcal{LP} \left[ I_1(\bm{\omega}) \right] \right| , \left| \mathcal{LP} \left[ \frac{1}{s^{*2}} e^{-j \langle S_{s^*}^{-1} R_{\theta^*} \bm{\omega}, \bm{c}_0 \rangle} \right] \mathcal{LP} \left[ I_1(S_{s^*}^{-1} R_{\theta^*} \bm{\omega}) \right] \right| \right)(x, y) \\
&\text{Apply Log-Polar shift property} \\
= &PC \left( \left| \mathcal{LP} \left[ I_1 \right](\rho, \theta) \right| , \left| \mathcal{LP} \left[ \frac{1}{s^{*2}} e^{-j \langle S_{s^*}^{-1} R_{\theta^*} \bm{\omega}, \bm{c}_0 \rangle} \right] \mathcal{LP} \left[ I_1 \right](\rho + \ln \frac{1}{s^*}, \theta + \theta_0) \right| \right)(x, y) \\
= &PC \left( \left| \mathcal{LP} \left[ I_1 \right](\rho, \theta) \right| , \left| \mathcal{LP} \left[ I_1 \right](\rho + \ln \frac{1}{s^*}, \theta + \theta_0) \right| \right)(x, y) \\
= &\delta \left(x - \ln \frac{1}{s^*}, y - \theta_0 \right)
\end{aligned}
$$

where $\mathcal{LP}$ is the Log-Polar transform.


### Mutual Information

Viola and Wells introduced a new class of registration methods in 1994 based on entropy of image pairs.  This class of methods has proven effective in multimodal registration so it has achieved significant popularity in medical imaging.


In the early 20th century, Hartley was looking for a way to measure the transmission of information, particularly in relation to the telegraph as a communications system.  He considered a system in which a finite set of symbols ('dit' or 'dah', telegraph 1's or 0's) are sent sequentially through a channel (telegraph wire).

The number of unique messages that can be encoded given a message length of $n$ and $s$ unique symbols is $s^n$.  However, Hartley wanted a measure that would grow linearly with message length.  A message which is twice as long should contain twice as much information.

He therefore settled on the following measure of information:

$$
H = \log s^n = n \log s
$$

From the first formulation, it is apparent that information grows linearly with $n$.  Another interesting feature of this measure is that if there is only one symbol, we know exactly what the message will be and so it contains no information $(H = n \log 1 = 0)$.  This suggests that entropy can also be viewed as a measure of uncertainty.

A disadvantage of Hartley's entropy measure is that it assumes all symbols are equally likely to occur in a message, which is generally not true.

In 1948, Shannon introduced a new measure of information which takes this fact into account by weighting Hartley's entropy by the probability that symbols occur.  This is now known as Shannon entropy.  For a set of $s$ symbols with probabilities $p_1, ..., p_s$ of occuring, Shannon entropy is given as


$$
H = \sum_k p_k \log \frac{1}{p_k} = - \sum_i p_k \log p_k
$$

Like Hartley's entropy, Shannon entropy can be viewed as a measure of uncertainty.  If a particular symbol has a very high probability of occuring, our uncertainty about the message decreases and hence information decreases.  If all symbols have an equal probability of occuring, entropy is maximized.  Thus Shannon entropy may also be considered as a measure of spread of a probability distribution.  A distribution with most mass concentrated around a few peaks will have low entropy while a more uniform distribution will have higher entropy.

To compute Shannon entropy of an image, all possible intensity values of the pixels can be interpreted as symbols in the message.  For an image with bit depth of 8 bits, one can collect all the intensity values into a histogram in order to compute $p_0, ..., p_{255}$, as shown below.

![An image and its intensity histogram](histogram.png)

Now that we can compute entropy for images we must introduce one more concept before registration can occur, joint histograms.  A joint histogram is a 2D function which, for all possible pairs of intensities, describes how many times intensity pairs occur for a pair of registered images.  For example, if a joint histogram has value 17 at coordinate [33, 34], then for this particular registration there are 17 pixels in which the first image has intensity 33 and the second has intensity 34.  In the case of two 8 bit images, the joint histogram is a 256x256 image.  An example joint histogram for two images is shown below.

![Two registered images and their joint histogram, or feature space](feature_space.png)

The joint histogram changes with the alignment of the images.  For a correctly aligned pair of images, structures within the image align and vary with each other, so we expect the intensities to correlate which manifests as clustering in the joint histogram.  As the image pair becomes misaligned, more greyscale combinations are introduced and the joint histogram exhibits more uniformity.  By measuring this uniformity we now have a similarity measure for registration.

Formally, the joint Shannon entropy for a pair of registered images

$$
H(i_1, i_2(f)) = -\sum_{m, n} p(m, n) \log p(m, n)
$$

where $p(i, j)$ is the joint histogram of $i_1$ and candidate registered $i_2(f)$ in the region of overlap $X$. <!-- FIXME -->

However, a problem that can occur when joint entropy is used directly is that low entropy (high degree of reported alignment) can occur for invalid registrations if the images contain large regions of uniform intensity.  For example, if the images in the figure above are aligned so that only their corners containing background overlap, the joint histogram will have approximately a single peak and the joint entropy will be very low.  To account for this, one can make use of the marginal entropies to penalize alignments where the region $X$ contains little information in the images.  This is known as mutual information.

$$
MI(i_1, i_2(f)) = H(i_1) + H(i_2(f)) - H(i_1, i_2(f))
$$

With this new measure, if the overlap region contains little information, terms $H(i_1)$ and $H(i_2(f))$ will be small and counteract joint entropy.  Also note that since mutual information contains $-H(i_1, i_2(f))$, minimizing joint entropy is related to maximizing mutual information.


# Subpixel Registration

# Multiframe Subpixel Registration

# Numerical Experiments

# Conclusion

<!-- ### Optimization-Based Methods -->

<!-- Many of the above methods introduce various similarity metrics as measures of alignment between registration candidates.  They mostly rely on an exhaustive search through all potential registration candidates and as such are restricted to situations where the set of all possible $f$ candidates are small, usually simple translation.  In situations where the number of parameters controlling $f$ is large, such as elastic transform, it is appropriate to make use optimization methods that can find minima or maxima in the chosen similarity measure in a feasible amount of time. -->


<!-- # Summary -->

<!-- Area-based methods are preferred when images have salient details and information is provided by pixel intensities rather than shapes and structures in the image.  The images' intensities must be similar or at least statistically related.  The set of candidate transforms $f$ that can be searched is generally limited to translation with small amounts of rotation or skew, but there are some extensions to methods that support large rotations or skews so long as the degrees of freedom of $f$ remains small.  Pyramid search techniques and sophisticated optimization strategies are available to more quickly find extrema of the similarity measure. -->

<!-- Feature-based methods are generally utilized when shapes in structures in the image pair contain more alignment information than the pixel intensities, such as between a picture of an object and a computer model of an object.  The drawback of these methods is that such features can be hard to detect and match with each other.  It is critical that chosen feature detector be robust against any differences between the images. -->

<!-- | Method | Application | Noise | -->
<!-- |--------|-------------|-------| -->
<!-- | foo    |             |       | -->
<!-- |        |             |       | -->


# References
- [A Survey of Mutual Information Based Registration](https://www.google.com/search?q=survey%20of%20mutual%20information%20based%20registration) - Pluim, Maintz, Viergever 2003

[^1]: Motion Estimation - Konrad

[^zitova]: [Image registration methods: a survey](https://www.sciencedirect.com/science/article/pii/S0262885603001379/pdfft?md5=9ac6884a88ac624d4861de8fe7666e27&pid=1-s2.0-S0262885603001379-main.pdf) - Zitova, Flusser 2003

[^brown]: Brown Survey Paper

[^oktem]: F. S. Oktem, F. Kamalabadi, and J. M. Davila, "High-resolution computational spectral imaging with photon sieves," in 2014 IEEE International Conference on Image Processing (ICIP). IEEE, 2014, pp. 5122-5126.

[^farsiu2004]: Fast and Robust Multiframe Super Resolution - 2004, 2343 Citations

[^4]: [Barnea, Silverman 1972](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5008923)

[^5]: [De Castro, Morandi 1987](https://ieeexplore.ieee.org/document/4767966)

[^6]: [Guizar-Sicairos, Thurman, Fienup 2008](https://www.osapublishing.org/ol/viewmedia.cfm?uri=ol-33-2-156&seq=0)

[^7]: [Foroosh, Zerubia, Berthod 2002](https://ieeexplore.ieee.org/document/988953)

[^8]: [Sarvaiya, Patnaik, Kothari 2012](http://www.jprr.org/index.php/jprr/article/view/355)

[^9]: Feature-Based Deformable Image Registration with RANSAC Based Search Correspondence - Colleu, Shen, Matuszewski, Shark, Cariou

[^10]: An Automatic Satellite Image Registration Technique Based on Harris Corner Detection and Random Sample Consensus (RANSAC) Outlier Rejection Model - Misra, Moorthi, Dhar, Ramakrishnan
