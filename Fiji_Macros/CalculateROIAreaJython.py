import os
from ij import IJ
from ij.plugin.frame import RoiManager
from ij.measure import ResultsTable

# Directories
basefileDir = "D:/PSM/SST_images/SST/Red/"  # Directory with basefile images
roiDir = "D:/PSM/SST_images/SST/avg/Processed_ROIs/"  # Directory with ROI files
outputCSV = "D:/PSM/SST_images/SST/avg/roi_measurements.csv"  # Path to save the results CSV

# ROI suffixes
roi_suffixes = ["_full.roi", "_s_oriens.roi", "_s_pyrimidale.roi", "_s_radiatum.roi"]

# Get list of basefiles
basefiles = [f for f in os.listdir(basefileDir) if f.endswith(".tif")]

# Initialize output
output = "Filename,ROI,Area (microns)\n"  # CSV Header

# Process each basefile
for basefile in basefiles:
    basefile_name = basefile.replace("Red_", "").replace(".tif", "")  # Remove "Red_" prefix and ".tif"
    basefile_path = os.path.join(basefileDir, basefile)
    print("Processing basefile: {}".format(basefile_name))

    # Open the basefile image
    imp = IJ.openImage(basefile_path)
    if imp is None:
        print("Error: Could not open image {}".format(basefile_path))
        continue
    imp.show()

    found_rois = 0  # Track how many ROIs are found per basefile
    for suffix in roi_suffixes:
        roi_name = "Red_{}{}".format(basefile_name, suffix)
        roi_path = os.path.join(roiDir, roi_name)

        if os.path.exists(roi_path):
            print("  Found ROI: {}".format(roi_name))
            
            # Load the ROI
            rm = RoiManager.getInstance()
            if rm is None:
                rm = RoiManager()
            rm.reset()
            rm.runCommand("Open", roi_path)

            # Select the ROI and measure
            roi = rm.getRoi(0)
            if roi is not None:
                imp.setRoi(roi)
                IJ.run("Measure")
                
                # Get the area measurement from the Results table
                rt = ResultsTable.getResultsTable()
                if rt.size() > 0:
                    area = rt.getValue("Area", rt.size() - 1)
                    print("    Measured ROI: {}, Area: {}".format(suffix, area))

                    # Append to output
                    output += "{},{},{}\n".format(basefile_name, suffix, area)
                rt.reset()
                found_rois += 1
        else:
            print("  Missing ROI: {}".format(roi_name))

    # Check if no ROIs were found for this basefile
    if found_rois == 0:
        print("  Warning: No ROIs found for basefile: {}".format(basefile_name))

    # Close the image
    imp.changes = False  # Prevent "Save changes?" prompt
    imp.close()

# Save the output to CSV
with open(outputCSV, "w") as f:
    f.write(output)
print("Results saved to: {}".format(outputCSV))

