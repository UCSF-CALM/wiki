//have a series of data, with mulitple fields of view, multiple colors, and z-stacks, collected on one day. 
//For each field of view, open each of 4 colors of a z-stack, max project, save as tif

//First set-up the file-paths and naming scheme - these should be checked and adjusted by hand before starting a macro run
parentPath = "/Users/susanner/work/Teaching/ImageJTutorial/";
pathToSaveTo = parentPath + "PreprocessData/";

myDate = "070811";
myExptCondition = "_control"

//make a folder for each channel within the PreprocessData folder. If it already exists, do nothing.
exist1 = File.isDirectory(pathToSaveTo + "maxProjectMito"); if (exist1!=1){File.makeDirectory(pathToSaveTo + "maxProjectMito");}
exist1 = File.isDirectory(pathToSaveTo + "maxProjectNucleus"); if (exist1!=1){File.makeDirectory(pathToSaveTo + "maxProjectNucleus");}
exist1 = File.isDirectory(pathToSaveTo + "maxProjectNucleolus"); if (exist1!=1){File.makeDirectory(pathToSaveTo + "maxProjectNucleolus");}
exist1 = File.isDirectory(pathToSaveTo + "maxProjectActin"); if (exist1!=1){File.makeDirectory(pathToSaveTo + "maxProjectActin");}

//iterate through all of the data collected that day

numFiles = 5;	//these are the total number of fields of view - adjust number as necessary
for (i = 1; i<numFiles+1; i++){
	myFileNum = "_" + i;	
	setBatchMode(true);	//this makes automation faster because images are only loaded, not opened as image data

//first Cy5 -> actin
	//on top is the original code to open the file #1 in this channel (commented out by // at the start of the line). 
	//below is the new code,with strings of text replaced with the variables defined above 
	//run("Image Sequence...", "open=/Users/susanner/work/Teaching/ImageJTutorial/RawData/070811_control_1/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=C or=[] sort");
	run("Image Sequence...", "open=" + parentPath + "RawData/" + myDate + myExptCondition + myFileNum +"/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=C or=[] sort");
	numFrames = nSlices; run("Z Project...", "start=1 stop=" + nSlices + " projection=[Max Intensity]");
	//again, old code on top, new code below
	//run("Save", "save=/Users/susanner/work/Teaching/ImageJTutorial/PreprocessData/maxProjectActin/070811_control_1_actin_maxProj.tif");
	run("Save", "save=" + pathToSaveTo + "maxProjectActin/" + myDate + myExptCondition + myFileNum + "_actin_maxProj.tif");
	close();
	close();

//DAPI -> DNA/nucleus
	run("Image Sequence...", "open=" + parentPath + "RawData/" + myDate + myExptCondition + myFileNum +"/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=D or=[] sort");
	numFrames = nSlices; run("Z Project...", "start=1 stop=" + nSlices + " projection=[Max Intensity]");
	run("Save", "save=" + pathToSaveTo +  "maxProjectNucleus/" + myDate + myExptCondition + myFileNum + "_nucleus_maxProj.tif");
	close();
	close();

//GFP -> mitochondria
	run("Image Sequence...", "open=" + parentPath + "RawData/" + myDate + myExptCondition + myFileNum +"/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=G or=[] sort");
	numFrames = nSlices; run("Z Project...", "start=1 stop=" + nSlices + " projection=[Max Intensity]");
	run("Save", "save=" + pathToSaveTo +  "maxProjectMito/" + myDate + myExptCondition + myFileNum + "_mito_maxProj.tif");
	close();
	close();

//RFP -> nucleolus
	run("Image Sequence...", "open=" + parentPath + "RawData/" + myDate + myExptCondition + myFileNum +"/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=R or=[] sort");
	numFrames = nSlices; run("Z Project...", "start=1 stop=" + nSlices + " projection=[Max Intensity]");
	run("Save", "save=" + pathToSaveTo +  "maxProjectNucleolus/" + myDate + myExptCondition + myFileNum + "_nucleolus_maxProj.tif");
	close();
	close();

	setBatchMode(false);	 	//turn off batch mode so it is not left on

//IMPORTANT: this "for" statement requires a closing bracket at the end
}

