import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from datetime import datetime
import pytz
import os

# Download lexicon if not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

# ----------------------------------------------------
# 1. DATA PREPARATION & CLEANING
# ----------------------------------------------------
def load_and_clean_data():
    # Paths updated to Dataset/ folder
    apps_df = pd.read_csv('Dataset/Play Store Data.csv')
    reviews_df = pd.read_csv('Dataset/User Reviews.csv')
    
    # Clean apps rating
    apps_df = apps_df.dropna(subset=['Rating'])
    for column in apps_df.columns:
        apps_df[column] = apps_df[column].fillna(apps_df[column].mode()[0])
    apps_df.drop_duplicates(inplace=True)
    apps_df = apps_df[apps_df['Rating'] <= 5]
    
    # Clean reviews
    reviews_df.dropna(subset=['Translated_Review'], inplace=True)
    
    # Conversions
    apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce').fillna(0).astype(int)
    
    # Convert installs
    apps_df['Installs'] = apps_df['Installs'].astype(str).str.replace(',', '').str.replace('+', '').str.strip()
    apps_df = apps_df[apps_df['Installs'].str.isnumeric()]
    apps_df['Installs'] = apps_df['Installs'].astype(float)
    
    # Price and Size
    apps_df['Price'] = apps_df['Price'].astype(str).str.replace('$', '').astype(float)
    
    def convert_size(size):
        if 'M' in size:
            return float(size.replace('M', ''))
        elif 'k' in size:
            return float(size.replace('k', '')) / 1024
        else:
            return np.nan
            
    apps_df['Size'] = apps_df['Size'].apply(convert_size)
    apps_df['Size'] = apps_df['Size'].fillna(apps_df['Size'].median())
    
    # Extra columns
    apps_df['Log_Installs'] = np.log1p(apps_df['Installs'])
    apps_df['Log_Reviews'] = np.log1p(apps_df['Reviews'])
    apps_df['Revenue'] = apps_df['Price'] * apps_df['Installs']
    
    # Year
    apps_df['Last Updated'] = pd.to_datetime(apps_df['Last Updated'], errors='coerce')
    apps_df = apps_df.dropna(subset=['Last Updated'])
    apps_df['Year'] = apps_df['Last Updated'].dt.year
    
    # Sentiment
    sia = SentimentIntensityAnalyzer()
    reviews_df['Sentiment_Score'] = reviews_df['Translated_Review'].apply(
        lambda x: sia.polarity_scores(str(x))['compound']
    )
    
    merged_df = pd.merge(apps_df, reviews_df, on='App', how='inner')
    
    return apps_df, reviews_df, merged_df

# Load the cleaned data
apps_df, reviews_df, merged_df = load_and_clean_data()

# ----------------------------------------------------
# 2. COLOR PALETTE & STYLING CONSTANTS (DARK THEME)
# ----------------------------------------------------
BG_MAIN = '#121212'      # Slate-charcoal main background
BG_CARD = '#1E1E1E'      # Slightly lighter card background
ACCENT = '#BB86FC'       # Matte violet accent
ACCENT_MUTED = '#2C2C2C' # Dark grey for unselected
TEXT_PRIMARY = '#E1E1E1' # Light grey text
TEXT_MUTED = '#888888'   # Muted grey text
GRID_COLOR = '#333333'

