from ij import IJ, ImagePlus
from ij.plugin.frame import RoiManager
from ij.plugin.filter import ThresholdToSelection
from ij.gui import Overlay, NonBlockingGenericDialog
import os

# Directories
base_dir = r"D:\PSM\SST_images\SST\LabkitSegmentation\5"
seg_dir = r"D:\PSM\SST_images\SST\LabkitSegmentation"
output_dir = r"D:\PSM\SST_images\SST\best_segmentation"
folders = ["1", "2", "3", "4", "6"]

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get all base images
base_images = [f for f in os.listdir(base_dir) if f.endswith('.tif')]

# Function to binarize an image using Otsu's method
def binarize_image(slice_processor):
    slice_imp = ImagePlus("slice", slice_processor)
    IJ.run(slice_imp, "8-bit", "")
    IJ.setAutoThreshold(slice_imp, "Otsu dark")  # Use Otsu's method explicitly
    IJ.run(slice_imp, "Convert to Mask", "")
    return slice_imp.getProcessor()

# Process each base image
for base_file in base_images:
    base_path = os.path.join(base_dir, base_file)
    base_imp = IJ.openImage(base_path)
    base_stack = base_imp.getStack()  # Access the full stack

    # Create a list to store synchronized images
    images_to_compare = []

    for folder in folders:
        seg_path = os.path.join(seg_dir, folder, base_file.replace(".tif", "_seg.tif"))
        if not os.path.exists(seg_path):
            IJ.log("Segmentation file missing: {}".format(seg_path))
            continue
        
        seg_imp = IJ.openImage(seg_path)
        seg_stack = seg_imp.getStack()  # Access the full stack
        
        if seg_stack.getSize() != base_stack.getSize():
            IJ.error("Stack sizes do not match for {} in folder {}".format(base_file, folder))
            seg_imp.close()
            continue

        # Duplicate the base image for slice-specific overlays
        base_dup = base_imp.duplicate()
        overlay_per_slice = Overlay()

        # Process slice by slice
        for slice_idx in range(1, base_stack.getSize() + 1):  # 1-based indexing for slices
            seg_imp.setSlice(slice_idx)
            seg_slice = seg_imp.getProcessor()
            binarized_slice = binarize_image(seg_slice)  # Binarize the segmentation slice
            
            # Convert to outlines and add to overlay for the current slice
            outlines = ThresholdToSelection.run(ImagePlus("slice", binarized_slice))
            if outlines:
                outlines.setPosition(slice_idx)  # Link the overlay to the specific slice
                overlay_per_slice.add(outlines)

        # Add the slice-specific overlay to the duplicated base image
        base_dup.setOverlay(overlay_per_slice)
        base_dup.setTitle(folder)
        images_to_compare.append(base_dup)
        
        seg_imp.close()

    # Display synchronized images
    for img in images_to_compare:
        img.show()
    IJ.run("Synchronize Windows")

    # Ask user for input with a non-blocking dialog
    gd = NonBlockingGenericDialog("Best Segmentation")
    gd.addMessage("Which segmentation looks best?")
    for folder in folders:
        gd.addCheckbox(folder, False)
    gd.showDialog()
    
    if gd.wasCanceled():
        IJ.log("Script canceled.")
        break
    
    selected = [folders[i] for i in range(len(folders)) if gd.getNextBoolean()]
    if len(selected) != 1:
        IJ.error("Please select exactly one segmentation.")
        for img in images_to_compare:
            img.close()
        continue
    
    selected_folder = selected[0]
    selected_seg_path = os.path.join(seg_dir, selected_folder, base_file.replace(".tif", "_seg.tif"))
    if os.path.exists(selected_seg_path):
        output_path = os.path.join(output_dir, base_file.replace(".tif", "_" + selected_folder + "_seg.tif"))
        IJ.save(IJ.openImage(selected_seg_path), output_path)
        IJ.log("Saved best segmentation for {} to {}".format(base_file, output_path))

    # Close images
    for img in images_to_compare:
        img.close()

print("Processing complete.")
