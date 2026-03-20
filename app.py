"""
India Carbon Emissions Tracker - Streamlit Dashboard
AI-powered emissions analytics for MoSPI portfolio project
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import os
import json

from ai_agent import EmissionsIQAgent

# Page configuration
st.set_page_config(
    page_title="India Carbon Emissions Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with green accents
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #00ff88;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #aaaaaa;
        text-align: center;
        padding-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e3a1e 0%, #0d1f0d 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00ff88;
        margin: 1rem 0;
    }
    .tier-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
    }
    .tier-on-track {
        background-color: #00ff88;
        color: black;
    }
    .tier-needs-attention {
        background-color: #ffaa00;
        color: black;
    }
    .tier-critical {
        background-color: #ff4444;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load all required datasets."""
    data = {}
    
    try:
        data['forecast'] = pd.read_csv('data/emissions_forecast.csv')
        data['tiers'] = pd.read_csv('data/state_tiers.csv')
        data['state'] = pd.read_csv('data/state_emissions.csv')
        data['gaps'] = pd.read_csv('data/net_zero_gaps.csv')
        return data
    except FileNotFoundError as e:
        st.error(f"Data files not found. Please run data pipeline first: {e}")
        return None


@st.cache_resource
def load_agent():
    """Load AI agent (cached)."""
    return EmissionsIQAgent()


def render_tier_badge(tier: str) -> str:
    """Render HTML tier badge."""
    class_map = {
        'On Track': 'tier-on-track',
        'Needs Attention': 'tier-needs-attention',
        'Critical': 'tier-critical'
    }
    return f'<span class="tier-badge {class_map.get(tier, "")}">{tier}</span>'


