---
template: project.j2
date: 2019-01-27
title: Outline
---

#### Reference Theses

- [MRI Registration and Segmentation for Machine Learning Diagnosis of Parkinson's Disease](http://hdl.handle.net/2142/55634)

<!--

- is [^1] equivalent to Prony's method when using all image pixels?
- Guizar-Sicairos multiframe extension
    - can we estimate expected registration error?  [ argmax(sum) ] vs [ mean(argmax, argmax, ...) ]

-->

#### Outline

Goal: combine work from *Guizar-Sicairos, Thurman, Fienup* [^5] (linear subpixel registration), *Sarvaiya, Patnaik, Kothari* [^6] (rotational, scaling registration), and extend to a multiframe setting

- Introduction
    - Define registration, motion estimation, segmentation
    - Registration model (from thesis draft) [Draft](https://uiuc-sine.github.io/thesis/intro.html#introduction)
    - 4 step generalization of registration methods [^2]
        1. Feature detection
        2. Feature matching
        3. Transform model estimation
        4. Image transformation
    
- Chapter 1 - Registration via Phase Correlation
    - Area based methods - cross correlation, normalized CC, etc
    - Frequency based methods - Phase correlation
        - Based on Fourier shift property - CPSD of shifted signal gives complex exponential
        - Provides sharper peak compared to CC based methods
        - Resistance
    - Pre whitening
    - Rotational/Scaling Extension to Phase correlation
    
- Chapter 2 - Subpixel Registration
    - 

- Chapter 3 - Multiframe Registration (needs expanding)
    - Give definition and expand registration model from introduction
    - Prior work
    - Introduce my multiframe extension to *Guizar-Sicairos, Thurman, Fienup*
        - How does this compare to simply averaging registration estimates for adjacent frames (expected registration error)

[^1]: [Extension of phase correlation to subpixel registration](https://ieeexplore.ieee.org/abstract/document/988953) - Foroosh, Zerubia, Berthod
[^2]: [Image registration methods: a survey](https://www.sciencedirect.com/science/article/pii/S0262885603001379/pdfft?md5=9ac6884a88ac624d4861de8fe7666e27&pid=1-s2.0-S0262885603001379-main.pdf) - Zitova, Flusser 2003
[^5]: [Registration of Translate and Rotated Images Using Finite Fourier Transforms](https://ieeexplore.ieee.org/document/4767966) - De Castro, Morandi 1987
[^6]: [Efficient subpixel image registration algorithms](https://www.osapublishing.org/ol/viewmedia.cfm?uri=ol-33-2-156&seq=0) - Guizar-Sicairos, thurman, Fienup 2008
[^8]: [Image Registration Using Log Polar Transform and Phase Correlation to Recover Higher Scale](http://www.jprr.org/index.php/jprr/article/view/355) - Sarvaiya, Patnaik, Kothari 2012


#### Multiframe Methods
- Fast and accurate image registration: Applications ot on-boad satellite imaging
  - Rais
  - https://tel.archives-ouvertes.fr/tel-01485321/file/75996_RAIS_2016_archivage.pdf
  - Great numerical overview/comparison of two-frame methods under different settings
  - Plots comparing runtimes and errors
  - Implementation: https://github.com/martinraism/shiftestimationipol
  
- Super-resolution: a comprehensive survey - 2014, 400 citations
  - Nasrollahi, Moeslund
  - https://link.springer.com/article/10.1007/s00138-014-0623-4
  - Section 3.1 Geometric Registration
    - 

- RASL: Robust Alignment by Sparse and Low-rank Decomposition of Linearly Correlated Images - 2010, 170 citations
  - Yi-Ma
  - assumes aligned images arranged as columns of a matrix will have low rank
    - not a good assumption for linearly translated images (esp first and last images)
  - assumes noise is low magnitude gaussian (section 1C paragraph 2)
    - other models and higher noise levels out of scope of paper

- A bayesian approach to adaptive video super resolution - 2011, 181 citations
  - Ce Liu, Deqing Sun
  - estimates motion, blur kernel and noise level
  - Implementations:
    - https://github.com/qiaopTDUN/bayesian-video-super-resolution (matlab)
  
- Fast and Robust Multiframe Super Resolution - 2004, 2343 Citations
  - Farsiu, Robinson
  - Implementations: 
    - https://github.com/allwillbeok/SuperResolution-1
    - https://github.com/thomas-koehler/SupER
    - https://github.com/enry12/super_resolution
    - https://github.com/debugCVML/FRSR-Matlab/blob/cc0b766e7b588a43b653ca0f80896e6320b45479/FastRobustSR.m
  - Super resolution only, assumes images already registered

##### NN Based

- Detail-revealing Deep Video Super-resolution - 2017, 137 citations

- Real-Time Single Image and Video Super-Resolution Using an Efficient Sub-Pixel Convolutional Neural Network

##### Time delay estimation

- TIME DELAY ESTIMATION VIA MULTICHANNEL CROSS-CORRELATION
  - could be natural extension of this method to 2D images
  - doesnt seem to support subpixel registration out of box (not sure)
  - allows nonuniform sensor placement (i.e. non uniform video frame sample times)

- Robust Time Delay Estimation Exploiting Redundancy Among Multiple Microphones

- Time delay estimation by generalized cross correlation methods

- tikhonov parameter estimation
  - https://onlinelibrary.wiley.com/doi/full/10.1046/j.1365-2818.2000.00671.x
