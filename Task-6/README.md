# Task 6: Play Store Category Analytics Dashboard

This folder contains the complete implementation for **Task-6** of the Play Store analysis project. It features a Python data processing pipeline and a Streamlit dashboard with a time-lock mechanism that restricts access to the interactive chart outside 1:00 PM – 2:00 PM IST, while providing a simulation override.

---

## 📂 Project Directory Structure

```
Task-6/
├── Dataset/
│   ├── play_store.csv
│   └── reviews.csv
│
├── Documentation/
│   ├── Implementation_Plan.md
│   ├── Walkthrough.md
│   └── Report.md
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

- **Dataset/**: Contains the cleaned and filtered dataset CSVs.
- **Documentation/**: Contains the project planning, system walkthrough, and final analysis report.
- **Screenshots/**: Visual validation screenshots demonstrating both locked/unlocked states and the standalone chart.
- **Analysis.ipynb**: Jupyter notebook prototyping the entire data-cleaning pipeline.
- **dashboard.py**: Streamlit application rendering the dashboard UI.

---

## ⚙️ Filter Criteria Applied

All apps are cleaned and filtered using the following strict criteria:
1. **Installs**: $\ge 10,000$ downloads
2. **Revenue**: $\ge \$10,000$ for paid apps (Free apps are kept to allow comparative analysis)
3. **Android Version**: Strictly $> 4.0$ (e.g., `4.1` is kept; `4.0` is excluded)
4. **Size**: Strictly $> 15\text{ MB}$ (Megabytes)
5. **Content Rating**: `'Everyone'`
6. **App Name Length**: $\le 30$ characters (including spaces and special characters)

---

## 🚀 How to Run

### 1. Requirements
Ensure you have the required packages installed:
```bash
pip install streamlit pandas numpy plotly kaleido pytz
```

### 2. Run the Notebook
To inspect the prototype pipeline, open and run the Jupyter notebook:
```bash
jupyter notebook Task-6/Analysis.ipynb
```

### 3. Run the Dashboard
To start the interactive Streamlit server locally:
```bash
streamlit run Task-6/dashboard.py
```
By default, the server will launch on `http://localhost:8501`. 

*Note: Since the visualization is locked outside 1 PM – 2 PM IST, use the **"Time Simulation Mode"** dropdown in the sidebar to simulate the unlocked hour and view the active dashboard.*
