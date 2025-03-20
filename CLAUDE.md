# CLAUDE.md - Wind Data Repository Guide

Welcome to this repository for **wind data archival and cleaning**. Please read and follow these guidelines before generating or modifying any files.

## Repository Purpose

This repo houses raw wind measurement data for two main projects:

1. **Pismo Wind Study** – A wind simulation study with multiple sensors in an overwintering grove in Pismo, California. The data suffers from:
   - Gaps in time
   - Erroneously high measurements
   - Time shift issues (e.g., daylight savings)
2. **VSFB Camera Study** – A wind measurement paired with image data at Vandenberg Space Force Base. Fewer data issues, but daylight savings time still applies.

Your job is to help produce a **single cleaned CSV** per project while keeping the user-facing Quarto documents **light on code** and **heavy on explanation**.

---

## Technical Overview

1. **Primary Languages**:  
   - **R** (using `tidyverse`) for data wrangling.  
   - **Quarto** (`.qmd` files) for the main narrative documents.

2. **Data Folders**:
   - `/raw_data` holds all wind files prior to any modifications.
   - `pismo/` and `vsfb/` will contain project-specific outputs and possibly project-specific scripts.
   - `scripts/` holds **modular R scripts** with function definitions you can source.

3. **Cleaning Workflow**:
   - Each project has (or will have) a **Quarto** document:  
     - `wind_cleaning_pismo.qmd`  
     - `wind_cleaning_vsfb.qmd`
   - These `.qmd` files **source** R scripts from `scripts/` to keep inline code minimal.
   - Each `.qmd` runs from top to bottom, reading from `/raw_data`, performing cleaning, then writing out a final CSV.

4. **AI-Editable Code**:
   - Keep each `.R` file **under ~500 lines** to ensure the user can easily share code blocks with you in future prompts.
   - Within these `.R` files, use clear function names and docstrings (e.g., `#'` comments) so it’s easy to see each function’s purpose.
   - If you need to split logic into multiple scripts (e.g., `functions_pismo.R`, `functions_vsfb.R`, `utils.R`), do so to maintain readability.

---

## Expectations & Guidelines for You, the LLM

1. **Avoid Over-Verbose Code in Quarto**:  
   - The user will supply narrative around the data-wrangling steps.  
   - You should place **most R logic in separate files** under `scripts/`.
   - In Quarto documents, limit yourself to brief code chunks that call the helper functions.

2. **Respect File Boundaries**:  
   - Do not place multi-hundred-line functions in a single script.  
   - When asked to modify or add a function, create or update the relevant `.R` file in the `scripts/` folder.

3. **Time Zone / DST Handling**:  
   - Be prepared to shift timestamps or adjust for daylight savings.  
   - The user may ask for a standardized timezone.

4. **Data Validations**:
   - Look out for numeric outliers, missing data, or duplicate rows.  
   - The user might ask you to remove extreme wind-speed spikes.

5. **Project Separation**:
   - The user may integrate a QGIS metadata table to identify which raw files belong to each project.  
   - Keep Pismo logic independent of Camera Study logic, unless the user explicitly wants a shared function.

6. **Minimal Commentary**:
   - The user typically wants to control the narrative in the Quarto files.  
   - Provide concise in-line comments within R scripts only to clarify function behavior or parameters.

---

## Possible Next Steps

- **Pismo Wind Study**:  
  - Write or refine a function to parse raw wind logs.  
  - Add corrections for daylight savings time.  
  - Filter out erroneous spikes.  
  - Summarize data into a final CSV.

- **VSFB Camera Study**:  
  - Similar data read-in and DST adjustments, but with fewer known anomalies.  
  - Output a single CSV for downstream analysis.

*(The user will confirm details or request new logic as the project evolves.)*

---

## Final Note

Remember, **you** (the LLM) should read and adhere to this file’s guidelines before any new session or significant code generation. This ensures:

1. The Quarto docs remain short and user-friendly.  
2. The R scripts in `scripts/` remain modular, AI-editable, and version-controlled.  
3. We produce two final CSV datasets, one for each project, following best practices in data cleaning.

Thank you for your cooperation—happy coding!