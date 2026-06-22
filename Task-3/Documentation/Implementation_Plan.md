# Implementation Plan - Time Series Dashboard & Data Restructuring

This plan outlines the implementation of **Task-3**, which requires:
1. Re-structuring the project files into standard directories (`Dataset/`, `Documentation/`, `Screenshots/`).
2. Creating a Jupyter Notebook `Analysis.ipynb` for the analysis part.
3. Creating a GUI application `dashboard.py` in Tkinter with a dark, premium theme containing several visualizations.
4. Implementing a new time-series line chart showing cumulative installs over time by category, filtered and translated according to rules, with shaded growth periods (>20% MoM).
5. Ensuring the time-series visualization displays only between 6 PM and 9 PM IST.
6. Generating and organizing screenshots for both visible and hidden states of the dashboard.

## Proposed Changes

### 1. File Restructuring

We will move the CSV files into a `Dataset` folder, and place documentation and screenshots in their respective subdirectories.

#### [NEW] [Play Store Data.csv](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Dataset/Play%20Store%20Data.csv) (Moved)
#### [NEW] [User Reviews.csv](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Dataset/User%20Reviews.csv) (Moved)
#### [DELETE] [Play Store Data.csv](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Play%20Store%20Data.csv)
#### [DELETE] [User Reviews.csv](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/User%20Reviews.csv)

---

### 2. Documentation and Metadata

#### [NEW] [Implementation_Plan.md](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Documentation/Implementation_Plan.md)
#### [NEW] [Walkthrough.md](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Documentation/Walkthrough.md)
#### [NEW] [README.md](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/README.md)

---

### 3. Analysis Code

#### [NEW] [Analysis.ipynb](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Analysis.ipynb)
A clean, documented Jupyter Notebook executing the exact data preparation steps, printing stats, and saving the standalone graph to `Screenshots/Graph1.png`.

---

### 4. Interactive Dashboard

#### [NEW] [dashboard.py](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/dashboard.py)
A Tkinter application that runs the interactive dashboard with:
- **Premium Dark UI**: Using a slate-charcoal and neon-accent theme (deep charcoal background, rounded card containers, custom styled tabs, clean typography).
- **Sidebar Tabbed Layout**: Allowing easy navigation between overview plots, ratings, ML evaluations, and the new time-series installs trend plot.
- **Dynamic Time Series Graph Visibility**: Check IST timezone current time. If it is between 6:00 PM IST and 9:00 PM IST, the trend graph is rendered and active. Outside this time window, a placeholder message ("Visualization Locked: Only available between 6 PM and 9 PM IST") will be displayed.
- **Data Filtering**:
  - Exclude app names starting with X, Y, Z (case-insensitive).
  - Exclude app names containing 'S' (case-insensitive).
  - Filter for categories starting with E, C, B, OR equal to DATING.
  - Filter for apps with reviews > 500.
- **Category Translations**:
  - `BEAUTY` -> `सौंदर्य` (Hindi)
  - `BUSINESS` -> `வணிகம்` (Tamil)
  - `DATING` -> `Dating` (German)
  - Others will use their default names.
- **Shaded Growth Periods**: Use matplotlib `fill_between` to shade under the category curve between consecutive months where MoM cumulative installs increase by >20%.
- **Fonts**: Set matplotlib font to `Nirmala UI` to support Tamil and Devanagari scripts natively on Windows.

---

### 5. Screenshots

We will write a screenshot generator script that runs the dashboard in a mocked time environment to produce:
- `Screenshots/Graph1.png` (standalone matplotlib plot)
- `Screenshots/Dashboard_Visible.png` (dashboard showing the active time-series tab)
- `Screenshots/Dashboard_Hidden.png` (dashboard showing the locked/hidden time-series tab)

## Verification Plan

### Manual Verification
- We will run `python dashboard.py` with mock time settings to inspect the visible/hidden layouts.
- We will verify that Devanagari and Tamil characters are rendered correctly without missing glyphs.
- We will verify that app filtering is correctly implemented (checking list of categories, starts with X/Y/Z, contains S, and reviews > 500).
- We will check that `Graph1.png` is generated correctly.
