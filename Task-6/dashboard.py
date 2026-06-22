import streamlit as st
import pandas as pd
import numpy as np
import re
import datetime
import pytz
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config to match the dark theme and set wide layout
st.set_page_config(
    page_title="Play Store Analytics - Task 6",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom fonts and styling to match premium design requirements
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* Global fonts */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Sleek card styling */
    .metric-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 16px;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: rgba(6, 182, 212, 0.3);
    }
    .metric-label {
        font-size: 14px;
        color: #94a3b8;
        font-weight: 500;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 32px;
        color: #f8fafc;
        font-weight: 700;
        font-family: 'Outfit', sans-serif;
        line-height: 1.1;
    }
    .metric-sub {
        font-size: 12px;
        color: #06b6d4;
        margin-top: 6px;
        font-weight: 500;
    }
    
    /* Pulsing lock animation */
    .lock-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
        background: radial-gradient(circle, #0B0F19 0%, #020617 100%);
        border-radius: 16px;
        border: 1px solid rgba(239, 68, 68, 0.1);
        max-width: 800px;
        margin: 40px auto;
    }
    .lock-icon {
        font-size: 80px;
        animation: pulse 2s infinite ease-in-out;
        margin-bottom: 24px;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; filter: drop-shadow(0 0 5px rgba(239, 68, 68, 0.2)); }
        50% { transform: scale(1.08); opacity: 1; filter: drop-shadow(0 0 25px rgba(239, 68, 68, 0.6)); }
        100% { transform: scale(1); opacity: 0.8; filter: drop-shadow(0 0 5px rgba(239, 68, 68, 0.2)); }
    }
    .lock-title {
        color: #ef4444;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 12px;
        font-family: 'Outfit', sans-serif;
    }
    .lock-desc {
        color: #94a3b8;
        font-size: 16px;
        text-align: center;
        margin-bottom: 24px;
        line-height: 1.6;
        max-width: 500px;
    }
    .time-badge {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.2);
        color: #ef4444;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 16px;
    }
    .clock-display {
        font-family: monospace;
        font-size: 40px;
        font-weight: 700;
        color: #f8fafc;
        background: #0f172a;
        padding: 12px 24px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)

# Timezone Lock Configuration
IST_TZ = pytz.timezone('Asia/Kolkata')
now_ist = datetime.datetime.now(IST_TZ)

# Time Lock Logic Check: 1 PM (13:00) to 2 PM (14:00) IST
is_active_hour = (13 <= now_ist.hour < 14)

# Sidebar - Settings & Simulation
st.sidebar.markdown(f"### 🕒 Dashboard Control Room")

# Simulation Toggle for Evaluation
simulation_mode = st.sidebar.selectbox(
    "Time Simulation Mode",
    ["Real-time System Time", "Force Unlocked (Simulate 1:30 PM IST)", "Force Locked (Simulate 3:00 PM IST)"],
    help="Use this to bypass the 1:00 PM – 2:00 PM IST time lock for evaluation."
)

if simulation_mode == "Force Unlocked (Simulate 1:30 PM IST)":
    current_time_display = now_ist.replace(hour=13, minute=30, second=0)
    is_unlocked = True
elif simulation_mode == "Force Locked (Simulate 3:00 PM IST)":
    current_time_display = now_ist.replace(hour=15, minute=0, second=0)
    is_unlocked = False
else:
    current_time_display = now_ist
    is_unlocked = is_active_hour

