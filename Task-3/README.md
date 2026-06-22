# Google Play Store Reviews & Installs Analysis (Task-3)

This project contains the source code, data analysis, and dashboard for the Google Play Store App Reviews & Installs dataset.

## Project Structure

```
├── Dataset/
│   ├── Play Store Data.csv
│   └── User Reviews.csv
│
├── Documentation/
│   ├── Implementation_Plan.md
│   └── Walkthrough.md
│
├── Screenshots/
│   ├── Graph1.png
│   ├── Dashboard_Visible.png
│   └── Dashboard_Hidden.png
│
├── Analysis.ipynb
├── dashboard.py
└── README.md
```

## Features

1. **Clean Data Pipeline**: Automatic preprocessing of App Installs, Reviews, Last Updated timelines, and user sentiment analysis (VADER).
2. **Modern Dark Theme GUI (`dashboard.py`)**: Built with a sleek charcoal and matte violet accent aesthetic.
3. **Tabbed Visualization Layout**: Easily navigate between overview charts, rating distributions, installations trends, revenue details, and the Machine Learning rating predictor (Random Forest).
4. **Restricted Time Series Install Trend Plot**:
   - Only works/unlocks between **6 PM IST to 9 PM IST** (otherwise shows a visual lock screen).
   - Segments cumulative total installs over time by category.
   - Highlights period of significant growth (>20% MoM) by shading the areas under the curve.
   - Applies multi-lingual label translations:
     - `BEAUTY` -> `सौंदर्य` (Hindi)
     - `BUSINESS` -> `வணிகம்` (Tamil)
     - `DATING` -> `Dating` (German)
   - Uses `Nirmala UI` font for perfect native rendering of Devanagari and Tamil scripts on Windows.

## Installation & Setup

1. Make sure you have python 3.8+ installed.
2. Install the required dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn nltk pytz
   ```
3. Run the dashboard application:
   ```bash
   python dashboard.py
   ```

*Note: To test or capture screenshots of the locked time-series tab outside the 6 PM - 9 PM IST window, you can run the app with the `OVERRIDE_TIME` environment variable (e.g. `OVERRIDE_TIME=18:30 python dashboard.py`).*
