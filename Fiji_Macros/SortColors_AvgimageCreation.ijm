// Directories for saving the channels
outputDirBlue = "D:\\PSM\\SST_images\\DAPI\\Blue\\";
outputDirGreen = "D:\\PSM\\SST_images\\PV\\Green\\";
outputDirRed = "D:\\PSM\\SST_images\\SST\\Red\\";
outputDirAvg = "D:\\PSM\\SST_images\\DAPI\\avg\\";

// Directory containing the hyperstacks
inputDir = "D:\\PSM\\SST_images\\Full\\";

// Get a list of all files in the input directory
fileList = getFileList(inputDir);

for (i = 0; i < fileList.length; i++) {
    oldName = fileList[i];
    if (endsWith(oldName, ".tif")) {
        // Open the hyperstack
        open(inputDir + oldName);
        title = getTitle();
        
        // Split the hyperstack into individual channels
        run("Split Channels");

        // Process the Blue channel
        selectWindow("C1-" + title);
        blueName = "Blue_" + replace(title, "PSM_PV_SST.lif - ", "");
        saveAs("Tiff", outputDirBlue + blueName);
        run("Z Project...", "projection=[Average Intensity]");
        saveAs("Tiff", outputDirAvg + blueName);
        close();

        // Process the Green channel
        selectWindow("C2-" + title);
        greenName = "Green_" + replace(title, "PSM_PV_SST.lif - ", "");
        saveAs("Tiff", outputDirGreen + greenName);
        close();

        // Process the Red channel
        selectWindow("C3-" + title);
        redName = "Red_" + replace(title, "PSM_PV_SST.lif - ", "");
        saveAs("Tiff", outputDirRed + redName);
        close();

        // Close all remaining images to ensure clean processing for the next file
        run("Close All");
    }
}
// Directory containing the green channel .tif files
inputDirGreen = "D:\\PSM\\SST_images\\PV\\Green\\";

// Directory to save the averaged z-stack images
outputDirAvg = "D:\\PSM\\SST_images\\PV\\avg\\";

// Get a list of all files in the input directory
fileList = getFileList(inputDirGreen);

for (i = 0; i < fileList.length; i++) {
    oldName = fileList[i];
    if (endsWith(oldName, ".tif")) {
        // Open the green channel .tif file
        open(inputDirGreen + oldName);
        title = getTitle();

        // Create an average z-stack projection
        run("Z Project...", "projection=[Average Intensity]");

        // Save the averaged image
        saveAs("Tiff", outputDirAvg + title);

        // Close the current image to ensure clean processing for the next file
        run("Close All");
    }
}
