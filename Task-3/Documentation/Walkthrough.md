# Walkthrough - Play Store Reviews & Installs Analysis

This walkthrough summarizes the changes made to complete **Task-3**, including dataset restructuring, creating the Jupyter Notebook, developing the Tkinter dashboard, and generating screenshots.

## Changes Made

### 1. File Restructuring
We created structured directories and moved datasets:
- Moved original CSVs into `Dataset/Play Store Data.csv` and `Dataset/User Reviews.csv`.
- Created documentation in `Documentation/` and screenshots in `Screenshots/`.

### 2. Time-Series Analysis Notebook
- Created [Analysis.ipynb](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Analysis.ipynb) to clean raw data, parse date-times, apply custom filters, resample to consecutive months, calculate cumulative installs, compute month-over-month (MoM) growth rates, and plot the trend.
- Switched the Y-axis to a **logarithmic scale** to prevent high-install categories (like COMMUNICATION) from compressing other categories (like BEAUTY or BUSINESS), making all categories clearly readable.
- Saved the standalone installs trend line chart to [Graph1.png](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Screenshots/Graph1.png).

### 3. Dynamic Dark-Themed GUI
- Created [dashboard.py](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/dashboard.py) with a slate-charcoal and neon-violet style.
- Developed left sidebar buttons for tab-based navigation across overview charts, user reviews sentiments, installation volumes, revenue metrics, and rating predictors.
- The new Time Series plot is displayed only when the dashboard current time in IST is between **6:00 PM and 9:00 PM**.
- Shaded areas under each category's curve down to the baseline `y2=1` where the cumulative installs growth rate exceeded 20% MoM.
- Applied category name translations:
  - `BEAUTY` -> `सौंदर्य` (Hindi)
  - `BUSINESS` -> `வணிகம்` (Tamil)
  - `DATING` -> `Verabredung` (German)
- Set Matplotlib default font to `Nirmala UI` to natively support Hindi and Tamil rendering on Windows.

---

## Shaded Cumulative Installs Trend Graph
Below is the standalone line chart showing the total cumulative installs over time by category, with growth periods (>20% MoM) shaded under the curve:

![Installs Trend Graph (Graph1.png)](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Screenshots/Graph1.png)

---

## Interactive Dashboard States

### 1. Visible State (Between 6 PM and 9 PM IST)
When accessed during the permitted hours, the Time Series tab displays the interactive Matplotlib plot:

![Dashboard in Visible State (Dashboard_Visible.png)](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Screenshots/Dashboard_Visible.png)

### 2. Hidden State (Outside 6 PM - 9 PM IST Window)
When accessed outside of the permitted hours, the Time Series tab is replaced by a visual lock screen:

![Dashboard in Hidden/Locked State (Dashboard_Hidden.png)](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Screenshots/Dashboard_Hidden.png)
