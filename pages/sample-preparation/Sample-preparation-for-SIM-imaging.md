---
layout: default
title: Sample preparation for SIM imaging
author: Delaine Larsen
---

# Sample preparation for SIM imaging

Structured Illumination (SIM) imaging is extremely sensitive to spherical aberration. To get the highest quality images (or even to get proper reconstruction), you need to minimize spherical aberration. This means:

- You should use [high precision 0.17 mm coverslips](High-Precision-Coverslips.html).

- You should mount in an appropriate mounting medium. Nikon recommends mounting either in [2,2-thiodiethanol](http://www.ncbi.nlm.nih.gov/pubmed/17131355) or in [Prolong Gold](http://www.invitrogen.com/site/us/en/home/brands/Molecular-Probes/Key-Molecular-Probes-Products/ProLong-Antifades-Brand-Page.html) or a newer equivalent (for a hard-set mounting medium). If using Prolong Gold, be aware of potential shrinkage when it cures.
  - > **Note:** Hard-set mounting mediums will flatten out your sample — see figure below.
  - > **⚠️ DO NOT USE** Fluoromount G. We have had people try this. It does not work.
  - > **⚠️ DO NOT USE** mounting medium which contains DAPI or other fluorophores.

- You should have your sample as close to the coverslip as possible (e.g. cells grown on coverslip, not on slide).

- You should use bright and stable fluorophores.

---

## Effect of Mounting Media on Sample

<div style="text-align: center; margin: 1.5em 0;">
  <img src="{{ '/assets/img/OMX/mountingmedia-effect-on-sample.PNG' | relative_url }}" alt="Comparison of mounting media effects on sample thickness and flatness for SIM imaging" style="max-width: 100%; height: auto; border-radius: 4px;" />
  <p style="font-style: italic; margin-top: 0.5em; font-size: 0.9em;">Effect of different mounting media on sample — hard-set media flatten the sample relative to aqueous media.</p>
</div>

---

## OMX-SR Oil Effect on PSF

<div style="text-align: center; margin: 1.5em 0;">
  <img src="{{ '/assets/img/OMX/OMX_PSF_oil_test_with_beads.png' | relative_url }}" alt="OMX-SR PSF bead test comparing different immersion oils" style="max-width: 100%; height: auto; border-radius: 4px;" />
  <p style="font-style: italic; margin-top: 0.5em; font-size: 0.9em;">PSF bead test on the OMX-SR showing the effect of immersion oil on point spread function quality.</p>
</div>
