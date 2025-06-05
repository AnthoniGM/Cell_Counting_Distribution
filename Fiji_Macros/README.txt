Open all images in FIJI/ImageJ

Run HyperstackOpening_namesCleaned.ijm
which will reorganize files and clean the names

Run SortColors_AvgimageCreation.ijm
This will split channels into relevant directories and create some z-projections that can be used for later ROI drawing

***
At this point there should be two directories, one for the GREEN/PV images and one for the RED/SST images
within each of these should be the following folders: “avg”, “best_segmentation”, “classifiers”, “csvs”, “Green”/”Red”, “LabSegmentation”, “results”. The following scripts/codes will reference these directories. 

The next steps are as follows: 
1.	draw ROIs – fiji script
a.	verify subregion identification – fiji script
b.	Measure ROI area
2.	classify objects using several classifiers to best reflect true objects – fiji script
a.	determine best classification per image – fiji script
3.	count objects from best classification – fiji script
4.	stratify objects across CA1 strata (oriens, pyrimidale, radiatum) – Jupyter script (Python)

The scripts will need to be modified for either the SST or PV directories

1.	Draw ROIs. Use either the Green or Blue channel averages (or any combination you prefer that let’s you clearly delineate our regions of interest). 
Run the following script in FIJI (click the main FIJI bar and tap “[“ to open the macro tool. The saved file is “ROI_drawer.py”, run this using the Jython language. Use the polygon tool to draw the primary ROI, then the Segmented Line tool to draw the boundaries (these boundaries MUST begin and end outside of the primary ROI).

Run ROI_drawer.py using Jython
This will allow the user to draw a full ROI using the polygon selector tool, then subdivide it first isolating oriens, then radiatum using the segmented line tool. Ensure the segmented line portion extends outside of the bounds of the original full ROI

Run ROI_checker.py using Jython
This will label the image with the centroid location of stratum oriens (so) and stratum radiatum (sr) - if the orientation is correct the file will remain - if the orientation is backwards, the relevant ROI files will be renamed to match the correct placement. 
When complete, copy all ROIs to the other directory (probably the SST one). You may need to rename the 'color' associated with them

Calculate the ROI areas using CalculateROIAreaJython.py using Jython

Next use the Fiji plugin 'LabKit' to create several classifiers for (one at a time) the PV and SST directories and save these classifiers in the “classifiers” subdirectory. Try to create these via markedly different signal:noise images types so that for all images, there will be at least one that does a great job classifying objects. Use the Batch Segment feature of the LabKit plugin to run all images through each of the classifiers you created. Have these classified files saved into the directory “LabKitSegmentation” each under the number of the classifier you created (just use 1, 2, 3, …etc”).
a.	Next use the “BestSegChooser.py” in FIJI (again with the Jython language) to choose the best of the segmented options for each base image. When you select the best one, it will automatically be saved into the “best_segmentation” subdirectory. 

We are now done with FIJI/ImageJ
Make sure to spot check along the way!

We will next use Python for individual cell counting/filtering/and distribution as well as grouping. 