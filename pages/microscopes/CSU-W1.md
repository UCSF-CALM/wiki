---
layout: default
title: CSU-W1 Spinning Disk/High Speed Widefield
author: Delaine Larsen
---

# CSU-W1 Spinning Disk/High Speed Widefield

## [FPBASE](https://www.fpbase.org/microscope/rEXNDBCjfs9NtpVz8Z9dfj/)

## Objectives

1. Plan Apo λ 10x / 0.45
2. Plan Apo λ 20x / 0.75
3. Apo LWD 40x / 1.15 WI
4. Plan Apo 60x / 1.27 WI
5. Plan Apo VC 100x / 1.4 Oil
6. Apo TIRF 100x / 1.49 Oil

(only 10x and 20x are installed on Microscope; others are in cabinet)

## Filter Turret (top)

5. Photobleaching / photactivation cube (has an OD2 excitation filter
and a TB 355-405-473 dichroic mirror)

## Filter Turret (bottom)

1. Sedat Quad ([Semrock](http://www.semrock.com/SetDetails.aspx?id=2929))
2. CFP/YFP([Semrock](http://www.semrock.com/SetDetails.aspx?id=2926))
3. Empty
4. Empty
5. Empty
6. Analyzer

## Emission Wheel (for Widefield)

1. Open
2. 440/521/607/700 Multipass
3. 440/40
4. 525/30
5. 607/36
6. 684/34
7. 472/30
8. 542/27
9. 464/547 Multipass

## Emission Wheel (for W1)

1. 447/60
2. 525/50
3. 607/36
4. 685/40
5. empty
6. empty
7. empty
8. empty
9. empty
10. empty


## Dichroics in the W1

1. CSU-W1 Quad Dichroic 405/445/514/785
2. CSU-W1 Penta Dichroic 405/488/561/640/755

## Lasers

- 405 nm 100mW
- 488 nm 150 mW
- 561 100 mW
- 639 160mW
- 785 150mW


## Hardware

- Andor Zyla 5.2 (Right Camera Port)
- Andor Zyla 4.2 (USB3, CSU-W1 left port)
- Andor iXon Ultra DU888 1k x 1k EMCCD (CSU-W1 back port)
- Nikon Ti with PFS3, Stage up with two turrets
- ASI XYZ stage (150 um travel piezo Z; COM8 Baud 115200)
- Lumencor Spectra-X (COM4, Baud 9600) with ESIO AOTF controller (COM5, Baud 57600)
- Sutter Emission Wheel and Lambda 10-B controller (COM9, Baud 128000)
- Sutter TLED, White
- Rapp Optoelectronic UGA-40 photobleaching system (COM6)
- Vortran 405 and 473 nm lasers for photoactivation and photobleaching
- Arduino (BF shutter/Zoom encoder; COM3)
- W1 Spinning Disk with Borealis upgrade (Left Camera Port; COM7, Baud 115200)
- Vortran VersaLase (8) - 5 line laser launch (405-100, 488-150,
 561-100, 639-160 and 785-150 installed, MM 50μm core with 2m fiber and
 FC/PC output)
- TriggerScope (COM10)

### Click title to expand PDFs

<details>
<summary><strong>Triggering a Device from Multiple Cameras (Arduino Setup)</strong> (<a href="{{ '/assets/pdf/microscope/W1/W1 set up-arduino.pdf' | relative_url }}">Download PDF</a>)</summary>

<iframe src="https://docs.google.com/viewer?url={{ site.url }}{{ '/assets/pdf/microscope/W1/W1 set up-arduino.pdf' | relative_url }}&embedded=true" width="100%" height="600px" frameborder="0"></iframe>

</details>

<details>
<summary><strong>Interlocking Multiple Devices on a Microscope</strong> (<a href="{{ '/assets/pdf/microscope/W1/W1-interlocking-multiple devices.pdf' | relative_url }}">Download PDF</a>)</summary>

<iframe src="https://docs.google.com/viewer?url={{ site.url }}{{ '/assets/pdf/microscope/W1/W1-interlocking-multiple devices.pdf' | relative_url }}&embedded=true" width="100%" height="600px" frameborder="0"></iframe>

</details>

<details>
<summary><strong>BNC Breakout Board Images</strong> (<a href="{{ '/assets/pdf/microscope/W1/w1-board-wiringpicitre.pdf' | relative_url }}">Download PDF</a>)</summary>

<iframe src="https://docs.google.com/viewer?url={{ site.url }}{{ '/assets/pdf/microscope/W1/w1-board-wiringpicitre.pdf' | relative_url }}&embedded=true" width="100%" height="600px" frameborder="0"></iframe>

</details>

<details>
<summary><strong>BNC Breakout Board Wiring Diagram</strong> (<a href="{{ '/assets/pdf/microscope/W1/W1 board wiring copy.pdf' | relative_url }}">Download PDF</a>)</summary>

<iframe src="https://docs.google.com/viewer?url={{ site.url }}{{ '/assets/pdf/microscope/W1/W1 board wiring copy.pdf' | relative_url }}&embedded=true" width="100%" height="600px" frameborder="0"></iframe>

</details>



## Firmware / Software

- Ti firmware v5.0 (Combination N)
- Ti Driver v2.0.5.1
- TiControl v4.4.1
- Micro Manager 2.0 (how to cite Micro
 Manager: https://micro-manager.org/Citing_Micro-Manager)
 - Current build Nightly build: 2025-06-10

## PC

- Asus Prime X299-A
- Windows 10 64-bit
- Core i9 3.3GHz
- 64 GB RAM
- NVidia GeForce RTX2080
- Samsung 970 EVO Plus 2000Gb M.2 NVMe x 4 22x80 SSD (Fast Data)
- HGST 0F27452 DC HC510 ISE 10,000gb 7200rpm 256mb Cache SATA 6.0Gb/s
 (Data)

- Micron 5300 PRO 960gb SSD


## Photobleaching

Open the Projector plugin in Micro-mananger to control the
photobleaching system. Instructions on using the Projector plugin [are
here](https://www.micro-manager.org/wiki/Projector "https://www.micro-manager.org/wiki/Projector"). To control the laser powers, open the Vortran control
panel. To calibrate either laser, you can use an 0.01 mg/ml fluorescein
solution, imaged in the FITC channel. A bottle of this solution is in
the cabinet. Right now there is no way to save the calibration, so if
you switch lasers you\'ll need to recalibrate.

For photoconverting mEos2, using the correct laser power is critical. If
the laser power is too high, the protein will bleach instead of
photoconverting. With the current OD2 filter, a 405 nm power of 50 mW
works well (once we switch to an OD1 filter, use 5 mW). The Rapp unit
ignores the spot dwell time parameter; to control how long the area is
converted, adjust the loop parameter. For the laser power above, 10
loops gives good photoconversion and is still relatively rapid (\~1s for
areas of a few μm^2^ at 100x). For bleaching GFP you\'ll need to use
higher power.

Laser powers measured out of 10x objective, each laser at 50 mW power
(no ND filter in)



## Quickstart Guide

### Click title to expand PDFs

<details>
<summary><strong>FRAP Guide</strong> (<a href="{{ '/assets/pdf/microscope/W1/FRAP Set up W1-v2.pdf' | relative_url }}">Download PDF</a>)</summary>

<iframe src="https://docs.google.com/viewer?url={{ site.url }}{{ '/assets/pdf/microscope/W1/FRAP Set up W1-v2.pdf' | relative_url }}&embedded=true" width="100%" height="600px" frameborder="0"></iframe>

</details>

