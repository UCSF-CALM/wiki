/*This converts a folder full of images (your input folder) into OME.tifs and to put them in a new out put folder
 * it is also set up to remove the suffix (i.e. ".ND2") from the image name just to clean it up a bit
 * */


oneFilePerSlice = false;

directory = getDirectory("Choose input files");
fileList = getFileList(directory);

outputDirectory = getDirectory("Choose output directory");

run("Bio-Formats Macro Extensions");
setBatchMode(true);

for (i=0; i<fileList.length; i++) {
  file = directory + fileList[i];
  if (oneFilePerSlice) {
    Ext.setId(file);
    Ext.getImageCount(imageCount);
    for (image=0; image<imageCount; image++) {
      Ext.openImage("", image);
      name = fileList[i];
      s=lastIndexOf(name, '.');                          // next three lines are code to strip off the .tif extension from the filename
      name=substring(name, 0,s);
      name=replace(name,".","_");
      outFile = outputDirectory + name + "-" +  ".ome.tif";
      saveFile(outFile);
      close();
    }
    Ext.close();
  }
  else {
    Ext.openImagePlus(file);
      name = fileList[i];
      s=lastIndexOf(name, '.');                          // next three lines are code to strip off the .tif extension from the filename
      name=substring(name, 0,s);
      name=replace(name,".","_");
      outFile = outputDirectory + name + "-" +  ".ome.tif";
    saveFile(outFile);
    close();
  }
}

showStatus("Finished.");
setBatchMode(false);

function saveFile(outFile) {
   run("Bio-Formats Exporter", "save=[" + outFile + "] compression=Uncompressed");
}