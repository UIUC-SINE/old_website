---
template: project.j2
author: Evan Widloski
date: 2019-08-05
title: Weekly Report
---

### CSBS Presentation Outline

Ulas and I drafted an outline for what a conference presentation on CSBS might look like.  We want to write a conference paper draft before the Summer is up, but thought it would be easier to get ideas down in presentation form first.

Title: A Greedy Algorithm for Measurement Configuration Selection in Spectral Imaging

##### Slide 1 - Motivation

- heliophysicists interested in multi wavelength imaging because:
    - foo
    - bar

- this is called spectral imaging

##### Slide 2 - Spectral Imaging
- several types of spectral imaging
    - filter wheel
    - moving slit
    - diffractive element + moving imager
  
##### Slide 3 - Choice of Measurement Locations

- where should measurements be taken
- is it always best to take measurements at the focal planes?

##### Slide 4 - Extremely High Dimensional Search Space

- N candidate measurement locations, K measurements
    - *N^K* measurement combinations to test
    - for our particular problem this is a large number
  
##### Slide 5 - CSBS: A Greedy Algorithm

- CSBS works by eliminating 1 candidate measurement location at a time
- the measurement location which contributes the least to image quality is selected for elimination
    - multiple cost metrics, e.g. SSE cost
  
##### Slide 6 - SSE Cost

- not sure whether to include this

##### Slide 7 - Numerical Results