def page_national_overview(data):
    """Render Page 1: National Overview."""
    st.markdown('<div class="main-header">🌍 National Overview</div>', unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate KPIs
    latest_year = data['state']['year'].max()
    current_total = data['state'][data['state']['year'] == latest_year]['co2_mt'].sum()
    prev_year_total = data['state'][data['state']['year'] == latest_year - 1]['co2_mt'].sum()
    yoy_change = ((current_total - prev_year_total) / prev_year_total) * 100
    
    on_track = len(data['tiers'][data['tiers']['tier'] == 'On Track'])
    needs_attention = len(data['tiers'][data['tiers']['tier'] == 'Needs Attention'])
    critical = len(data['tiers'][data['tiers']['tier'] == 'Critical'])
    
    with col1:
        st.metric(
            "Total Emissions (2023)",
            f"{current_total:,.0f} MT",
            f"{yoy_change:+.1f}% YoY"
        )
    
    with col2:
        st.metric("States On Track", on_track, f"🟢 {on_track}/{len(data['tiers'])}")
    
    with col3:
        st.metric("Needs Attention", needs_attention, f"🟡 {needs_attention}/{len(data['tiers'])}")
    
    with col4:
        st.metric("Critical States", critical, f"🔴 {critical}/{len(data['tiers'])}")
    
    st.markdown("---")
    
    # Two columns: Map and Sector breakdown
    col_map, col_chart = st.columns([1.2, 1])
    
    with col_map:
        st.subheader("🗺️ State-wise Emission Heatmap")
        
        # Get state totals for latest year
        state_totals = data['state'][data['state']['year'] == latest_year].groupby('state')['co2_mt'].sum().reset_index()
        state_totals.columns = ['state', 'total_emission']
        
        # Simple choropleth (placeholder - would need actual geojson for real map)
        st.info("💡 Interactive map showing emissions by state. Darker = Higher emissions")
        
        # Show as bar chart instead (map requires geojson)
        fig = px.bar(
            state_totals.sort_values('total_emission', ascending=False).head(10),
            x='total_emission',
            y='state',
            orientation='h',
            title="Top 10 Emitting States",
            color='total_emission',
            color_continuous_scale='Reds',
            labels={'total_emission': 'CO2 (MT)', 'state': 'State'}
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart:
        st.subheader("📊 National Emissions by Sector")
        
        # Sector breakdown over time
        sector_yearly = data['state'].groupby(['year', 'sector'])['co2_mt'].sum().reset_index()
        
        fig = px.area(
            sector_yearly,
            x='year',
            y='co2_mt',
            color='sector',
            title="Sector-wise Emissions Trend",
            labels={'co2_mt': 'CO2 (MT)', 'year': 'Year', 'sector': 'Sector'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)


def page_state_deep_dive(data):
    """Render Page 2: State Deep Dive."""
    st.markdown('<div class="main-header">🔍 State Deep Dive</div>', unsafe_allow_html=True)
    
    # State selector
    selected_state = st.selectbox("Select State", sorted(data['tiers']['state'].unique()))
    
    # Get state data
    state_tier = data['tiers'][data['tiers']['state'] == selected_state].iloc[0]
    state_forecast = data['forecast'][data['forecast']['state'] == selected_state]
    state_gap = data['gaps'][data['gaps']['state'] == selected_state].iloc[0]
    
    # Display tier badge
    st.markdown(
        f"### {selected_state} {render_tier_badge(state_tier['tier'])}",
        unsafe_allow_html=True
    )
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Emission", f"{state_tier['current_emission_mt']:.0f} MT")
    
    with col2:
        st.metric("Forecast 2035", f"{state_tier['forecast_2035_mt']:.0f} MT")
    
    with col3:
        st.metric("Growth Rate", f"{state_tier['avg_growth_rate']:.1f}% /year")
    
    with col4:
        st.metric("Peak Year", int(state_tier['peak_year']))
    
    st.markdown("---")
    
    # Two columns: Forecast chart and sector breakdown
    col_forecast, col_sector = st.columns([1.5, 1])
    
    with col_forecast:
        st.subheader("📈 Historical & Forecasted Emissions")
        
        # Separate historical and forecast
        historical = state_forecast[~state_forecast['is_forecast']]
        forecast = state_forecast[state_forecast['is_forecast']]
        
        fig = go.Figure()
        
        # Historical line (solid)
        fig.add_trace(go.Scatter(
            x=historical['year'],
            y=historical['co2_mt'],
            mode='lines+markers',
            name='Historical',
            line=dict(color='#00ff88', width=3),
            marker=dict(size=6)
        ))
        
        # Forecast line (dashed)
        fig.add_trace(go.Scatter(
            x=forecast['year'],
            y=forecast['co2_mt'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#ffaa00', width=3, dash='dash'),
            marker=dict(size=6, symbol='diamond')
        ))
        
        fig.update_layout(
            title=f"{selected_state} Emission Trajectory (2005-2035)",
            xaxis_title="Year",
            yaxis_title="CO2 Emissions (MT)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_sector:
        st.subheader("🏭 Sector Breakdown (2023)")
        
        # Get latest year sector data
        latest_year = data['state']['year'].max()
        state_sectors = data['state'][
            (data['state']['state'] == selected_state) & 
            (data['state']['year'] == latest_year)
        ]
        sector_totals = state_sectors.groupby('sector')['co2_mt'].sum().reset_index()
        
        fig = px.pie(
            sector_totals,
            values='co2_mt',
            names='sector',
            title=f"Total: {sector_totals['co2_mt'].sum():.0f} MT",
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Net-Zero Gap Progress Bar
    st.markdown("---")
    st.subheader("🎯 Net-Zero Gap Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        current = state_gap['current_emission_mt']
        target = state_gap['target_emission_mt']
        progress = (target / current) * 100
        
        st.markdown(f"**Current:** {current:.0f} MT → **Target (2030):** {target:.0f} MT")
        st.progress(progress / 100)
        st.caption(f"Gap: {state_gap['net_zero_gap_mt']:.0f} MT ({state_gap['reduction_needed_pct']:.0f}% reduction needed)")
    
    with col2:
        if state_tier['tier'] == 'Critical':
            st.error("⚠️ **Action Required**\nEmissions growing too fast")
        elif state_tier['tier'] == 'Needs Attention':
            st.warning("⚡ **Monitor Closely**\nModerate growth rate")
        else:
            st.success("✅ **On Track**\nManageable growth rate")


def page_net_zero_analyzer(data):
    """Render Page 3: Net-Zero Gap Analyzer."""
    st.markdown('<div class="main-header">🎯 Net-Zero Gap Analyzer</div>', unsafe_allow_html=True)
    
    st.info("📌 Context: India has committed to achieving net-zero by 2070 and reducing emission intensity by 45% by 2030.")
    
    # Merge gap and tier data
    gap_analysis = data['gaps'].merge(data['tiers'][['state', 'tier']], on='state')
    gap_analysis = gap_analysis.sort_values('net_zero_gap_mt', ascending=False)
    
    # Gap ranking chart
    st.subheader("📊 States Ranked by Net-Zero Gap")
    
    fig = px.bar(
        gap_analysis,
        x='net_zero_gap_mt',
        y='state',
        orientation='h',
        color='tier',
        title="States with Largest Gap (Biggest Challenge → Smallest)",
        labels={'net_zero_gap_mt': 'Net-Zero Gap (MT)', 'state': 'State'},
        color_discrete_map={
            'Critical': '#ff4444',
            'Needs Attention': '#ffaa00',
            'On Track': '#00ff88'
        }
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed table
    st.subheader("📋 Detailed Gap Analysis")
    
    # Format table
    display_df = gap_analysis[['state', 'current_emission_mt', 'target_emission_mt', 'net_zero_gap_mt', 'tier']].copy()
    display_df.columns = ['State', 'Current (MT)', 'Target (MT)', 'Gap (MT)', 'Tier']
    
    # Add tier styling
    def highlight_tier(row):
        if row['Tier'] == 'Critical':
            return ['background-color: #ff444433'] * len(row)
        elif row['Tier'] == 'Needs Attention':
            return ['background-color: #ffaa0033'] * len(row)
        else:
            return ['background-color: #00ff8833'] * len(row)
    
    st.dataframe(
        display_df.style.apply(highlight_tier, axis=1),
        use_container_width=True,
        height=500
    )


def page_ai_assistant(data):
    """Render Page 4: AI Policy Assistant."""
    st.markdown('<div class="main-header">🤖 EmissionsIQ - AI Policy Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Powered by Claude Haiku</div>', unsafe_allow_html=True)
    
    # Load agent
    agent = load_agent()
    
    # Example prompts
    st.subheader("💡 Try These Questions:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔴 Which states are most critical?"):
            st.session_state.query = "Which states are most critical?"
        
        if st.button("📊 Compare Maharashtra and Gujarat"):
            st.session_state.query = "Compare Maharashtra and Gujarat"
    
    with col2:
        if st.button("🎯 What's Odisha's net-zero gap?"):
            st.session_state.query = "What's Odisha's net-zero gap?"
        
        if st.button("📋 Generate policy brief for Punjab"):
            st.session_state.query = "Generate policy brief for Punjab"
    
    st.markdown("---")
    
    # Chat interface
    st.subheader("💬 Ask EmissionsIQ")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'query' not in st.session_state:
        st.session_state.query = ""
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask about state emissions, gaps, comparisons, or policy recommendations...")
    
    # Process button click or text input
    if st.session_state.query or user_input:
        query = user_input if user_input else st.session_state.query
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        
        with st.chat_message("user"):
            st.markdown(query)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("EmissionsIQ is analyzing..."):
                response = agent.chat(query)
                st.markdown(response)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear query
        st.session_state.query = ""
        st.rerun()


# Main App
def main():
    """Main application logic."""
    
    # Header
    st.markdown('<div class="main-header">India Carbon Emissions Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">EmissionsIQ — AI Policy Analyst | MoSPI Portfolio Project</div>', unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    
    if data is None:
        st.error("⚠️ Data not loaded. Please run the data pipeline:")
        st.code("python data_fetcher.py\npython ml_model.py", language="bash")
        return
    
    # Sidebar navigation
    st.sidebar.title("📍 Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "🌍 National Overview",
            "🔍 State Deep Dive",
            "🎯 Net-Zero Gap Analyzer",
            "🤖 AI Policy Assistant"
        ]
    )
    
    st.sidebar.markdown("---")
    
    # Filters (optional, for future enhancement)
    st.sidebar.title("🎛️ Filters")
    
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=int(data['state']['year'].min()),
        max_value=int(data['state']['year'].max()),
        value=(int(data['state']['year'].min()), int(data['state']['year'].max()))
    )
    
    selected_sectors = st.sidebar.multiselect(
        "Sectors",
        options=data['state']['sector'].unique(),
        default=data['state']['sector'].unique()
    )
    
    # Filter data based on sidebar selections
    filtered_data = {
        'forecast': data['forecast'],
        'tiers': data['tiers'],
        'state': data['state'][
            (data['state']['year'] >= year_range[0]) & 
            (data['state']['year'] <= year_range[1]) &
            (data['state']['sector'].isin(selected_sectors))
        ],
        'gaps': data['gaps']
    }
    
    st.sidebar.markdown("---")
    st.sidebar.info("🎓 **MoSPI Internship Project**\n\nDeveloped for Ministry of Statistics & Programme Implementation portfolio")
    
    # Route to selected page
    if "National Overview" in page:
        page_national_overview(filtered_data)
    elif "State Deep Dive" in page:
        page_state_deep_dive(filtered_data)
    elif "Net-Zero Gap Analyzer" in page:
        page_net_zero_analyzer(filtered_data)
    elif "AI Policy Assistant" in page:
        page_ai_assistant(filtered_data)


if __name__ == "__main__":
    main()
