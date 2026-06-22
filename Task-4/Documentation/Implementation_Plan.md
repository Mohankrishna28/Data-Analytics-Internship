# Implementation Plan - Play Store App Analytics Stacked Area Chart & Dashboard

This document details the plan to create a stacked area chart visualization and interactive dashboard for Google Play Store app data, including strict data filtering, category translations, month-over-month growth highlighting, and time-based access control.

## User Review Required

> [!IMPORTANT]
> **Time-based Lock**: The visualization is strictly restricted to be displayed between **4:00 PM IST and 6:00 PM IST**.
> Outside this time window, the dashboard will display a **Locked Screen** indicating that access is restricted.
> To make it easy for developers and reviewers to test the dashboard at any hour, we will include a **"Time Override / Simulation"** widget in the sidebar. This allows toggling between real system time and a custom simulated hour.

> [!NOTE]
> **High Growth Highlighting**: We will highlight months with >25% month-over-month (MoM) cumulative install growth.
> To make this visually spectacular, we will implement **two visualization modes** in the dashboard:
> 1. **Interactive Plotly Area Chart**: Highlights high-growth months using vertical golden bands with hover tooltips.
> 2. **Segmented Matplotlib Area Chart**: Directly increases the color intensity of the specific category's area bands during the months they experienced >25% MoM growth.

---

## Open Questions

None at this time. The requirements are fully detailed.

---

## Proposed Changes

We will create a new folder `Task-4/` with the specified structure.

### Component 1: Data Analytics Notebook

#### [NEW] [Analysis.ipynb](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Task-4/Analysis.ipynb)
A Jupyter Notebook containing:
- Data loading and cleaning of `Play Store Data.csv`.
- Implementing the 5 filters:
  1. Average rating $\ge 4.2$.
  2. App names containing no numbers.
  3. App categories starting with "T" or "P".
  4. Reviews $> 1,000$.
  5. App sizes between 20 MB and 80 MB.
- Reindexing the dataset to a continuous monthly timeline (from min to max date in filtered data) to handle sparse data points.
- Calculating cumulative installs and MoM growth percentage.
- Translating legend categories:
  - "Travel & Local" $\rightarrow$ "Voyage et guides locaux" (French)
  - "Productivity" $\rightarrow$ "Productividad" (Spanish)
  - "Photography" $\rightarrow$ "写真" (Japanese)
- Visualizing and saving `Graph1.png` to the screenshots folder.

### Component 2: Streamlit Dashboard Application

#### [NEW] [dashboard.py](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Task-4/dashboard.py)
A Streamlit web application that:
- Detects the current local time in Indian Standard Time (IST).
- Displays a premium, themed lock screen if the current time is outside 4 PM - 6 PM IST.
- If within the 4 PM - 6 PM IST window (or if bypassed/simulated), renders:
  - KPI cards with key metrics (total installs, total apps, top category).
  - The stacked area chart with category translations.
  - Controls to adjust filtering parameters interactively.
  - A toggle to switch between Plotly (Interactive) and Matplotlib (Precise color-intensity highlighting) chart versions.

### Component 3: Project Documentation & Assets

#### [NEW] [README.md](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Task-4/README.md)
Instructions on how to setup, run, and interact with the dashboard.

#### [NEW] [Implementation_Plan.md](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Task-4/Documentation/Implementation_Plan.md)
A copy of this implementation plan for the user folder.

#### [NEW] [Walkthrough.md](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Task-4/Documentation/Walkthrough.md)
A final project walkthrough highlighting the results, screenshots, and visual outputs.

#### [NEW] [Screenshots](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Task-4/Screenshots/)
- `Graph1.png`: Standalone high-growth highlighted stacked area chart.
- `Dashboard_View.png`: Unlocked dashboard view displaying the chart.
- `Locked_View.png`: Locked dashboard view displaying the access restriction.

---

## Verification Plan

### Automated Verification
- We will run a python verification script to ensure data filters select the exact 139 records.
- We will test the date-parsing and cumulative math.

### Manual / Visual Verification
1. We will run `streamlit run Task-4/dashboard.py` on a local port.
2. We will use the browser subagent to:
   - Navigate to the running dashboard outside 4-6 PM (locked state) and capture `Locked_View.png`.
   - Toggle the time simulation to 5 PM (unlocked state), view the chart, and capture `Dashboard_View.png`.
   - Check the translations in the legend.
   - Verify the color intensity highlight on high-growth months.
