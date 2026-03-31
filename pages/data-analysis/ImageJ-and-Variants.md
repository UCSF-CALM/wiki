---
layout: default
title: ImageJ and Variants
author: Delaine Larsen
---

# ImageJ and Variants

### Distributions

- [ImageJ](https://imagej.net/) is one of the older free, open source image analysis programs. Alone, it\'s not
that powerful; it\'s real strength is the vast array of plugins for it.
It runs on Windows, Mac, and Linux.

- [FIJI](http://fiji.sc "http://fiji.sc") is probably the best distribution of ImageJ for routine data analysis.
It comes with a vast array of plugins already installed and ready to use and has an automatic updater so you always have the latest versions of them.

- [Micro-Manager](http://www.micro-manager.org/ "http://www.micro-manager.org/") is a microscope control package that is built on top of
ImageJ. It\'s developed at UCSF and is very powerful; we use it to
control the Spinning Disk Confocal in the Nikon Imaging Center.


- A tutorial on getting started with micro-manager:
[http://www.youtube.com/watch?v=y-R9WmhzPdI&feature=related](http://www.youtube.com/watch?v=y-R9WmhzPdI&feature=related)

- A screen cast tutorial on multi dimensional acquisition using
micro-manager:
[http://www.youtube.com/watch?v=6LoKX6Eect0](http://www.youtube.com/watch?v=6LoKX6Eect0)


### Plugins

The following plugins may be of particular interest to our users:

- [Bioformats](https://www.openmicroscopy.org/bio-formats/)- Software tool to open files from a variety of formats.
This plugin will allow you to open nd2 files in ImageJ/FIJI.

- [SIMcheck](https://www.micron.ox.ac.uk/software/SIMcheck/)- Plugin for assessing the quality and reliability of
Structured Illumination Microscopy data. This plugin is useful for
anyone doing SIM imaging to watch for artifacts and other problems with
your data.

- Reference: [Ball, et al. SIMcheck: a Toolbox for Successful
 Super-resolution Structured Illumination Microscopy. Scientific
 Reports 5, Article number: 15915
 (2015)](https://www.nature.com/articles/srep15915)

- [ClearVolume](ClearVolume.html) - 3D volume viewer. the easy
install is listed here along with the quick fix for the rendering
issue.


### Forums

- [Image.sc](https://forum.image.sc/) -
Community forum for multiple open-source image analysis software
packages where you can find answer to common problems and post questions
to the community. The forum is very active and you can get help quickly.

- [Microforum](https://forum.microlist.org/)- Community forum based on hardware, acquisition, and
specimen-related question.


### Macros

Kari\'s 2020 webinar ([box link here](https://urldefense.proofpoint.com/v2/url?u=https-3A__ucsf.box.com_v_IntroToMacros-2D20200402&d=DwMF-g&c=iORugZls2LlYyCAZRB3XLg&r=rWHGLgGRKCB9UJ_3gjETqRC0fXrJ1iZZJnwLO8_WuLc&m=t8wrlXRnTmwCXxNw3nIiR2nwA4ltf57v82_DnEO1xRA&s=F_OfLx-5hsc3D_FP_XiIQPOKckz4sykfUznFpqe3IjY&e=)) has a basic introduction to macros. Below are some Basic Macro\'s that were written  and last run on in Fiji, ImageJ v
1.53f51, Java 1.81-172 (64-bit).

To open: Download then drag and drop onto ImageJ/Fiji Tool Bar

<details>
<summary><strong>🔧 SaveLIFseries.ijm</strong> — Batch convert LIF files to OME.tif</summary>
<pre><code>/*this is a macro for batch processing LIF files in to ome.tif files.
 * Instructions:
 * Put your LIF files you want to convert into a folder. This is your Input/source directory
 * Create a folder for your files to be out put to. This is your output/destination directory
 * If you want to run any processes on the images while you are converting them you can change the code below where indicated.
 * When you are readt, click "Run"
 * It will prompt you to select your input folder, choose it and click select
 * It will then prompt you to click your output folder, choose it and click select
 * It should run and process all your files
*/
run("Bio-Formats Macro Extensions");
setBatchMode(true);

currentDirectory = getDirectory("Choose a Source Directory");
outputDirectory = getDirectory("Select Destination");

fileList = getFileList(currentDirectory);

for (file = 0; file &lt; fileList.length; file++) {
    Ext.isThisType(currentDirectory + fileList[file], supportedFileFormat);
    if (supportedFileFormat=="true") {
        Ext.setId(currentDirectory + fileList[file]);
        Ext.getSeriesCount(seriesCount);
        for (series = 1; series &lt;= seriesCount; series++) {
            run("Bio-Formats Importer", "open=[" + currentDirectory + fileList[file] + "] autoscale color_mode=Composite rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_"+series);
            name=getTitle();
            run("Bio-Formats Exporter", "save=[" + outputDirectory + name + ".ome.tif" + "] compression=Uncompressed");
            close();
        }
    } else if (endsWith(fileList[file], "/")) {
        processBioFormatFiles(currentDirectory + fileList[file]);
    }
}

setBatchMode(false);</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/Macros/561967062.ijm' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/Macros/561967062.ijm' | relative_url }}" download><strong>⬇ Download Macro</strong></a>
</p>
</details>

<details>
<summary><strong>🔧 ConvertND2-ColorOME.ijm</strong> — Convert BF Color RGB ND2 to OME.tif and reorder channels</summary>
<pre><code>// batchTiffConvert.txt

/*This converts BF Color RGB ND2 Files into BF Color RGB TIF files and re orders the channels
 * because NIS elements writes the colors in a Differnt header order than Fiji
*/
oneFilePerSlice = false;

directory = getDirectory("Input files");
fileList = getFileList(directory);
outputDirectory = getDirectory("Output directory");

run("Bio-Formats Macro Extensions");
setBatchMode(true);

for (i=0; i&lt;fileList.length; i++) {
  file = directory + fileList[i];
  if (oneFilePerSlice) {
    Ext.setId(file);
    Ext.getImageCount(imageCount);
    for (image=0; image&lt;imageCount; image++) {
      Ext.openImage("", image);
      outFile = outputDirectory + fileList[i] + "-" + image + ".ome.tiff";
      saveFile(outFile);
      close();
    }
    Ext.close();
  } else {
    Ext.openImagePlus(file);
    outFile = outputDirectory + fileList[i] + ".ome.tiff";
    saveFile(outFile);
    close();
  }
}

showStatus("Finished.");
setBatchMode(false);

function saveFile(outFile) {
    Stack.setChannel(1); run("Blue");
    Stack.setChannel(2); run("Green");
    Stack.setChannel(3); run("Red");
    run("Make Composite");
    run("RGB Color");
    name=getTitle();
    s=lastIndexOf(name, '.');
    name=substring(name, 0,s);
    run("Bio-Formats Exporter", "save=[" + outputDirectory + name + ".ome.tif" + "] compression=Uncompressed");
}
close();</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/Macros/561967066.ijm' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/Macros/561967066.ijm' | relative_url }}" download><strong>⬇ Download Macro</strong></a>
</p>
</details>

<details>
<summary><strong>🔧 ConvertND2toOMEremoveND2.ijm</strong> — Convert ND2 folder to OME.tif and strip file suffix</summary>
<pre><code>/*This converts a folder full of images (your input folder) into OME.tifs and puts them in a new output folder.
 * It is also set up to remove the suffix (i.e. ".ND2") from the image name just to clean it up a bit.
*/

oneFilePerSlice = false;

directory = getDirectory("Choose input files");
fileList = getFileList(directory);
outputDirectory = getDirectory("Choose output directory");

run("Bio-Formats Macro Extensions");
setBatchMode(true);

for (i=0; i&lt;fileList.length; i++) {
  file = directory + fileList[i];
  if (oneFilePerSlice) {
    Ext.setId(file);
    Ext.getImageCount(imageCount);
    for (image=0; image&lt;imageCount; image++) {
      Ext.openImage("", image);
      name = fileList[i];
      s=lastIndexOf(name, '.');
      name=substring(name, 0,s);
      name=replace(name,".","_");
      outFile = outputDirectory + name + "-" + ".ome.tif";
      saveFile(outFile);
      close();
    }
    Ext.close();
  } else {
    Ext.openImagePlus(file);
    name = fileList[i];
    s=lastIndexOf(name, '.');
    name=substring(name, 0,s);
    name=replace(name,".","_");
    outFile = outputDirectory + name + "-" + ".ome.tif";
    saveFile(outFile);
    close();
  }
}

showStatus("Finished.");
setBatchMode(false);

function saveFile(outFile) {
   run("Bio-Formats Exporter", "save=[" + outFile + "] compression=Uncompressed");
}</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/Macros/561967067.ijm' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/Macros/561967067.ijm' | relative_url }}" download><strong>⬇ Download Macro</strong></a>
</p>
</details>

<details>
<summary><strong>🔧 BatchSplit-3channel-tif.ijm</strong> — Batch split 3-channel images into separate C1, C2, C3 tiff files</summary>
<pre><code>/* This is a batch processing macro that has been designed to process
 * a folder of images (your source directory) and to split a 3 channel image into 3 separate tiff files
 * naming them C1, C2, and C3 and save them in a separate specified folder.
 * You can comment out channels you do not need or add more if needed.
*/

sourcedir=getDirectory("Source directory with images");
destdir=getDirectory("Destination directory for images and data");

fileList=getFileList(sourcedir);

setBatchMode(true);
run("Bio-Formats Macro Extensions");

for (i=0; i&lt;fileList.length; i++) {
    file = sourcedir + fileList[i];
    Ext.openImagePlus(file);
    outFile1 = destdir + "C1-"+ fileList[i];
    outFile2 = destdir + "C2-"+ fileList[i];
    outFile3 = destdir + "C3-"+ fileList[i];
    saveFile(outFile1);
}

setBatchMode(false);

function saveFile(outFile){
 run("Split Channels");
  selectWindow("C1-"+ fileList[i]);
    saveAs("Tiff",+ outFile1 + );
 selectWindow("C2-"+ fileList[i]);
    saveAs("Tiff",+ outFile2+ );
 selectWindow("C3-"+ fileList[i]);
    saveAs("Tiff",+ outFile3 + );
}

close();</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/Macros/561967069.ijm' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/Macros/561967069.ijm' | relative_url }}" download><strong>⬇ Download Macro</strong></a>
</p>
</details>

<details>
<summary><strong>🔧 BatchSplit-3channel-tif-fixed.ijm</strong> — Fixed version of the 3-channel batch split macro</summary>
<pre><code>/* This is a batch processing macro that has been designed to process
 * a folder of images (your source directory) and to split a 3 channel image into 3 separate tiff files
 * naming them C1, C2, and C3 and save them in a separate specified folder.
 * You can comment out channels you do not need or add more if needed.
*/

sourcedir=getDirectory("Source directory with images");
destdir=getDirectory("Destination directory for images and data");

fileList=getFileList(sourcedir);

setBatchMode(true);
run("Bio-Formats Macro Extensions");

for (i=0; i&lt;fileList.length; i++) {
    file = sourcedir + fileList[i];
    Ext.openImagePlus(file);
    outFile1 = destdir + "C1-"+ fileList[i];
    outFile2 = destdir + "C2-"+ fileList[i];
    outFile3 = destdir + "C3-"+ fileList[i];
    saveFile(outFile1);
}

setBatchMode(false);

function saveFile(outFile){
 run("Split Channels");
  selectWindow("C1-"+ fileList[i]);
    saveAs("Tiff", outFile1);
 selectWindow("C2-"+ fileList[i]);
    saveAs("Tiff", outFile2);
 selectWindow("C3-"+ fileList[i]);
    saveAs("Tiff", outFile3);
}

close();</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/Macros/618628296.ijm' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/Macros/618628296.ijm' | relative_url }}" download><strong>⬇ Download Macro</strong></a>
</p>
</details>

