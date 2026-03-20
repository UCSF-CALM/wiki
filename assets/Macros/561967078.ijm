/* This is a batch processing macro that has been designed to process 
 *  a folder of images (your source directory)by opening them with the 
 *  Bio-Formats importer and apply the commands found in the function.
 *  It includes a steps for nameing and saving results in the 
 *  measurement window. All the steps have been commented for what you  
 *  are doing and what each line does! Feel free to play with it. 
 *  Comment out what you don't need and add commands to the function 
 *  that you want to run!
 *  
 *  This file was modified by Francois Mifsud to find the central plane and select a specific region around it!
 *  Modified by AB and FM on 05-03-21 to select the same number of slices at the center of each stack
 */
 
sourcedir=getDirectory("Source directory");			//chose folder that has images
destdir=getDirectory("Destination directory"); 		//chose directory for images and data
ntarget = 10;   	                                //has to be even and lower or equal to the lowest number of slices in all images
nchannels = 3 ;                                     //enter number of channels in the images 

  
fileList=getFileList(sourcedir); 		//define your images as a list so loops can identify them

setBatchMode(true);  					//If batch mode is set to true, then newly opened images will not be displayed. 
run("Bio-Formats Macro Extensions");	//Comanand for enabling Bio-Formats functions

for (i=0; i<fileList.length; i++) { 	//starting code line for the loop keeps it flexible with i
	file = sourcedir + fileList[i]; 	//path for where the files are tells the computer to work though those files sequentially
    Ext.openImagePlus(file); 			//open the image in bioformats
       name = fileList[i];
      s=lastIndexOf(name, '.');                          // next three lines are code to strip off the .tif extension from the filename
      name=substring(name, 0,s);
      name=replace(name,".ome","");
      name=replace(name,".","_");
    outFile = destdir + fileList[i]; 	//if you are not using an ome.tif already then use outFile = destdir + fileList[i] + ".ome.tif"; 
  saveFile(outFile); 					//create a variable for writing your own function where you can run the other processess
  } 									//close the loop

setBatchMode(false);

function saveFile(outFile){ 			//defines the saveFile function listed above
n = nSlices()/nchannels ;                   //has to be even
if (n%2 != 0) {
	write("Number of slices is odd, dropped last slice");
	n = n-1;
}

binf = (n/2) - (ntarget/2) + 1;         //minimum slice index is 1
bsup = (n/2) + (ntarget/2);
write("Original number of slices=" + n + ", Keeping slices "+ binf + "-" + bsup);

run("Make Substack...", "channels=1-3 slices="+ binf + "-" + bsup ); //ADD THINGS HERE!!!!
run("Bio-Formats Exporter",  " save=[" + outFile + "] write_each_z_section write_each_channel export compression=Uncompressed"); 	//saving using bioformats
   	close();
} 																//Closes the function
//close(); 														//Closes the last window left open from the batch mode