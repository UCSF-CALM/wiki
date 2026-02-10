// find the frame in the z-stack with the maximum average intensity and duplicate it, and close the old z-stack

//name current selected image
current = getImageID;
// now can refer to that image as "current"

//set the measurements (do a "record macro" to get this list)
run("Set Measurements...", "area mean standard modal min limit display redirect=None decimal=3");

//go to slice 1 and measure its mean to get a starting value
setSlice(1);
getStatistics(area, mean, min, max,stdev);	//now have stored mean of intensities into the variable "mean"
maxMean = mean;	//call the current value of the mean the first maxMean 

//iterate through all slices, measure the mean, and compare to the maxMean
for (n=1; n<=nSlices; n++) {
	setSlice(n);
	getStatistics(area, mean, min, max, stdev);
	if (mean>maxMean) {
		maxMean = mean;	//if it is larger than maxMean, then mark this slice as the new maxMean
		frameToDup = n;
	}
}

setSlice(frameToDup);	//go to the frame that has the maximum Mean value
run("Duplicate...", "title=centerframe");	//duplicate that frame, calling it "centerframe"
dup = getImageID;	//give this new image the name "dup"

selectImage(current);
close();
selectImage(dup);	//ends the macro with the new image selected
// now can save this image etc.
