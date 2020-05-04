---
template: project.j2
date: 2020-04-27
title: Outline
---

<!--
- is [^1] equivalent to Prony's method when using all image pixels?
- Guizar-Sicairos multiframe extension
    - can we estimate expected registration error?  [ argmax(sum) ] vs [ mean(argmax, argmax, ...) ]
-->

<style> c { color: gray } </style>


First and second level bullets are sections and subsections.  Third level bullets are further content breakdowns of subsections.

- Abstract
- Contribution of Thesis
    - Goal: Extend work from *Guizar-Sicairos, Thurman, Fienup* [^5] (linear subpixel registration) to a multiframe setting

- Chapter 1 - Introduction
    - Motion Estimation, Segmentation, and Registration
        - <c>Describe techniques of motion estimation, segmentation, registration.  What fields are they used in (GIS, CT, remote sensing, etc) and related applications. </c>
    - Registration Problem Model
        - <c>Generic mathematical model for a two-frame registration problem, describing how registration involves finding some specific transform which warps the *reference* image to the *template* image.</c>
    - Categorizing Registration Methods
        - <c> 4 step generalization of registration methods [^2]
            1. Feature detection
            2. Feature matching
            3. Transform model estimation
            4. Image transformation
            </c>
    - Choice of Motion Prior
        - <c>Describe some families of transforms (translation, rotation, affine, scale, rubbersheeting, etc.) and which are used in some common problems (.e.g rubbersheet transform might be used to align faces of different shapes).  e.g. Mention effects on algorithm complexity.</c>
    - Motivating Problem
        - <c>1 page description of VISORS project and justification for why this choice of motion prior (constant translation) is appropriate.  Show some simulated images to illustrate extreme observation noise.</c>
    - Outline
        - <c>Chapter 2 introduces classes of image registration and describes popular registration methods from each class.  Chapter 3 introduces the idea of subpixel registration, its uses, and gives a summary of a fast subpixel registration algorithm which is used to derive a new fast multi-frame subpixel algorithm, described in chapter 4.  Chapter 5 contains numerical registration experiments under various settings, a description of the pipeline used to generate the test images, and some tests involving other classes of images unrelated to the VISORS project.</c>
        
- Chapter 2 - Review of Global Registration Methods
    - <c>The primary purpose of this chapter is to overview the classes of registration methods and highlight strenghts and weaknesses. </c>
    - Area Based Methods
        - <c>Methods include Cross Correlation, Normalized CC and Selective Similarity Detection Algorithm</c>
        - <c>Appropriate for situations where high noise immunity is needed.</c>
    - Information Based Methods
        - <c>Mutual Information</c>
    - Optimization Based Methods
        - <c>Lukas-Kanade Optical Flow</c>
    - Featured Based Methods
        - <c>Currently state of the art for handheld video super resolution applications
        - <c>RANSAC</c>
        - <c>Features need to be accurately detected and localized -> not good for high noise</c>
    - Frequency Based Methods
        - <c>Methods include phase correlation, de Castro, Morandi Method [^5]</c>
        - <c>In the next section I introduce another frequency based method which my work is based upon</c>
    
- Chapter 3 - Subpixel Registration [^6]
    - Coarse Estimation
        - <c>Coarse estimation step of algorithm.  Just a simple argmax of circular cross correlation implemented via FFTs</c>
    - Fine Estimation
        - <c>Fine estimation step of algorithm.  Involves direct DFT evaluation of a small patch centered around coarse pixel.</c>
    - Optimality
    - Padded FFT vs Direct DFT
        - <c>Explanation of why direct DFT evaluation is significantly faster than a padded FFT approach for the fine estimation step.  Computational complexity analysis?</c>
    
- Chapter 4 - Multiframe Subpixel Registration
    - Multiframe Registration Model
        - <c>Introduce mathematical model for multiframe registration describing how registration involves finding a set of transforms parameterized by frame number rather than a single transform.</c>
    - Coarse Estimation with All Frames
    - Fine Estimation with All Frames
    - Optimality
        - <c>I have a [partial proof](/reports/2020-03-07/) showing that the ML solution to a multiframe registration problem is similar to my algorithm.  Need to revisit this before deciding to include it.</c>
        
- Chapter 5 - Numerical Experiments
    - Generation of Test Data
        - <c>Nanoflare Scene Generation</c>
        - <c>Video Sequence Generation</c>
            - <c>Optical Blurring and Point Spread Functions</c>
            - <c>Photon Sieve</c>
            - <c>Motion Blurring</c>
        - <c>Gaussian and Poisson Noise at Detector</c>
    - Registration Results
        - <c>Test algorithm under different noise levels, drift velocities, drift angles, framerates, number of frames.</c>
        - <c>This would also be the section to compare my algorithm against another multiframe registration algorithm.</c>
    - Other Image Classes
        - <c>Similar tests on other images unrelated to VISORS to show algorithm is more generally applicable.  These images will have much less noise.</c>
        - <c>What are some other scenarios where a constant translation motion prior is appropriate?</c>
    
- Chapter 6 - Conclusion
    - Future Work
        - Extension to Rotational Motion [^8]
        
# Timeline

- May 4 - Introduction completed.
    - Some of this introductory material is present in the previous draft.
- May 11 - Chapter 3 completed.
    - Chapter 3 will be a writeup of the Guizar-Sicairos paper [^6].
- May 25 - Chapter 4 completed.  End of numerical experiments.
- June 2 - Chapters 2, 5 completed.  Editing by Farzad begins.
    - Much of chapter 2 will come from previous drafts.
    - Chapter 5 follows the same format as the [optics pipeline document](https://uiuc-sine.github.io/reports/pipeline/)
- July 2 - Last day to start MS thesis check.
- July 24 - MS thesis deposit

# Thesis Checklist

- [x] Registered for ECE599
- [ ] Thesis/Dissertation Approval Form
- [ ] Apply for graduation
- [ ] File thesis title with department
- [ ] Electronic Submission

[^1]: [Extension of phase correlation to subpixel registration](https://ieeexplore.ieee.org/abstract/document/988953) - Foroosh, Zerubia, Berthod
[^2]: [Image registration methods: a survey](https://www.sciencedirect.com/science/article/pii/S0262885603001379/pdfft?md5=9ac6884a88ac624d4861de8fe7666e27&pid=1-s2.0-S0262885603001379-main.pdf) - Zitova, Flusser 2003
[^5]: [Registration of Translate and Rotated Images Using Finite Fourier Transforms](https://ieeexplore.ieee.org/document/4767966) - De Castro, Morandi 1987
[^6]: [Efficient subpixel image registration algorithms](https://www.osapublishing.org/ol/viewmedia.cfm?uri=ol-33-2-156&seq=0) - Guizar-Sicairos, thurman, Fienup 2008
[^8]: [Image Registration Using Log Polar Transform and Phase Correlation to Recover Higher Scale](http://www.jprr.org/index.php/jprr/article/view/355) - Sarvaiya, Patnaik, Kothari 2012

    
  
