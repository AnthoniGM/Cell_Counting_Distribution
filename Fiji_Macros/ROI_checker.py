#@ File(label="Image directory", style="directory") imageDir
#@ File(label="ROI directory", style="directory") roiDir

# This script will call up the stratum oriens and radiatum and label 
# them in the image for manual checking. If they are correct nothing 
# happens, if they are incorrect, select as much and the filenames will swap. 
from ij import IJ, ImagePlus
from ij.plugin.frame import RoiManager
from ij.gui import GenericDialog, WaitForUserDialog, Overlay, TextRoi
import os
import shutil

# Get all TIF files in the image directory
imageList = [f for f in os.listdir(imageDir.getPath()) if f.endswith('.tif')]

# Initialize ROI Manager
rm = RoiManager.getInstance()
if rm is None:
    rm = RoiManager()
else:
    rm.reset()

for imageFile in imageList:
    try:
        # Open the image
        imagePath = os.path.join(imageDir.getPath(), imageFile)
        imp = IJ.openImage(imagePath)
        imp.show()

        baseName = os.path.splitext(imageFile)[0]

        # Load ROIs for the image
        roiOriensPath = os.path.join(roiDir.getPath(), "{}_s_oriens.roi".format(baseName))
        roiRadiatumPath = os.path.join(roiDir.getPath(), "{}_s_radiatum.roi".format(baseName))

        if not os.path.exists(roiOriensPath) or not os.path.exists(roiRadiatumPath):
            IJ.error("Missing ROIs for {}. Skipping this image.".format(baseName))
            imp.close()
            continue

        rm.runCommand("Open", roiOriensPath)
        rm.runCommand("Open", roiRadiatumPath)

        # Get ROIs and add labels
        roiOriens = rm.getRoi(0)
        roiRadiatum = rm.getRoi(1)

        # Create an overlay for labels
        overlay = Overlay()

        # Add text labels at the center of each ROI
        for roi, label in zip([roiOriens, roiRadiatum], ["SO", "SR"]):
            bounds = roi.getBounds()
            centerX = bounds.x + bounds.width // 2
            centerY = bounds.y + bounds.height // 2
            textRoi = TextRoi(centerX, centerY, label)
            textRoi.setStrokeColor(roi.getStrokeColor())  # Match text color with ROI color
            overlay.add(textRoi)

        # Set the overlay on the image
        imp.setOverlay(overlay)

        # Show a dialog to confirm if labeling is correct
        gd = GenericDialog("Verify ROIs for {}".format(baseName))
        gd.addMessage("Is the labeling correct?")
        gd.enableYesNoCancel("Correct", "Incorrect")
        gd.showDialog()

        if gd.wasCanceled():
            IJ.log("User canceled at {}. Exiting.".format(baseName))
            imp.close()
            break

        elif gd.wasOKed():  # Correct labeling
            IJ.log("Labeling confirmed for {}.".format(baseName))
            imp.close()
            rm.reset()

        else:  # Incorrect labeling
            IJ.log("Labeling incorrect for {}. Swapping ROI names.".format(baseName))

            # Swap ROI files
            tempOriensPath = os.path.join(roiDir.getPath(), "{}_s_oriens_temp.roi".format(baseName))
            shutil.move(roiOriensPath, tempOriensPath)
            shutil.move(roiRadiatumPath, roiOriensPath)
            shutil.move(tempOriensPath, roiRadiatumPath)

            IJ.log("ROI names swapped for {}.".format(baseName))

            imp.close()
            rm.reset()

    except Exception as e:
        IJ.error("Error processing {}: {}".format(imageFile, e))
        if imp:
            imp.close()
        continue  # Move to the next file

IJ.log("Processing complete.")
