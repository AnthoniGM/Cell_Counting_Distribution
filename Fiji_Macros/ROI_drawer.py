#@ File(label="Input directory", style="directory") mainDir
#@ File(label="Output directory", style="directory") outputDir

from ij import IJ, ImagePlus
from ij.plugin.frame import RoiManager
from ij.gui import WaitForUserDialog, ShapeRoi, Roi
import os
import sys  # To allow graceful script termination

# Ensure output directory exists
if not os.path.exists(outputDir.getPath()):
    os.makedirs(outputDir.getPath())

# Get all TIF files in the input directory
fileList = [f for f in os.listdir(mainDir.getPath()) if f.endswith('.tif')]

for fileName in fileList:
    try:
        imagePath = os.path.join(mainDir.getPath(), fileName)
        imp = IJ.openImage(imagePath)
        imp.show()

        fileBaseName = os.path.splitext(fileName)[0]

        # Initialize the ROI Manager
        rm = RoiManager.getInstance()
        if rm is None:
            rm = RoiManager()
        else:
            rm.reset()

        # Prompt user to draw the primary ROI
        WaitForUserDialog("Draw the primary ROI for: " + fileName).show()
        primaryRoi = imp.getRoi()
        if primaryRoi is None:
            IJ.error("No ROI was drawn. Exiting script.")
            imp.close()
            sys.exit()  # Exit gracefully

        # Add and save the primary ROI
        rm.addRoi(primaryRoi)
        primaryRoiName = fileBaseName + "_full"
        primaryRoi.setName(primaryRoiName)
        roiFilePath = os.path.join(outputDir.getPath(), primaryRoiName + ".roi")
        rm.select(rm.getCount() - 1)
        rm.runCommand("Save", roiFilePath)
        print("Saved full ROI: " + roiFilePath)

        # Prompt user to draw the first dividing line
        WaitForUserDialog("Draw the first dividing line (Stratum Oriens boundary) and press OK.").show()
        firstDivider = imp.getRoi()
        if firstDivider is None:
            IJ.error("No dividing line was drawn. Exiting script.")
            imp.close()
            sys.exit()

        rm.addRoi(firstDivider)

        # Prompt user to draw the second dividing line
        WaitForUserDialog("Draw the second dividing line (Stratum Pyrimidale boundary) and press OK.").show()
        secondDivider = imp.getRoi()
        if secondDivider is None:
            IJ.error("No dividing line was drawn. Exiting script.")
            imp.close()
            sys.exit()

        rm.addRoi(secondDivider)

        # Proceed to split the primary ROI
        try:
            # Convert the primary ROI to a ShapeRoi
            primaryShapeRoi = ShapeRoi(primaryRoi)

            # Convert the dividing lines into area ROIs by adding a stroke width
            lineWidth = 10  # Adjust as needed to ensure the lines fully cross the ROI

            # First dividing line
            firstDivider.setStrokeWidth(lineWidth)
            firstDividerShape = ShapeRoi(firstDivider)

            # Second dividing line
            secondDivider.setStrokeWidth(lineWidth)
            secondDividerShape = ShapeRoi(secondDivider)

            # Combine the two divider shapes
            combinedDividers = firstDividerShape.or(secondDividerShape)

            # Subtract the dividers from the primary ROI to get the remaining areas
            subtractedRoi = primaryShapeRoi.not(combinedDividers)

            # Get individual subregions from the resulting ShapeRoi
            rois = subtractedRoi.getRois()

            # Check if we have the expected number of subregions
            if len(rois) != 3:
                IJ.error("Unexpected number of subregions detected: " + str(len(rois)))
            else:
                subregionNames = ['s_oriens', 's_pyrimidale', 's_radiatum']
                for idx, roi in enumerate(rois):
                    roiName = fileBaseName + "_" + subregionNames[idx]
                    roi.setName(roiName)
                    rm.addRoi(roi)
                    # Save the ROI
                    roiFilePath = os.path.join(outputDir.getPath(), roiName + ".roi")
                    rm.select(rm.getCount() - 1)
                    rm.runCommand("Save", roiFilePath)
                    print("Saved ROI: " + roiFilePath)

        except Exception as e:
            IJ.error("An error occurred while processing " + fileName + ": " + str(e))

        # Clean up for the next image
        imp.close()
        rm.reset()

    except KeyboardInterrupt:
        IJ.error("Script interrupted. Exiting.")
        break  # Gracefully exit the loop
    except SystemExit:
        IJ.error("Exiting script.")
        break  # Gracefully exit the loop
    except Exception as e:
        IJ.error("Unexpected error: " + str(e))
        break  # Gracefully exit in case of an error

print("Processing complete.")
