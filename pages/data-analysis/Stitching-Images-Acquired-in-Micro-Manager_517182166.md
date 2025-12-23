---
layout: default
title: Stitching Images Acquired in Micro-Manager
author: Delaine Larsen
---

There are a number of programs available for stitching images acquired
in Micro-Manager, or stitching images more generally. For images
acquired from Micro-Manager, the simplest option is to use the
Grid/Collection Stitching Plugin. This is installed by default in the
[FIJI](http://fiji.sc "http://fiji.sc"){.external-link rel="nofollow"}
distribution. The major disadvantage to this program that I am aware of
is that it will not stitch images larger than 2 gigapixels. This
corresponds to about 400 images acquired on the High-Speed Microscope
(or 500 when using the 2048 x 2048 ROI). The exact number depends on the
overlap between images and whether you are using the full FOV of the
camera or an ROI.

## Protocol

### Acquiring a grid of images in Micro-Manager

For stitching to work, images must be saved in the image stack format,
with each image saved in a separate stack (Tools → Options → Save XY
positions in separate Image Stack Files).

The easiest way to acquire a grid of images is by using the Create Grid
option in the Multi-Dimensional acquisition GUI. To access it:

1.  Open up Multi-Dimensional Acquisition in Micro-Manager.

2.  Click the Edit position list button.

3.  Click the Create Grid button.

4.  Move to the left edge of your sample and click the left-most set
    button.

5.  Repeat this procedure for the other three edges of your sample.

6.  Set the overlap (5-20% seems to work well).

7.  Acquire your data (make sure to save in Image stack format).

8.  You may want to use the MultiChannelShading plugin to flat-field
    correct your images.

### Stitching images using the Grid/Collection Stitching plugin in Fiji

1.  The Grid/Collection Stitching Plugin is located in Plugins →
    Stitching → Grid/Collection Stitching.

2.  In the first dialog box, select Type: "Positions from file" and
    Order: "Defined by image metadata"

3.  In the second dialog box select the first position in your grid for
    "Multi series file".

4.  Do you need to check one of the invert Coordinates boxes?

    1.  For data acquired on high-speedspeed microscope, check "Invert Y
        Coordinates".

    2.  For data acquired on the spinning disk confocal, check "Invert X
        Coordinates" and "Invert Y Coordinates".

    3.  For data acquired on the CSU-W1 spinning disk confocal, check
        "Invert X Coordinates".

    4.  For data acquired on the light sheet microscope, check "Invert X
        Coordinates".

    5.  For data acquired on the Weill CSU-W1/SoRa, you DO NOT need to
        invert coordinats

5.  Otherwise, the default options usually work well.

6.  Hit OK, and you should have your stitched image in a few minutes.

7.  This works for single channel and multicolor Z-stack images.

## Other Stitching Options

For images bigger than 2 gigapixels, or if this doesn\'t work for you
for some other reason, a number of other stitching programs have been
published. I\'ve listed a few here:

- [Microsoft Image Composite Editor
  (ICE)](http://research.microsoft.com/en-us/um/redmond/groups/ivm/ice/ "http://research.microsoft.com/en-us/um/redmond/groups/ivm/ice/"){.external-link
  rel="nofollow"}. This was developed for stitching panoramas acquired
  on digital SLR, but has a motion model (Planar Motion 1) for images
  acquired by X-Y translation. It has no limit to the size of the image
  that can be stitched, but cannot stitch 3D images or data other than
  grayscale or RGB images. For large 2D stitching projects, however, it
  works well. To use it, you will want to save your images as one image
  per position. You will want to know the number of images acquired in
  the X and Y directions. Use "New Structured Panorama" to load your
  images, specify the order they were acquired in, select "Planar Motion
  1" for the camera motion, and it will do the rest.

- [TrakEM2](http://www.ini.uzh.ch/~acardona/trakem2.html), part of Fiji, is supposed to do stitching. I have not
  tested it extensively.

- [Terastitcher](http://abria.github.io/TeraStitcher/){.external-link
  rel="nofollow"} can stitch 2D and 3D images and has no size
  limitations for stitching, however it cannot save stitched images
  larger than 2 gigapixels. I have not tested it extensively.

- [iStitch](https://code.google.com/p/vaa3d/wiki/imageStitch "https://code.google.com/p/vaa3d/wiki/imageStitch"){.external-link
  rel="nofollow"}, a plugin for Vaa3D. I have not tested it.

- [XuvTools](http://www.xuvtools.org/ "http://www.xuvtools.org/"){.external-link
  rel="nofollow"} does 3D stitching but not 2D stitching. No size
  limitations on stitching. I have not tested it.

- [Photoshop](http://help.adobe.com/en_US/photoshop/cs/using/WSfd1234e1c4b69f30ea53e41001031ab64-75e8a.html "http://help.adobe.com/en_US/photoshop/cs/using/WSfd1234e1c4b69f30ea53e41001031ab64-75e8a.html"){.external-link
  rel="nofollow"} has an image stitching option, as do several other
  image manipulation programs. I haven\'t tried any of these.

## References

1.  [Preibisch S. et al. Globally optimal stitching of tiled 3D
    microscopic image acquisitions. Bioinformatics 2009
    25(11):1463-5.](http://www.ncbi.nlm.nih.gov/pubmed/19346324 "http://www.ncbi.nlm.nih.gov/pubmed/19346324"){.external-link
    rel="nofollow"}

2.  [Bria A. and Iannello G. TeraStitcher - a tool for fast automatic
    3D-stitching of teravoxel-sized microscopy images. BMC
    Bioinformatics 2012
    13:316.](http://www.ncbi.nlm.nih.gov/pubmed/23181553 "http://www.ncbi.nlm.nih.gov/pubmed/23181553"){.external-link
    rel="nofollow"}

3.  [Emmenlauer M et al. XuvTools: free, fast and reliable stitching of
    large 3D datasets. J. Microsc. 2009
    233(1):42-60.](http://www.ncbi.nlm.nih.gov/pubmed/19196411 "http://www.ncbi.nlm.nih.gov/pubmed/19196411"){.external-link
    rel="nofollow"}