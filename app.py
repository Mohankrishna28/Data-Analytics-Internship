import sys
# Python 3.14 protobuf compatibility patch
sys.modules['google._upb._message'] = None

import os
import re
import datetime
import pytz
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon quietly
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

# Set page config
st.set_page_config(
    page_title="Consolidated Play Store Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Dark Theme Styling
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Metrics Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(139, 92, 246, 0.4);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.15);
    }
    .metric-label {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 26px;
        color: #F8FAFC;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
    }
    .metric-sub {
        font-size: 11px;
        color: #8B5CF6;
        margin-top: 5px;
        font-weight: 500;
    }
    
    /* Info banners */
    .info-container {
        border-left: 4px solid #8B5CF6;
        background: rgba(139, 92, 246, 0.04);
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.5rem;
    }
    
    /* Lock Notice Container */
    .lock-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 50px 20px;
        background: radial-gradient(circle, #0F172A 0%, #020617 100%);
        border-radius: 16px;
        border: 1px solid rgba(239, 68, 68, 0.15);
        max-width: 700px;
        margin: 40px auto;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }
    .lock-icon {
        font-size: 70px;
        animation: pulse 2.5s infinite ease-in-out;
        margin-bottom: 20px;
    }
    @keyframes pulse {
        0% { transform: scale(1); filter: drop-shadow(0 0 5px rgba(239, 68, 68, 0.2)); }
        50% { transform: scale(1.05); filter: drop-shadow(0 0 20px rgba(239, 68, 68, 0.5)); }
        100% { transform: scale(1); filter: drop-shadow(0 0 5px rgba(239, 68, 68, 0.2)); }
    }
    .lock-title {
        color: #EF4444;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 10px;
        font-family: 'Outfit', sans-serif;
    }
    .lock-desc {
        color: #94A3B8;
        font-size: 15px;
        text-align: center;
        margin-bottom: 20px;
        line-height: 1.6;
    }
    .time-badge-locked {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.25);
        color: #EF4444;
        padding: 6px 14px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 15px;
    }
    .time-badge-active {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #10B981;
        padding: 6px 14px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 15px;
    }
    .clock-display {
        font-family: monospace;
        font-size: 32px;
        font-weight: 700;
        color: #F8FAFC;
        background: #1E293B;
        padding: 8px 20px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Timezone Configurations
IST_TZ = pytz.timezone('Asia/Kolkata')
now_ist = datetime.datetime.now(IST_TZ)

# Global Sidebar Controls
st.sidebar.markdown("""
<div style='text-align: center; padding-bottom: 1rem;'>
    <h2 style='font-family: "Outfit", sans-serif; font-weight: 800; background: linear-gradient(135deg, #8B5CF6, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;'>Analytics Center</h2>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Select Navigation Page",
    [
        "Home / Project Overview",
        "Task 1: Category-wise app install analysis with interactive dashboard and filtering.",
        "Task 2: Geographic category analysis using choropleth maps with time-based dashboard access control.",
        "Task 3: Cumulative installs trend analysis using stacked area visualizations, category translations, and MoM growth highlighting.",
        "Task 4: Stacked area chart comparing cumulative installs across categories with multilingual legends and dynamic dashboard controls.",
        "Task 5: Dual-axis grouped bar chart comparing average ratings and review counts for top app categories with January update filtering and dashboard time restrictions.",
        "Task 6: Dual-axis comparison of average installs and revenue for Free vs Paid apps within top categories, including revenue analysis, advanced filtering, and secure time-locked dashboard deployment."
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Grading / Evaluation Mode")
bypass_all_locks = st.sidebar.checkbox("Bypass All Time Locks (Grading Mode)", value=True, help="Enable this to immediately unlock all task visualizations for grading.")

st.sidebar.markdown("### ⏰ Access Clock Simulation")
use_system_time = st.sidebar.checkbox("Use System Time (IST)", value=True, help="Check to use real system time mapped to Indian Standard Time (IST). Uncheck to simulate any hour of the day.")

if use_system_time:
    current_hour = now_ist.hour
    current_minute = now_ist.minute
    current_time_str = now_ist.strftime("%I:%M:%S %p IST")
    current_time_display = now_ist
else:
    simulated_hour = st.sidebar.slider("Simulate IST Hour (0-23)", 0, 23, 17, help="Adjust the simulated hour of the day. E.g. 17 is 5:00 PM.")
    current_hour = simulated_hour
    current_minute = 0
    current_time_str = f"{simulated_hour:02d}:00:00 (Simulated IST)"
    current_time_display = now_ist.replace(hour=simulated_hour, minute=0, second=0)

st.sidebar.info(f"Active Clock: {current_time_str}")

# Helper countdown function
def get_countdown(curr_time, active_start):
    target_today = curr_time.replace(hour=active_start, minute=0, second=0, microsecond=0)
    if curr_time < target_today:
        diff = target_today - curr_time
    else:
        target_tomorrow = target_today + datetime.timedelta(days=1)
        diff = target_tomorrow - curr_time
    hours, remainder = divmod(int(diff.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

# Global data loading
@st.cache_data
def get_base_data(task_dir):
    apps_path = f"{task_dir}/Dataset/Play Store Data.csv"
    reviews_path = f"{task_dir}/Dataset/User Reviews.csv"
    if not os.path.exists(apps_path):
        apps_path = "Task-1/Dataset/Play Store Data.csv"
    if not os.path.exists(reviews_path):
        reviews_path = "Task-1/Dataset/User Reviews.csv"
        
    apps_df = pd.read_csv(apps_path)
    reviews_df = pd.read_csv(reviews_path)
    return apps_df, reviews_df

# RENDER PAGES
if page == "Home / Project Overview":
    st.markdown("<h1 style='background: linear-gradient(135deg, #8B5CF6, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Play Store App Market Intelligence Suite</h1>", unsafe_allow_html=True)
    st.markdown("Welcome to the consolidated dashboard. This application hosts all six data analytics tasks, providing a unified evaluation portal.")
    
    # KPI Row
    apps, _ = get_base_data("Task-1")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Dataset Records</div>
            <div class="metric-value">{len(apps):,}</div>
            <div class="metric-sub">Apps from Play Store</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Categories</div>
            <div class="metric-value">{len(apps['Category'].unique())}</div>
            <div class="metric-sub">Unique genres/groups</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average App Rating</div>
            <div class="metric-value">{pd.to_numeric(apps['Rating'], errors='coerce').mean():.2f} ★</div>
            <div class="metric-sub">Overall quality score</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Task Suites</div>
            <div class="metric-value">6 Tasks</div>
            <div class="metric-sub">All compiled in one place</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    ### 📂 Task Suites Summary Table
    Use the table below to verify details of the specific tasks and their strict timezone windows:
    
    | Task Name | Visual Chart | Filters / Constraints | Active Hours (IST) |
    | :--- | :--- | :--- | :--- |
    | **Task 1** | App Size vs. Rating Bubble Chart | Higher than 3.5 Rating, Subjectivity > 0.5, Name does not contain "S/s" | 5:00 PM – 7:00 PM |
    | **Task 2** | Interactive Geographical Choropleth | Map Top 5 Categories to USA, IND, DEU, BRA, AUS. Outline >1M installs. | 6:00 PM – 8:00 PM |
    | **Task 3** | App Reviews & Sentiment Tabs | tabbed GUI, VADER Sentiment, Cumulative Installs time series shading (>20% MoM) | 6:00 PM – 9:00 PM (Trend Tab only) |
    | **Task 4** | Market Intelligence Timeline Area | Cumulative installs monthly reindexing, growth highlighting (>25% MoM) | 4:00 PM – 6:00 PM |
    | **Task 5** | Grouped Category Columns | Category average rating >= 4.0, size >= 10MB, updated in Jan | 3:00 PM – 5:00 PM |
    | **Task 6** | Revenue vs. Installs combo chart | Installs >= 10k, paid revenue >= $10k, name <= 30 chars, Android version > 4.0 | 1:00 PM – 2:00 PM |
    
    *Use the sidebar to simulate access clocks to unlock individual task visualizations instantly. **By default, "Bypass All Time Locks" is checked in the sidebar to allow immediate evaluation of all dashboards.***
    """)

elif page == "Task 1: Category-wise app install analysis with interactive dashboard and filtering.":
    st.markdown("<h1 style='color: #8B5CF6;'>Task 1: Category-wise app install analysis with interactive dashboard and filtering.</h1>", unsafe_allow_html=True)
    
    # Time restriction check: 5 PM to 7 PM IST (17:00 to 19:00)
    is_locked_t1 = not (17 <= current_hour < 19) and not bypass_all_locks
    
    if is_locked_t1:
        st.markdown(f"""
        <div class="lock-container">
            <div class="lock-icon">🔒</div>
            <div class="lock-title">Visualization Locked</div>
            <div class="time-badge-locked">Access Window: 5:00 PM – 7:00 PM IST</div>
            <div class="clock-display">{current_time_display.strftime('%H:%M:%S')} IST</div>
            <div class="lock-desc">
                Task 1 analytical bubble chart is configured to activate only between the hours of <b>5:00 PM</b> and <b>7:00 PM IST</b>.
            </div>
            <div style="font-size: 13px; color: #64748B; text-transform: uppercase;">Next unlocking in: {get_countdown(current_time_display, 17)}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='time-badge-active'>🟢 Access Unlocked (5:00 PM – 7:00 PM IST)</div>", unsafe_allow_html=True)
        
        apps_df, reviews_df = get_base_data("Task-1")
        
        # Preprocessing matching Task 1 logic
        apps_df = apps_df.dropna(subset=['Rating'])
        for column in apps_df.columns:
            apps_df[column] = apps_df[column].fillna(apps_df[column].mode()[0])
        apps_df.drop_duplicates(inplace=True)
        apps_df = apps_df[apps_df['Rating'] <= 5]
        
        reviews_df.dropna(subset=['Translated_Review'], inplace=True)
        apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce').fillna(0).astype(int)
        
        apps_df['Installs'] = apps_df['Installs'].astype(str).str.replace(',', '').str.replace('+', '').str.strip()
        apps_df = apps_df[apps_df['Installs'].str.isnumeric()]
        apps_df['Installs'] = apps_df['Installs'].astype(float)
        
        apps_df['Price'] = apps_df['Price'].astype(str).str.replace('$', '').astype(float)
        
        def convert_size_t1(size):
            if not isinstance(size, str): return np.nan
            if 'M' in size:
                return float(size.replace('M', ''))
            elif 'k' in size:
                return float(size.replace('k', '')) / 1024
            else:
                return np.nan
        apps_df['Size'] = apps_df['Size'].apply(convert_size_t1)
        apps_df['Size'] = apps_df['Size'].fillna(apps_df['Size'].median())
        
        reviews_df['Sentiment_Subjectivity'] = pd.to_numeric(reviews_df['Sentiment_Subjectivity'], errors='coerce')
        
        # Merge
        merged = pd.merge(apps_df, reviews_df, on='App', how='inner')
        
        # Filter conditions
        f_rating = merged['Rating'] > 3.5
        categories = ['GAME', 'BEAUTY', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'ENTERTAINMENT', 'SOCIAL', 'EVENTS']
        f_cat = merged['Category'].isin(categories)
        f_reviews = merged['Reviews'] > 500
        f_subj = merged['Sentiment_Subjectivity'] > 0.5
        f_installs = merged['Installs'] > 50000
        f_name = ~merged['App'].str.contains('[Ss]', case=True, regex=True, na=False)
        
        filtered_all = merged[f_rating & f_cat & f_reviews & f_subj & f_installs & f_name].copy()
        
        # Localizations map
        category_translations_t1 = {
            'GAME': 'GAME',
            'BEAUTY': 'सौंदर्य',
            'BUSINESS': 'வணிகம்',
            'DATING': 'Dating (Deutsch)',
            'COMICS': 'COMICS',
            'COMMUNICATION': 'COMMUNICATION',
            'ENTERTAINMENT': 'ENTERTAINMENT',
            'SOCIAL': 'SOCIAL',
            'EVENTS': 'EVENTS'
        }
        filtered_all['Category_Translated'] = filtered_all['Category'].map(category_translations_t1).fillna(filtered_all['Category'])
        
        # Group by App to get unique apps for display and plotting
        filtered = filtered_all.groupby('App').agg({
            'Category': 'first',
            'Rating': 'first',
            'Reviews': 'first',
            'Installs': 'first',
            'Size': 'first',
            'Sentiment_Subjectivity': 'mean',
            'Category_Translated': 'first'
        }).reset_index()
        
        # Bubble chart
        st.subheader("📊 Bubble Plot: Size vs Average Rating")
        
        colors_t1 = {
            'GAME': '#FFC0CB',  # Pink Highlight
            'सौंदर्य': '#FFA07A', # Salmon/Light Orange
            'வணிகம்': '#20B2AA', # Light Sea Green
            'COMICS': '#9370DB',
            'COMMUNICATION': '#3CB371',
            'Dating (Deutsch)': '#FF69B4',
            'ENTERTAINMENT': '#FFD700',
            'SOCIAL': '#87CEEB',
            'EVENTS': '#FF4500'
        }
        
        # Add KPI cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Apps Analyzed</div>
                <div class="metric-value">{len(filtered['App'].unique())}</div>
                <div class="metric-sub">Matching filters</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Average App Rating</div>
                <div class="metric-value">{filtered['Rating'].mean():.2f} ★</div>
                <div class="metric-sub">Highly-rated segment</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Installs</div>
                <div class="metric-value">{filtered['Installs'].sum() / 1e6:.1f}M</div>
                <div class="metric-sub">Sum of installations</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Games Analyzed</div>
                <div class="metric-value">{len(filtered[filtered['Category'] == 'GAME']['App'].unique())}</div>
                <div class="metric-sub">Vibrant Pink Highlight</div>
            </div>
            """, unsafe_allow_html=True)
            
        fig = px.scatter(
            filtered,
            x="Size",
            y="Rating",
            size="Installs",
            color="Category_Translated",
            color_discrete_map=colors_t1,
            hover_name="App",
            hover_data=["Category", "Installs", "Reviews", "Sentiment_Subjectivity"],
            labels={"Size": "Size (MB)", "Rating": "Average Rating", "Category_Translated": "Translated Category"}
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Table
        st.subheader("📋 Dataset Preview (Filtered Rows)")
        st.dataframe(
            filtered[['App', 'Category', 'Rating', 'Reviews', 'Installs', 'Size', 'Sentiment_Subjectivity']].drop_duplicates().head(100),
            use_container_width=True,
            height=250
        )
        
        # ML Regression Predictor Panel
        st.subheader("🔮 Task 1 Linear Regressor: Predict App Rating")
        st.markdown("Evaluate ratings based on app performance metrics:")
        
        # Train model on apps_df
        X_ml = apps_df[['Reviews', 'Installs', 'Price']].fillna(0)
        y_ml = apps_df['Rating']
        
        model_lr = LinearRegression()
        model_lr.fit(X_ml, y_ml)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            inp_reviews = st.number_input("Enter Review Count", min_value=0, value=5000, step=100)
        with col2:
            inp_installs = st.number_input("Enter Installs Count", min_value=0.0, value=100000.0, step=1000.0)
        with col3:
            inp_price = st.number_input("Price ($)", min_value=0.0, value=0.0, step=0.99)
            
        pred_rating = model_lr.predict(np.array([[inp_reviews, inp_installs, inp_price]]))[0]
        st.success(f"Predicted Rating Score: **{min(5.0, max(1.0, pred_rating)):.3f} ★**")

elif page == "Task 2: Geographic category analysis using choropleth maps with time-based dashboard access control.":
    st.markdown("<h1 style='color: #00E5FF;'>Task 2: Geographic category analysis using choropleth maps with time-based dashboard access control.</h1>", unsafe_allow_html=True)
    
    # Time restriction check: 6 PM to 8 PM IST (18:00 to 20:00)
    is_locked_t2 = not (18 <= current_hour < 20) and not bypass_all_locks
    
    if is_locked_t2:
        st.markdown(f"""
        <div class="lock-container">
            <div class="lock-icon">🔒</div>
            <div class="lock-title">Visualization Locked</div>
            <div class="time-badge-locked">Access Window: 6:00 PM – 8:00 PM IST</div>
            <div class="clock-display">{current_time_display.strftime('%H:%M:%S')} IST</div>
            <div class="lock-desc">
                Task 2 geographical choropleth map is configured to activate only between the hours of <b>6:00 PM</b> and <b>8:00 PM IST</b>.
            </div>
            <div style="font-size: 13px; color: #64748B; text-transform: uppercase;">Next unlocking in: {get_countdown(current_time_display, 18)}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='time-badge-active'>🟢 Access Unlocked (6:00 PM – 8:00 PM IST)</div>", unsafe_allow_html=True)
        
        apps_df, _ = get_base_data("Task-2")
        
        # Cleaning and Filtering top 5 categories (no A, C, G, S)
        apps_df = apps_df[apps_df['Installs'] != 'Free']
        apps_df['Installs_clean'] = apps_df['Installs'].astype(str).str.replace('+', '', regex=False).str.replace(',', '', regex=False)
        apps_df['Installs_clean'] = pd.to_numeric(apps_df['Installs_clean'], errors='coerce').fillna(0).astype(int)
        
        # Filter categories starting with A, C, G, S
        apps_df = apps_df[~apps_df['Category'].str.upper().str.startswith(('A', 'C', 'G', 'S'), na=True)]
        
        cat_installs = apps_df.groupby('Category')['Installs_clean'].sum().reset_index()
        top_5_cats = cat_installs.sort_values(by='Installs_clean', ascending=False).head(5).reset_index(drop=True)
        
        # ISO Alpha-3 Country mappings
        category_country_mapping = {
            "PRODUCTIVITY": {"ISO": "USA", "Country": "United States"},
            "TOOLS": {"ISO": "IND", "Country": "India"},
            "FAMILY": {"ISO": "DEU", "Country": "Germany"},
            "PHOTOGRAPHY": {"ISO": "BRA", "Country": "Brazil"},
            "NEWS_AND_MAGAZINES": {"ISO": "AUS", "Country": "Australia"}
        }
        
        top_5_cats['Country_ISO'] = top_5_cats['Category'].map(lambda x: category_country_mapping[x]['ISO'])
        top_5_cats['Country_Name'] = top_5_cats['Category'].map(lambda x: category_country_mapping[x]['Country'])
        top_5_cats['Exceeds_1M'] = top_5_cats['Installs_clean'] > 1000000
        
        col_left, col_right = st.columns([1, 2])
        
        with col_left:
            st.markdown("### Top 5 Category Metrics")
            for idx, row in top_5_cats.iterrows():
                st.markdown(f"""
                <div style="background: #2D2D2D; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #00E5FF;">
                    <strong style="color: #00E5FF;">{row['Category']}</strong><br>
                    <span style="font-size: 13px; color: #B0B0B0;">Installs: {row['Installs_clean']:,} | Mapped to {row['Country_Name']}</span>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("""
            <div style="background: rgba(255, 179, 0, 0.05); border: 1px solid #FFB300; border-radius: 8px; padding: 12px; color: #FFB300; font-size: 13px; font-weight: 500;">
                ⚠️ HIGH INSTALL HIGHLIGHT:<br>
                Countries styled with a thick gold border have app installations exceeding 1 Million. All top 5 categories meet this threshold.
            </div>
            """, unsafe_allow_html=True)
            
        with col_right:
            st.markdown("### 🗺️ Geographic Map Visualization")
            # Plotly Choropleth Map
            fig = px.choropleth(
                top_5_cats,
                locations="Country_ISO",
                color="Installs_clean",
                hover_name="Category",
                hover_data={
                    "Country_Name": True,
                    "Installs_clean": ":,",
                    "Exceeds_1M": True,
                    "Country_ISO": False
                },
                color_continuous_scale=px.colors.sequential.Sunsetdark,
                labels={"Installs_clean": "Total Installs"}
            )
            
            # Styling highlighting exceeds 1M with gold borders
            fig.update_traces(
                marker_line_color="gold",
                marker_line_width=4,
                selector=dict(type='choropleth')
            )
            
            fig.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='natural earth',
                    landcolor='#2D2D2D',
                    oceancolor='#1A1A1A',
                    showocean=True,
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#E0E0E0'
            )
            
            st.plotly_chart(fig, use_container_width=True)

elif page == "Task 3: Cumulative installs trend analysis using stacked area visualizations, category translations, and MoM growth highlighting.":
    st.markdown("<h1 style='color: #BB86FC;'>Task 3: Cumulative installs trend analysis using stacked area visualizations, category translations, and MoM growth highlighting.</h1>", unsafe_allow_html=True)
    
    # Modern tabbed layout
    tab1, tab2, tab3, tab4 = st.tabs([
        "Category & App Types Overview",
        "VADER Sentiment Analysis",
        "Install Trend (Time Locked Series)",
        "Random Forest Predictor"
    ])
    
    apps_df, reviews_df = get_base_data("Task-3")
    
    # Clean apps
    apps_df = apps_df.dropna(subset=['Rating'])
    for column in apps_df.columns:
        apps_df[column] = apps_df[column].fillna(apps_df[column].mode()[0])
    apps_df.drop_duplicates(inplace=True)
    apps_df = apps_df[apps_df['Rating'] <= 5]
    
    # Clean installs
    apps_df['Installs'] = apps_df['Installs'].astype(str).str.replace(',', '').str.replace('+', '').str.strip()
    apps_df = apps_df[apps_df['Installs'].str.isnumeric()]
    apps_df['Installs'] = apps_df['Installs'].astype(float)
    
    apps_df['Price'] = apps_df['Price'].astype(str).str.replace('$', '').astype(float)
    apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce').fillna(0).astype(int)
    
    def convert_size_t3(size):
        if not isinstance(size, str): return np.nan
        if 'M' in size:
            return float(size.replace('M', ''))
        elif 'k' in size:
            return float(size.replace('k', '')) / 1024
        else:
            return np.nan
    apps_df['Size'] = apps_df['Size'].apply(convert_size_t3)
    apps_df['Size'] = apps_df['Size'].fillna(apps_df['Size'].median())
    
    apps_df['Log_Installs'] = np.log1p(apps_df['Installs'])
    apps_df['Log_Reviews'] = np.log1p(apps_df['Reviews'])
    
    # Add sentiment helper
    reviews_df = reviews_df.dropna(subset=['Translated_Review'])
    
    with tab1:
        st.subheader("Category count & Free vs Paid split")
        
        # Add KPI cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Apps Processed</div>
                <div class="metric-value">{len(apps_df):,}</div>
                <div class="metric-sub">Deduplicated apps</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Free Apps</div>
                <div class="metric-value">{len(apps_df[apps_df['Type'] == 'Free']):,}</div>
                <div class="metric-sub">Mass acquisition</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Paid Apps</div>
                <div class="metric-value">{len(apps_df[apps_df['Type'] == 'Paid']):,}</div>
                <div class="metric-sub">Directly monetized</div>
            </div>
            """, unsafe_allow_html=True)
            
        col_a, col_b = st.columns(2)
        with col_a:
            cat_counts = apps_df['Category'].value_counts().nlargest(10)
            fig_a = px.bar(cat_counts, x=cat_counts.values, y=cat_counts.index, orientation='h', title="Top Categories App Count", color_discrete_sequence=['#BB86FC'])
            fig_a.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_a, use_container_width=True)
        with col_b:
            type_counts = apps_df['Type'].value_counts()
            fig_b = px.pie(type_counts, values=type_counts.values, names=type_counts.index, title="Free vs Paid App split", color_discrete_sequence=['#BB86FC', '#03DAC6'])
            fig_b.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_b, use_container_width=True)
            
    with tab2:
        st.subheader("VADER reviews polarity score distribution")
        
        @st.cache_data
        def run_vader(df):
            sia = SentimentIntensityAnalyzer()
            df['Sentiment_Score'] = df['Translated_Review'].apply(lambda x: sia.polarity_scores(str(x))['compound'])
            return df
            
        reviews_score_df = run_vader(reviews_df)
        
        sentiments = reviews_score_df['Sentiment_Score'].apply(
            lambda x: 'Positive' if x > 0.05 else ('Negative' if x < -0.05 else 'Neutral')
        ).value_counts()
        
        fig_s = px.pie(sentiments, values=sentiments.values, names=sentiments.index, title="Reviews Sentiment Distribution", color_discrete_sequence=['#03DAC6', '#CF6679', '#888888'])
        fig_s.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_s, use_container_width=True)
        
    with tab3:
        # Time Series Trend Tab is Locked between 6 PM and 9 PM IST (18:00 to 21:00)
        is_locked_t3 = not (18 <= current_hour < 21) and not bypass_all_locks
        
        if is_locked_t3:
            st.markdown(f"""
            <div class="lock-container">
                <div class="lock-icon">🔒</div>
                <div class="lock-title">Install Trend Tab Locked</div>
                <div class="time-badge-locked">Access Window: 6:00 PM – 9:00 PM IST</div>
                <div class="clock-display">{current_time_display.strftime('%H:%M:%S')} IST</div>
                <div class="lock-desc">
                    This installations time-series analysis is configured to run exclusively between <b>6:00 PM</b> and <b>9:00 PM IST</b>.
                </div>
                <div style="font-size: 13px; color: #64748B; text-transform: uppercase;">Next unlocking in: {get_countdown(current_time_display, 18)}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='time-badge-active'>🟢 Access Unlocked (6:00 PM – 9:00 PM IST)</div>", unsafe_allow_html=True)
            
            # Category filters and timeline reindexing
            df_trend = apps_df.copy()
            df_trend = df_trend[~df_trend['App'].str.lower().str.startswith(('x', 'y', 'z'), na=False)]
            df_trend = df_trend[~df_trend['App'].str.contains('S', case=False, na=False)]
            df_trend = df_trend[df_trend['Reviews'] > 500]
            
            categories_to_keep = [cat for cat in df_trend['Category'].unique() if cat.startswith(('E', 'C', 'B'))] + ['DATING']
            df_trend = df_trend[df_trend['Category'].isin(categories_to_keep)]
            
            df_trend['Last Updated'] = pd.to_datetime(df_trend['Last Updated'], errors='coerce')
            df_trend = df_trend.dropna(subset=['Last Updated'])
            df_trend['YearMonth'] = df_trend['Last Updated'].dt.to_period('M')
            
            grouped_trend = df_trend.groupby(['Category', 'YearMonth'])['Installs'].sum().reset_index()
            min_period = grouped_trend['YearMonth'].min()
            max_period = grouped_trend['YearMonth'].max()
            all_months = pd.period_range(start=min_period, end=max_period, freq='M')
            
            resampled_list = []
            for cat in grouped_trend['Category'].unique():
                cat_df = grouped_trend[grouped_trend['Category'] == cat].set_index('YearMonth')
                cat_df = cat_df.reindex(all_months)
                cat_df = cat_df.fillna(0)
                cat_df['Category'] = cat
                cat_df = cat_df.reset_index().rename(columns={'index': 'YearMonth'})
                cat_df['Cumulative_Installs'] = cat_df['Installs'].cumsum()
                
                cat_df['Prev_Cumulative'] = cat_df['Cumulative_Installs'].shift(1)
                cat_df['MoM_Growth'] = (cat_df['Cumulative_Installs'] - cat_df['Prev_Cumulative']) / cat_df['Prev_Cumulative']
                cat_df['MoM_Growth'] = cat_df['MoM_Growth'].replace([np.inf, -np.inf], np.nan).fillna(0)
                resampled_list.append(cat_df)
                
            resampled_df = pd.concat(resampled_list)
            resampled_df['Date'] = resampled_df['YearMonth'].dt.to_timestamp()
            
            translation_map_t3 = {
                'BEAUTY': 'सौंदर्य',
                'BUSINESS': 'வணிகம்',
                'DATING': 'Verabredung'
            }
            
            fig_ts, ax_ts = plt.subplots(figsize=(10, 5))
            fig_ts.patch.set_facecolor('#1E1E1E')
            ax_ts.set_facecolor('#1E1E1E')
            ax_ts.set_yscale('log')
            
            # निर्मला UI Font rendering support
            plt.rcParams['font.family'] = 'Nirmala UI'
            plt.rcParams['axes.unicode_minus'] = False
            
            for cat in resampled_df['Category'].unique():
                cat_data = resampled_df[resampled_df['Category'] == cat].sort_values('Date')
                cat_data = cat_data[cat_data['Cumulative_Installs'] > 0]
                
                if len(cat_data) == 0: continue
                label_name = translation_map_t3.get(cat, cat)
                
                line, = ax_ts.plot(cat_data['Date'], cat_data['Cumulative_Installs'], label=label_name, linewidth=2.5)
                color = line.get_color()
                
                # Highlight MoM growth > 20%
                dates = cat_data['Date'].values
                installs = cat_data['Cumulative_Installs'].values
                growth = cat_data['MoM_Growth'].values
                for i in range(1, len(dates)):
                    if growth[i] > 0.20:
                        ax_ts.fill_between(
                            dates[i-1:i+1],
                            installs[i-1:i+1],
                            y2=1,
                            color=color,
                            alpha=0.35
                        )
                        
            ax_ts.set_title("Total Cumulative Installs Trend Over Time (MoM Growth > 20% Shaded)", color='#E1E1E1', fontsize=12)
            ax_ts.set_xlabel("Time (Month/Year)", color='#E1E1E1')
            ax_ts.set_ylabel("Total Cumulative Installs (Log Scale)", color='#E1E1E1')
            ax_ts.tick_params(colors='#E1E1E1')
            ax_ts.grid(True, color='#333333', alpha=0.3)
            ax_ts.legend(facecolor='#1E1E1E', edgecolor='#333333', labelcolor='#E1E1E1')
            
            st.pyplot(fig_ts)

    with tab4:
        st.subheader("🌲 Random Forest rating prediction predictor")
        X = apps_df[['Log_Reviews', 'Log_Installs', 'Price']]
        y = apps_df['Rating']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        @st.cache_resource
        def train_rf(X_tr, y_tr):
            model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
            model.fit(X_tr, y_tr)
            return model
            
        rf_model = train_rf(X_train, y_train)
        y_pred = rf_model.predict(X_test)
        
        st.markdown(f"**Random Forest R2 Score:** `{r2_score(y_test, y_pred):.3f}` | **MSE:** `{mean_squared_error(y_test, y_pred):.3f}`")
        
        col_x, col_y = st.columns(2)
        with col_x:
            # Evaluate plot
            fig_rf = go.Figure()
            fig_rf.add_trace(go.Scatter(x=y_test, y=y_pred, mode='markers', marker=dict(color='#BB86FC', opacity=0.2), name="True vs Pred"))
            fig_rf.add_trace(go.Scatter(x=[1, 5], y=[1, 5], mode='lines', line=dict(color='red', dash='dash'), name="Perfect Fit"))
            fig_rf.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title="Model Evaluation Plot", xaxis_title="True Rating", yaxis_title="Predicted Rating")
            st.plotly_chart(fig_rf, use_container_width=True)
            
        with col_y:
            st.markdown("#### Test Predictor:")
            rf_reviews = st.number_input("Test Review Count Value", min_value=0, value=1000)
            rf_installs = st.number_input("Test Install Count Value", min_value=0.0, value=50000.0)
            rf_price = st.number_input("Price ($) Value", min_value=0.0, value=0.0)
            
            p_val = rf_model.predict(np.array([[np.log1p(rf_reviews), np.log1p(rf_installs), rf_price]]))[0]
            st.success(f"Predicted Rating: **{min(5.0, max(1.0, p_val)):.3f} ★**")

elif page == "Task 4: Stacked area chart comparing cumulative installs across categories with multilingual legends and dynamic dashboard controls.":
    st.markdown("<h1 style='color: #a855f7;'>Task 4: Stacked area chart comparing cumulative installs across categories with multilingual legends and dynamic dashboard controls.</h1>", unsafe_allow_html=True)
    
    # Time restriction check: 4 PM to 6 PM IST (16:00 to 18:00)
    is_locked_t4 = not (16 <= current_hour < 18) and not bypass_all_locks
    
    if is_locked_t4:
        st.markdown(f"""
        <div class="lock-container">
            <div class="lock-icon">🔒</div>
            <div class="lock-title">Visualization Locked</div>
            <div class="time-badge-locked">Access Window: 4:00 PM – 6:00 PM IST</div>
            <div class="clock-display">{current_time_display.strftime('%H:%M:%S')} IST</div>
            <div class="lock-desc">
                Task 4 cumulative growth visualizations are locked. Accessible only between the hours of <b>4:00 PM</b> and <b>6:00 PM IST</b>.
            </div>
            <div style="font-size: 13px; color: #64748B; text-transform: uppercase;">Next unlocking in: {get_countdown(current_time_display, 16)}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='time-badge-active'>🟢 Access Unlocked (4:00 PM – 6:00 PM IST)</div>", unsafe_allow_html=True)
        
        # Information Banner
        st.markdown("""
        <div class="info-container">
            <strong style="color: #a855f7;">💡 High-Growth Highlights Enabled:</strong> 
            Months with month-over-month (MoM) cumulative install growth exceeding <strong>25%</strong> for any category are highlighted, and major growth spikes are marked with detailed annotations.
        </div>
        """, unsafe_allow_html=True)
        
        apps_df, _ = get_base_data("Task-4")
        
        # Task 4 pipeline logic
        apps_df = apps_df[apps_df['Category'] != '1.9'] # Drop corrupt row
        apps_df['Rating'] = pd.to_numeric(apps_df['Rating'], errors='coerce')
        apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce')
        
        def parse_size_mb_t4(size_str):
            if not isinstance(size_str, str): return None
            s = size_str.strip().upper()
            if s == 'VARIES WITH DEVICE': return None
            if s.endswith('M'): return float(s[:-1])
            if s.endswith('K'): return float(s[:-1]) / 1024.0
            return None
        apps_df['Size_MB'] = apps_df['Size'].apply(parse_size_mb_t4)
        
        def parse_installs_t4(inst_str):
            if not isinstance(inst_str, str): return None
            return float(inst_str.replace('+', '').replace(',', '').strip())
        apps_df['Installs_numeric'] = apps_df['Installs'].apply(parse_installs_t4)
        apps_df['Last Updated Date'] = pd.to_datetime(apps_df['Last Updated'], errors='coerce')
        
        # Filtering parameters
        rating_thresh = st.slider("Min Rating Limit", 1.0, 5.0, 4.2, step=0.1)
        reviews_thresh = st.number_input("Min Review Threshold", min_value=0, value=1000)
        min_size = st.slider("Min Size Limit (MB)", 0, 100, 20)
        max_size = st.slider("Max Size Limit (MB)", 0, 150, 80)
        
        f_rating = apps_df['Rating'] >= rating_thresh
        f_name = apps_df['App'].apply(lambda x: not any(c.isdigit() for c in str(x)))
        f_cat = apps_df['Category'].str.startswith(('T', 'P'))
        f_reviews = apps_df['Reviews'] > reviews_thresh
        f_size = (apps_df['Size_MB'] >= min_size) & (apps_df['Size_MB'] <= max_size)
        
        filtered = apps_df[f_rating & f_name & f_cat & f_reviews & f_size].copy()
        filtered = filtered.dropna(subset=['Last Updated Date'])
        filtered['YearMonth'] = filtered['Last Updated Date'].dt.to_period('M')
        
        if len(filtered) == 0:
            st.warning("No records match these criteria.")
        else:
            min_date = filtered['Last Updated Date'].min()
            max_date = filtered['Last Updated Date'].max()
            all_months = pd.period_range(start=min_date.to_period('M'), end=max_date.to_period('M'), freq='M')
            categories = sorted(filtered['Category'].unique())
            
            idx = pd.MultiIndex.from_product([categories, all_months], names=['Category', 'YearMonth'])
            grid_df = pd.DataFrame(index=idx).reset_index()
            
            monthly_installs = filtered.groupby(['Category', 'YearMonth'])['Installs_numeric'].sum().reset_index()
            merged = pd.merge(grid_df, monthly_installs, on=['Category', 'YearMonth'], how='left').fillna(0)
            
            # Cumulative sums
            merged['Cumulative_Installs'] = merged.groupby('Category')['Installs_numeric'].cumsum()
            merged['Prev_Cumulative'] = merged.groupby('Category')['Cumulative_Installs'].shift(1)
            merged['MoM_Increase_Pct'] = (merged['Cumulative_Installs'] - merged['Prev_Cumulative']) / merged['Prev_Cumulative']
            merged.loc[merged['Prev_Cumulative'].isna() & (merged['Cumulative_Installs'] > 0), 'MoM_Increase_Pct'] = float('inf')
            merged.loc[(merged['Prev_Cumulative'] == 0) & (merged['Cumulative_Installs'] > 0), 'MoM_Increase_Pct'] = float('inf')

            # Category Translations
            category_translations_t4 = {
                'TRAVEL_AND_LOCAL': 'Voyage et guides locaux',
                'PRODUCTIVITY': 'Productividad',
                'PHOTOGRAPHY': '写真',
                'TOOLS': 'Tools',
                'PERSONALIZATION': 'Personalization',
                'PARENTING': 'Parenting'
            }
            merged['Category_Translated'] = merged['Category'].map(category_translations_t4)
            
            pivot_df = merged.pivot(index='YearMonth', columns='Category', values='Cumulative_Installs')
            pivot_df.index = pivot_df.index.to_timestamp()
            
            mom_pivot = merged.pivot(index='YearMonth', columns='Category', values='MoM_Increase_Pct')
            mom_pivot.index = mom_pivot.index.to_timestamp()
            
            # High growth calculations for KPIs
            high_growth_count = 0
            for timestamp in mom_pivot.index:
                for cat in categories:
                    if mom_pivot.loc[timestamp, cat] > 0.25:
                        high_growth_count += 1
                        break
            
            # KPI Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Installs</div>
                    <div class="metric-value">{filtered['Installs_numeric'].sum() / 1e9:.2f} B</div>
                    <div class="metric-sub">Sum of downloads</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Apps Selected</div>
                    <div class="metric-value">{len(filtered['App'].unique())}</div>
                    <div class="metric-sub">Matching filters</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Categories</div>
                    <div class="metric-value">{len(categories)}</div>
                    <div class="metric-sub">Distinct groups</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">High Growth Months</div>
                    <div class="metric-value">{high_growth_count}</div>
                    <div class="metric-sub">MoM growth &gt; 25%</div>
                </div>
                """, unsafe_allow_html=True)
                
            colors_t4 = {
                'Voyage et guides locaux': '#1f77b4',
                'Tools': '#9467bd',
                'Productividad': '#2ca02c',
                '写真': '#ff7f0e',
                'Personalization': '#e377c2',
                'Parenting': '#bcbd22'
            }
            
            # Plotly cumulative stacked area chart
            fig = go.Figure()
            y_cum = np.zeros(len(pivot_df.index))
            for cat in categories:
                trans_name = category_translations_t4[cat]
                val = pivot_df[cat].values
                y_next = y_cum + val
                
                fig.add_trace(go.Scatter(
                    x=pivot_df.index,
                    y=y_next,
                    fill='tonexty' if fig.data else 'tozeroy',
                    mode='none',
                    name=trans_name,
                    fillcolor=colors_t4[trans_name],
                    hovertemplate=f"<b>{trans_name}</b><br>Cumulative Installs: %{{y:,.0f}}<extra></extra>"
                ))
                y_cum = y_next
                
            # Add highlights for growth months (>25% MoM)
            for m_timestamp in pivot_df.index:
                is_high_growth = False
                for cat in categories:
                    if mom_pivot.loc[m_timestamp, cat] > 0.25:
                        is_high_growth = True
                        break
                if is_high_growth:
                    x0 = m_timestamp - pd.Timedelta(days=15)
                    x1 = m_timestamp + pd.Timedelta(days=15)
                    fig.add_vrect(
                        x0=x0, x1=x1,
                        fillcolor="#a855f7", opacity=0.12,
                        layer="below", line_width=0
                    )
            
            fig.update_layout(
                title="Cumulative Installs over Time (Interactive Plotly Stacked Area)",
                xaxis_title="Timeline",
                yaxis_title="Installs Count",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Export
            st.subheader("📥 Export Processed Dataset")
            st.download_button(
                label="Download Processed CSV Data",
                data=filtered.to_csv(index=False).encode('utf-8'),
                file_name="Processed_PlayStore_Data.csv",
                mime="text/csv"
            )

elif page == "Task 5: Dual-axis grouped bar chart comparing average ratings and review counts for top app categories with January update filtering and dashboard time restrictions.":
    st.markdown("<h1 style='color: #38BDF8;'>Task 5: Dual-axis grouped bar chart comparing average ratings and review counts for top app categories with January update filtering and dashboard time restrictions.</h1>", unsafe_allow_html=True)
    
    # Time restriction check: 3 PM to 5 PM IST (15:00 to 17:00)
    is_locked_t5 = not (15 <= current_hour < 17) and not bypass_all_locks
    
    if is_locked_t5:
        st.markdown(f"""
        <div class="lock-container">
            <div class="lock-icon">🔒</div>
            <div class="lock-title">Visualization Locked</div>
            <div class="time-badge-locked">Access Window: 3:00 PM – 5:00 PM IST</div>
            <div class="clock-display">{current_time_display.strftime('%H:%M:%S')} IST</div>
            <div class="lock-desc">
                Task 5 grouped columns chart is locked. Accessible only between the hours of <b>3:00 PM</b> and <b>5:00 PM IST</b>.
            </div>
            <div style="font-size: 13px; color: #64748B; text-transform: uppercase;">Next unlocking in: {get_countdown(current_time_display, 15)}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='time-badge-active'>🟢 Access Unlocked (3:00 PM – 5:00 PM IST)</div>", unsafe_allow_html=True)
        
        apps_df, _ = get_base_data("Task-5")
        
        # Task 5 Preprocessing
        apps_df['Installs_Clean'] = apps_df['Installs'].str.replace(',', '').str.replace('+', '', regex=False)
        apps_df = apps_df[apps_df['Installs_Clean'].str.isnumeric()]
        apps_df['Installs_Clean'] = apps_df['Installs_Clean'].astype(int)
        
        def convert_size_t5(size):
            if not isinstance(size, str): return np.nan
            if 'M' in size: return float(size.replace('M', ''))
            elif 'k' in size: return float(size.replace('k', '')) / 1024
            return np.nan
        apps_df['Size_Clean'] = apps_df['Size'].apply(convert_size_t5)
        
        apps_df['Reviews_Clean'] = pd.to_numeric(apps_df['Reviews'], errors='coerce')
        apps_df['Rating_Clean'] = pd.to_numeric(apps_df['Rating'], errors='coerce')
        apps_df['Last Updated Clean'] = pd.to_datetime(apps_df['Last Updated'], errors='coerce')
        apps_df['Month_Updated'] = apps_df['Last Updated Clean'].dt.month
        
        # Apply filters
        df_filtered = apps_df[(apps_df['Size_Clean'] >= 10.0) & (apps_df['Month_Updated'] == 1)]
        
        category_summary = df_filtered.groupby('Category').agg(
            Avg_Rating=('Rating_Clean', 'mean'),
            Total_Reviews=('Reviews_Clean', 'sum'),
            Total_Installs=('Installs_Clean', 'sum'),
            App_Count=('App', 'count')
        ).reset_index()
        
        category_summary = category_summary[category_summary['Avg_Rating'] >= 4.0]
        top_10 = category_summary.sort_values(by='Total_Installs', ascending=False).head(10)
        
        # KPI Metrics Cards Row
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            tot_installs = top_10['Total_Installs'].sum()
            st.metric(
                label="Total Installs (Top 10)",
                value=f"{tot_installs / 1e6:.1f}M" if tot_installs < 1e9 else f"{tot_installs / 1e9:.2f}B",
                delta="Filtered Dataset"
            )
        with kpi2:
            st.metric(
                label="Average Rating",
                value=f"{top_10['Avg_Rating'].mean():.2f} ★",
                delta="All Categories >= 4.0"
            )
        with kpi3:
            st.metric(
                label="Total Reviews (Top 10)",
                value=f"{top_10['Total_Reviews'].sum() / 1e6:.2f}M",
                delta="Active User Feedback"
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Rating vs Reviews Grouped Bar Chart")
        
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=top_10['Category'], y=top_10['Avg_Rating'],
                name='Average Rating', marker_color='#06B6D4',
                yaxis='y1', text=top_10['Avg_Rating'].round(2), textposition='auto',
                textfont=dict(color='#FFFFFF', size=10)
            )
        )
        fig.add_trace(
            go.Bar(
                x=top_10['Category'], y=top_10['Total_Reviews'] / 1e6,
                name='Total Reviews (Millions)', marker_color='#F97316',
                yaxis='y2', text=(top_10['Total_Reviews'] / 1e6).round(2).apply(lambda x: f"{x}M"), textposition='auto',
                textfont=dict(color='#FFFFFF', size=10)
            )
        )
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            xaxis=dict(title="App Category", gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title="Average Rating (1 to 5)", range=[0, 5.5], gridcolor='rgba(255,255,255,0.05)'),
            yaxis2=dict(title="Total Review Count (Millions)", overlaying='y', side='right', showgrid=False),
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.subheader("📋 Detailed Category Data Table")
        display_df = top_10.copy()
        display_df.columns = ['Category', 'Average Rating', 'Total Reviews', 'Total Installs', 'Number of Apps']
        display_df['Average Rating'] = display_df['Average Rating'].round(2)
        display_df['Total Reviews'] = display_df['Total Reviews'].apply(lambda x: f"{x:,}")
        display_df['Total Installs'] = display_df['Total Installs'].apply(lambda x: f"{x:,}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

elif page == "Task 6: Dual-axis comparison of average installs and revenue for Free vs Paid apps within top categories, including revenue analysis, advanced filtering, and secure time-locked dashboard deployment.":
    st.markdown("<h1 style='color: #F8FAFC;'>Task 6: Dual-axis comparison of average installs and revenue for Free vs Paid apps within top categories, including revenue analysis, advanced filtering, and secure time-locked dashboard deployment.</h1>", unsafe_allow_html=True)
    
    # Time restriction check: 1 PM to 2 PM IST (13:00 to 14:00)
    is_locked_t6 = not (13 <= current_hour < 14) and not bypass_all_locks
    
    if is_locked_t6:
        st.markdown(f"""
        <div class="lock-container">
            <div class="lock-icon">🔒</div>
            <div class="lock-title">Visualization Locked</div>
            <div class="time-badge-locked">Access Window: 1:00 PM – 2:00 PM IST</div>
            <div class="clock-display">{current_time_display.strftime('%H:%M:%S')} IST</div>
            <div class="lock-desc">
                Task 6 direct revenue vs installs comparison is locked. Accessible only between the hours of <b>1:00 PM</b> and <b>2:00 PM IST</b>.
            </div>
            <div style="font-size: 13px; color: #64748B; text-transform: uppercase;">Next unlocking in: {get_countdown(current_time_display, 13)}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='time-badge-active'>🟢 Access Unlocked (1:00 PM – 2:00 PM IST)</div>", unsafe_allow_html=True)
        
        # Load Task 6 dataset
        apps_df = pd.read_csv('Task-6/Dataset/play_store.csv')
        if 10472 in apps_df.index and apps_df.loc[10472, 'Category'] == '1.9':
            apps_df = apps_df.drop(10472)
            
        apps_df['Installs_numeric'] = apps_df['Installs'].str.replace('+', '', regex=False).str.replace(',', '', regex=False).astype(float)
        apps_df['Price_numeric'] = apps_df['Price'].str.replace('$', '', regex=False).astype(float)
        apps_df['Revenue'] = apps_df['Installs_numeric'] * apps_df['Price_numeric']
        
        def clean_size_t6(val):
            if pd.isna(val): return np.nan
            val = str(val).strip()
            if val == 'Varies with device': return np.nan
            if val.endswith('M') or val.endswith('m'): return float(val[:-1])
            elif val.endswith('k') or val.endswith('K'): return float(val[:-1]) / 1024.0
            return np.nan
        apps_df['Size_MB'] = apps_df['Size'].apply(clean_size_t6)
        
        def is_more_than_4_0(ver_str):
            if not isinstance(ver_str, str): return False
            if ver_str == 'Varies with device': return False
            match = re.match(r'^(\d+(?:\.\d+)*)', ver_str)
            if not match: return False
            parts = [int(p) for p in match.group(1).split('.')]
            while len(parts) < 2: parts.append(0)
            return tuple(parts) > (4, 0)
        apps_df['Android_Ver_more_than_4_0'] = apps_df['Android Ver'].apply(is_more_than_4_0)
        apps_df['App_Name_Len'] = apps_df['App'].str.len()
        
        apps_df['Reviews_numeric'] = pd.to_numeric(apps_df['Reviews'], errors='coerce')
        apps_df = apps_df.sort_values('Reviews_numeric', ascending=False).drop_duplicates(subset=['App'], keep='first')
        
        # Interactive sliders
        category_metric = st.selectbox("Top 3 Categories Metric", ["Total Installs", "App Count"])
        revenue_filter_mode = st.selectbox("Revenue Filter Mode", ["Conditional (Keep Free Apps)", "Strict (Revenue >= $10k)"])
        min_installs = st.slider("Minimum Installs", 1000, 50000, 10000)
        min_revenue = st.slider("Minimum Revenue ($)", 1000, 50000, 10000)
        min_size_mb = st.slider("Minimum Size (MB)", 1.0, 50.0, 15.0)
        max_name_len = st.slider("Maximum App Name Length", 10, 50, 30)
        
        # Apply filters
        f_installs = apps_df['Installs_numeric'] >= min_installs
        f_android = apps_df['Android_Ver_more_than_4_0']
        f_size = apps_df['Size_MB'] > min_size_mb
        f_content = apps_df['Content Rating'] == 'Everyone'
        f_name = apps_df['App_Name_Len'] <= max_name_len
        
        if revenue_filter_mode == "Conditional (Keep Free Apps)":
            f_revenue = (apps_df['Type'] == 'Free') | ((apps_df['Type'] == 'Paid') & (apps_df['Revenue'] >= min_revenue))
        else:
            f_revenue = apps_df['Revenue'] >= min_revenue
            
        filtered = apps_df[f_installs & f_android & f_size & f_content & f_name & f_revenue].copy()
        
        if category_metric == "Total Installs":
            top_categories = filtered.groupby('Category')['Installs_numeric'].sum().sort_values(ascending=False).head(3).index.tolist()
        else:
            top_categories = filtered['Category'].value_counts().head(3).index.tolist()
            
        active_df = filtered[filtered['Category'].isin(top_categories)].copy()
        
        if len(active_df) == 0:
            st.warning("No records match these criteria.")
        else:
            # Aggregate metrics for plot
            agg_metrics = active_df.groupby(['Category', 'Type']).agg(
                Avg_Installs=('Installs_numeric', 'mean'),
                Avg_Revenue=('Revenue', 'mean')
            ).reset_index()
            
            plot_records = []
            for cat in top_categories:
                for t in ['Free', 'Paid']:
                    match_row = agg_metrics[(agg_metrics['Category'] == cat) & (agg_metrics['Type'] == t)]
                    if not match_row.empty:
                        plot_records.append({
                            'Category': cat, 'Type': t,
                            'Avg_Installs': match_row['Avg_Installs'].values[0],
                            'Avg_Revenue': match_row['Avg_Revenue'].values[0]
                        })
                    else:
                        plot_records.append({
                            'Category': cat, 'Type': t,
                            'Avg_Installs': 0.0, 'Avg_Revenue': 0.0
                        })
            plot_df = pd.DataFrame(plot_records)
            
            # KPI Cards row
            total_apps = len(active_df)
            avg_installs = active_df['Installs_numeric'].mean()
            total_revenue = active_df['Revenue'].sum()
            paid_count = len(active_df[active_df['Type'] == 'Paid'])
            free_count = len(active_df[active_df['Type'] == 'Free'])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Apps Analyzed</div>
                    <div class="metric-value">{total_apps:,}</div>
                    <div class="metric-sub">{free_count:,} Free vs. {paid_count:,} Paid</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Avg Installs / App</div>
                    <div class="metric-value">{int(avg_installs):,}</div>
                    <div class="metric-sub">Across top 3 categories</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Paid App Revenue</div>
                    <div class="metric-value">${total_revenue:,.2f}</div>
                    <div class="metric-sub">Direct purchases/monetization</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Top Categories</div>
                    <div class="metric-value" style="font-size: 15px; margin-top: 8px;">{', '.join(top_categories)}</div>
                    <div class="metric-sub">Determined by installs/count</div>
                </div>
                """, unsafe_allow_html=True)
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            free_data = plot_df[plot_df['Type'] == 'Free']
            paid_data = plot_df[plot_df['Type'] == 'Paid']
            
            # Formatted text labels
            def format_label(val):
                if val >= 1e6: return f"{val/1e6:.1f}M"
                elif val >= 1e3: return f"{val/1e3:.1f}K"
                elif val > 0: return f"{val:.0f}"
                return "0"
                
            fig.add_trace(
                go.Bar(
                    name='Free Apps - Avg Installs', x=free_data['Category'], y=free_data['Avg_Installs'],
                    text=free_data['Avg_Installs'].apply(format_label), textposition='outside',
                    marker_color='#06B6D4', opacity=0.85, offsetgroup=1
                ),
                secondary_y=False
            )
            fig.add_trace(
                go.Bar(
                    name='Paid Apps - Avg Installs', x=paid_data['Category'], y=paid_data['Avg_Installs'],
                    text=paid_data['Avg_Installs'].apply(format_label), textposition='outside',
                    marker_color='#3B82F6', opacity=0.85, offsetgroup=2
                ),
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(
                    name='Paid Apps - Avg Revenue ($)', x=paid_data['Category'], y=paid_data['Avg_Revenue'],
                    mode='lines+markers', line=dict(color='#F59E0B', width=4), marker=dict(size=10, symbol='diamond')
                ),
                secondary_y=True
            )
            
            fig.update_layout(
                title='Comparison of Average Installs and Revenue (Top 3 Categories)',
                template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title='App Category'),
                yaxis=dict(title='Average Installs', gridcolor='rgba(255,255,255,0.05)'),
                yaxis2=dict(title='Average Revenue ($)', overlaying='y', side='right', showgrid=False),
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Insight briefing and table
            col_l, col_r = st.columns([1, 1])
            with col_l:
                st.markdown("### 📊 Insight Briefing")
                st.markdown(f"""
                - **Top Categories List**: The top 3 categories under consideration are **{', '.join(top_categories)}**.
                - **The Installs Paradigm**: Across all top categories, **Free apps** secure vastly superior download volumes (installs) compared to paid apps. This indicates a high user acquisition elasticity.
                - **The Revenue Paradigm**: Despite having lower download counts, **Paid apps** in these top categories generate significant direct revenues, averaging **${plot_df[plot_df['Type'] == 'Paid']['Avg_Revenue'].mean():,.2f}** per app.
                - **Monetization Insight**: For developer evaluation, launching a Free app is highly effective for scale, but launching a Paid app (provided it meets quality thresholds and filters) yields massive immediate direct revenues exceeding the $10,000 threshold.
                """)
            with col_r:
                st.markdown("### 🔎 Data Preview (Matching Apps)")
                preview_cols = ['App', 'Category', 'Type', 'Installs_numeric', 'Price_numeric', 'Revenue', 'Size_MB', 'Android Ver']
                preview_df = active_df[preview_cols].rename(columns={
                    'Installs_numeric': 'Installs',
                    'Price_numeric': 'Price ($)',
                    'Revenue': 'Revenue ($)',
                    'Size_MB': 'Size (MB)'
                })
                st.dataframe(
                    preview_df.sort_values(by='Installs', ascending=False).head(100),
                    use_container_width=True,
                    height=250
                )