<details>
<summary><strong>🔧 Batch-imageSeq-bioformats.ijm</strong> — Batch open with Bio-Formats and save as image sequence</summary>
<pre><code>/* This is a batch processing macro that has been designed to process
 * a folder of images (your source directory) by opening them with the
 * Bio-Formats importer and apply the commands found in the function.
 * This particular macro is set up to save the images as an image sequence.
*/

sourcedir=getDirectory("Source directory");
destdir=getDirectory("Destination directory");

fileList=getFileList(sourcedir);

setBatchMode(true);
run("Bio-Formats Macro Extensions");

for (i=0; i&lt;fileList.length; i++) {
    file = sourcedir + fileList[i];
    Ext.openImagePlus(file);
    outFile = destdir + fileList[i];
    saveFile(outFile);
}

setBatchMode(false);

function saveFile(outFile){
}

run("Image Sequence... ", " dir=[" + destdir + "] format=TIFF ");
close();</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/Macros/561967075.ijm' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/Macros/561967075.ijm' | relative_url }}" download><strong>⬇ Download Macro</strong></a>
</p>
</details>

<details>
<summary><strong>🔧 Batch-imageSeq_CentralSelector-Bioformats.ijm</strong> — Batch open and select central Z-slices per stack</summary>
<pre><code>/* This is a batch processing macro that has been designed to process
 * a folder of images (your source directory) by opening them with the
 * Bio-Formats importer and apply the commands found in the function.
 * This file was modified by Francois Mifsud to find the central plane and select a specific region around it!
 * Modified by AB and FM on 05-03-21 to select the same number of slices at the center of each stack.
*/

