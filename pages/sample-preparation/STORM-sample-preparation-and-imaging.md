---
layout: default
title: STORM sample preparation and imaging
author: Delaine Larsen
---

# STORM sample preparation and imaging

This page is intended to be a repository of useful information for STORM
sample preparation and imaging.

## Factors to consider in setting up a STORM experiment


### Labeling Method

- Fluorescent proteins, SNAP-tags, other genetically encodable
 molecules.

- Indirect immunofluorescence: The added bulk of two antibodies attached
 to your protein of interest has been shown to degrade the effective
 resolution.

- Direct immunofluorescence: Direct immunofluorescence, ideally with Fab
 fragments or nanobodies, results in your dyes being much closer to
 your protein of interest and thereby giving higher resolution images.

- Vital dyes: Mitotracker, ER-tracker, and DiI, among others, have
 recently been shown to photoswitch. See Shim et. al. 2012.

### Dye Choice

Any dye which can be switched from an off state to an on state can be
used for super-resolution imaging by localization microscopy. This has
led to a large number of different experimental designs in the
literature. Here we highlight a few commonly used approaches.

- Photoactivatible fluorescent proteins: This is the method that was
 originally described as PALM and FPALM. A fluorescent protein that can
 be switched from off to on or from green to red is used. One of the
 most commonly used proteins is mEos or tdEos, but a large number of
 photoswitchable and photoconvertible proteins can be used. We have put
 together [a table of some of the more commonly used fluorescent
 proteins for
 superresolution](Fluorescent-Proteins-for-Localization-Microscopy.html).

- Stochastic switching of small molecule dyes: often called direct STORM
 (dSTORM) or GSDIM (ground-state depletion with individual molecule
 return). High power excitation of a number of small molecule dyes in a
 buffer containing an oxygen scavenging system and a thiol results in
 there reversible conversion to a dark state. This then stochatically
 return to the emitting state and are localized. Typically they cycle
 between the on and off states many times before photobleaching.
 Alexa647 or Cy5 have the best performance in this imaging modality,
 but Atto488 and Cy3B can be used for multicolor imaging. The paper by
 Dempsey et al. extensively characterizes 26 dyes in this imaging
 modality.

- Combined reporter/activator dyes: classic STORM imaging. This uses the
 Alexa647 reporter above, but instead of waiting for spontaneous return
 from the dark state, it is paired with an activator dye (typically
 Alexa405, Alexa488, or Alexa568). Excitation of the activator dye
 triggers the return of nearby Alexa647 molecules to the on state.
 Using this method requires labeling your own antibodies with the
 activator/reporter combination.