# ----------------------------------------------------
# 3. DASHBOARD APPLICATION CLASS
# ----------------------------------------------------
class ModernDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Play Store Insights & Growth Dashboard")
        self.geometry("1300x850")
        self.configure(bg=BG_MAIN)
        
        # Style configuration
        self.custom_styles()
        
        # Sidebar for navigation
        self.sidebar = tk.Frame(self, bg=BG_CARD, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Title in sidebar
        title_label = tk.Label(
            self.sidebar, 
            text="Play Store\nAnalytics", 
            font=("Nirmala UI", 18, "bold"), 
            bg=BG_CARD, 
            fg=ACCENT, 
            justify="center",
            pady=20
        )
        title_label.pack()
        
        # Main content area
        self.main_content = tk.Frame(self, bg=BG_MAIN)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Pages container
        self.pages = {}
        self.active_button = None
        
        # Navigation buttons mapping
        self.nav_items = [
            ("Category & App Types", self.show_overview_page),
            ("Ratings & Sentiments", self.show_ratings_page),
            ("Installs & Updates", self.show_installs_page),
            ("Revenue & Genres", self.show_revenue_page),
            ("ML Rating Predictor", self.show_ml_page),
            ("Installs Trend (Time Series)", self.show_trend_page)
        ]
        
        for name, func in self.nav_items:
            self.create_nav_button(name, func)
            
        # Default page
        self.show_overview_page()

    def custom_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('.', background=BG_MAIN, foreground=TEXT_PRIMARY)
        style.configure('TFrame', background=BG_MAIN)
        style.configure('Card.TFrame', background=BG_CARD, borderwidth=1, relief="flat")
        style.configure('TLabel', background=BG_MAIN, foreground=TEXT_PRIMARY, font=("Nirmala UI", 10))
        style.configure('Header.TLabel', background=BG_CARD, foreground=ACCENT, font=("Nirmala UI", 12, "bold"))
        style.configure('Vertical.TScrollbar', gripcount=0, background=BG_CARD, troughcolor=BG_MAIN)

    def create_nav_button(self, name, command):
        # We use a custom styled tk.Button to look modern and allow easy coloring
        btn = tk.Button(
            self.sidebar,
            text=name,
            font=("Nirmala UI", 11, "bold"),
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            activebackground=ACCENT,
            activeforeground=BG_MAIN,
            bd=0,
            padx=20,
            pady=15,
            anchor="w",
            cursor="hand2",
            relief="flat"
        )
        btn.configure(command=lambda: [self.set_active_button(btn), command()])
        btn.pack(fill=tk.X, pady=2)

    def set_active_button(self, button):
        if self.active_button:
            self.active_button.configure(bg=BG_CARD, fg=TEXT_PRIMARY)
        self.active_button = button
        self.active_button.configure(bg=ACCENT, fg=BG_MAIN)

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        plt.close('all')

    def create_page_header(self, title):
        header_frame = tk.Frame(self.main_content, bg=BG_MAIN, height=60)
        header_frame.pack(fill=tk.X, padx=25, pady=15)
        lbl = tk.Label(header_frame, text=title, font=("Nirmala UI", 20, "bold"), bg=BG_MAIN, fg=TEXT_PRIMARY)
        lbl.pack(side=tk.LEFT)

    # ----------------------------------------------------
    # PAGE 1: OVERVIEW & APP TYPES
    # ----------------------------------------------------
    def show_overview_page(self):
        self.clear_content()
        self.create_page_header("Overview & Demographics")
        
        # Grid layout for charts
        grid_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.rowconfigure(0, weight=1)
        
        # Top Categories Card
        f1 = ttk.Frame(grid_frame, style='Card.TFrame', padding=15)
        f1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        tk.Label(f1, text="Top Categories by App Count", font=("Nirmala UI", 12, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        
        fig1, ax1 = plt.subplots(figsize=(5, 4.5))
        plt.style.use('dark_background')
        fig1.patch.set_facecolor(BG_CARD)
        ax1.set_facecolor(BG_CARD)
        
        category_counts = apps_df['Category'].value_counts().nlargest(8)
        sns.barplot(x=category_counts.values, y=category_counts.index, palette='coolwarm', ax=ax1)
        ax1.set_xlabel('Number of Apps', color=TEXT_PRIMARY)
        ax1.tick_params(colors=TEXT_PRIMARY)
        ax1.grid(True, color=GRID_COLOR, alpha=0.3)
        fig1.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, master=f1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Free vs Paid Card
        f2 = ttk.Frame(grid_frame, style='Card.TFrame', padding=15)
        f2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        tk.Label(f2, text="Free vs Paid App Distribution", font=("Nirmala UI", 12, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        
        fig2, ax2 = plt.subplots(figsize=(5, 4.5))
        fig2.patch.set_facecolor(BG_CARD)
        ax2.set_facecolor(BG_CARD)
        
        type_counts = apps_df['Type'].value_counts()
        ax2.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=140, 
                colors=['#BB86FC', '#03DAC6'], textprops={'color': TEXT_PRIMARY})
        fig2.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, master=f2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

    # ----------------------------------------------------
    # PAGE 2: RATINGS & SENTIMENT
    # ----------------------------------------------------
    def show_ratings_page(self):
        self.clear_content()
        self.create_page_header("Ratings & Sentiment Analysis")
        
        grid_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.rowconfigure(0, weight=1)
        
        # Rating Distribution Card
        f1 = ttk.Frame(grid_frame, style='Card.TFrame', padding=15)
        f1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        tk.Label(f1, text="App Rating Distribution Histogram", font=("Nirmala UI", 12, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        
        fig1, ax1 = plt.subplots(figsize=(5, 4.5))
        fig1.patch.set_facecolor(BG_CARD)
        ax1.set_facecolor(BG_CARD)
        sns.histplot(apps_df['Rating'], bins=25, kde=True, color='#03DAC6', ax=ax1)
        ax1.tick_params(colors=TEXT_PRIMARY)
        ax1.set_xlabel('Rating', color=TEXT_PRIMARY)
        ax1.grid(True, color=GRID_COLOR, alpha=0.3)
        fig1.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, master=f1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Sentiment Pie Card
        f2 = ttk.Frame(grid_frame, style='Card.TFrame', padding=15)
        f2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        tk.Label(f2, text="User Reviews Sentiment Distribution", font=("Nirmala UI", 12, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        
        fig2, ax2 = plt.subplots(figsize=(5, 4.5))
        fig2.patch.set_facecolor(BG_CARD)
        ax2.set_facecolor(BG_CARD)
        
        sentiments = reviews_df['Sentiment_Score'].apply(
            lambda x: 'Positive' if x > 0.05 else ('Negative' if x < -0.05 else 'Neutral')
        ).value_counts()
        
        ax2.pie(sentiments, labels=sentiments.index, autopct='%1.1f%%', startangle=140,
                colors=['#03DAC6', '#CF6679', '#888888'], textprops={'color': TEXT_PRIMARY})
        fig2.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, master=f2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

    # ----------------------------------------------------
    # PAGE 3: INSTALLATIONS & UPDATES
    # ----------------------------------------------------
    def show_installs_page(self):
        self.clear_content()
        self.create_page_header("Installations & Updates")
        
        grid_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.rowconfigure(0, weight=1)
        
        # Installs by Category Card
        f1 = ttk.Frame(grid_frame, style='Card.TFrame', padding=15)
        f1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        tk.Label(f1, text="Top Installations by Category", font=("Nirmala UI", 12, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        
        fig1, ax1 = plt.subplots(figsize=(5, 4.5))
        fig1.patch.set_facecolor(BG_CARD)
        ax1.set_facecolor(BG_CARD)
        installs_by_cat = apps_df.groupby('Category')['Installs'].sum().nlargest(8)
        sns.barplot(x=installs_by_cat.values, y=installs_by_cat.index, palette='Spectral', ax=ax1)
        ax1.tick_params(colors=TEXT_PRIMARY)
        ax1.set_xlabel('Installs', color=TEXT_PRIMARY)
        ax1.grid(True, color=GRID_COLOR, alpha=0.3)
        fig1.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, master=f1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Updates over Years Card
        f2 = ttk.Frame(grid_frame, style='Card.TFrame', padding=15)
        f2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        tk.Label(f2, text="App Updates Trend over Time", font=("Nirmala UI", 12, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        
        fig2, ax2 = plt.subplots(figsize=(5, 4.5))
        fig2.patch.set_facecolor(BG_CARD)
        ax2.set_facecolor(BG_CARD)
        updates = apps_df['Year'].value_counts().sort_index()
        sns.lineplot(x=updates.index, y=updates.values, marker='o', color='#BB86FC', linewidth=2.5, ax=ax2)
        ax2.tick_params(colors=TEXT_PRIMARY)
        ax2.set_xlabel('Year', color=TEXT_PRIMARY)
        ax2.set_ylabel('Number of Updates', color=TEXT_PRIMARY)
        ax2.grid(True, color=GRID_COLOR, alpha=0.3)
        fig2.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, master=f2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

    # ----------------------------------------------------
    # PAGE 4: REVENUE & GENRES
    # ----------------------------------------------------
    def show_revenue_page(self):
        self.clear_content()
        self.create_page_header("Revenue & Genre Distribution")
        
        grid_frame = tk.Frame(self.main_content, bg=BG_MAIN)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.rowconfigure(0, weight=1)
        
        # Revenue by Category Card
        f1 = ttk.Frame(grid_frame, style='Card.TFrame', padding=15)
        f1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        tk.Label(f1, text="Top Estimated Revenue by Category", font=("Nirmala UI", 12, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        
        fig1, ax1 = plt.subplots(figsize=(5, 4.5))
        fig1.patch.set_facecolor(BG_CARD)
        ax1.set_facecolor(BG_CARD)
        revenue_by_cat = apps_df.groupby('Category')['Revenue'].sum().nlargest(8)
        sns.barplot(x=revenue_by_cat.values, y=revenue_by_cat.index, palette='viridis', ax=ax1)
        ax1.tick_params(colors=TEXT_PRIMARY)
        ax1.set_xlabel('Estimated Revenue ($)', color=TEXT_PRIMARY)
        ax1.grid(True, color=GRID_COLOR, alpha=0.3)
        fig1.tight_layout()
        
        canvas1 = FigureCanvasTkAgg(fig1, master=f1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Top Genres Card
        f2 = ttk.Frame(grid_frame, style='Card.TFrame', padding=15)
        f2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        tk.Label(f2, text="Top App Genres on Play Store", font=("Nirmala UI", 12, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w")
        
        fig2, ax2 = plt.subplots(figsize=(5, 4.5))
        fig2.patch.set_facecolor(BG_CARD)
        ax2.set_facecolor(BG_CARD)
        genres_counts = apps_df['Genres'].str.split(';').explode().value_counts().nlargest(8)
        sns.barplot(x=genres_counts.values, y=genres_counts.index, palette='magma', ax=ax2)
        ax2.tick_params(colors=TEXT_PRIMARY)
        ax2.set_xlabel('App Count', color=TEXT_PRIMARY)
        ax2.grid(True, color=GRID_COLOR, alpha=0.3)
        fig2.tight_layout()
        
        canvas2 = FigureCanvasTkAgg(fig2, master=f2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

    # ----------------------------------------------------
    # PAGE 5: ML RATING PREDICTOR
    # ----------------------------------------------------
    def show_ml_page(self):
        self.clear_content()
        self.create_page_header("ML Rating Predictor (Random Forest)")
        
        card = ttk.Frame(self.main_content, style='Card.TFrame', padding=20)
        card.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        tk.Label(
            card, 
            text="Model Evaluation: Predicting Rating based on Reviews, Installs, and Price", 
            font=("Nirmala UI", 12, "bold"), 
            bg=BG_CARD, 
            fg=ACCENT
        ).pack(anchor="w")
        
        # Simple ML Evaluation Plot
        X = apps_df[['Log_Reviews', 'Log_Installs', 'Price']]
        y = apps_df['Rating']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_facecolor(BG_CARD)
        ax.set_facecolor(BG_CARD)
        
        ax.scatter(y_test, y_pred, alpha=0.2, color='#BB86FC')
        ax.plot([1, 5], [1, 5], 'r--', linewidth=2, label="Perfect Fit")
        ax.set_title(f'Random Forest Evaluation (MSE: {mse:.3f}, R2 Score: {r2:.3f})', color=TEXT_PRIMARY, fontsize=12)
        ax.set_xlabel('True Rating', color=TEXT_PRIMARY)
        ax.set_ylabel('Predicted Rating', color=TEXT_PRIMARY)
        ax.tick_params(colors=TEXT_PRIMARY)
        ax.grid(True, color=GRID_COLOR, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=15)

    # ----------------------------------------------------
    # PAGE 6: TIME SERIES GRAPH (WITH TIME-BASED ACCESSIBILITY)
    # ----------------------------------------------------
    def show_trend_page(self):
        self.clear_content()
        self.create_page_header("Total Installs Trend Over Time")
        
        card = ttk.Frame(self.main_content, style='Card.TFrame', padding=25)
        card.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        # Check time restriction (6 PM to 9 PM IST)
        # Check override environment variable
        override_time = os.environ.get("OVERRIDE_TIME")
        
        is_visible = False
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)
        
        if override_time:
            # Parse mock time (format HH:MM)
            try:
                h, m = map(int, override_time.split(':'))
                now_ist = now_ist.replace(hour=h, minute=m)
                is_visible = (18 <= h < 21)
            except Exception:
                is_visible = (18 <= now_ist.hour < 21)
        else:
            is_visible = (18 <= now_ist.hour < 21)
            
        if not is_visible:
            # Show "Hidden" Screen
            lbl_lock = tk.Label(
                card, 
                text="🔒 VISUALIZATION LOCKED", 
                font=("Nirmala UI", 18, "bold"), 
                bg=BG_CARD, 
                fg="#CF6679"
            )
            lbl_lock.pack(pady=(120, 10))
            
            lbl_msg = tk.Label(
                card, 
                text="This visual report is only accessible between 6:00 PM IST and 9:00 PM IST.\n"
                     f"Current Dashboard Time: {now_ist.strftime('%I:%M:%S %p')} IST", 
                font=("Nirmala UI", 12), 
                bg=BG_CARD, 
                fg=TEXT_PRIMARY,
                justify="center"
            )
            lbl_msg.pack(pady=10)
            return

        # Time Series Generation
        # Data preparation inside the page block to filter specifically
        df = apps_df.copy()
        
        # App filters:
        # Exclude starts with X, Y, Z
        df = df[~df['App'].str.lower().str.startswith(('x', 'y', 'z'), na=False)]
        # Exclude contains 'S' (case insensitive)
        df = df[~df['App'].str.contains('S', case=False, na=False)]
        # Reviews > 500
        df = df[df['Reviews'] > 500]
        
        # Category filter (starts with E, C, B or DATING)
        categories_to_keep = [cat for cat in df['Category'].unique() if cat.startswith(('E', 'C', 'B'))] + ['DATING']
        df = df[df['Category'].isin(categories_to_keep)]
        
        # Resample monthly
        df['YearMonth'] = df['Last Updated'].dt.to_period('M')
        
        # Group by category and YearMonth
        grouped = df.groupby(['Category', 'YearMonth'])['Installs'].sum().reset_index()
        grouped = grouped.sort_values(['Category', 'YearMonth'])
        
        min_period = grouped['YearMonth'].min()
        max_period = grouped['YearMonth'].max()
        all_months = pd.period_range(start=min_period, end=max_period, freq='M')
        
        resampled_list = []
        for cat in grouped['Category'].unique():
            cat_df = grouped[grouped['Category'] == cat].set_index('YearMonth')
            cat_df = cat_df.reindex(all_months, fill_value=0)
            cat_df['Category'] = cat
            cat_df = cat_df.reset_index().rename(columns={'index': 'YearMonth'})
            cat_df['Cumulative_Installs'] = cat_df['Installs'].cumsum()
            cat_df['Prev_Cumulative'] = cat_df['Cumulative_Installs'].shift(1)
            cat_df['MoM_Growth'] = (cat_df['Cumulative_Installs'] - cat_df['Prev_Cumulative']) / cat_df['Prev_Cumulative']
            cat_df['MoM_Growth'] = cat_df['MoM_Growth'].replace([np.inf, -np.inf], np.nan).fillna(0)
            resampled_list.append(cat_df)
            
        resampled_df = pd.concat(resampled_list)
        resampled_df['Date'] = resampled_df['YearMonth'].dt.to_timestamp()
        
        # Translation map
        translation_map = {
            'BEAUTY': 'सौंदर्य',
            'BUSINESS': 'வணிகம்',
            'DATING': 'Verabredung'
        }
        
        # Plotting the Time Series Graph
        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_facecolor(BG_CARD)
        ax.set_facecolor(BG_CARD)
        ax.set_yscale('log')
        
        # Use Nirmala UI font for legends/unicode text rendering
        plt.rcParams['font.family'] = 'Nirmala UI'
        plt.rcParams['axes.unicode_minus'] = False
        
        for cat in resampled_df['Category'].unique():
            cat_data = resampled_df[resampled_df['Category'] == cat].sort_values('Date')
            # Filter out 0 cumulative installs to avoid log(0) issues
            cat_data = cat_data[cat_data['Cumulative_Installs'] > 0]
            
            if len(cat_data) == 0:
                continue
                
            label_name = translation_map.get(cat, cat)
            
            line, = ax.plot(cat_data['Date'], cat_data['Cumulative_Installs'], label=label_name, linewidth=2)
            color = line.get_color()
            
            # Shading growth regions (>20% MoM)
            dates = cat_data['Date'].values
            installs = cat_data['Cumulative_Installs'].values
            growth = cat_data['MoM_Growth'].values
            
            for i in range(1, len(dates)):
                if growth[i] > 0.20:
                    ax.fill_between(
                        dates[i-1:i+1],
                        installs[i-1:i+1],
                        y2=1,
                        color=color,
                        alpha=0.35
                    )

                    
        ax.set_title("Total Cumulative Installs Over Time by Category (MoM Growth > 20% Shaded)", 
                     fontsize=12, color=TEXT_PRIMARY, pad=10)
        ax.set_xlabel("Timeline (Year-Month)", color=TEXT_PRIMARY)
        ax.set_ylabel("Total Cumulative Installs", color=TEXT_PRIMARY)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        ax.tick_params(colors=TEXT_PRIMARY)
        plt.xticks(rotation=45)
        ax.grid(True, color=GRID_COLOR, alpha=0.3)
        ax.legend(title="Category", loc="upper left", facecolor=BG_CARD, edgecolor=GRID_COLOR, labelcolor=TEXT_PRIMARY)
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

    def save_screenshot_and_close(self, filename):
        self.deiconify()
        self.lift()
        self.attributes('-topmost', True)
        self.focus_force()
        self.update_idletasks()
        self.update()
        
        import sys
        if sys.platform == 'win32':
            import ctypes
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass
        
        import time
        time.sleep(0.3)
        
        self.deiconify()
        self.lift()
        self.attributes('-topmost', True)
        self.focus_force()
        self.update_idletasks()
        self.update()
        
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()
        
        from PIL import ImageGrab

        bbox = (x, y, x + w, y + h)
        img = ImageGrab.grab(bbox)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        img.save(filename)
        print(f"Screenshot successfully saved to {filename}")
        self.destroy()
        sys.exit(0)


if __name__ == "__main__":
    import sys
    
    # Check if run with command line flags for screenshot generation
    if "--screenshot-visible" in sys.argv:
        os.environ["OVERRIDE_TIME"] = "18:30"
    elif "--screenshot-hidden" in sys.argv:
        os.environ["OVERRIDE_TIME"] = "10:00"
        
    app = ModernDashboard()
    
    if "--screenshot-visible" in sys.argv:
        app.show_trend_page()
        for child in app.sidebar.winfo_children():
            if isinstance(child, tk.Button) and "Trend" in child.cget("text"):
                app.set_active_button(child)
        app.after(2500, app.save_screenshot_and_close, "Screenshots/Dashboard_Visible.png")
    elif "--screenshot-hidden" in sys.argv:
        app.show_trend_page()
        for child in app.sidebar.winfo_children():
            if isinstance(child, tk.Button) and "Trend" in child.cget("text"):
                app.set_active_button(child)
        app.after(2500, app.save_screenshot_and_close, "Screenshots/Dashboard_Hidden.png")
        
    app.mainloop()


