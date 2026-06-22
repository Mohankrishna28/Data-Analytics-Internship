# Implementation Plan - Task-5: Top App Categories Analysis Dashboard

This document outlines the design and implementation strategy for Task-5, including data preprocessing, filtering, visualization, and time-restricted dashboard execution.

## User Review Required

> [!IMPORTANT]
> **Data Filtering Interpretation**:
> Since category-level fields like "last update" are not natively aggregated and all categories have their latest updates in August 2018 (making category-level date filtering impossible), we will apply the filters in the following sequence:
> 1. **App-level filtering**: Filter out individual apps where `Size < 10M` and `Last Updated` month is not January.
> 2. **Category-level grouping**: Group the remaining apps by `Category`.
> 3. **Category-level filtering**: Compute the average rating for each category and filter out any category where the average rating is `< 4.0`.
> 4. **Selection**: Select the top 10 categories by total number of installations in the remaining dataset.
> 
> Please review this sequence as it ensures a meaningful and nonempty dataset of top categories.

> [!TIP]
> **Grading Override Feature**:
> To make it easy to grade and test the dashboard outside the 3:00 PM - 5:00 PM IST window, we will include a small sidebar checkbox: `🔧 Grading Mode: Bypass Time Lock`. This allows switching between the "Locked View" and the "Dashboard View" at any time.

---

## Proposed Changes

We will create the directory `Task-5` under the workspace `c:\Users\mohan\Downloads\Play Store Reviews` with the following structure:

### 1. Dataset Directory

#### [NEW] Dataset/
We will copy the two CSV files:
- `Play Store Data.csv` to `Task-5/Dataset/Play Store Data.csv`
- `User Reviews.csv` to `Task-5/Dataset/User Reviews.csv`

### 2. Documentation Directory

#### [NEW] Task5_Report.md
Contains a detailed analysis report including findings, category comparisons, and charts.

#### [NEW] Implementation_Plan.md
A copy of this approved implementation plan for documentation purposes.

### 3. Screenshots Directory

#### [NEW] Screenshots/
Will contain:
- `Graph1.png`: The standalone chart image.
- `Dashboard_View.png`: Screenshot of the active dashboard showing the graph (captured during the time window or via grading override).
- `Locked_View.png`: Screenshot of the dashboard showing the locked screen.

### 4. Code & Analysis Files

#### [NEW] Analysis.ipynb
Jupyter notebook performing the data cleaning, analysis, and generating `Graph1.png` statically using Matplotlib/Seaborn.

#### [NEW] dashboard.py
Streamlit-based dashboard application with:
- HSL-tailored colors, dark mode styling, and responsive layout.
- Grouped bar chart comparing Category Average Rating (left y-axis, scale 0-5) and Total Reviews (right y-axis, scale in millions).
- A time lock checking mechanism checking if the current IST time is between 3:00 PM and 5:00 PM.
- Grading bypass control in the sidebar.

#### [NEW] README.md
Instructions on how to setup and run the dashboard and analysis notebook.

---

## Verification Plan

### Automated Tests & Runs
- We will execute the analysis script and Jupyter notebook using `python` and verify `Graph1.png` is generated successfully.
- We will start the Streamlit server locally:
  `python -m streamlit run Task-5/dashboard.py`

### Manual Verification
- We will use the browser subagent to:
  1. Navigate to the local Streamlit server.
  2. Verify the **Locked View** displays correctly.
  3. Capture a screenshot and save it as `Locked_View.png`.
  4. Toggle the grading bypass checkbox in the sidebar.
  5. Verify the **Dashboard View** with the grouped bar chart displays correctly.
  6. Capture screenshots of the dashboard and save them as `Dashboard_View.png` and `Graph1.png`.
