# Google Play Store Data Analytics & Intelligence Dashboard

Welcome to the **Google Play Store Analytics** repository. This project is a comprehensive suite of data cleaning, statistical analysis, machine learning modeling, and interactive visualization dashboards developed during a Data Analytics Internship. 

The repository is structured into six independent tasks, each addressing specific analytical criteria, data pipelines, localized translation requirements, and time-based security lockouts.

---

## 📁 Repository Structure & Tasks Overview

This repository is organized into six self-contained task folders (`Task-1` through `Task-6`). Each folder includes its own raw or processed datasets, interactive dashboards, Jupyter notebooks, visual screenshots, and walkthrough documentation.

| Task | Focus Area | Key Visualizations | Time Lock (IST) | Directory Link |
|:---:|:---|:---|:---:|:---:|
| **[Task-1](#-task-1-bubble-chart-analysis--tkinter)** | App Size vs. Rating Analysis | Interactive Matplotlib Bubble Chart with localized labels (Hindi, Tamil, German) & Tkinter layout | 5:00 PM – 7:00 PM | [Task-1](file:///c:/Users/mohan/OneDrive/Documents/Task_1_Google_Play_Store_Analysis/Task-1) |
| **[Task-2](#-task-2-global-installation-choropleth-map)** | Geographical Distribution Analysis | Plotly Interactive Choropleth Map mapping top categories to representative countries | 6:00 PM – 8:00 PM | [Task-2](file:///c:/Users/mohan/OneDrive/Documents/Task_1_Google_Play_Store_Analysis/Task-2) |
| **[Task-3](#-task-3-tabbed-analysis-dashboard--random-forest)** | Sentiment & Growth Trend Tracking | Modern Dark-Themed GUI with cumulative install area charts and VADER sentiment analytics | 6:00 PM – 9:00 PM | [Task-3](file:///c:/Users/mohan/OneDrive/Documents/Task_1_Google_Play_Store_Analysis/Task-3) |
| **[Task-4](#-task-4-cumulative-growth-intelligence-dashboard)** | Market Intelligence Area Charting | Streamlit Dashboard showcasing category growth over time with dynamic >25% MoM highlighting | 4:00 PM – 6:00 PM | [Task-4](file:///c:/Users/mohan/OneDrive/Documents/Task_1_Google_Play_Store_Analysis/Task-4) |
| **[Task-5](#-task-5-grouped-category-comparison)** | Aggregated Category Comparison | Streamlit Dashboard showcasing grouped column distributions and top category metrics | 3:00 PM – 5:00 PM | [Task-5](file:///c:/Users/mohan/OneDrive/Documents/Task_1_Google_Play_Store_Analysis/Task-5) |
| **[Task-6](#-task-6-dual-axis-revenue-vs-installs-dashboard)** | Revenue vs. Installation Metrics | Streamlit Dashboard containing dual-axis combo charts for free vs. paid app comparisons | 1:00 PM – 2:00 PM | [Task-6](file:///c:/Users/mohan/OneDrive/Documents/Task_1_Google_Play_Store_Analysis/Task-6) |

---

## ⚙️ Environment Setup & Installation

To run any of the notebooks or dashboards, ensure you have **Python 3.8+** installed. You can install all required dependencies by running:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn nltk plotly streamlit pytz kaleido
```

*Note: `pytz` is required for time lock timezone validation. `kaleido` is recommended for exporting static Plotly plots.*

---

## 🔍 Task-Specific Details

### 📊 Task-1: Bubble Chart Analysis & Tkinter
*   **Objective**: Analyze the correlation between App Size (MB) and Average Rating for the most popular categories.
*   **Data Pipeline Filters**:
    *   Rating > 3.5 & Installs > 50,000.
    *   Reviews > 500 & Sentiment Subjectivity > 0.5.
    *   Exclude any app name containing the letter `"S"` or `"s"` (case-insensitive).
*   **Design & Translations**:
    *   Vibrant **Pink** highlight for the `GAME` category.
    *   Localizations: `BEAUTY` ➔ `सौंदर्य` (Hindi), `BUSINESS` ➔ `வணிகம்` (Tamil), `DATING` ➔ `Dating (Deutsch)` (German).
*   **Time Lock**: Only available from **5 PM to 7 PM IST**. Displays a visual lock screen outside this window.

### 🗺️ Task-2: Global Installation Choropleth Map
*   **Objective**: Aggregate global installation metrics and represent them geographically.
*   **Data Pipeline Filters**: Exclude categories starting with `'A'`, `'C'`, `'G'`, or `'S'`. Display the top 5 remaining categories.
*   **Geographical Mapping**:
    *   `PRODUCTIVITY` ➔ USA, `TOOLS` ➔ India (IND), `FAMILY` ➔ Germany (DEU), `PHOTOGRAPHY` ➔ Brazil (BRA), `NEWS_AND_MAGAZINES` ➔ Australia (AUS).
*   **Design Details**: Interactive tooltips with comma-formatted installs. Outlines countries with installs exceeding 1 Million with a bold **gold border**.
*   **Time Lock**: Only available from **6 PM to 8 PM IST**. (Bypass via `--test-mode` command-line flag).

### 📈 Task-3: Tabbed Analysis Dashboard & Random Forest
*   **Objective**: Integrate sentiment analysis (VADER) and install trends in a unified interface.
*   **Design & Layout**: Built using a modern charcoal and matte violet accent aesthetic.
*   **Visual Highlights**: Cumulative area chart with shaded regions signifying >20% month-over-month (MoM) growth. Nirmala UI font overrides for Hindi/Tamil rendering.
*   **Machine Learning**: Features a Random Forest regressor to predict app ratings.
*   **Time Lock**: Time-series installs tab is restricted to **6 PM to 9 PM IST** (Bypass via `OVERRIDE_TIME` environment variable).

### 💡 Task-4: Cumulative Growth Intelligence Dashboard
*   **Objective**: Dynamic monitoring of cumulative installs with strict size and name filtering.
*   **Data Pipeline Filters**:
    *   Rating $\ge 4.2$ & reviews > 1,000.
    *   Exclude apps containing numbers/digits in their names.
    *   Categories starting with "T" or "P" only. Size strictly between 20 MB and 80 MB.
*   **Design Details**: Areas on the Matplotlib chart are shaded with a high-saturation `0.95` opacity during periods of >25% MoM growth (regular months are muted at `0.40`).
*   **Time Lock**: Restricted to **4 PM to 6 PM IST** (Bypass via Streamlit sidebar "Grading Mode" slider).

### 📊 Task-5: Grouped Category Comparison
*   **Objective**: Highlight comparisons between categories on rating and size metrics.
*   **Visualization**: Interactive Plotly grouped bar chart representing multiple variables per category.
*   **Time Lock**: Restricted to **3 PM to 5 PM IST** (Bypass via Streamlit sidebar grading mode checkbox).

### ⚖️ Task-6: Dual-Axis Revenue vs. Installs Dashboard
*   **Objective**: Compare average installs and revenue generated across free vs. paid apps.
*   **Data Pipeline Filters**:
    *   Installs $\ge 10,000$ & Android Version $> 4.0$.
    *   Size $> 15$ MB & Content Rating: 'Everyone'.
    *   Paid apps must have Revenue $\ge \$10,000$.
    *   App name length must be $\le 30$ characters.
*   **Visualization**: Sleek dual-axis combo chart plotting average installs (left axis) and average revenue (right axis) for the top 3 categories.
*   **Time Lock**: Restricted to **1 PM to 2 PM IST** (Bypass via Streamlit sidebar Time Simulation Mode).

---

## 🚀 Execution Guide

### Jupyter Notebooks
Navigate to any task directory and run the interactive prototype:
```bash
jupyter notebook Task-[1-6]/Analysis.ipynb
```

### Tkinter Applications (Tasks 1, 2, 3)
Run the standalone graphical user interface from the root directory:
```bash
python Task-2/dashboard.py --test-mode
python Task-3/dashboard.py
```

### Streamlit Dashboards (Tasks 4, 5, 6)
To run the Streamlit dashboards, execute:
```bash
streamlit run Task-4/dashboard.py
streamlit run Task-5/dashboard.py
streamlit run Task-6/dashboard.py
```
*(Use the respective sidebar checkboxes/controls to bypass active time-gates for evaluation outside the scheduled window).*
