---
author: Evan Widloski
title: Validating CSBS on a hypothetical imaging element
date: 2019-05-15
template: project.j2
---

Here I test CSBS with SSE cost on a hypothetical imaging element with hand-crafted PSF DFTs.  Unlike a photon sieve, this element has PSF DFTs which are *not* maximized at the focal length for all frequencies.  The goal of this report is to show that our CSBS implementation chooses a sane measurement configuration when presented with a set of PSFs with very different frequency supports.

![PSF DFTs of hypothetical element at 49 measurement locations.](square_dfts.png)

![PSF DFTs of typical photon sieve at 49 measurement locations.](photonsieve_dfts.png)

# CSBS SSE Cost

$$\text{trace}((A^TA + \lambda^2 L^TL)^{-1})$$

![CSBS result for photon sieve. \\(L^TL = D_h^TD_h + D_v^TD_v\\), \\(\lambda = 1\\).  PSFs with low frequency components are prioritized.](square_csbs_order1.png)

![CSBS result for photon sieve. \\(L^TL = I\\), \\(\lambda = 1\\).  All PSFs have equal importance.](square_csbs_order0.png)
