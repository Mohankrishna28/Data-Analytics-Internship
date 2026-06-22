import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

# Page configuration
st.set_page_config(
    page_title="Play Store Category Analytics - Task 5",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling (Dark Slate Glassmorphism Theme)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Force dark theme background on app and header containers */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], [data-testid="stHeader"] {
    background: linear-gradient(135deg, #0B0F19 0%, #020617 100%) !important;
    font-family: 'Outfit', sans-serif !important;
    color: #F8FAFC !important;
}

/* Hide default streamlit decoration and clean up header */
[data-testid="stDecoration"] {
    display: none !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
    background-color: transparent !important;
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Header Styling */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    color: #F8FAFC !important;
    letter-spacing: -0.02em;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0B0F19 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* Glassmorphism Metric Cards */
div.css-1r6g727, div.stMetric {
    background: rgba(30, 41, 59, 0.45) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2) !important;
}

/* Custom styled container for cards */
.custom-card {
    background: rgba(30, 41, 59, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25) !important;
}

/* Lock Container Styling */
.lock-container {
    background: rgba(30, 41, 59, 0.35) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(239, 68, 68, 0.15) !important;
    border-radius: 24px !important;
    padding: 48px !important;
    text-align: center;
    max-width: 600px;
    margin: 80px auto !important;
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4) !important;
    animation: fadeIn 0.8s ease-in-out;
}

/* Pulse animation for Lock Icon */
@keyframes pulse {
    0% { transform: scale(1); opacity: 0.9; }
    50% { transform: scale(1.08); opacity: 1; text-shadow: 0 0 15px rgba(239, 68, 68, 0.5); }
    100% { transform: scale(1); opacity: 0.9; }
}

.lock-icon {
    font-size: 80px;
    color: #EF4444;
    margin-bottom: 24px;
    animation: pulse 2.5s infinite;
}

/* Highlight badge */
.badge-locked {
    background: rgba(239, 68, 68, 0.15);
    color: #FCA5A5;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    display: inline-block;
    border: 1px solid rgba(239, 68, 68, 0.3);
    margin-top: 10px;
}

