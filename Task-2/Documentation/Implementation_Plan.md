# Implementation Plan - Google Play Store Analysis (Task 2)

This plan details the design, data cleaning, and implementation steps for creating an interactive Plotly Choropleth map that visualizes global installs by category.

## User Review Required

> [!IMPORTANT]
> **Lack of Country Data**: Standard Google Play Store datasets (including the provided one) do not contain a country column. To show this on a Choropleth map, we will map each of the top 5 filtered categories to a representative country ISO Alpha-3 code (e.g., USA, India, Germany, Brazil, Australia).
>
> **Time-Based Gate**: The visualization must only show between 6 PM IST and 8 PM IST. Outside of this time, a message indicating the chart is hidden will be displayed in the notebook and Tkinter dashboard. We will include a `TEST_MODE` toggle to allow easy verification outside of these hours.

---

## Proposed Changes

We will create a new directory structure `Task-2` within the workspace:

```text
Task-2/
├── Dataset/
│   └── Play Store Data.csv     # Copied dataset
├── Analysis.ipynb              # Notebook containing cleaning, mapping, and Tkinter code
├── Screenshots/                # Visual verification outputs
│   └── choropleth_map.png
└── Documentation/              # Documentation outputs
    ├── README.md
    └── choropleth_map.html     # Interactive HTML version of the Plotly map
```

### 1. Data Processing & Filter Logic

We will write cleaning code in [Analysis.ipynb](../Analysis.ipynb):
- Clean the `Installs` column by removing commas and `+` symbols, converting values to integers.
- Filter out categories starting with letters **'A'**, **'C'**, **'G'**, or **'S'** (case-insensitive).
- Group the data by category to calculate total installs per category.
- Sort to identify the **top 5** app categories.
- Ensure that the top 5 categories have installs exceeding 1 million (all exceed 7B).

### 2. Geographical Mapping & Plotly Choropleth Map

- Define a mapping dictionary associating categories with country ISO Alpha-3 codes:
  - `PRODUCTIVITY` -> `USA` (United States)
  - `TOOLS` -> `IND` (India)
  - `FAMILY` -> `DEU` (Germany)
  - `PHOTOGRAPHY` -> `BRA` (Brazil)
  - `NEWS_AND_MAGAZINES` -> `AUS` (Australia)
- Create a pandas DataFrame containing these country mappings and their total category installs.
- Build the Choropleth map using `plotly.graph_objects.Choropleth` (or `plotly.express.choropleth`).
- Highlight regions where installs exceed 1 million by styling their borders with a distinct color (e.g., gold or red) and width.
- Add an interactive slider or dropdown in the notebook so the user can filter/inspect categories.

### 3. IST Time Restriction

- Determine if the current time is between **6:00 PM IST** and **8:00 PM IST** (hours 18:00 to 20:00).
- If outside this window:
  - Notebook output: Print a placeholder message `Dashboard Hidden: The Category Installs Choropleth Map is only available between 6 PM and 8 PM IST.`
  - Tkinter Dashboard: Exclude or hide the Choropleth map visualization panel.
- Implement an override toggle (`TEST_MODE = True`) to bypass the gate for manual testing and screenshot generation.

### 4. Tkinter Dashboard Integration

- In [Analysis.ipynb](../Analysis.ipynb), add a class `AppDashboard` using `tkinter` that acts as the GUI.
- Save the Plotly choropleth map to `Task-2/Screenshots/choropleth_map.png`.
- In the Tkinter dashboard, render this static image inside a panel if the time is within the allowed window. If not, show an "Access Restricted" message panel.

---

## Verification Plan

### Automated Verification
- Run a Python script to verify category filtering logic (A, C, G, S exclusion).
- Run Python unit tests to confirm the timezone conversion (IST) and time-gating check functions.

### Manual Verification
- Run the Tkinter dashboard with `TEST_MODE = True` to verify the map loads properly.
- Run the dashboard with `TEST_MODE = False` to verify it displays the hidden message (since local time is currently 2:14 PM IST).
- Verify files are created in the correct `Task-2` directory layout.
- Generate screenshots of both active and inactive states in `Task-2/Screenshots/`.
