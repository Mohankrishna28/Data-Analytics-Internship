import sys
# Python 3.14 protobuf compatibility patch
sys.modules['google._upb._message'] = None

import os
import datetime
import pytz
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="App Market Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using HTML/CSS
st.markdown("""
<style>
    /* Dark theme & fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .stApp {
        background-color: #0e1117;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.2rem;
        background: linear-gradient(135deg, #a855f7, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
        padding-top: 0.5rem;
    }
    
    .subtitle {
        color: #9ca3af;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
        margin-top: -0.25rem;
    }
    
    /* Locked Screen Styles */
    .locked-container {
        background: rgba(31, 38, 135, 0.03);
        border: 1px solid rgba(168, 85, 247, 0.15);
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        margin-top: 4rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(168, 85, 247, 0.1);
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .lock-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        animation: pulse 2s infinite alternate;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); filter: drop-shadow(0 0 5px rgba(59, 130, 246, 0.4)); }
        100% { transform: scale(1.1); filter: drop-shadow(0 0 20px rgba(168, 85, 247, 0.7)); }
    }
    
    .locked-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
        color: #a855f7;
        margin-bottom: 1rem;
    }
    
    .locked-desc {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .time-badge {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(59, 130, 246, 0.15));
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        display: inline-block;
        font-weight: bold;
        color: #e9d5ff;
        font-size: 1.1rem;
        font-family: 'Outfit', sans-serif;
        letter-spacing: 1px;
    }
    
    /* Metrics Cards */
    .metric-card {
        background: rgba(31, 38, 135, 0.04);
        border: 1px solid rgba(138, 43, 226, 0.15);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(59, 130, 246, 0.35);
        background: rgba(31, 38, 135, 0.07);
        box-shadow: 0 8px 25px rgba(138, 43, 226, 0.15);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #9ca3af;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 1.9rem;
        font-weight: bold;
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #a855f7, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Info banners */
    .info-container {
        border-left: 4px solid #a855f7;
        background: rgba(168, 85, 247, 0.04);
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Timezone configurations
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.datetime.now(ist)

# Sidebar - Title and Simulated Time Controls
st.sidebar.markdown("""
<div style='text-align: center; padding-bottom: 1.5rem;'>
    <h2 style='font-family: "Outfit", sans-serif; font-weight: 800; background: linear-gradient(135deg, #a855f7, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Dashboard Controls</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.subheader("⏰ Access Clock Simulation")
use_system_time = st.sidebar.checkbox("Use System Time (IST)", value=True, help="Check to use your computer's real-time zone translated to IST. Uncheck to simulate any hour of the day for testing purposes.")

if use_system_time:
    current_hour = now_ist.hour
    current_minute = now_ist.minute
    current_time_str = now_ist.strftime("%I:%M:%S %p IST")
else:
    simulated_hour = st.sidebar.slider("Simulate IST Hour", 0, 23, 17, help="Select the hour to simulate (e.g. 17 is 5 PM).")
    current_hour = simulated_hour
    current_minute = 0
    current_time_str = f"{simulated_hour:02d}:00:00 (Simulated IST)"

st.sidebar.info(f"Active Time: {current_time_str}")

# Filter variables in the sidebar (Default matching user requirements)
st.sidebar.subheader("🔍 Interactive Filters")
rating_thresh = st.sidebar.slider("Min Avg Rating", 1.0, 5.0, 4.2, step=0.1)
reviews_thresh = st.sidebar.number_input("Min Reviews Count", min_value=0, value=1000, step=100)
min_size = st.sidebar.slider("Min Size (MB)", 0.0, 100.0, 20.0, step=1.0)
max_size = st.sidebar.slider("Max Size (MB)", 0.0, 150.0, 80.0, step=1.0)
exclude_numbers = st.sidebar.checkbox("Exclude Apps with Numbers in Name", value=True)

# Active access check (Visualization visible ONLY between 4 PM IST and 6 PM IST: 16:00 to 18:00)
is_accessible = (16 <= current_hour < 18)

if not is_accessible:
    # LOCKED VIEW
    st.markdown(f"""
    <div class="locked-container">
        <div class="lock-icon">🔒</div>
        <div class="locked-title">Access Restricted</div>
        <p class="locked-desc">
            This analytical visualization dashboard is under strict security constraints. 
            Access is only permitted during the analytics review window:
        </p>
        <div class="time-badge">4:00 PM IST – 6:00 PM IST</div>
        <p style="color: #6a7b8c; font-size: 0.85rem; margin-top: 2rem;">
            Current access time: {current_time_str}<br>
            Please check back during the authorized hours, or toggle 'Use System Time' off in the sidebar to simulate the active window (e.g., 5 PM).
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # UNLOCKED VIEW (Dashboard main layout)
    st.markdown("<h1 class='main-title'>📊 Google Play Store Analytics Dashboard - Task 4</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>🚀 App Market Intelligence & Cumulative Install Growth Over Time</div>", unsafe_allow_html=True)
    
    # Information Banner
    st.markdown("""
    <div class="info-container">
        <strong style="color: #a855f7;">💡 High-Growth Highlights Enabled:</strong> 
        Months with month-over-month (MoM) cumulative install growth exceeding <strong>25%</strong> for any category are highlighted with increased color intensity, and major growth spikes are marked with detailed annotations.
    </div>
    """, unsafe_allow_html=True)

    # Cache dataset loading
    @st.cache_data
    def load_and_preprocess_data():
        csv_path = 'Task-4/Dataset/Play Store Data.csv'
        if not os.path.exists(csv_path):
            csv_path = 'Dataset/Play Store Data.csv' # fallback if run from workspace root
            
        df_raw = pd.read_csv(csv_path)
        df_raw = df_raw[df_raw['Category'] != '1.9'] # Drop corrupt row
        
        df_raw['Rating'] = pd.to_numeric(df_raw['Rating'], errors='coerce')
        df_raw['Reviews'] = pd.to_numeric(df_raw['Reviews'], errors='coerce')
        
        def parse_size_mb(size_str):
            if not isinstance(size_str, str): return None
            s = size_str.strip().upper()
            if s == 'VARIES WITH DEVICE': return None
            if s.endswith('M'): return float(s[:-1])
            if s.endswith('K'): return float(s[:-1]) / 1024.0
            return None
            
        df_raw['Size_MB'] = df_raw['Size'].apply(parse_size_mb)
        
        def parse_installs_num(inst_str):
            if not isinstance(inst_str, str): return None
            inst_str = inst_str.replace('+', '').replace(',', '').strip()
            return float(inst_str)
            
        df_raw['Installs_numeric'] = df_raw['Installs'].apply(parse_installs_num)
        df_raw['Last Updated Date'] = pd.to_datetime(df_raw['Last Updated'], errors='coerce')
        return df_raw

    # Load data
    df = load_and_preprocess_data()

    # Dynamic filtering based on sidebar controls
    # 1. Rating
    f_rating = df['Rating'] >= rating_thresh
    # 2. Exclude numbers
    if exclude_numbers:
        f_name = df['App'].apply(lambda x: not any(c.isdigit() for c in str(x)))
    else:
        f_name = pd.Series(True, index=df.index)
    # 3. Category starting with T or P
    f_cat = df['Category'].str.startswith(('T', 'P'))
    # 4. Reviews
    f_reviews = df['Reviews'] > reviews_thresh
    # 5. Size
    f_size = (df['Size_MB'] >= min_size) & (df['Size_MB'] <= max_size)

    filtered_df = df[f_rating & f_name & f_cat & f_reviews & f_size].copy()
    filtered_df = filtered_df.dropna(subset=['Last Updated Date'])
    filtered_df['YearMonth'] = filtered_df['Last Updated Date'].dt.to_period('M')

    if len(filtered_df) == 0:
        st.warning("⚠️ No records match the selected filters. Please adjust the sidebar controls.")
    else:
        # Construct complete timeline
        min_date = filtered_df['Last Updated Date'].min()
        max_date = filtered_df['Last Updated Date'].max()
        all_months = pd.period_range(start=min_date.to_period('M'), end=max_date.to_period('M'), freq='M')
        categories = sorted(filtered_df['Category'].unique())

        idx = pd.MultiIndex.from_product([categories, all_months], names=['Category', 'YearMonth'])
        grid_df = pd.DataFrame(index=idx).reset_index()

        monthly_installs = filtered_df.groupby(['Category', 'YearMonth'])['Installs_numeric'].sum().reset_index()
        merged = pd.merge(grid_df, monthly_installs, on=['Category', 'YearMonth'], how='left').fillna(0)

        # Cumulative Sum
        merged['Cumulative_Installs'] = merged.groupby('Category')['Installs_numeric'].cumsum()

        # MoM calculations
        merged['Prev_Cumulative'] = merged.groupby('Category')['Cumulative_Installs'].shift(1)
        merged['MoM_Increase_Pct'] = (merged['Cumulative_Installs'] - merged['Prev_Cumulative']) / merged['Prev_Cumulative']
        
        merged.loc[merged['Prev_Cumulative'].isna() & (merged['Cumulative_Installs'] > 0), 'MoM_Increase_Pct'] = float('inf')
        merged.loc[(merged['Prev_Cumulative'] == 0) & (merged['Cumulative_Installs'] > 0), 'MoM_Increase_Pct'] = float('inf')

        # Translate legend categories
        category_translations = {
            'TRAVEL_AND_LOCAL': 'Voyage et guides locaux', # French
            'PRODUCTIVITY': 'Productividad',              # Spanish
            'PHOTOGRAPHY': '写真',                        # Japanese
            'TOOLS': 'Tools',                             # English
            'PERSONALIZATION': 'Personalization',         # English
            'PARENTING': 'Parenting'                      # English
        }
        
        merged['Category_Translated'] = merged['Category'].map(category_translations)

        # Pivot data
        pivot_df = merged.pivot(index='YearMonth', columns='Category', values='Cumulative_Installs')
        pivot_df.index = pivot_df.index.to_timestamp()

        mom_pivot = merged.pivot(index='YearMonth', columns='Category', values='MoM_Increase_Pct')
        mom_pivot.index = mom_pivot.index.to_timestamp()

        categories_translated_sorted = [category_translations[cat] for cat in categories]

        colors = {
            'Voyage et guides locaux': '#1f77b4', # blue
            'Tools': '#9467bd',                 # purple
            'Productividad': '#2ca02c',          # green
            '写真': '#ff7f0e',                   # orange
            'Personalization': '#e377c2',        # pink
            'Parenting': '#bcbd22'               # olive
        }

        # Key Metrics / KPIs Calculations
        total_installs = filtered_df['Installs_numeric'].sum()
        total_apps = len(filtered_df['App'].unique())
        
        # Clean KPI Installs Formatting (e.g. 4.33 Billion or 4.33B)
        if total_installs >= 1e9:
            total_installs_str = f"{total_installs * 1e-9:.2f} B"
        elif total_installs >= 1e6:
            total_installs_str = f"{total_installs * 1e-6:.1f} M"
        else:
            total_installs_str = f"{total_installs:,.0f}"

        # Count high growth months (MoM growth > 25% for any category)
        high_growth_months_count = 0
        for month_timestamp in mom_pivot.index:
            for cat in categories:
                if mom_pivot.loc[month_timestamp, cat] > 0.25:
                    high_growth_months_count += 1
                    break

        # Display Metrics Dashboard Row (KPI cards above chart)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Installs</div>
                <div class="metric-value">{total_installs_str}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Apps Selected</div>
                <div class="metric-value">{total_apps}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Categories</div>
                <div class="metric-value">{len(categories)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">High Growth Months</div>
                <div class="metric-value">{high_growth_months_count}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Height stacking setup for annotations
        y_stacked = [pivot_df[cat].values for cat in categories]
        y_stacked_cum = np.vstack([np.zeros(len(pivot_df.index))] + [np.sum(y_stacked[:i+1], axis=0) for i in range(len(categories))])

        # Interactive Plotly Chart (Only visual option on page)
        st.subheader("📈 Cumulative Installs Stacked Area Chart (Interactive Plotly)")
        
        fig = go.Figure()
        
        # Accumulate heights manually to build stacked traces
        y_cum = np.zeros(len(pivot_df.index))
        for cat in categories:
            trans_name = category_translations[cat]
            val = pivot_df[cat].values
            y_next = y_cum + val
            
            fig.add_trace(go.Scatter(
                x=pivot_df.index,
                y=y_next,
                fill='tonexty' if fig.data else 'tozeroy',
                mode='none',
                name=trans_name,
                fillcolor=colors[trans_name],
                hovertemplate=f"<b>{trans_name}</b><br>Cumulative Installs: %{{y:,.0f}}<extra></extra>"
            ))
            y_cum = y_next

        # Add vertical shapes for high growth months in Plotly
        for month_timestamp in pivot_df.index:
            is_high_growth_month = False
            high_growth_cats = []
            for cat in categories:
                if mom_pivot.loc[month_timestamp, cat] > 0.25:
                    is_high_growth_month = True
                    high_growth_cats.append(category_translations[cat])
            
            if is_high_growth_month:
                x0 = month_timestamp - pd.Timedelta(days=15)
                x1 = month_timestamp + pd.Timedelta(days=15)
                
                fig.add_vrect(
                    x0=x0, x1=x1,
                    fillcolor="#a855f7", opacity=0.12,
                    layer="below", line_width=0,
                    name="High Growth Month"
                )

        # Add growth annotations (🚀 +XX%) on Plotly for major spikes
        for c_idx, cat in enumerate(categories):
            trans_name = category_translations[cat]
            for i in range(1, len(pivot_df.index)):
                month_timestamp = pivot_df.index[i]
                growth = mom_pivot.loc[month_timestamp, cat]
                prev_val = pivot_df.loc[pivot_df.index[i-1], cat]
                
                if 0.50 < growth < float('inf') and prev_val > 1000000:
                    growth_pct = int(round(growth * 100))
                    y_val = y_stacked_cum[c_idx+1, i] # Top of that category band
                    
                    fig.add_annotation(
                        x=month_timestamp,
                        y=y_val,
                        text=f"🚀 +{growth_pct}%",
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor="#FFD700",
                        arrowsize=1,
                        arrowwidth=1.5,
                        ax=20,
                        ay=-25 if cat != 'TRAVEL_AND_LOCAL' else 25,
                        font=dict(size=9, color="#FFD700", family="Inter, sans-serif"),
                        bgcolor="#1f2235",
                        bordercolor="#FFD700",
                        borderwidth=1,
                        borderpad=4,
                        opacity=0.9
                    )

        fig.update_layout(
            title="Cumulative Installs over Time (Interactive Plotly Stacked Area)",
            xaxis_title="Time (Month/Year)",
            yaxis_title="Cumulative Installs",
            template="plotly_dark",
            hovermode="x unified",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            legend=dict(
                title="App Categories",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(30, 34, 53, 0.7)"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # Download option for processed data
        st.subheader("📥 Export Processed Dataset")
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Processed CSV Data",
            data=csv_data,
            file_name="Processed_PlayStore_Data.csv",
            mime="text/csv"
        )
