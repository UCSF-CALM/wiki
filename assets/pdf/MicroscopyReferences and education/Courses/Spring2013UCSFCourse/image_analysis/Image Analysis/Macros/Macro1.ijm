//open a z-stack
//in this case, open only the Cy5 channel, which is actin
run("Image Sequence...", "open=/Users/susanner/work/Teaching/ImageJTutorial/RawData/070811_control_1/img_000000000_Cy5_000.tif number=132 starting=1 increment=1 scale=100 file=Cy5 or=[] sort");

//do a maximum intensity projection
//**make sure that the "stop" in the max projection command is >= the number of frames in the z-stack
run("Z Project...", "start=1 stop=33 projection=[Max Intensity]");

//save to a new folder, with a new name, including the channel (actin)
run("Save", "save=/Users/susanner/work/Teaching/ImageJTutorial/PreprocessData/070811_control_1_actin_maxProj.tif");

//close both images
close();
close();