- Caged / Photoswitchable small molecule dyes: Stefan Hell\'s group has
 developed sets of caged dyes and photoswitchable dyes that start in a
 non-fluorescent state but that can be converted to a fluorescent state
 (see papers below). These are commercially available from
 [Abberior](https://abberior-labels.com/products/cage/).

### Sample Prep

In order to collect good STORM imaging data sample prep is key. Below
are important aspects to optimize and consider.

- Fixation protocol. Proper fixation to preserve sample ultrastructure
 is critical for good super-resolution imaging. A recent paper
 characterized the effect of different fixation protocols on STORM
 image quality and has optimized protocols for the best image quality.
 See [Whelan et al.
 2015](http://www.nature.com/articles/srep07924 "http://www.nature.com/articles/srep07924").

<!-- -->

- Signal-to-Noise Ratio: High background and/or weak signal makes it
 significantly harder to obtain molecule localizations.

 - Optimize your fixation and staining to reduce background and
 increase signal. The use of techniques such as reduction with Sodium
 Borohydride can greatly reduce some of the autofluorescence
 associated with fixation

 - Pick the best dye/protein to do the job. The paper by Dempsey et al.
 (see link below) characterizes 26 dyes, make sure the dye you have
 picked will work well for your application.

<!-- -->

- Dishes vs. Slides: If at all possible we recommend that you prepare
 your samples for imaging in glass-bottomed petri dishes.

 - Allows for easy exchange of imaging buffer. In order to use
 stochastic switching of small molecule dyes for STORM imaging a
 special imaging buffer is required (see protocols below) that needs
 to be added fresh right before imaging.

 - Allows for the use Perfect Focus to help prevent z-drift during
 imaging.

## Protocols

- [These protocols for GSDIM sample prep from Leica may also be
 useful.](http://www.leica-microsystems.com/science-lab/sample-preparation-for-gsdim-localization-microscopy-protocols-and-tips/ "http://www.leica-microsystems.com/science-lab/sample-preparation-for-gsdim-localization-microscopy-protocols-and-tips/")

<details>
<summary><strong>📄 Nikon N-STORM Sample Preparation Manual</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/nikon_storm_sample_preparation.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/nikon_storm_sample_preparation.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

## References

Heilemann M, van de Linde S, Schüttpelz M, Kasper R, Seefeldt B,
Mukherjee A, Tinnefeld P, Sauer M. Subdiffraction-resolution
fluorescence imaging with conventional fluorescent probes. Angew Chem
Int Ed Engl. 2008;47(33):6172-6. The paper describing dSTORM.

<details>
<summary><strong>📄 Heilemann - dSTORM</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/Heilemann-dstorm.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/Heilemann-dstorm.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Fölling J, Bossi M, Bock H, Medda R, Wurm CA, Hein B, Jakobs S,
Eggeling C, Hell SW. Fluorescence nanoscopy by ground-state depletion
and single-molecule return. Nat Methods. 2008 Nov;5(11):943-5. The paper describing GSDIM.

<details>
<summary><strong>📄 Fölling - GSDIM</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/Fölling-gsdim.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/Fölling-gsdim.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Lana Lau, Yin Loon Lee, Steffen J. Sahl, Tim Stearns, and W. E.
Moerner. STED Microscopy with Optimized Labeling Density Reveals 9-Fold
Arrangement of a Centriole Protein. Biophysical Journal. 2012 June
102:2926--2935. This paper has a nice test of the effect of antibody labeling density on image resolution using STED microscopy.

<details>
<summary><strong>📄 Lau & Moerner - STED Labeling</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/Lau-moerner_sted_labeling.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/Lau-moerner_sted_labeling.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Ries J, Kaplan C, Platonova E, Eghlidi H, Ewers H. A simple, versatile
method for GFP-based super-resolution microscopy via nanobodies. Nat
Methods. 2012 Apr 29. This paper demonstrates the use of a single chain antibody (nanobody) against GFP for STORM imaging of
GFP tagged proteins, by binding an Alexa 647 labeled nanobody to
GFP-tagged proteins. The nanobody is commercially available from here:
[http://www.chromotek.com/](http://www.chromotek.com/)

<details>
<summary><strong>📄 Ries - GFP Nanobody STORM</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/Ries-gfpnanobody_storm.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/Ries-gfpnanobody_storm.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Lew MD, Lee SF, Ptacin JL, Lee MK, Twieg RJ, Shapiro L, Moerner WE.
Three-dimensional superresolution colocalization of intracellular
protein superstructures and the cell surface in live Caulobacter
crescentus. Proc Natl Acad Sci U S A. 2011 Nov 15;108(46):E1102-10. A localization microscopy
experiment combining single molecule blinking of eYFP and localization
of Nile Red by random insertion of the dye into the membrane at very low
concentration.

<details>
<summary><strong>📄 Lew - SpRaiPaint</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/Lew-spraipaint.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/Lew-spraipaint.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Jones SA, Shim SH, He J, Zhuang X. Fast, three-dimensional
super-resolution imaging of live cells. Nat Methods. 2011
Jun;8(6):499-508. This paper demonstrates fast STORM imaging of live cells; it also compares the performance of a
number of photoswitchable dyes and mEos2 and tdEos.

<details>
<summary><strong>📄 Jones 2011 - Fast STORM</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/jones2011faststorm.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/jones2011faststorm.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Fluorescent Proteins

Shroff H, Galbraith CG, Galbraith JA, White H, Gillette J, Olenych S,
Davidson MW, Betzig E. Dual-color superresolution imaging of genetically
expressed probes within individual adhesion complexes. Proc Natl Acad
Sci U S A. 2007 Dec 18;104(51):20308-13. This paper describes a number of
methods for two-color PALM imaging using genetically encoded fluorescent
proteins.

<details>
<summary><strong>📄 Shroff 2007 - Dual-color PALM</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/shroff2007.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/shroff2007.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Lippincott-Schwartz J, Patterson GH. Photoactivatable fluorescent
proteins for diffraction-limited and super-resolution imaging. Trends
Cell Biol. 2009 Nov;19(11):555-65. A nice review of
photoactivatible fluorescent proteins for localization microscopy as of 2009.

<details>
<summary><strong>📄 Lippincott-Schwartz - Photoactivatable FPs</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/Lippincott-schwartz-jls_ticb.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/Lippincott-schwartz-jls_ticb.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Whelan DR, Bell TD. Image artifacts in Single Molecule Localization
Microscopy: why optimization of sample preparation protocols matters.
Scientific Reports. 2015. 10.1038/srep07924. A critical exploration of how
sample preparation affects image quality. Has optimized fixation
protocols for STORM imaging.

<details>
<summary><strong>📄 Whelan & Bell 2014 - Sample Prep Optimization</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/sci_rep_2014_whelan_dr.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/sci_rep_2014_whelan_dr.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Single Dye Imaging

Dempsey GT, Vaughan JC, Chen KH, Bates M, Zhuang X. Evaluation of
fluorophores for optimal performance in localization-based
super-resolution imaging. Nat Methods. 2011 Nov 6;8(12):1027-36. This paper directly compares the
performance of 26 different dyes for single dye localization microscopy
(dSTORM). An excellent resource for choosing dyes for multicolor
imaging.

<details>
<summary><strong>📄 Dempsey - Evaluation of Fluorophores</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/dempsey_evaluation.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/dempsey_evaluation.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Caged / Photoswitchable Dyes

Belov VN, Wurm CA, Boyarskiy VP, Jakobs S, Hell SW. Rhodamines NN: a
novel class of caged fluorescent dyes. Angew Chem Int Ed Engl. 2010 May
3;49(20):3520-3.

<details>
<summary><strong>📄 Belov 2010 - Rhodamines NN Caged Dyes</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/belov2010.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/belov2010.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Belov VN, Bossi ML, Fölling J, Boyarskiy VP, Hell SW. Rhodamine
spiroamides for multicolor single-molecule switching fluorescent
nanoscopy. Chemistry. 2009 Oct 19;15(41):10762-76.

<details>
<summary><strong>📄 Belov 2009 - Rhodamine Spiroamides</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/belov2009.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/belov2009.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Other Dyes

Shim SH, Xia C, Zhong G, Babcock HP, Vaughan JC, Huang B, Wang X, Xu C,
Bi GQ, Zhuang X. Super-resolution fluorescence imaging of organelles in
live cells with photoswitchable membrane probes. Proc Natl Acad Sci U S
A. 2012 Aug 28;109(35):13978-83. This paper demonstrates that a
number of commonly used vital dyes, including DiI and dyes from the
Mito-tracker, ER-tracker, and Lyso-tracker families, photoswitch and can
be used for localization microscopy.

<details>
<summary><strong>📄 Shim et al. 2012 - Photoswitchable Membrane Probes</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/shim_et_al_2012.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/shim_et_al_2012.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Multicolor Imaging

Bates M, Huang B, Dempsey GT, Zhuang X. Multicolor super-resolution
imaging with photo-switchable fluorescent probes. Science. 2007 Sep
21;317(5845):1749-53. Multi-color STORM imaging using
dye-pair labeled antibodies.

<details>
<summary><strong>📄 Bates et al. 2007 - Multicolor STORM</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/bates_et_al_2007.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/bates_et_al_2007.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Dani A, Huang B, Bergan J, Dulac C, Zhuang X. Superresolution imaging
of chemical synapses in the brain. Neuron. 2010 Dec
9;68(5):843-56. Describes using three color STORM
imaging to localize proteins within synapses in 10 um brain sections.

<details>
<summary><strong>📄 Dani & Huang - Synapse STORM</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/dani_huang_synapse_storm.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/dani_huang_synapse_storm.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Testa I, Wurm CA, Medda R, Rothermel E, von Middendorf C, Fölling J,
Jakobs S, Schönle A, Hell SW, Eggeling C. Multicolor fluorescence
nanoscopy in fixed and living cells by exciting conventional
fluorophores with a single wavelength. Biophys J. 2010 Oct
20;99(8):2686-94. Three color imaging of Alexa
488, Alexa 514, Atto 532, and Cy3 in PVA-embedded samples at the
relatively high laser power of 10 kW/cm2.

<details>
<summary><strong>📄 Testa et al. 2010 - Multicolor Nanoscopy</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/testa_et_al_2010.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/testa_et_al_2010.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Vaughan JC, Jia S, Zhuang X. Ultrabright
photoactivatable fluorophores created by reductive caging. Nat Methods.
2012 Oct 28. doi: 10.1038/nmeth.2214. Conversion of Atto488, Cy3,
Cy3B, Alexa647, and Cy5.5 to a dark stage that can be photoactivated by
UV illumination.

<details>
<summary><strong>📄 Vaughan - Reductive Caging</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/Vaughan-reductivecaging.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/Vaughan-reductivecaging.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Reviews

Fernández-Suárez M, Ting AY. Fluorescent probes for super-resolution
imaging in living cells. Nat Rev Mol Cell Biol. 2008
Dec;9(12):929-43.

<details>
<summary><strong>📄 Fernández-Suárez & Ting 2008 - Fluorescent Probes Review</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/fernandez-suarez_and_ting_2008_nat_rev.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/fernandez-suarez_and_ting_2008_nat_rev.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Huang B, Babcock H, Zhuang X. Breaking the diffraction barrier:
super-resolution imaging of cells. Cell. 2010 Dec
23;143(7):1047-58.

<details>
<summary><strong>📄 Huang - Super-Resolution Review</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/huang_review.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/huang_review.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Moerner WE. Microscopy beyond the diffraction limit using actively
controlled single molecules. J Microsc. 2012
Jun;246(3):213-20.

<details>
<summary><strong>📄 Moerner - Microscopy Beyond Diffraction Limit</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/moerner.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/moerner.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

Manley S, Gunzenhäuser J, Olivier N. A starter kit for
point-localization super-resolution imaging. Curr Opin Chem Biol. 2011
Dec;15(6):813-21.

<details>
<summary><strong>📄 Manley - Point-Localization Super-Resolution Review</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/manley_review.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/manley_review.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

van de Linde S, Sauer M. How to switch a fluorophore: from undesired
blinking to controlled photoswitching. Chem Soc Rev. 2013 Aug 13.

<details>
<summary><strong>📄 van de Linde & Sauer 2013 - How to Switch a Fluorophore</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/papers/storm/lindesauer2013.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/papers/storm/lindesauer2013.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

[Dempsey, Wang, and Zhuang. Fluorescence Imaging at
Sub-Diffraction-Limit Resolution with Stochastic Optical Reconstruction
Microscopy. In Handbook of Single-Molecule Biophysics, Hinterdorfer and
Van Oijen,
eds.](http://books.google.com/books?id=pT3WaiL5YNkC&pg=PA96&dq=storm+microscopy&hl=en&sa=X&ei=pLbfT4nuJoq42wWr_tCyCg&ved=0CEcQ6AEwAg#v=onepage&q&f=false)
