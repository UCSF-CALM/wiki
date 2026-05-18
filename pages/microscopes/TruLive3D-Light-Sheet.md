---
layout: default
title: TruLive3D Light Sheet
author: Herrington, Kari
date: Jun 13, 2025
---

# TruLive3D Light Sheet

## Optics
### Objectives

| Position | Objective | Pixel Size |
|---|---|---|
| 1. | Two Nikon CFI Plan Fluor 10x W 0.3 NA water immersion objective lens for illumination | |
| 2. | One Nikon CFI Apo 25x (eff. 50x) W 1.1 NA water immersion objective lens for detection | |

Tube lens Magnifier for detection objective

1. 0.5 x = Effective Magnification 12.5 x
2. Â 1 xÂ  = Effective Magnification 25 x
3. Â 1.5 xÂ  = Effective Magnification 37.5 x
4. Â 2 x Â  = Effective MagnificationÂ  50 x

### Excitation Wavelengths:

- For light sheet
 - 405nm
 - 488nm
 - 515nm
 - 561nm
 - 642nm
 - 685nm
- For Ablation
 - 532 Pulsed CryLas

### Transmission Light

- 880 LED for Bright field

### Emission Filter Short Camera

1. BP 418-462 = Chroma ET 440/40
2. LP 498 = Semrock 488LP
3. BP 497-554 = Semrock 525/50
4. BP 526-564 = Chroma ET 545/40
5. BP 580-627 = Chroma ET 605/50
6. BP 610-629 = Semrock 620/14

### Emission Filter Long Camera

1. LP 498 = Semrock 488LP
2. BP 497-554 = Semrock 525/50
3. BP 526-564 = Chroma ET 545/40
4. BP 580-627 = Chroma ET 605/50
5. BP 610-629 = Semrock 620/14
6. BP 655-704Â  = Semrock Brightline 679/41
7. LP 656 =Â  Chroma 655 LP
8. LP 696 = Chroma 700LP
9. BP 710-749 = Semrock 730/39


### Dichroics between cameras

1. Â 500LP Camera splitting dichroic
 1. Splits emission light longer than 500 to one\
 Â camera and shorter than 500nm to a second camera

2. Â 565LP Camera splitting dichroic
 1. Â Splits emission light longer than 565 to one\
 Â camera and shorter than 565nm to a second camera.

3. 640LP Camera splitting dichroic
 1. Â Splits emission light longer than 640 to one\
 Â camera and shorter than 640nm to a second camera.

<details>
<summary><strong>ðŸ“„ Dichroic Diagram</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/Trulive/Dichroic Diagram.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/Trulive/Dichroic Diagram.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Hardware

- Hamamatsu Fire sCmossCamera x2
- Â MEMS-Based Steering Module for Advanced Beam Control and Destriping
- Â Dispersion-free iris-based beam expander module (Tag lens)
- Â Temperature control for the MuVi or InVi SPIM sample chamber with gas
 mixer (Ibidi) for full\
 Â control of gas composition (CO2, O2, humidity). Range 18 -- 40Â°C
 - Currently set up for CO2 only
- Luxendo MuVi SPIM Laser Switcher
 - Â Switches visible lasers between the light sheet optics and\
 Â photomanipulation module.

- Â Ablation Photomanipulation unit for a MuVi SPIM

### Lasers

- 405 nm CW diode laser, 40mW before fiber
- 488 nm CW diode laser, 40mW before fiber
- 515 nm CW diode laser, 40mW before fiber
- 561 nm CW diode laser, 40mW before fiber
- 642 nm CW diode laser, 40mW before fiber
- 685 nm CW diode laser, 40mW before fiber
- Pulsed 532nm VIS laser, 1.5ns pulse length\
 Â Diffraction-limited focal size

Neutral density filters for lasers

- 1%
- 10%
- 100%

### PC

- Win pro 11 Verxion 23H2
- AMD Thred Ripper Pro 5955X 16-Cored 4.0 Ghz
- 256 RAM
- C: Drive (SSD) 1TB
- Data Drive 30TB, micron MTFDKCC30T7TGH-1BC1ZABYY, R/W speed 7000 MB/s

### Software

- Lux control 5.01


### Data Handling

The Data is big! make sure to get on our server, visit the [Data Storage
and Compute](../data-analysis/Data-Storage-and-Compute.html) page

[Python scripts page for
Luxendo](../data-analysis/Python-Scripts-for-TruLive.html)

[Luxendo Image Git
Hub](https://github.com/Luxendo/luxendo-image)

Read here for the Data structure and opening:

## Documentation

### Manual

<details>
<summary><strong>ðŸ“„ TruLive Manual</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/Trulive/TreLiveManual.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/Trulive/TreLiveManual.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

### Photo Manipulation

<details>
<summary><strong>ðŸ“„ Photomanipulation</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/Trulive/Photomanipulation.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/Trulive/Photomanipulation.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>ðŸ“„ Luxendo Photomanipulation</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/Trulive/LuxendoPhotomanipulation.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/Trulive/LuxendoPhotomanipulation.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>

<details>
<summary><strong>ðŸ“„ CryLas Photomanipulation</strong></summary>
<div class="embed-container">
<iframe src="{{ '/assets/pdf/microscope/Trulive/Crylas-Photomanipulation.pdf' | relative_url }}" width="100%" height="600px" style="border: none;"></iframe>
</div>
<p><a href="{{ '/assets/pdf/microscope/Trulive/Crylas-Photomanipulation.pdf' | relative_url }}" target="_blank">Open PDF in new tab</a></p>
</details>