sourcedir=getDirectory("Source directory");
destdir=getDirectory("Destination directory");
ntarget = 10;       // has to be even and lower or equal to the lowest number of slices in all images
nchannels = 3;      // enter number of channels in the images

fileList=getFileList(sourcedir);

setBatchMode(true);
run("Bio-Formats Macro Extensions");

for (i=0; i&lt;fileList.length; i++) {
    file = sourcedir + fileList[i];
    Ext.openImagePlus(file);
    name = fileList[i];
    s=lastIndexOf(name, '.');
    name=substring(name, 0,s);
    name=replace(name,".ome","");
    name=replace(name,".","_");
    outFile = destdir + fileList[i];
    saveFile(outFile);
}

setBatchMode(false);

function saveFile(outFile){
    n = nSlices()/nchannels;
    if (n%2 != 0) {
        write("Number of slices is odd, dropped last slice");
        n = n-1;
    }
    binf = (n/2) - (ntarget/2) + 1;
    bsup = (n/2) + (ntarget/2);
    write("Original number of slices=" + n + ", Keeping slices "+ binf + "-" + bsup);
    run("Make Substack...", "channels=1-3 slices="+ binf + "-" + bsup);
    run("Bio-Formats Exporter", " save=[" + outFile + "] write_each_z_section write_each_channel export compression=Uncompressed");
    close();
}</code></pre>
<p style="margin-top: 0.5em;">
  <a href="{{ '/assets/Macros/561967078.ijm' | relative_url }}" target="_blank"><strong>↗ Open in new tab</strong></a>
  &nbsp;|&nbsp; <a href="{{ '/assets/Macros/561967078.ijm' | relative_url }}" download><strong>⬇ Download Macro</strong></a>
</p>
</details>

### Resources for learning

[Peter Bankhead: Analyzing fluorescence microscopy images with ImageJ](https://petebankhead.gitbooks.io/imagej-intro/content/)

[Kari\'s Webinar — Introduction to Fiji](https://urldefense.proofpoint.com/v2/url?u=https-3A__ucsf.box.com_v_Fijiworkshop-2D20200323&d=DwMF-g&c=iORugZls2LlYyCAZRB3XLg&r=rWHGLgGRKCB9UJ_3gjETqRC0fXrJ1iZZJnwLO8_WuLc&m=t8wrlXRnTmwCXxNw3nIiR2nwA4ltf57v82_DnEO1xRA&s=TvTBncaI1qX_eNSoSnYBU-u5hWPZ1X6wdwK16a8wK_Y&e=)
