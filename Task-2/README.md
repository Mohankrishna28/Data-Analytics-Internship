# Google Play Store Analysis - Task 2 Documentation

This folder contains the interactive visualization and implementation details for Task 2.

## Project Structure

The project has been organized into the following structure under the `Task-2` directory:
```text
Task-2/
├── Dataset/
│   └── Play Store Data.csv       # Cleaned Google Play Store dataset
├── Analysis.ipynb                # Jupyter Notebook with data processing & Tkinter code
├── dashboard.py                  # Standalone Python script to run the dashboard GUI
├── Screenshots/                  # Saved visualization assets and dashboard views
│   ├── choropleth_map.png        # High-resolution static map representation
│   ├── Dashboard_Active.png      # Dashboard preview in active state (test mode/active hour)
│   └── Dashboard_Inactive.png    # Dashboard preview in restricted state
└── Documentation/                # Interactive outputs and documentation guides
    ├── README.md                 # This documentation file
    └── choropleth_map.html       # Fully interactive, hoverable Plotly Choropleth map
```

---

## Applied Rules & Specifications

### 1. Data Cleaning and Filtering
*   **Categories Exclusion**: Filtered out all categories starting with the characters **'A'**, **'C'**, **'G'**, or **'S'** (case-insensitive, e.g., GAME, SOCIAL, SHOPPING, ART_AND_DESIGN, COMMUNICATION, etc.).
*   **Total Installations**: Aggregated total installations per category.
*   **Top 5 Categories**: Filtered to retain only the top 5 categories by total installations:
    1.  **PRODUCTIVITY** (14.1 Billion installs)
    2.  **TOOLS** (11.4 Billion installs)
    3.  **FAMILY** (10.2 Billion installs)
    4.  **PHOTOGRAPHY** (10.0 Billion installs)
    5.  **NEWS_AND_MAGAZINES** (7.4 Billion installs)

### 2. Geographical Mapping Decision
Since the original Play Store dataset represents global app statistics and does not specify installations by country, we map each of the top 5 filtered categories to a representative country using ISO Alpha-3 codes:
*   `PRODUCTIVITY` ➔ `USA` (United States)
*   `TOOLS` ➔ `IND` (India)
*   `FAMILY` ➔ `DEU` (Germany)
*   `PHOTOGRAPHY` ➔ `BRA` (Brazil)
*   `NEWS_AND_MAGAZINES` ➔ `AUS` (Australia)

### 3. Interactive Plotly Choropleth Map
*   Developed using Plotly to show global installations.
*   **Threshold Highlight**: Highlights categories where total installations exceed **1 Million** using a distinct **gold border outline** (`marker_line_color="gold"`, `marker_line_width=4`).
*   **Tooltip Interactivity**: Hover tooltips show Category Name, Representative Country, and Total Installs formatted with commas.

### 4. Time-Based Access Restriction
*   The visualization is strictly gated to be visible **only between 6:00 PM IST and 8:00 PM IST**.
*   Outside of this time window, both the notebook cell output and the Tkinter dashboard hide the graph and display an access restriction screen.
*   To enable developer testing and evaluation outside this window, a **`TEST_MODE` / `--test-mode`** bypass has been built into both the notebook and standalone scripts.

---

## How to Run & Verify

### Pre-requisites
Ensure you have the required python packages installed:
```bash
pip install pandas numpy plotly pillow pytz
```
*Note: Plotly uses `kaleido` for exporting static PNG images. If you need to recompile the notebook and save images, make sure it is installed:*
```bash
pip install kaleido
```

### 1. View the Interactive Map
Simply open [choropleth_map.html](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Task-2/Documentation/choropleth_map.html) in any web browser to interact with the map, hover over countries, zoom/pan, and see details.

### 2. Run the Tkinter Dashboard
To run the dashboard, execute the standalone Python script from your terminal:

*   **To test the strict time-gate** (currently locked since current time is 2:22 PM IST):
    ```bash
    python Task-2/dashboard.py
    ```
*   **To bypass the time-gate and view the active dashboard**:
    ```bash
    python Task-2/dashboard.py --test-mode
    ```

### 3. Open the Jupyter Notebook
Open the [Analysis.ipynb](file:///c:/Users/mohan/Downloads/Play%20Store%20Reviews/Task-2/Analysis.ipynb) file inside Jupyter to view the step-by-step code and verification logs. Toggle `TEST_MODE = True/False` in Cell 2 to inspect both states.
