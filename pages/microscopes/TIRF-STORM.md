---
layout: default
title: TIRF/N-STORM
author: Delaine Larsen
---

# TIRF/N-STORM

## [FPBASE](https://www.fpbase.org/microscope/JFEfwYnD6RpAZyTgh2PNkj/)

## Optics
### Objectives

1. Plan Fluor 10x /0.3 (Ph1) 1600 nm/pixel
2. Plan Apo 20x/0.75 (DIC N2 / 20X) 785 nm/pixel
3. Empty
4. Plan Apo VC 60XA/1.20 Water
5. Plan Apo lambda 100x/1.45 TIRF Oil 157 nm/pixel
6. Apo TIRF 100x/1.49 Oil (DIC N2 / 100X I) 157 nm/pixel

### Filter Turret 1 (FL1)

1. Empty
2. Analyzer
3. Quad N-STORM
4. DAPI/FITC/Rhodamine Triple (for eyepiece viewing with arc lamp)
5. CFPHQ
6. DAPI

### Filter Turret 1 (FL2)

1. FRAP cube-Longpass dichroic for reflecting 473 and 405 to sample
 plane (T495lpxr-UF2)

2. Empty
3. Empty
4. Empty
5. Empty
6. Empty

### Emission Wheel (Andor Du897)

1. ET455/50m
2. ET525/50m
3. ET600/60m
4. ET705/72m
5. ZET488/561/640m (triple bandpass)
6. DualBP 59012m (515/30m, 598/45m)
7. ZET405/488m-TRF
8. Empty
9. Blocker
10. Blocker


### Emission Wheel (Hamamatsu)

1. Blocker
2. ZET405/488/561/640m (quadruple bandpass)
3. ET455/50m
4. ET525/50m
5. ET600/60m
6. ET705/72m
7. Empty
8. Empy
9. Empty
10. Empty

### Hardware

- Nikon Ti-E Microscope
- ~~Sutter emission wheel and 10-B (COM 5 baud rate auto) ~~
- Sutter Lambda 10-3 Controller
- Nikon motorized stage
- Andor DU897 on right port ~~with 3D STORM lens~~
- Hammamatsu Orca Flash 4 (left port, COM 4)
- Sutter LB 10-N filter Wheel in front of each camera
- Agilent MLC400 (405nm, 488nm, 561nm, 647nm) with NIDAQ interface(v18.oo)
- Brightfield shutter controlled by Sutter Lambda SC through Ti
- FRAP System UGA-42 Firefly
- FRAP lasers diode lasers - 405nm /100mW and 473nm 100mW

### Interface Requirements

- Camera link board- Orca Flash 4 PCIe- 1x-CLD-2PE8
- [CCI-24 ]PCIe[ controller ]card-
 Andor DU897

- [NI PCI 6723 board connected though PXI box -Agilent Lasers MLC
 400B ]
 - [Custom board added for FRAP
 integration]
- USB for Sutter 10-B
- USB Oko lab bold line
- USB - Nikon Ti


### Firmware

- Ti: Combination I
- TiControl: 5.2

### PC

- Intel(R) Xeon(R) W-2245 CPU @ 3.90GHz, 3912 Mhz, 8 Core(s)
- 64 GB RAM
- 64 bit Windows 10 Pro
- NVidia RTX 4000
- 500GB C: Hard drive
- 1TB D: Hard drive (RAID 1)

### Software

- MicroManager 2.0
- how to cite Micro
 Manager: https://micro-manager.org/Citing_Micro-Manager

 ## Information For Imaging

 [STORM resources](STORM-sample-preparation-and-imaging_517184503.html)