// select any shape and crop out that shape through the entire z-stack
// then do a 3D maximum volume projection
//this code assumes 16-bit data initially. Adjust it accordingly

//start with a stack opened and a selection on the image

//name current selected image
orig = getImageID; // now can refer to that image as "orig"

// first find the minimum value within the selection within the entire z-stack
minmin =65535; //this is the maximum value for a 16-bit image and a starting point
setBatchMode(true);	//so this is done in the background/faster
for (n=1; n<=nSlices; n++) {
	setSlice(n);
	getStatistics(area, mean, min, max);
	if (min<minmin) minmin = min;
	}
setBatchMode(false);

//make a new image z-stack of set dimensions that is larger than the selection
//make sure this image is of the same type as the orig (16-bit, 8-bit, RGB etc)
//use "recordMacro" to find the necessary settings to make the image black or white etc
//make sure the image is large enough. Default is to make the image the same dimensions as orig

newImage("cropped", "16-bit Black", 300, 300, nSlices);
final = getImageID;	//now can refer to this new z-stack as "final" and go back and forth between orig and final

//add the value of minmin everywhere such that the "black" background is this value for image contrast scaling purposes
run("Add...", "stack value="+minmin);

//paste selection into the new stack frame by frame
setBatchMode(true);
for (n=1; n<=nSlices; n++) {
	selectImage(orig);
	setSlice(n);
	run("Copy");
	selectImage(final);
	setSlice(n);
	run("Paste");
}
setBatchMode(false);

//find the frame with the maximum intensity, go to that frame and reset brightness/contrast on that frame for easy viewing
maxmax =0;
setBatchMode(true);
for (n=1; n<=nSlices; n++) {
	setSlice(n);
	getStatistics(area, mean, min, max);
	if (max > maxmax) {
		maxmax = max;
		nofmax = n;		}
}
setBatchMode(false);

// now go to slice with the maxmax and use that to reset intensities in the stack
setSlice(nofmax);
run("Brightness/Contrast...");
resetMinAndMax();

//convert the new stack into 8-bit, which is required for 3D volume projection
selectImage(final);
run("8-bit");

//run the 3D projection viewer. Do a "record macro" to get your settings right. Make sure to enter the appropriate xy to z pixel ratio
//for example, 200nm steps with 61nm/pixel in x,y is a ratio of 3.28
run("3D Project...", "projection=[Brightest Point] axis=Y-Axis slice=3.28 initial=0 total=360 rotation=9 lower=1 upper=255 opacity=0 surface=100 interior=50 interpolate");
