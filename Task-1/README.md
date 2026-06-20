# Google Play Store Reviews Analysis (Task 1)

This project contains visual analysis and modeling on the Google Play Store apps dataset, investigating the relationship between app size, average rating, installs, and user reviews sentiment subjectivity.

## Project Structure

The project has been organized into the following layout:
```text
Task_1_Google_Play_Store_Analysis/
│
├── Analysis.ipynb            # Active, fully verified Jupyter Notebook
│
├── Dataset/                  # Raw CSV data files
│   ├── Play Store Data.csv
│   └── User Reviews.csv
│
├── Screenshots/              # Output visualization screenshots
│   ├── Graph1.png            # Premium Bubble Chart visualization
│   ├── Dashboard.png         # Combined insights dashboard layout
│   └── Results.png           # Machine Learning Regressor fit plot
│
└── Documentation/            # Detailed PDF documentation guides
    ├── Implementation_Plan.pdf
    └── Walkthrough_Guide.pdf
```

---

## Visual Bubble Chart Specifications

The core analysis consists of a bubble chart plotting **App Size (MB)** on the X-axis against **Average Rating** on the Y-axis. The bubble size represents the **Number of Installs**.

### Applied Data Filters:
*   **Rating**: Only apps with rating higher than `3.5`.
*   **Categories**: GAME, BEAUTY, BUSINESS, COMICS, COMMUNICATION, DATING, ENTERTAINMENT, SOCIAL, and EVENTS.
*   **Reviews**: Greater than `500`.
*   **Subjectivity**: Sentiment subjectivity greater than `0.5`.
*   **Installs**: More than `50,000` (50k).
*   **App Name**: Exclude any app name containing the letter `"S"` or `"s"` (case-insensitive).

### Unique Design Aesthetics:
*   **GAME Highlight**: Highlighted in a vibrant **Pink** color.
*   **Category Translations**:
    *   `BEAUTY` is translated and displayed as `सौंदर्य` (Hindi).
    *   `BUSINESS` is translated and displayed as `வணிகம்` (Tamil).
    *   `DATING` is translated and displayed as `Dating (Deutsch)` (German).
*   **Matplotlib Unicode Support**: The visualization configuration overrides standard fonts to fallback to `Nirmala UI` and `Segoe UI Historic` for correct rendering of Devanagari and Tamil scripts on Windows.

---

## IST Time Restriction

> [!WARNING]
> This bubble chart visualization **works only between 5 PM IST and 7 PM IST**. 
> Outside of this timeframe:
> *   The Jupyter Notebook will output `Dashboard Hidden: Available only between 5 PM and 7 PM IST`.
> *   The Tkinter `AppDashboard` window will hide the bubble chart panel from the layout.

---

## How to Run

1. Make sure you have python installed along with dependencies: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `nltk`, `pytz`.
2. To run the notebook, open jupyter and run all cells in [Analysis.ipynb](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Task_1_Google_Play_Store_Analysis/Analysis.ipynb).
3. To test or open the Tkinter app dashboard, execute cell 13 in the notebook (which starts the main GUI loop).
