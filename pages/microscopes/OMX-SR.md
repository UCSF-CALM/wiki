---
layout: default
title: OMX-SR
author: Delaine Larsen
---

# OMX-SR

## [FPBASE](https://www.fpbase.org/microscope/zxVNaRzVxTc8heRDnBPXhW/)

## Optics
### Objectives

1. Plan ApoN 60x/1.42
2. TIRF Apo 60x/1.49

### Cameras and Emission Filters

3 x liquid cooled [pco.edge 5.5 sCMOS
cameras]

- Camera 1: DAPI: 435/31 Cy5: 683/40 DIC
- Camera 2: A488: 528/48
- Camera 3: A568: 609/37

### Lasers

- 405 nm
- 488 nm
- 568 nm
- 640 nm

### Sample holder compatibility

- Standard microscope slides
- 35 mm glass bottom dishes
- Multiwell chambered coverslips

### Interface Requirements


### PC

- Linux Centos 6.8
- Kernel Linux 2.6.32-642.13.1.e16x86_64
- GNOME 2.28.2
- Intel Core i7 2600 CPU
- NVidia NVS300
- Drives 1 TB SATA boot drive\
 RAID 3 × 1 TB SATA in RAID5 configuration

## Notes on usage:

SIM imaging is extremely sensitive to spherical aberration. To get the
highest quality images you need to minimize spherical aberration. This
means:

- You should use [high precision 0.17 mm
 coverslips](High-Precision-Coverslips.html)

- You should mount only a single coverslip in the center of the slide.
- You should mount in an appropriate mounting medium. Fixed samples
 should be mounted in high refractive index mounting media with
 antifade. Be aware that hard-set mounting medium can cause shrinkage
 when it cures. We also recommend that you do not use mounting medium
 which contains DAPI or other fluorophores.

- You should have your sample as close to the coverslip as possible
 (e.g. cells grown on coverslip not on slide).

- You should use bright and stable fluorophores.
- You should select the correct immersion oil for you sample. You can
 use the [GE immersion oil
 calculator](https://www.cytivalifesciences.com/en/us/support/online-tools/cell-imaging-and-microscopy/immersion-oil-calculator/web-app) to determine the best oil to start with. The also have
 the calculator as a phone app.

As a general rule, if the sample doesn\'t look good in widefield or
confocal, SIM imaging will not improve it. You should make every attempt
to optimize your staining and reduce background from out-of-focus
fluorescence for the best results.

## Effect of mounting media on sample:

![mountingmedia-effect-on-sample]({{ '/assets/img/OMX/mountingmedia-effect-on-sample.PNG' | relative_url }})
*mountingmedia-effect-on-sample*

## Oil Effect on beads:

![OMX_PSF_oil_test_with_beads]({{ '/assets/img/OMX/OMX_PSF_oil_test_with_beads.png' | relative_url }})
*OMX_PSF_oil_test_with_beads*


## Documentation

### Application Guides

<details>
<summary><strong>📄 Oil Optimization Application Guide</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMX_AppGuide_OilOpt_29250659AA.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMX_AppGuide_OilOpt_29250659AA.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Quick Reference Guides

<details>
<summary><strong>📄 DLM Acquisition Quick Reference</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMX_QRef1_DLMAcqusition_29156918AB.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMX_QRef1_DLMAcqusition_29156918AB.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>📄 DLM Analysis Quick Reference</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMX_QRef2_DLMAnalysis_29156919AC.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMX_QRef2_DLMAnalysis_29156919AC.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>📄 OMX-SR Acquisition Quick Reference</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMXSR_QRef1_Acq_29159151AB.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMXSR_QRef1_Acq_29159151AB.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>📄 OMX-SR Reconstruction Quick Reference</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMXSR_QRef2_Recon_29159154AB.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMXSR_QRef2_Recon_29159154AB.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### System Information

<details>
<summary><strong>📄 OMX-SR System Information</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMXSR_SI_29159606AA.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMXSR_SI_29159606AA.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>📄 OMX-SR E-Controller</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMXSR_EController_29144496AA.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMXSR_EController_29144496AA.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>📄 Ultimate Focus</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMX_UltimateFocus_04-720181-000_A_01.PDF' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMX_UltimateFocus_04-720181-000_A_01.PDF' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>


<details>
<summary><strong>📄 Ring TIRF</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMX_RingTIRF_04-720166-000_B_01.PDF' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMX_RingTIRF_04-720166-000_B_01.PDF' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Imaging Techniques

<details>
<summary><strong>📄 Image Registration</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMX_ImageReg_04-720165-000CB.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMX_ImageReg_04-720165-000CB.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>📄 Localization</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMX_Localization_04-720170-000AB.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMX_Localization_04-720170-000AB.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>📄 PhotoKinetics</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMX_PhotoKinetics_29093629AB.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMX_PhotoKinetics_29093629AB.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>📄 PhotoKinetics (PK)</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/DVOMX_PK_29093629AB.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/DVOMX_PK_29093629AB.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>


<details>
<summary><strong>📄 FRAP Product Note</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/FRAP_ProductNote.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/FRAP_ProductNote.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### SIM Artifacts & Troubleshooting

<details>
<summary><strong>📄 Common SIM Artifacts (2016)</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/OMX/2016_06_20 Common SIM Artifacts.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/OMX/2016_06_20 Common SIM Artifacts.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

## Getting your Data off the OMX!

- Can I use Box/drop box?
 - NO-As the OMX has gotten older, the Oporating system is nolonger
 compatible with versions of browswers that can run box and drop box
- How does my hard drive need to be formatted?
 - FAT32 or NTFS. **These are the ONLY 2 that will work**
 - Please Note FAT 32 can not handle file sizes larger than 4GB
 - NTFS has limited Read-only capabilities on Mac.




