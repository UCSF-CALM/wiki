//This macro "measures" each slice in the stack

//set the measurements (do a "record macro" to get this list)
run("Set Measurements...", "area mean standard modal min limit display redirect=None decimal=3");

//loop through each slice
for (n=1; n<=nSlices; n++){	//nSlices refers to the number of slices in the selected stack
	setSlice(n); //go to slice n
	run("Measure"); 	//
}


