"""
Data Weaver Dashboard - Weather vs Egg Price Correlation Analysis
A Streamlit application that analyzes correlations between weather patterns 
and egg prices across major Indian cities.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import numpy as np
from scipy import stats
from data_processor import load_weather_data, load_egg_price_data, merge_datasets, filter_by_date_range
from visualizations import create_correlation_scatter, create_time_series_chart, create_dual_axis_chart
from statistics import calculate_correlations, generate_insights, format_correlation_value
from utils import get_data_summary, create_download_link

# Configure Streamlit page
st.set_page_config(
    page_title="Data Weaver Dashboard",
    page_icon="🌤️🥚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better spacing and appearance
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .stPlotlyChart {
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    
    h1, h2, h3, h4 {
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    .stSelectbox, .stMultiSelect, .stDateInput {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    st.title("🌤️ Data Weaver Dashboard 🥚")
    st.markdown("### Weather vs Egg Price Correlation Analysis")
    st.markdown("Explore relationships between weather patterns and egg prices across major Indian cities")
    
    # Sidebar for controls
    selected_cities, start_date, end_date = setup_sidebar()
    
    # Main dashboard content
    display_dashboard(selected_cities, start_date, end_date)

def setup_sidebar():
    """Set up sidebar controls"""
    st.sidebar.header("📊 Analysis Controls")
    
    # City selection
    cities = ['Ahmedabad', 'Bengaluru', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune']
    selected_cities = st.sidebar.multiselect(
        "Select Cities",
        cities,
        default=['Delhi', 'Mumbai', 'Chennai']
    )
    
    # Date range selection
    st.sidebar.subheader("📅 Date Range")
    start_date = st.sidebar.date_input("Start Date", date(2017, 5, 1))
    end_date = st.sidebar.date_input("End Date", date(2024, 12, 31))
    
    return selected_cities, start_date, end_date

# Chart creation functions moved to visualizations.py module

def display_dashboard(selected_cities, start_date, end_date):
    """Display main dashboard content"""
    
    if not selected_cities:
        st.warning("Please select at least one city from the sidebar to view data.")
        return
    
    # Load and process data
    with st.spinner("Loading data..."):
        weather_df = load_weather_data(selected_cities)
        price_df = load_egg_price_data(selected_cities)
        
        if weather_df.empty or price_df.empty:
            st.error("Unable to load data. Please check if the CSV files exist in the 'csv' folder.")
            return
        
        # Merge datasets
        merged_df = merge_datasets(weather_df, price_df)
        
        if merged_df.empty:
            st.error("No matching data found for the selected cities and date range.")
            return
        
        # Filter by date range
        filtered_df = filter_by_date_range(merged_df, start_date, end_date)
        
        if filtered_df.empty:
            st.warning("No data available for the selected date range. Please adjust your selection.")
            return
    
    # Display data summary
    st.success(f"📊 Loaded {len(filtered_df)} data points for {len(selected_cities)} cities")
    
    # Display cities included
    cities_text = ", ".join(selected_cities)
    st.info(f"🏙️ **Cities included:** {cities_text}")
    
    # Time Series Charts Section
    st.markdown("---")
    st.subheader("📈 Time Series Trends")
    
    # Add proper spacing
    st.markdown("")
    
    # Create two separate sections with better spacing
    st.markdown("#### 🌡️ Temperature Trends")
    temp_chart = create_time_series_chart(filtered_df, selected_cities, 'temperature')
    st.plotly_chart(temp_chart, use_container_width=True)
    
    # Add spacing between charts
    st.markdown("")
    st.markdown("")
    
    st.markdown("#### 🥚 Egg Price Trends")
    price_chart = create_time_series_chart(filtered_df, selected_cities, 'egg_price')
    st.plotly_chart(price_chart, use_container_width=True)
    
    # Correlation Analysis Section
    st.markdown("---")
    st.subheader("🔗 Correlation Analysis")
    
    # Calculate correlations
    correlations_df = calculate_correlations(filtered_df)
    overall_correlation = filtered_df['temperature'].corr(filtered_df['egg_price'])
    
    # Display correlation metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Correlation", f"{overall_correlation:.3f}")
    
    with col2:
        st.metric("Data Points", len(filtered_df))
    
    with col3:
        significance = "Significant" if abs(overall_correlation) > 0.3 else "Weak"
        st.metric("Relationship", significance)
    
    # Generate and display insights
    insights = generate_insights(filtered_df, correlations_df)
    
    st.markdown("#### 💡 Key Insights")
    for insight in insights:
        st.write(f"• {insight}")
    
    # Correlation scatter plot with proper spacing
    st.markdown("")
    scatter_chart = create_correlation_scatter(filtered_df)
    st.plotly_chart(scatter_chart, use_container_width=True)
    
    # City-wise correlation details
    if not correlations_df.empty:
        st.markdown("#### 🏙️ City-wise Correlations")
        
        # Format correlation data for display
        display_corr = correlations_df.copy()
        display_corr['correlation_formatted'] = display_corr['correlation'].apply(format_correlation_value)
        display_corr['p_value'] = display_corr['p_value'].round(4)
        
        st.dataframe(
            display_corr[['city', 'correlation_formatted', 'p_value', 'is_significant']].rename(columns={
                'city': 'City',
                'correlation_formatted': 'Correlation',
                'p_value': 'P-Value',
                'is_significant': 'Significant'
            }),
            use_container_width=True
        )
    
    # Export functionality
    st.markdown("---")
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Download Filtered Data"):
            csv_link = create_download_link(filtered_df, "weather_egg_data", "csv")
            st.markdown(csv_link, unsafe_allow_html=True)
    
    with col2:
        if st.button("📈 Download Correlations"):
            if not correlations_df.empty:
                corr_link = create_download_link(correlations_df, "correlation_analysis", "csv")
                st.markdown(corr_link, unsafe_allow_html=True)
            else:
                st.warning("No correlation data to download")
    
    # Data table (expandable)
    with st.expander("📋 View Raw Data"):
        st.dataframe(
            filtered_df[['Date', 'city', 'temperature', 'egg_price']].round(3),
            use_container_width=True
        )

if __name__ == "__main__":
    main()