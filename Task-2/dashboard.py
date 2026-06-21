import os
import pandas as pd
import numpy as np
import pytz
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys

# Load and clean the dataset
def load_data():
    csv_path = 'Dataset/Play Store Data.csv'
    if not os.path.exists(csv_path):
        # Fallback if run from parent directory
        csv_path = 'Task-2/Dataset/Play Store Data.csv'
        
    df = pd.read_csv(csv_path)
    df = df[df['Installs'] != 'Free']
    df['Installs_clean'] = df['Installs'].astype(str).str.replace('+', '', regex=False).str.replace(',', '', regex=False)
    df['Installs_clean'] = pd.to_numeric(df['Installs_clean'], errors='coerce').fillna(0).astype(int)
    
    # Filter categories: Exclude A, C, G, S
    df = df[~df['Category'].str.upper().str.startswith(('A', 'C', 'G', 'S'), na=True)]
    
    # Group and find top 5
    cat_installs = df.groupby('Category')['Installs_clean'].sum().reset_index()
    top_5 = cat_installs.sort_values(by='Installs_clean', ascending=False).head(5).reset_index(drop=True)
    
    # Geographic mapping
    category_country_mapping = {
        'PRODUCTIVITY': {'ISO': 'USA', 'Country': 'United States'},
        'TOOLS': {'ISO': 'IND', 'Country': 'India'},
        'FAMILY': {'ISO': 'DEU', 'Country': 'Germany'},
        'PHOTOGRAPHY': {'ISO': 'BRA', 'Country': 'Brazil'},
        'NEWS_AND_MAGAZINES': {'ISO': 'AUS', 'Country': 'Australia'}
    }
    
    top_5['Country_ISO'] = top_5['Category'].map(lambda x: category_country_mapping[x]['ISO'])
    top_5['Country_Name'] = top_5['Category'].map(lambda x: category_country_mapping[x]['Country'])
    top_5['Exceeds_1M'] = top_5['Installs_clean'] > 1000000
    return top_5

