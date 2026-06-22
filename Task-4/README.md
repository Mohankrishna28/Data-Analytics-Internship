# Play Store App Market Intelligence Dashboard

This project is a visual intelligence dashboard built on Google Play Store app records. It analyzes and visualizes cumulative installs over time, with advanced filters, localized legends, MoM growth-based highlighting, and a time-based security lock.

## Project Structure

```text
Task-4/
├── Dataset/
│   ├── Play Store Data.csv
│   └── User Reviews.csv
│
├── Screenshots/
│   ├── Graph1.png           # Standalone High-Growth Highlighted Chart (Matplotlib)
│   ├── Dashboard_View.png   # Unlocked Dashboard view (between 4 PM and 6 PM IST)
│   └── Locked_View.png      # Locked Dashboard view (outside the review window)
│
├── Documentation/
│   ├── Implementation_Plan.md
│   └── Walkthrough.md
│
├── Analysis.ipynb           # Complete Data Prep and Analytics Notebook
├── dashboard.py             # Streamlit Dashboard App
└── README.md                # Project Overview and Setup Guide
```

---

## Analytical Requirements & Logic

### 1. Data Prep and Filtering Pipeline
Before visual mapping, the dataset is loaded and cleaned of corruption (such as removing category `'1.9'`). It then applies five strict filters:
1. **Rating Constraint**: Include only apps with average ratings $\ge 4.2$.
2. **Naming Constraint**: Exclude apps with names containing any digits `[0-9]`.
3. **Category Constraint**: Include only categories starting with **"T"** or **"P"** (`TRAVEL_AND_LOCAL`, `TOOLS`, `PRODUCTIVITY`, `PHOTOGRAPHY`, `PERSONALIZATION`, `PARENTING`).
4. **Popularity Constraint**: Apps must have more than **1,000** reviews.
5. **Size Constraint**: Apps must have sizes between **20 MB and 80 MB** (kilobytes are converted dynamically, and "Varies with device" is filtered out).

After filtering, **139 apps** match all conditions.

### 2. Cumulative Install Math and Timeline Reindexing
To display the cumulative growth over time without visual distortions due to sparse updates:
1. A continuous monthly timeline is built spanning from the minimum date (`Nov 2014`) to the maximum date (`Aug 2018`) in the filtered records.
2. For each category and month, installs of apps updated in that month are aggregated (non-update months are filled with `0` installs).
3. The running sum is computed chronologically for each category.

### 3. Localization / Translation Mapping
The legend entries are translated directly into the requested languages:
*   **"Travel & Local"** $\rightarrow$ French: `"Voyage et guides locaux"`
*   **"Productivity"** $\rightarrow$ Spanish: `"Productividad"`
*   **"Photography"** $\rightarrow$ Japanese: `"写真"`
*   *(Other categories "Tools", "Personalization", "Parenting" remain in English).*

### 4. High-Growth Highlighting (>25% MoM)
*   **Matplotlib Plot (`Graph1.png`)**: Draws the area chart month-by-month. If a month experiences a month-over-month (MoM) cumulative install increase $> 25\%$ for any category, the alpha value of the category areas in that segment is set to a highly-saturated **`0.95`**. Regular months are muted at **`0.40`** opacity.
*   **Plotly Plot**: Uses background yellow shaded regions (`fig.add_vrect`) with special indicator nodes and custom hover tooltips showing which categories drove the growth.

### 5. Time-based Access Control
The dashboard is strictly locked and cannot be accessed outside **4:00 PM IST to 6:00 PM IST** (16:00 - 18:00).
*   **Standard Mode**: Checks local system time translated into the Indian Standard Time (IST) zone (`Asia/Kolkata`).
*   **Simulation / Developer Mode**: A checkbox in the sidebar allows developers and reviewers to disable system time and manually adjust a slider to simulate the active hour (e.g. 5 PM) to unlock and test the interactive dashboard.

---

## Setup and Run Instructions

### Prerequisites
Ensure python packages are installed:
```bash
pip install pandas numpy matplotlib plotly streamlit pytz
```

### Run the Dashboard
Since the application runs a custom compatibility patch to run seamlessly under Python 3.14, execute the following command in the terminal to launch:
```bash
python -m streamlit run Task-4/dashboard.py
```
Or use the wrapper execution script:
```bash
python C:\Users\mohan\.gemini\antigravity-ide\scratch\run_dashboard.py
```

Open `http://localhost:8501` in your browser.
To view the unlocked dashboard state, navigate to the sidebar, uncheck **"Use System Time (IST)"**, and slide the simulated hour to **17** (5 PM).
