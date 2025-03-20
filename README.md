# Wind Data Archive and Cleaning

This repository contains raw wind data and scripts for processing it into two final, analysis-ready datasets. There are two main projects:

- **Pismo Wind Study**: Overwintering grove wind measurements (subject to data gaps, time shifts, and outliers).  
- **VSFB Camera Study**: Wind measurements paired with image data (mainly daylight savings adjustments needed).

## Project Structure

```
.
├── raw_data/
│   └── ... (original CSV/log files)
├── pismo/
│   └── (outputs and project-specific scripts)
├── camera_study/
│   └── (outputs and project-specific scripts)
├── scripts/
│   └── (Python functions for data cleaning/modular logic)
├── wind_cleaning_pismo.qmd       (Quarto doc for Pismo workflow)
├── wind_cleaning_camera.qmd      (Quarto doc for Camera Study workflow)
└── README.md                     (this file)
```

## Quick Start

1. **Clone this repo** to your local machine.  
2. Install [**Python** (≥ 3.8)](https://www.python.org/downloads/) and [**Quarto**](https://quarto.org/).  
3. Install the required Python packages:
   ```bash
   pip install pandas numpy matplotlib
   ```
4. Open either `wind_cleaning_pismo.qmd` or `wind_cleaning_camera.qmd` in your preferred environment.
5. **Render** the Quarto document (e.g., click “Render” in RStudio or run `quarto render wind_cleaning_pismo.qmd` in the terminal).

The final cleaned CSVs will appear in the corresponding project folder (`pismo/` or `camera_study/`).

## Notes

- **Data Cleaning**: Most of the data-wrangling logic is kept in separate `.py` scripts under `scripts/`, so the Quarto documents remain primarily explanatory.
- **Daylight Savings & Gaps**: Time shifts, missing data, and outliers are addressed within the workflow; any manual interventions will be noted in the Quarto text.
- **License**: License information is not currently specified.  
- **Support**: If you have questions, open an Issue or contact the repository owner.

---
