# Cell_Counting_Distribution
Semi-automated preprocessing, identification, sorting, and distribution mapping of green and red fluorescent cells in CA1 subfields. 

---

## 🔧 Key Features

### ✅ Cell Segmentation & ROI Mapping
- Uses 3D segmentation in FIJI to label SST+ cells.
- ROIs are drawn manually or semi-automatically to define **oriens**, **pyrimidale**, and **radiatum**.
- ROI boundaries are applied programmatically using Python and `shapely`.

### ✅ Radiatum Filtering via Deep Learning
- Cells in **radiatum** are filtered based on a trained CNN that distinguishes real vs. artifact detections.
- Only radiatum cells with label = 1 (true positive) are retained.
- Oriens and pyrimidale cells are retained without filtering.

### ✅ Distance Normalization
- Each cell’s relative position within its ROI is computed as a **% distance** from the shared ROI boundary.
- Results allow for group-wise comparison of cell distributions across layers.

### ✅ Exported Output
- Final Excel workbook `processed_results.xlsx` includes:
  - `base_id`, `obj_idx`, `ROI`, `Position%`, `X`, `Y`, and `label`
  - Separate sheets for Control (`C`) and SE (`SE`) groups

### ✅ QC Visualization
- Overlay of detected cells, ROIs, and shared boundaries on raw images.
- Quick visual validation of segmentation and region assignment.

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/SST-cell-counting.git
cd SST-cell-counting
pip install -r requirements.txt
