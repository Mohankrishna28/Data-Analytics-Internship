# Implementation Plan - Task-6 Play Store Analytics

This document details the final approved implementation plan for **Task-6**, including data cleaning filters, dual-axis chart design, folder structure, and time lock mechanism.

---

## Technical Specifications

### 1. Folder Structure
The task is implemented inside the `Task-6/` directory in the workspace with the following hierarchy:
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

### 2. Data Cleaning & Filters
The raw play store dataset is parsed and cleaned using the following criteria:
- **Corrupt Rows**: Dropped index `10472` where the data columns were shifted (e.g. `'Free'` in Installs and `'Everyone'` in Price).
- **Installs**: Stripped `+` and `,` characters and converted to numeric integers. Apps with **fewer than 10,000 installs** are excluded.
- **Price & Revenue**: Stripped `$` and converted to float values. Direct Revenue is calculated as `Installs * Price`.
- **Revenue Filter**: Applied a **conditional filter** to preserve the Free vs. Paid comparison:
  - If type is **Free**: Keep the app (Revenue is $0).
  - If type is **Paid**: Exclude the app if its revenue is **below $10,000** (Keep only if `Revenue >= 10,000`).
- **Android Version**: Extracted major/minor numbers using regex (e.g. `4.1` from `4.1 and up`). Filtered strictly for versions **greater than 4.0** (excluding 4.0 and below).
- **Size**: Parsed sizes ending in `'M'` (Megabytes) and `'k'` (Kilobytes) into float MB values. Apps with size **15M and below** are excluded.
- **Content Rating**: Kept only apps with rating **Everyone**.
- **App Name Length**: Filtered out apps with names **longer than 30 characters** (including spaces and symbols).

### 3. Determining Top 3 Categories
- **Default**: Selected the top 3 categories by **Total Installs** of the filtered dataset (which evaluates to `GAME`, `FAMILY`, and `TOOLS`).
- **Alternative**: Supported toggling the top 3 categories by **App Count** (`FAMILY`, `GAME`, `SPORTS`).

### 4. Dual-Axis Chart Design
- **X-Axis**: Category (Top 3).
- **Primary Y-Axis (Left)**: Grouped bars for **Average Installs** comparing Free vs. Paid apps.
- **Secondary Y-Axis (Right)**: Gold/amber line chart mapping the **Average Revenue** of Paid apps.

### 5. Time Lock Mechanism
- Restricted visualization visibility to **1:00 PM – 2:00 PM IST** (Indian Standard Time, `Asia/Kolkata` zone).
- Outside this window, a polished **Locked View** displays a digital countdown timer until the next access window.
- A **Time Simulation Mode** selector is added to the sidebar allowing evaluators to force-unlock the page for immediate testing.
