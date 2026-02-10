//open each of 4 colors of a z-stack, max project, save as tif

//first Cy5 -> actin
run("Image Sequence...", "open=/Users/susanner/work/Teaching/ImageJTutorial/RawData/070811_control_1/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=C or=[] sort");

//get the number of frames to make sure that the "stop" in the max projection command is > the number of frames in the z-stack
numFrames = nSlices;

//incorporate this variable (nSlices) into the code. All remaining text is in " " and text and variables are concatenated by a +. Make sure to keep all proper spacing within text
//this is the old code (with // in front because it is commented out) and the new code below for comparison
//run("Z Project...", "start=1 stop=33 projection=[Max Intensity]");
run("Z Project...", "start=1 stop=" + nSlices + " projection=[Max Intensity]");

//now save with proper channel name and close the windows
run("Save", "save=/Users/susanner/work/Teaching/ImageJTutorial/PreprocessData/070811_control_1_actin_maxProj.tif");
close();
close();

//DAPI -> DNA/nucleus
run("Image Sequence...", "open=/Users/susanner/work/Teaching/ImageJTutorial/RawData/070811_control_1/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=D or=[] sort");
numFrames = nSlices; run("Z Project...", "start=1 stop=" + nSlices + " projection=[Max Intensity]");
run("Save", "save=/Users/susanner/work/Teaching/ImageJTutorial/PreprocessData/070811_control_1_nucleus_maxProj.tif");
close();
close();

//GFP -> mitochondria
run("Image Sequence...", "open=/Users/susanner/work/Teaching/ImageJTutorial/RawData/070811_control_1/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=G or=[] sort");
numFrames = nSlices; run("Z Project...", "start=1 stop=" + nSlices + " projection=[Max Intensity]");
run("Save", "save=/Users/susanner/work/Teaching/ImageJTutorial/PreprocessData/070811_control_1_mito_maxProj.tif");
close();
close();

//RFP -> nucleolus
run("Image Sequence...", "open=/Users/susanner/work/Teaching/ImageJTutorial/RawData/070811_control_1/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=R or=[] sort");
numFrames = nSlices; run("Z Project...", "start=1 stop=" + nSlices + " projection=[Max Intensity]");
run("Save", "save=/Users/susanner/work/Teaching/ImageJTutorial/PreprocessData/070811_control_1_nucleolus_maxProj.tif");
close();
close();
