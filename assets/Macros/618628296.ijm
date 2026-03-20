/* This is a batch processing macro that has been designed to process 
 *  a folder of images (your source directory) and to split a 3 channel image into 3 separate tiff files
 *  nameing them C1, C2, and C3 and save them in a aeparate specified folder. You can comment out channels you do not need or add more if needed
 */
 
sourcedir=getDirectory("Source directory with images");								//chose folder that has images
destdir=getDirectory("Destination directory for images and data"); 		//chose directory for images and data
  
  
fileList=getFileList(sourcedir); 		//define your images as a list so loops can identify them

setBatchMode(true);  					//If batch mode is set to true, then newly opened images will not be displayed. 
run("Bio-Formats Macro Extensions");	//Comanand for enabling Bio-Formats functions

for (i=0; i<fileList.length; i++) { 	//starting code line for the loop keeps it flexible with i
	file = sourcedir + fileList[i]; 	//path for where the files are tells the computer to work though those files sequentially
    Ext.openImagePlus(file); 			//open the image in bioformats
    outFile1 = destdir + "C1-"+ fileList[i]; 	// creates output for C1
  	outFile2 = destdir + "C2-"+ fileList[i]; 	//creates output for C2			
	outFile3 = destdir + "C3-"+ fileList[i]; 	//creates output for C3 -- if you don't have a C3 you can modify here (use // to gomment out this line, make sure to comment out below as well) 
  	saveFile(outFile1); 					//create a variable for writing your own function where you can run the other processess
	
				 
  } 									//close the loop

setBatchMode(false);

function saveFile(outFile){ 									//defines the saveFile function listed above
 run("Split Channels");
  selectWindow("C1-"+ fileList[i]);							
	saveAs("Tiff", outFile1  ); 	//saving using tiff
 selectWindow("C2-"+ fileList[i]);							
	saveAs("Tiff", outFile2 );
 selectWindow("C3-"+ fileList[i]);							
	saveAs("Tiff",outFile3 );	//saving using tiff
} 	


   	close();

														//Closes the last window left open from the batch mode