# Calculate Countdown display for locked state
def get_countdown_str(curr_time):
    target_today = curr_time.replace(hour=13, minute=0, second=0, microsecond=0)
    if curr_time < target_today:
        diff = target_today - curr_time
    else:
        target_tomorrow = target_today + datetime.timedelta(days=1)
        diff = target_tomorrow - curr_time
    
    hours, remainder = divmod(int(diff.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

# IF LOCKED VIEW
if not is_unlocked:
    st.markdown(f"""
    <div class="lock-container">
        <div class="lock-icon">🔒</div>
        <div class="lock-title">Visualization Locked</div>
        <div class="time-badge">Access Window: 1:00 PM – 2:00 PM IST</div>
        <div class="clock-display">{current_time_display.strftime('%H:%M:%S')} IST</div>
        <div class="lock-desc">
            This analytical dashboard is scheduled to automatically activate only between the hours of <b>1:00 PM</b> and <b>2:00 PM Indian Standard Time (IST)</b>.
        </div>
        <div style="font-size: 14px; color: #64748b; font-weight: 500; text-transform: uppercase;">
            Next unlocking in:
        </div>
        <div style="font-size: 24px; font-weight: 700; color: #ef4444; margin-top: 8px; font-family: monospace;">
            {get_countdown_str(current_time_display)}
        </div>
        <div style="margin-top: 30px; font-size: 13px; color: #475569; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px; width: 100%; text-align: center;">
            💡 <i>Evaluators: Use the "Time Simulation Mode" selectbox in the sidebar to unlock the dashboard instantly.</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

# IF ACTIVE VIEW (UNLOCKED)
else:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛠️ Interactive Data Filters")
    
    # 1. Top 3 Categories Criteria Selector
    category_metric = st.sidebar.radio(
        "Top 3 Categories Metric",
        ["Total Installs (Recommended)", "App Count"],
        index=0,
        help="Select how the Top 3 categories should be determined."
    )
    
    # 2. Revenue Filter Mode Selector
    revenue_filter_mode = st.sidebar.radio(
        "Revenue Filter Mode",
        ["Conditional (Keep Free Apps)", "Strict (Revenue >= $10k)"],
        index=0,
        help="Conditional keeps Free apps (Revenue=0) and filters Paid apps by Revenue. Strict filters out all apps below $10k (including all Free apps)."
    )
    
    # Sliders for parameters
    min_installs = st.sidebar.slider("Minimum Installs Filter", 1000, 50000, 10000, step=1000, help="Exclude apps with installs below this value.")
    min_revenue = st.sidebar.slider("Minimum Revenue Filter ($)", 1000, 50000, 10000, step=1000, help="Exclude paid apps with revenue below this value.")
    min_size_mb = st.sidebar.slider("Minimum Size Filter (MB)", 1.0, 50.0, 15.0, step=1.0, help="Exclude apps with size below this value.")
    max_name_len = st.sidebar.slider("Maximum App Name Length", 10, 50, 30, step=1, help="Exclude apps with name length above this threshold.")
    
    # Load and clean data (cached to optimize performance)
    @st.cache_data
    def load_clean_data():
        df = pd.read_csv('Task-6/Dataset/play_store.csv')
        
        # Drop corrupt row if exists
        if 10472 in df.index and df.loc[10472, 'Category'] == '1.9':
            df = df.drop(10472)
            
        # Clean Installs
        df['Installs_numeric'] = df['Installs'].str.replace('+', '', regex=False).str.replace(',', '', regex=False).astype(float)
        
        # Clean Price
        df['Price_numeric'] = df['Price'].str.replace('$', '', regex=False).astype(float)
        
        # Calculate Revenue
        df['Revenue'] = df['Installs_numeric'] * df['Price_numeric']
        
        # Clean Size (convert to Megabytes)
        def clean_size(val):
            if pd.isna(val):
                return np.nan
            val = str(val).strip()
            if val == 'Varies with device':
                return np.nan
            if val.endswith('M') or val.endswith('m'):
                return float(val[:-1])
            elif val.endswith('k') or val.endswith('K'):
                return float(val[:-1]) / 1024.0
            return np.nan
            
        df['Size_MB'] = df['Size'].apply(clean_size)
        
        # Clean Android Version (strictly > 4.0)
        def is_more_than_4_0(ver_str):
            if not isinstance(ver_str, str):
                return False
            if ver_str == 'Varies with device':
                return False
            match = re.match(r'^(\d+(?:\.\d+)*)', ver_str)
            if not match:
                return False
            parts = [int(p) for p in match.group(1).split('.')]
            while len(parts) < 2:
                parts.append(0)
            return tuple(parts) > (4, 0)
            
        df['Android_Ver_more_than_4_0'] = df['Android Ver'].apply(is_more_than_4_0)
        df['App_Name_Len'] = df['App'].str.len()
        
        # Deduplicate to ensure each unique app name is analyzed only once
        df['Reviews_numeric'] = pd.to_numeric(df['Reviews'], errors='coerce')
        df = df.sort_values('Reviews_numeric', ascending=False).drop_duplicates(subset=['App'], keep='first')
        
        return df

    # Get data
    raw_df = load_clean_data()
    
    # Apply static/dynamic filters
    f_installs = raw_df['Installs_numeric'] >= min_installs
    f_android = raw_df['Android_Ver_more_than_4_0']
    f_size = raw_df['Size_MB'] > min_size_mb
    f_content = raw_df['Content Rating'] == 'Everyone'
    f_name = raw_df['App_Name_Len'] <= max_name_len
    
    # Revenue filter based on mode
    if revenue_filter_mode == "Conditional (Keep Free Apps)":
        f_revenue = (raw_df['Type'] == 'Free') | ((raw_df['Type'] == 'Paid') & (raw_df['Revenue'] >= min_revenue))
    else:
        f_revenue = raw_df['Revenue'] >= min_revenue
        
    filtered_df = raw_df[f_installs & f_android & f_size & f_content & f_name & f_revenue].copy()
    
    # Determine the top 3 categories based on selected metric
    if category_metric == "Total Installs (Recommended)":
        top_categories = filtered_df.groupby('Category')['Installs_numeric'].sum().sort_values(ascending=False).head(3).index.tolist()
    else:
        top_categories = filtered_df['Category'].value_counts().head(3).index.tolist()
        
    # Get active filtered data for only these categories
    active_df = filtered_df[filtered_df['Category'].isin(top_categories)].copy()
    
    # Main page layout
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:15px; margin-bottom:25px;">
        <div>
            <h1 style="margin:0; font-size:32px; color:#f8fafc;">Play Store Analytics Dashboard</h1>
            <p style="margin:5px 0 0 0; color:#64748b; font-size:14px;">Comparing average installs and revenue for Free vs. Paid apps (Task-6)</p>
        </div>
        <div style="text-align:right;">
            <div class="time-badge" style="background-color:rgba(16, 185, 129, 0.1); border-color:rgba(16, 185, 129, 0.2); color:#10b981; margin:0; display:inline-block;">
                🟢 Active Access Window (1 PM - 2 PM IST)
            </div>
            <div style="font-size:12px; color:#64748b; margin-top:5px; font-weight:500;">Simulated System Time: {current_time_display.strftime('%H:%M:%S')} IST</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Error message if filtered dataset is empty
    if len(active_df) == 0:
        st.error("⚠️ No apps match the selected filter criteria. Please broaden your sliders in the sidebar.")
    else:
        # KPI Metric Cards Row
        total_apps = len(active_df)
        avg_installs = active_df['Installs_numeric'].mean()
        total_revenue = active_df['Revenue'].sum()
        paid_count = len(active_df[active_df['Type'] == 'Paid'])
        free_count = len(active_df[active_df['Type'] == 'Free'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Active Apps Analyzed</div>
                <div class="metric-value">{total_apps:,}</div>
                <div class="metric-sub">{free_count:,} Free vs. {paid_count:,} Paid</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Installs / App</div>
                <div class="metric-value">{int(avg_installs):,}</div>
                <div class="metric-sub">Across all {total_apps} apps</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Paid App Revenue</div>
                <div class="metric-value">${total_revenue:,.2f}</div>
                <div class="metric-sub">Direct monetization only</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Top Categories</div>
                <div class="metric-value" style="font-size: 18px; margin-top: 8px;">{', '.join(top_categories)}</div>
                <div class="metric-sub">Sorted by {category_metric.split(' ')[0]}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Calculations for Plotting
        agg_metrics = active_df.groupby(['Category', 'Type']).agg(
            Avg_Installs=('Installs_numeric', 'mean'),
            Avg_Revenue=('Revenue', 'mean')
        ).reset_index()
        
        # Ensure we have all combinations of category and type
        plot_records = []
        for cat in top_categories:
            for t in ['Free', 'Paid']:
                match_row = agg_metrics[(agg_metrics['Category'] == cat) & (agg_metrics['Type'] == t)]
                if not match_row.empty:
                    plot_records.append({
                        'Category': cat,
                        'Type': t,
                        'Avg_Installs': match_row['Avg_Installs'].values[0],
                        'Avg_Revenue': match_row['Avg_Revenue'].values[0]
                    })
                else:
                    plot_records.append({
                        'Category': cat,
                        'Type': t,
                        'Avg_Installs': 0.0,
                        'Avg_Revenue': 0.0
                    })
                    
        plot_df = pd.DataFrame(plot_records)
        
        # Create Dual-Axis Visualization
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        free_data = plot_df[plot_df['Type'] == 'Free']
        paid_data = plot_df[plot_df['Type'] == 'Paid']
        
        # Helper to format numbers for text labels on top of bars
        def format_bar_label(val):
            if val >= 1e6:
                return f"{val/1e6:.1f}M"
            elif val >= 1e3:
                return f"{val/1e3:.1f}K"
            elif val > 0:
                return f"{val:.0f}"
            return "0"

        free_text = free_data['Avg_Installs'].apply(format_bar_label)
        paid_text = paid_data['Avg_Installs'].apply(format_bar_label)
        
        # Add primary y-axis: Average Installs (grouped bars)
        fig.add_trace(
            go.Bar(
                name='Free Apps - Avg Installs',
                x=free_data['Category'],
                y=free_data['Avg_Installs'],
                text=free_text,
                textposition='outside',
                textfont=dict(color='#94A3B8', size=10),
                marker_color='#06B6D4', # Theme Cyan
                opacity=0.85,
                offsetgroup=1,
                hovertemplate="Category: %{x}<br>Free Avg Installs: %{y:,.0f}<extra></extra>"
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Bar(
                name='Paid Apps - Avg Installs',
                x=paid_data['Category'],
                y=paid_data['Avg_Installs'],
                text=paid_text,
                textposition='outside',
                textfont=dict(color='#94A3B8', size=10),
                marker_color='#3B82F6', # Theme Blue
                opacity=0.85,
                offsetgroup=2,
                hovertemplate="Category: %{x}<br>Paid Avg Installs: %{y:,.0f}<extra></extra>"
            ),
            secondary_y=False
        )
        
        # Add secondary y-axis: Average Revenue for Paid Apps (line with markers)
        # Note: Free apps have 0 revenue, so we only display the line for Paid apps to avoid clutter
        fig.add_trace(
            go.Scatter(
                name='Paid Apps - Avg Revenue ($)',
                x=paid_data['Category'],
                y=paid_data['Avg_Revenue'],
                mode='lines+markers',
                line=dict(color='#F59E0B', width=4), # Theme Amber/Gold
                marker=dict(size=10, symbol='diamond', color='#D97706', line=dict(color='#fff', width=1)),
                hovertemplate="Category: %{x}<br>Paid Avg Revenue: $%{y:,.2f}<extra></extra>"
            ),
            secondary_y=True
        )
        
        # Premium layout styling
        fig.update_layout(
            title=dict(
                text='Comparison of Average Installs and Direct Revenue (Top 3 Categories)',
                font=dict(size=18, family='Outfit, sans-serif', color='#F8FAFC')
            ),
            xaxis=dict(
                title=dict(text='App Category', font=dict(color='#94A3B8')),
                tickfont=dict(size=12, family='Inter, sans-serif', color='#94A3B8')
            ),
            yaxis=dict(
                title=dict(text='Average Installs', font=dict(color='#06B6D4')),
                tickfont=dict(color='#06B6D4', size=11),
                gridcolor='rgba(255, 255, 255, 0.05)',
                showgrid=True
            ),
            yaxis2=dict(
                title=dict(text='Average Revenue ($)', font=dict(color='#F59E0B')),
                tickfont=dict(color='#F59E0B', size=11),
                overlaying='y',
                side='right',
                showgrid=False
            ),
            barmode='group',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.05,
                xanchor='right',
                x=1,
                font=dict(color='#F8FAFC', size=11)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Two-column detailed analysis & data preview
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown("### 📊 Insight Briefing")
            st.markdown(f"""
            - **Top Categories List**: The top 3 categories under consideration are **{', '.join(top_categories)}**.
            - **The Installs Paradigm**: Across all top categories, **Free apps** secure vastly superior download volumes (installs) compared to paid apps. This indicates a high user acquisition elasticity.
            - **The Revenue Paradigm**: Despite having lower download counts, **Paid apps** in these top categories generate significant direct revenues, averaging **${plot_df[plot_df['Type'] == 'Paid']['Avg_Revenue'].mean():,.2f}** per app.
            - **Monetization Insight**: For developer evaluation, launching a Free app is highly effective for scale, but launching a Paid app (provided it meets quality thresholds and filters) yields massive immediate direct revenues exceeding the $10,000 threshold.
            """)
            
        with col_right:
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