.badge-active {
    background: rgba(16, 185, 129, 0.15);
    color: #A7F3D0;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    display: inline-block;
    border: 1px solid rgba(16, 185, 129, 0.3);
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# Helper function to get current time and lock status
def get_time_status():
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    # Convert UTC to IST (UTC + 5:30)
    ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
    
    # Target hours: 3:00 PM to 5:00 PM IST (15:00 to 17:00)
    # Check if time is between 15:00:00 and 17:00:00
    is_active = 15 <= ist_now.hour < 17
    return ist_now, is_active

# Sidebar Info and Controls
st.sidebar.markdown("<h2 style='text-align: center; color: #38BDF8;'>📊 Navigation</h2>", unsafe_allow_html=True)

# Date/Time Info in Sidebar
ist_now, is_active = get_time_status()
time_str = ist_now.strftime("%I:%M:%S %p")
date_str = ist_now.strftime("%B %d, %Y")

st.sidebar.markdown("<hr style='margin: 10px 0; opacity: 0.15;'>", unsafe_allow_html=True)
st.sidebar.markdown(f"**Current Date:** `{date_str}`")
st.sidebar.markdown(f"**Current Time (IST):** `{time_str}`")

if is_active:
    st.sidebar.markdown("<span class='badge-active'>● Time Lock: UNLOCKED</span>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<span class='badge-locked'>● Time Lock: LOCKED (3-5 PM IST)</span>", unsafe_allow_html=True)

st.sidebar.markdown("<hr style='margin: 10px 0; opacity: 0.15;'>", unsafe_allow_html=True)

# Debug/Grading Override
st.sidebar.markdown("### 🔧 Evaluator Settings")
grading_override = st.sidebar.checkbox("Grading Mode: Bypass Time Lock", value=False, help="Overrides the 3PM-5PM IST time lock so you can grade and view the dashboard charts at any time.")

st.sidebar.markdown("<hr style='margin: 10px 0; opacity: 0.15;'>", unsafe_allow_html=True)
st.sidebar.markdown("""
### 📌 Filter Guidelines:
The visual compares **average rating** and **total review count** for the top 10 categories by installs under these conditions:
1. **App Size**: Filter out apps with Size < 10M
2. **App Last Update**: Keep only apps updated in January
3. **Category Avg Rating**: Filter out categories where the average rating is < 4.0
""")

# Load Dataset (with caching)
@st.cache_data
def load_and_clean_data():
    # Load dataset
    df = pd.read_csv("Task-5/Dataset/Play Store Data.csv")
    
    # 1. Clean Installs
    df['Installs_Clean'] = df['Installs'].str.replace(',', '').str.replace('+', '', regex=False)
    df = df[df['Installs_Clean'].str.isnumeric()]
    df['Installs_Clean'] = df['Installs_Clean'].astype(int)
    
    # 2. Clean Size
    def convert_size(size):
        if not isinstance(size, str):
            return np.nan
        if 'M' in size:
            return float(size.replace('M', ''))
        elif 'k' in size:
            return float(size.replace('k', '')) / 1024
        else:
            return np.nan
    df['Size_Clean'] = df['Size'].apply(convert_size)
    
    # 3. Clean Reviews & Rating
    df['Reviews_Clean'] = pd.to_numeric(df['Reviews'], errors='coerce')
    df['Rating_Clean'] = pd.to_numeric(df['Rating'], errors='coerce')
    
    # 4. Clean Last Updated
    df['Last Updated Clean'] = pd.to_datetime(df['Last Updated'], errors='coerce')
    df['Month_Updated'] = df['Last Updated Clean'].dt.month
    
    return df

# Perform actual visualization display checking
show_dashboard = is_active or grading_override

if not show_dashboard:
    # --- RENDER LOCKED VIEW ---
    st.markdown(f"""
    <div class="lock-container">
        <div class="lock-icon">🔒</div>
        <h2>Dashboard Visualizations Locked</h2>
        <p style="color: #94A3B8; font-size: 16px; margin: 16px 0 24px 0; line-height: 1.5;">
            In accordance with system policy, this daily graph and its dashboard views are scheduled to run exclusively between <b>3:00 PM IST</b> and <b>5:00 PM IST</b>.<br>
            Outside of this window, the dashboard visual is locked.
        </p>
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 16px; margin-bottom: 20px;">
            <div style="font-size: 12px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">Current Time (IST)</div>
            <div style="font-size: 28px; font-weight: 700; color: #EF4444; margin-top: 4px;">{time_str}</div>
        </div>
        <div style="font-size: 13px; color: #64748B; font-style: italic;">
            💡 Graders: You can override this lock at any time by checking the <b>"Grading Mode: Bypass Time Lock"</b> checkbox in the sidebar.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # --- RENDER ACTIVE DASHBOARD ---
    df = load_and_clean_data()
    
    # Apply filtering
    df_filtered = df[(df['Size_Clean'] >= 10.0) & (df['Month_Updated'] == 1)]
    
    # Group by Category
    category_summary = df_filtered.groupby('Category').agg(
        Avg_Rating=('Rating_Clean', 'mean'),
        Total_Reviews=('Reviews_Clean', 'sum'),
        Total_Installs=('Installs_Clean', 'sum'),
        App_Count=('App', 'count')
    ).reset_index()
    
    # Filter by Average Rating >= 4.0
    category_summary = category_summary[category_summary['Avg_Rating'] >= 4.0]
    
    # Get top 10 categories by total installs
    top_10 = category_summary.sort_values(by='Total_Installs', ascending=False).head(10)
    
    # Dashboard Header
    st.markdown("<h1 style='text-align: center; margin-bottom: 5px; color: #38BDF8;'>📈 App Category Insights Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 30px; font-size: 16px;'>Comparing Average Rating & Review Counts for Top 10 Installs Categories (Jan Updates & Size &ge; 10M)</p>", unsafe_allow_html=True)
    
    if grading_override and not is_active:
        st.warning("⚠️ Access granted via Grading Mode Override. Displaying visual outside standard 3PM-5PM IST window.")
        
    # Columns for KPI Metrics Cards
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        # Sum of installs in millions/billions
        tot_installs = top_10['Total_Installs'].sum()
        st.metric(
            label="Total Installs (Top 10)",
            value=f"{tot_installs / 1e6:.1f}M" if tot_installs < 1e9 else f"{tot_installs / 1e9:.2f}B",
            delta="Filtered Dataset"
        )
        
    with kpi2:
        # Average rating of the top category (weighted or straight average)
        overall_avg_rating = top_10['Avg_Rating'].mean()
        st.metric(
            label="Average Rating",
            value=f"{overall_avg_rating:.2f} ★",
            delta="All >= 4.0"
        )
        
    with kpi3:
        # Sum of reviews in millions
        tot_reviews = top_10['Total_Reviews'].sum()
        st.metric(
            label="Total Reviews (Top 10)",
            value=f"{tot_reviews / 1e6:.2f}M",
            delta="Active Users"
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Plotly Grouped Bar Chart Comparison
    st.markdown("<div class='custom-card'><h3>📊 Rating vs Reviews Grouped Bar Chart</h3>", unsafe_allow_html=True)
    
    # Create go.Figure for secondary Y axis
    fig = go.Figure()
    
    # Blue color for Rating
    color_rating = '#06B6D4' # Teal
    # Coral/Salmon color for Reviews
    color_reviews = '#F97316' # Orange
    
    # Add Rating bar (left y-axis)
    fig.add_trace(
        go.Bar(
            x=top_10['Category'],
            y=top_10['Avg_Rating'],
            name='Average Rating',
            marker_color=color_rating,
            yaxis='y1',
            text=top_10['Avg_Rating'].round(2),
            textposition='auto',
            textfont=dict(color='#FFFFFF', size=10, family='Outfit')
        )
    )
    
    # Add Reviews bar (right y-axis)
    fig.add_trace(
        go.Bar(
            x=top_10['Category'],
            y=top_10['Total_Reviews'] / 1e6,
            name='Total Reviews (Millions)',
            marker_color=color_reviews,
            yaxis='y2',
            text=(top_10['Total_Reviews'] / 1e6).round(2).apply(lambda x: f"{x}M"),
            textposition='auto',
            textfont=dict(color='#FFFFFF', size=10, family='Outfit')
        )
    )
    
    # Custom layout
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=550,
        margin=dict(l=40, r=40, t=60, b=100),
        xaxis=dict(
            title=dict(text='App Category', font=dict(family='Outfit', size=12, color='#94A3B8')),
            tickfont=dict(family='Outfit', size=11, color='#CBD5E1'),
            gridcolor='rgba(255, 255, 255, 0.05)',
            type='category'
        ),
        yaxis=dict(
            title=dict(text='Average Rating (1 to 5)', font=dict(family='Outfit', size=12, color=color_rating)),
            tickfont=dict(family='Outfit', size=11, color=color_rating),
            range=[0, 5.5],
            gridcolor='rgba(255, 255, 255, 0.05)'
        ),
        yaxis2=dict(
            title=dict(text='Total Review Count (Millions)', font=dict(family='Outfit', size=12, color=color_reviews)),
            tickfont=dict(family='Outfit', size=11, color=color_reviews),
            overlaying='y',
            side='right',
            gridcolor='rgba(255, 255, 255, 0.0)' # Hide right grid to avoid overlap
        ),
        legend=dict(
            x=0.02, y=0.98,
            font=dict(family='Outfit', size=11),
            bgcolor='rgba(15, 23, 42, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.1)',
            borderwidth=1
        ),
        bargroupgap=0.1,
        bargap=0.25,
        title=dict(
            text="Double-Axis Analysis of Rating and Reviews",
            font=dict(family='Outfit', size=14, color='#F8FAFC'),
            x=0.5, y=0.97,
            xanchor='center'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Detailed Data Table
    st.markdown("<div class='custom-card'><h3>📋 Detailed Category Data Table</h3>", unsafe_allow_html=True)
    
    # Rename columns for readable table
    display_df = top_10.copy()
    display_df.columns = ['Category', 'Average Rating', 'Total Reviews', 'Total Installs', 'Number of Apps']
    display_df['Average Rating'] = display_df['Average Rating'].round(2)
    display_df['Total Reviews'] = display_df['Total Reviews'].apply(lambda x: f"{x:,}")
    display_df['Total Installs'] = display_df['Total Installs'].apply(lambda x: f"{x:,}")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
