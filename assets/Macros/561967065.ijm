// batchTiffConvert.txt


/*This converts BF Color RGB ND2 Files into BF Color RGB TIF files and re orders the channels 
 * because NIS elements writes the colors in a Differnt header order than Fiji
 * 
 * 
*/
oneFilePerSlice = false;

directory = getDirectory("Input files");
fileList = getFileList(directory);

outputDirectory = getDirectory("Output directory");

run("Bio-Formats Macro Extensions");
setBatchMode(true);

for (i=0; i<fileList.length; i++) {
  file = directory + fileList[i];
  if (oneFilePerSlice) {
    Ext.setId(file);
    Ext.getImageCount(imageCount);
    for (image=0; image<imageCount; image++) {
      Ext.openImage("", image);
      outFile = outputDirectory + fileList[i] + "-" + image + ".ome.tiff";
      saveFile(outFile);
      close();
    }
    Ext.close();
  }
  else {
    Ext.openImagePlus(file);						 //opens as default stack
    outFile = outputDirectory + fileList[i] + ".ome.tiff"; 	//need ome.tiff
    saveFile(outFile);
    close();
  }
}

showStatus("Finished.");
setBatchMode(false);

function saveFile(outFile) {
	Stack.setChannel(1);				//Set colors perchannel
	run("Blue");
	Stack.setChannel(2);
	run("Green");
	Stack.setChannel(3);
	run("Red");						//makes composite
	run("Make Composite");
	run("RGB Color");				//converts to RGB image
    name=getTitle();
    s=lastIndexOf(name, '.');                          // next three lines are code to strip off the .nd2 extension from the filename
    name=substring(name, 0,s);
    
	
   run("Bio-Formats Exporter", "save=[" + outputDirectory + name + ".ome.tif" + "] compression=Uncompressed");		
}
close();