/*this is a macro for batch processing LIF files in to ome.tif files. 
 * Instructions:
 * Put your LIF files you want to convert into a folder. This is your Input/source directory
 * Create a folder for your files to be out put to. This is your output/destination directory
 * If you want to run any processes on the images while you are converting them you can change the code below where indicated.
 * When you are readt, click "Run"
 * It will prompt you to select your input folder, choose it and click select
 * It will then prompt you to click your output folder, choose it and click select
 * It should run and process all your files

*/
run("Bio-Formats Macro Extensions");
setBatchMode(true);

currentDirectory = getDirectory("Choose a Source Directory");
outputDirectory = getDirectory("Select Destination");



	fileList = getFileList(currentDirectory);

	for (file = 0; file < fileList.length; file++) {
		Ext.isThisType(currentDirectory + fileList[file], supportedFileFormat);
		if (supportedFileFormat=="true") {
			Ext.setId(currentDirectory + fileList[file]);
			Ext.getSeriesCount(seriesCount);
			for (series = 1; series <= seriesCount; series++) {
				//record the Bio-Formats importer with the setup you need if different from below and change accordingly
				run("Bio-Formats Importer", "open=[" + currentDirectory + fileList[file] + "] autoscale color_mode=Composite rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT series_"+series);
				name=getTitle();
				//You can add any process you want here! Use Plugins>Macro>Record for determining files
				run("Bio-Formats Exporter", "save=[" + outputDirectory + name + ".ome.tif" + "] compression=Uncompressed");		
close();
			}
		} else if (endsWith(fileList[file], "/")) {
			processBioFormatFiles(currentDirectory + fileList[file]);
		}
	}


setBatchMode(false);