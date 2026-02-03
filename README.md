````markdown
# Osdag Screening Task — Xarray & Plotly / Matplotlib

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC--BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

---

## 📌 About The Project

This repository contains my complete solution for the **Osdag Screening Task**, which focuses on structural engineering data visualization using **Xarray, Matplotlib, and Plotly**.

The task required:

- Extracting internal-force values from a **NetCDF (Xarray) dataset**
- Plotting **2D Shear Force Diagram (SFD)** and **2D Bending Moment Diagram (BMD)** for a specific girder
- Building **3D interactive diagrams** (SFD & BMD) for **all bridge girders**, similar to MIDAS post-processing style

The project aims to produce clean, professional, engineering-standard visual outputs while maintaining modular, readable, and well-structured Python code.

---

## 🏗️ Built With

- **Python 3.9+**
- **NumPy**
- **Xarray**
- **Matplotlib (Pyplot)**
- **Plotly**
- **Custom utilities (IO + plotting)**

---

## 🚀 Getting Started

This guide explains how to set up the project locally and run both tasks.

---

### ✔ Prerequisites

Ensure you have Python installed:

```bash
python3 --version
````

Install required libraries:

```bash
pip install -r requirements.txt
```

---

### ✔ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/osdag-screening.git
cd osdag-screening
```

Dataset is already included in:

```
data/screening_task.nc
```

---

## 🧩 Usage

Below are usage instructions for both Task-1 and Task-2.

---

### 🟦 **Task-1 — 2D SFD & BMD (Central Longitudinal Girder)**

**Girder elements used:**
`[15, 24, 33, 42, 51, 60, 69, 78, 83]`

Shear: `Vy_i`, `Vy_j`
Moment: `Mz_i`, `Mz_j`

Run:

```bash
python src/task1_2d_sfd_bmd.py \
    --dataset data/screening_task.nc \
    --nodes_py data/node.py \
    --elements_py data/element.py \
    --out outputs
```

**Outputs generated:**

* `outputs/task1_SFD.png`
* `outputs/task1_BMD.png`

---

### 🟩 **Task-2 — 3D Interactive SFD & BMD (All Girders)**

Covered Girders:

| Girder | Elements                           |
| ------ | ---------------------------------- |
| G1     | 13, 22, 31, 40, 49, 58, 67, 76, 81 |
| G2     | 14, 23, 32, 41, 50, 59, 68, 77, 82 |
| G3     | 15, 24, 33, 42, 51, 60, 69, 78, 83 |
| G4     | 16, 25, 34, 43, 52, 61, 70, 79, 84 |
| G5     | 17, 26, 35, 44, 53, 62, 71, 80, 85 |

Run:

```bash
python src/task2_3d_sfd_bmd.py \
    --dataset data/screening_task.nc \
    --nodes_py data/node.py \
    --elements_py data/element.py \
    --out outputs
```

**Outputs generated:**

* `outputs/task2_3d_SFD.html`
* `outputs/task2_3d_BMD.html`

(Open these HTML files in a browser for interactive 3D visualization.)

---

## 📦 Project Structure

```
osdag-screening/
├── src/
│   ├── task1_2d_sfd_bmd.py
│   ├── task2_3d_sfd_bmd.py
│   ├── io_utils.py
│   └── plot_utils.py
│
├── data/
│   ├── screening_task.nc
│   ├── node.py
│   └── element.py
│
├── outputs/
│   ├── task1_BMD.png
│   ├── task1_SFD.png
│   ├── task2_3d_BMD.html
│   └── task2_3d_SFD.html
│
├── requirements.txt
└── README.md
```

---

## 📊 Dataset Details

Dataset file: `screening_task.nc`
Main variable: `forces`

Available components:

```
Mx_i, Mx_j
My_i, My_j
Mz_i, Mz_j   → bending moment
Vx_i, Vx_j
Vy_i, Vy_j   → shear force
x, y, z
```

No manual sign flipping was performed; force values are used exactly as stored.

---

## 🛣 Roadmap

* Add video demonstration (YouTube)
* Improve SFD/BMD smoothing
* Add cross-section stress diagrams
* Integrate GUI for selecting girders
* Add animated 3D force extractor

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push
5. Open a Pull Request

---

## 📄 License

Distributed under the **Creative Commons Attribution–ShareAlike 4.0 International License**.

---

## 📬 Contact

**Your Name**
Email: [your-email@example.com](mailto:your-email@example.com)
LinkedIn: your-linkedin
GitHub: your-github

---

## 🙌 Acknowledgments

* Osdag Team (IIT Bombay)
* Xarray Documentation
* Plotly Python Docs
* Matplotlib Community
* NumPy Community

---

```


Just tell me!
```