class AppDashboard(tk.Tk):
    def __init__(self, test_mode=True, data=None):
        super().__init__()
        self.title("Google Play Store Analytics Dashboard - Task 2")
        self.geometry("1150x700")
        self.configure(bg="#121212")  # Premium Dark Theme
        
        self.test_mode = test_mode
        self.data = data if data is not None else load_data()
        self.check_time_and_render()

    def check_time_and_render(self):
        # Fetch timezone info for IST
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)
        hour = now_ist.hour
        is_active = (18 <= hour < 20)

        # Clean current widgets
        for widget in self.winfo_children():
            widget.destroy()

        if is_active or self.test_mode:
            self.build_active_dashboard(now_ist)
        else:
            self.build_restricted_dashboard(now_ist)

    def build_active_dashboard(self, time_now):
        # Main container
        main_container = tk.Frame(self, bg="#121212")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header section
        header = tk.Frame(main_container, bg="#1E1E1E", height=90, bd=0)
        header.pack(fill=tk.X, pady=(0, 20))

        title = tk.Label(
            header, 
            text="Play Store Installs - Geographic Category Analysis", 
            font=("Outfit", 22, "bold"), 
            fg="#00E5FF", 
            bg="#1E1E1E"
        )
        title.pack(side=tk.LEFT, padx=25, pady=20)

        time_display = time_now.strftime("%I:%M %p IST")
        info_label = tk.Label(
            header, 
            text=f"Time: {time_display} | Mode: {'TEST_BYPASS' if self.test_mode else 'LIVE'}", 
            font=("Inter", 11, "italic"), 
            fg="#A0A0A0", 
            bg="#1E1E1E"
        )
        info_label.pack(side=tk.RIGHT, padx=25, pady=25)

        # Dashboard layout
        content = tk.Frame(main_container, bg="#121212")
        content.pack(fill=tk.BOTH, expand=True)

        # Sidebar for category and details
        sidebar = tk.Frame(content, bg="#1E1E1E", width=350)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)

        sidebar_title = tk.Label(
            sidebar, 
            text="Top 5 Category Metrics", 
            font=("Outfit", 16, "bold"), 
            fg="#E0E0E0", 
            bg="#1E1E1E"
        )
        sidebar_title.pack(anchor="w", padx=20, pady=20)

        # Add list of categories and installs
        for idx, row in self.data.iterrows():
            cat_frame = tk.Frame(sidebar, bg="#2D2D2D", pady=8, padx=12, bd=0)
            cat_frame.pack(fill=tk.X, padx=20, pady=6)
            
            cat_name = tk.Label(
                cat_frame, 
                text=f"{row['Category']}", 
                font=("Inter", 11, "bold"), 
                fg="#00E5FF", 
                bg="#2D2D2D"
            )
            cat_name.pack(anchor="w")
            
            cat_desc = tk.Label(
                cat_frame, 
                text=f"Installs: {row['Installs_clean']:,} | mapped to {row['Country_Name']}", 
                font=("Inter", 9), 
                fg="#B0B0B0", 
                bg="#2D2D2D"
            )
            cat_desc.pack(anchor="w", pady=(4, 0))

        # Highlight Info Alert Box
        alert_box = tk.Frame(sidebar, bg="#2A1D0E", highlightbackground="#FFB300", highlightthickness=1)
        alert_box.pack(fill=tk.X, padx=20, pady=25)
        
        alert_text = tk.Label(
            alert_box,
            text="⚠️ HIGH INSTALL HIGHLIGHT:\nCountries styled with a thick gold border have app installations exceeding 1 Million.\nAll top 5 categories meet this threshold.",
            font=("Inter", 9, "bold"),
            fg="#FFB300",
            bg="#2A1D0E",
            justify="left",
            wraplength=270,
            padx=10,
            pady=10
        )
        alert_text.pack(fill=tk.BOTH)

        # Right side panel (displays map)
        map_container = tk.Frame(content, bg="#1E1E1E")
        map_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        map_header = tk.Label(
            map_container,
            text="Interactive Geographic Map Visualization (Plotly Export)",
            font=("Outfit", 15, "bold"),
            fg="#E0E0E0",
            bg="#1E1E1E"
        )
        map_header.pack(pady=15)

        # Render map image
        map_path = "Screenshots/choropleth_map.png"
        if not os.path.exists(map_path):
            map_path = "Task-2/Screenshots/choropleth_map.png"
            
        if os.path.exists(map_path):
            try:
                img = Image.open(map_path)
                img = img.resize((710, 420), Image.Resampling.LANCZOS)
                self.map_img_tk = ImageTk.PhotoImage(img)

                img_lbl = tk.Label(map_container, image=self.map_img_tk, bg="#1E1E1E")
                img_lbl.pack(padx=20, pady=10, expand=True, fill=tk.BOTH)
            except Exception as e:
                err_lbl = tk.Label(
                    map_container,
                    text=f"Error loading image asset: {str(e)}",
                    font=("Inter", 12),
                    fg="#FF5252",
                    bg="#1E1E1E"
                )
                err_lbl.pack(expand=True)
        else:
            missing_lbl = tk.Label(
                map_container,
                text="Visualization image asset not found.\nPlease run the Plotly cell to write the asset.",
                font=("Inter", 12),
                fg="#FFB300",
                bg="#1E1E1E"
            )
            missing_lbl.pack(expand=True)

    def build_restricted_dashboard(self, time_now):
        # Layout for unauthorized time
        frame = tk.Frame(self, bg="#121212")
        frame.pack(fill=tk.BOTH, expand=True)

        lock_lbl = tk.Label(
            frame,
            text="🔒 Dashboard Visuals Offline",
            font=("Outfit", 28, "bold"),
            fg="#FF5252",
            bg="#121212"
        )
        lock_lbl.pack(expand=True, pady=(180, 10))

        time_display = time_now.strftime("%I:%M:%S %p IST")
        desc_lbl = tk.Label(
            frame,
            text=f"The Category Installs Choropleth Map is only visible between 6:00 PM and 8:00 PM IST.\nCurrent local time: {time_display}.\n\n(To preview this dashboard now, run this script with '--test-mode'.)",
            font=("Inter", 13),
            fg="#A0A0A0",
            bg="#121212",
            justify="center"
        )
        desc_lbl.pack(expand=True, pady=(0, 180))

if __name__ == '__main__':
    # Default to False unless --test-mode is supplied
    test_mode = '--test-mode' in sys.argv
    data = load_data()
    app = AppDashboard(test_mode=test_mode, data=data)
    app.mainloop()
