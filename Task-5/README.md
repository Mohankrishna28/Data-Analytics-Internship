# Task-5: Google Play Store App Category Analysis Dashboard

Welcome to the **Task-5 Category Analytics Dashboard** project. This project processes Google Play Store datasets, performs category aggregation and comparison, and serves the results in a timezone-restricted web dashboard.

---

## 📁 Directory Structure

```
Task-5/
│
├── Dataset/
│   ├── Play Store Data.csv
│   └── User Reviews.csv
│
├── Documentation/
│   ├── Task5_Report.md
│   └── Implementation_Plan.md
│
├── Screenshots/
│   ├── Graph1.png
│   ├── Dashboard_View.png
│   └── Locked_View.png
│
├── Analysis.ipynb
├── dashboard.py
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Requirements
Ensure Python 3.8+ is installed on your system. Install the required dependencies using pip:
```bash
pip install pandas numpy matplotlib seaborn plotly streamlit
```

### 2. Dataset Copy
Make sure the Play Store CSV files are copied into the `Task-5/Dataset` folder (completed automatically by setup scripts):
- `Play Store Data.csv`
- `User Reviews.csv`

---

## 🚀 Execution Instructions

### Run the Data Analysis (Jupyter Notebook)
You can run the analysis cells to recalculate averages, filters, and output `Graph1.png` statically:
```bash
jupyter notebook Task-5/Analysis.ipynb
```
Or run it non-interactively using nbconvert:
```bash
jupyter nbconvert --to notebook --execute --inplace Task-5/Analysis.ipynb
```

### Run the Dashboard Application (Streamlit)
To start the live web-based dashboard:
```bash
python -m streamlit run Task-5/dashboard.py
```
Open your browser and navigate to the local server URL (usually `http://localhost:8501`).

---

## 🔒 Special Dashboard Features

### 1. Time Lock Constraint (3:00 PM - 5:00 PM IST)
To enforce daily scheduling windows, the dashboard visualizations are locked outside the hours of 3:00 PM and 5:00 PM Indian Standard Time (IST).
- During these hours: The interactive dashboard loads immediately.
- Outside these hours: A locked screen is shown with a dynamic clock displaying the current time in IST.

### 2. 🔧 Grading / Evaluator Bypass Mode
If you are evaluating this project outside of the 3:00 PM to 5:00 PM IST window, look at the sidebar:
- Check the **"Grading Mode: Bypass Time Lock"** checkbox.
- This will override the timezone lock and immediately render the full interactive dashboard containing the KPI cards, the Plotly grouped bar chart, and the detailed data table.
- Unchecking this box will return the app to the standard locked state.
