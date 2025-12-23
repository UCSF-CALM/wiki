---
layout: default
title: How to Acquire Flat Field correction
author: Delaine Larsen
---

This protocol describes how to capture flat field correction images for
performing shading correction of fluorescence images.

### The Problem

When you acquire a fluorescence image on a microscope, the fluorescence
is not uniform over the field of view. Due to uneven illumination and
detection, some regions of the image, typically the center, are
brighter, and others are dimmer. In addition, there is an offset to the
image - the camera does not read zero when no light hits it - and this
can vary from position to position within the image. Mathematically, our
measured image (I~meas~) is related to the true image (I~true~) by
I~meas~ = Dark + I~true~ \* Flat, where Dark is a dark image and Flat is
a flat field image. We can invert this to get I~true~ = (I~meas~ - Dark)
/ Flat. This correction procedure is implemented in the Micro-manager
[MultiChannelShading](http://www.micro-manager.org/wiki/MultiChannelShading "http://www.micro-manager.org/wiki/MultiChannelShading"){.external-link
rel="nofollow"} plugin, among other places.

### Samples

To acquire flat-field images, we need a uniform fluorescent sample. We
have found that the best results for flat-fielding of widefield images
result from using concentrated dye solutions, as described by Michael
Model
([1](http://www.ncbi.nlm.nih.gov/pubmed/11500847 "http://www.ncbi.nlm.nih.gov/pubmed/11500847"){.external-link
rel="nofollow"},
[2](http://www.ncbi.nlm.nih.gov/pubmed/18770832 "http://www.ncbi.nlm.nih.gov/pubmed/18770832"){.external-link
rel="nofollow"}). In particular we use the following solutions on
inexpensive dyes (links go to suppliers):

- DAPI channel: 50 mg/ml [7-diethylamino 4-methyl
  coumarin](http://www.sigmaaldrich.com/catalog/product/aldrich/d87759?lang=en&region=US){.external-link
  rel="nofollow"} in DMSO

- FITC channel: 100 mg/ml
  [fluorecein](http://www.sigmaaldrich.com/catalog/product/sigma/46960?lang=en&region=US){.external-link
  rel="nofollow"} in water

- Cy3 channel: 100 mg/ml [rose
  bengal](http://www.sigmaaldrich.com/catalog/product/sigma/r4507?lang=en&region=US){.external-link
  rel="nofollow"} in water

- Cy5 channel: 100 mg/ml [acid blue
  9](http://www.tcichemicals.com/eshop/en/us/commodity/B0790/ "http://www.tcichemicals.com/eshop/en/us/commodity/B0790/"){.external-link
  rel="nofollow"} in water

When you make these solutions, it\'s best to centrifuge them and filter
them through an 0.22 μm filter to remove particulate matter than may
make the fluorescence non-uniform.

### Data Acquisition and Analysis

For best results, you should acquire separate flat-field images for each
objective and fluorescence channel. In our experience, these images are
pretty stable if you don\'t realign your microscope, so you shouldn\'t
have to do it that frequently.

These instructions assume you\'re using ImageJ for your analysis. If
you\'re not, it should be straightforward to adapt them to another
program.

First, you must acquire a dark image. This is acquired with no light
reaching the camera. To acquire it:

1.  Set up the microscope so that no light reaches the camera.
    Typically, I set the microscope to use the eyepiece light path.

2.  Set the camera to a short exposure time (10 - 100 msec; the exact
    value is not crucial).

3.  Acquire a time lapse of 100 - 500 images

4.  Calculate the average of these images. This is most easily done by
    opening the image stack in ImageJ and using Image → Stacks →
    Z-project. Select average intensity for projection type.

5.  Save the resulting average image. This is your dark image.

Second, you must acquire flat-field images. To do so:

1.  Prepare a slide of an appropriate flat-field solution by placing a
    drop between a slide and a coverslip.

2.  Mount the slide on the microscope and focus on the solution. If
    there is an air bubble in the solution, it\'s easy to focus on that;
    otherwise you can use the edge of the coverslip to focus on.

3.  Move the microscope objective to a uniform area of the dye, away
    from bubbles and and the coverslip edge.

4.  Acquire many images of the sample in different positions. I
    typically acquire a 9×9 grid of images overlapping by 50%. This
    allows us to average out non-uniformities in the dye solution.

5.  Load the resulting image stack into ImageJ, and use the Z-projection
    tool to calculate a median intensity projection. Choosing the median
    intensity makes this robust to outliers, such as fluorescent dust
    particles. **Important**: the resulting projection will be a 32-bit
    image.

6.  To convert it back to 16-bit, **make sure** that Edit → Options →
    Conversions → Scale when converting is **unchecked**. If not, ImageJ
    will change your intensity values when you do the conversion. Use
    Image → Type → 16-bit to convert back to 16-bit.

7.  Subtract off the dark image. Load the dark image, if it\'s not
    already loaded, and use Process → Image Calculator to subtract the
    dark image from your median flatfield image.

8.  The resulting image is your flatfield image. Save it as a TIFF (or
    other lossless file format).