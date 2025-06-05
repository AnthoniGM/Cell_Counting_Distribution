For Python analysis use Jupyter notebooks (files are all .ipynb)

Run "3DObjectsCounter_Watershed" you may need to change pixel size/dimensions and the voxel cutoffs for objects. This script will apply a watershed to objects larger than a certain threshold. The watershed is designed to be 'gentle' and not create too many small objects - but you may need to play with this parameter. Required dependencies are listed (commented out) at the top of the file. Use Cell 2 to set directories (will need to run separately for PV and SST cells - i.e. the different colors). 
Consider using Cell 4 as a spot check. (commented out)


dependencies:
ipywidgets==8.1.2
joblib==1.4.2
matplotlib==3.10.3
numpy==1.23.5
pandas==2.2.3
pyarrow==20.0.0
roifile==2025.2.20
scipy==1.13.1
seaborn==0.13.2
shapely==2.0.6
tqdm==4.66.5
Pil
collections
datetime
pickle
re
shutil
skimange
sklearn


I ran into an issue of immunofluorescent 'junk' (very well could be sprouting) showing up exclusively in radiatum of SST channels. I used machine learning and blinded manual annotations to identify real cells vs 'junk'. To do similar, use the "radiatum_sorting.ipynb"

Spot-check files for bad labeling and mark which files will be used and which group they are in within the first cell of the next scripts "Cell 1: Import and Configurations" Run both "PV2_Best_Cell_Dist.ipynb" and "SST2_Best_Cell_Dist.ipynb" which will count objects (and remove 'junk' objects if you needed to classify those), calculate locations within ROIs (across the Oriens-Pyrimidale-Radiatum axis), plot the distributions, and scale according to control group. There is also a quality control viewer at the bottom of these scripts. The final collection of data is listed in the "processed_results.csv" for each cell-type (i.e. color)