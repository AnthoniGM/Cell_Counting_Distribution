// Directory where the hyperstack will be saved
outputDir = "D:\\PSM\\SST_images\\Full\\";

// Get the list of open images
imageTitles = getList("image.titles");

for (i = 0; i < imageTitles.length; i++) {
    // Select each open image by its title
    selectWindow(imageTitles[i]);
    title = getTitle();

    // Assign LUTs to each channel
    Stack.setChannel(1);
    run("Blue");
    Stack.setChannel(2);
    run("Green");
    Stack.setChannel(3);
    run("Red");

    // Save the hyperstack as a .tiff
    saveAs("Tiff", outputDir + title);
}

// Close all open images
run("Close All");

// Directory where the hyperstack was saved
outputDir = "D:\\PSM\\SST_images\\Full\\";

// Get a list of all files in the output directory
fileList = getFileList(outputDir);

for (i = 0; i < fileList.length; i++) {
    oldName = fileList[i];
    if (indexOf(oldName, "PSM_PV_SST.lif - ") >= 0) {
        // Create the new name by removing the unwanted text
        newName = replace(oldName, "PSM_PV_SST.lif - ", "");
        
        // Rename the file
        renameFile(outputDir + oldName, outputDir + newName);
    }
}

// Function to rename files
function renameFile(oldPath, newPath) {
    File.rename(oldPath, newPath);
}
