/* This is a batch processing macro that has been designed to process 
 *  a folder of images (your source directory)by opening them with the 
 *  Bio-Formats importer and apply the commands found in the function.
 *  This particular macro is set up to save the images in a seaparate folder as an image sequence

 */
 
sourcedir=getDirectory("Source directory");			//chose folder that has images
destdir=getDirectory("Destination directory"); 		//chose directory for images and data

  
fileList=getFileList(sourcedir); 		//define your images as a list so loops can identify them

setBatchMode(true);  					//If batch mode is set to true, then newly opened images will not be displayed. 
run("Bio-Formats Macro Extensions");	//Comanand for enabling Bio-Formats functions

for (i=0; i<fileList.length; i++) { 	//starting code line for the loop keeps it flexible with i
	file = sourcedir + fileList[i]; 	//path for where the files are tells the computer to work though those files sequentially
    Ext.openImagePlus(file); 			//open the image in bioformats
    outFile = destdir + fileList[i]; 	//if you are not using an ome.tif already then use outFile = destdir + fileList[i] + ".ome.tif"; 
  saveFile(outFile); 					//create a variable for writing your own function where you can run the other processess
  } 									//close the loop

setBatchMode(false);

function saveFile(outFile){ 			//defines the saveFile function listed above

}


run("Image Sequence... ",  " dir=[" + destdir + "] format=TIFF "); 	//saving using bioformats
   	close();
