# Osdag Screening Task — Xarray & Plotly / Matplotlib

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC--BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

---

## 🚀 Overview

This repository contains a concise solution to the **Osdag Xarray and Plotly/PyPlot Screening Task**. The goal is to extract internal force data from an **Xarray (NetCDF)** dataset and produce:

- 2D Shear Force Diagram (SFD) and Bending Moment Diagram (BMD) for the **central longitudinal girder** (Task 1)
- Interactive 3D SFD and BMD visualizations for **all bridge girders** (Task 2), styled similar to MIDAS post-processing

Both tasks are implemented in a modular, documented way and use the dataset provided in `data/screening_task.nc`.




1\. \*\*2D Shear Force Diagram (SFD) and Bending Moment Diagram (BMD)\*\* for the \*\*central longitudinal girder\*\*

2\. \*\*3D SFD and BMD visualizations\*\* for \*\*all bridge girders\*\*, similar to \*\*MIDAS post-processing style\*\*



Both \*\*Task-1 and Task-2\*\* have been completed as per the official requirements.



---



\## Project Structure



osdag-screening/

├── src/

│ ├── task1\_2d\_sfd\_bmd.py # Task-1: 2D SFD \& BMD

│ ├── task2\_3d\_sfd\_bmd.py # Task-2: 3D SFD \& BMD

│ ├── io\_utils.py # Dataset \& model loaders

│ └── plot\_utils.py # Plot helper utilities

│

├── data/

│ ├── screening\_task.nc # Xarray (NetCDF) dataset

│ ├── node.py # Node coordinates

│ └── element.py # Element connectivity

│

├── outputs/

│ ├── task1\_BMD.png # 2D Bending Moment Diagram

│ ├── task1\_SFD.png # 2D Shear Force Diagram

│ ├── task2\_3d\_BMD.html # 3D BMD (interactive)

│ └── task2\_3d\_SFD.html # 3D SFD (interactive)

│

├── requirements.txt

└── README.md


---



\## Requirements



\- Python \*\*3.9+\*\*

\- Required libraries (install using pip):

numpy

xarray

matplotlib

plotly



Install dependencies:



```bash

pip install -r requirements.txt

Dataset Description



Dataset file: screening\_task.nc



Data variable: forces



Dimensions:



Element



Component



The Component dimension includes:

Mx\_i, Mx\_j, My\_i, My\_j,

Mz\_i, Mz\_j,

Vx\_i, Vx\_j,

Vy\_i, Vy\_j,

x, y, z



Mz → Bending Moment



---

## 📊 Dataset & Variables

- File: `data/screening_task.nc`
- Main data variable: `forces`
- Component dimension contains:
  - `Mx_i`, `Mx_j`, `My_i`, `My_j`, `Mz_i`, `Mz_j`, `Vx_i`, `Vx_j`, `Vy_i`, `Vy_j`, `x`, `y`, `z`

Notes:
- `Mz` → bending moment
- `Vy` → shear force
- `_i` → start node of element, `_j` → end node

---

## 🧩 Methodology (summary)

**Task 1 (2D):**
- Central girder element IDs: `[15, 24, 33, 42, 51, 60, 69, 78, 83]`.
- Extract `Mz_i`/`Mz_j` for BMD and `Vy_i`/`Vy_j` for SFD.
- Use node X-coordinates as station values and plot with Matplotlib while preserving stored sign conventions.





Run Task-1

python src/task1\_2d\_sfd\_bmd.py \\

&nbsp; --dataset data/screening\_task.nc \\

&nbsp; --nodes\_py data/node.py \\

&nbsp; --elements\_py data/element.py \\

&nbsp; --out outputs



Outputs



outputs/task1\_BMD.png



outputs/task1\_SFD.png



Task-2: 3D SFD \& BMD (All Girders)

Girders Covered

Girder	Element IDs

Girder 1	13, 22, 31, 40, 49, 58, 67, 76, 81

Girder 2	14, 23, 32, 41, 50, 59, 68, 77, 82

Girder 3	15, 24, 33, 42, 51, 60, 69, 78, 83

Girder 4	16, 25, 34, 43, 52, 61, 70, 79, 84

Girder 5	17, 26, 35, 44, 53, 62, 71, 80, 85

Methodology



Node coordinates loaded from node.py



Element connectivity loaded from element.py



Bridge framing plotted in 3D



Shear force and bending moment values extruded in Y-direction



Interactive visualization using Plotly



MIDAS-style post-processing appearance



Run Task-2

python src/task2\_3d\_sfd\_bmd.py \\

&nbsp; --dataset data/screening\_task.nc \\

&nbsp; --nodes\_py data/node.py \\

&nbsp; --elements\_py data/element.py \\

&nbsp; --out outputs



Outputs



outputs/task2\_3d\_SFD.html



outputs/task2\_3d\_BMD.html



(Open HTML files in a web browser for interactive 3D view)



Notes



No manual sign flipping was performed.



Force and moment values are used exactly as stored in the Xarray dataset.



Code is modular, readable, and commented for clarity.



Submission Checklist



✅ Task-1 completed



✅ Task-2 completed



✅ ZIP file includes all relevant code and data



🔲 Video demonstration (unlisted YouTube)



🔲 GitHub repository link with osdag-admin as collaborator



🔲 PDF report explaining the implementation



License



This submission follows the Creative Commons Attribution-ShareAlike 4.0 International License as specified by FOSSEE / Osdag.



Author



Pranav Singal

Osdag Screening Task Submission

