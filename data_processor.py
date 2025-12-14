"""
Data Processing Module for Data Weaver Dashboard
Handles loading, cleaning, and preprocessing of weather and egg price data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import List, Tuple, Optional
import streamlit as st

@st.cache_data
def load_weather_data(cities: List[str] = None) -> pd.DataFrame:
    """
    Load and process weather data from CSV file.
    
    Args:
        cities: List of cities to filter for. If None, loads all cities.
        
    Returns:
        DataFrame with processed weather data
    """
    try:
        # Load temperature data
        df = pd.read_csv('csv/temperature.csv')
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Rename columns for consistency
        df = df.rename(columns={
            'Location': 'city',
            'amonthly average temp': 'temperature'
        })
        
        # Fix city name typo in data
        df['city'] = df['city'].replace('Hyerabad', 'Hyderabad')
        
        # Handle missing values
        df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
        
        # Remove rows with missing temperature data
        df = df.dropna(subset=['temperature'])
        
        # Filter by cities if specified
        if cities:
            df = df[df['city'].isin(cities)]
        
        # Sort by date and city
        df = df.sort_values(['Date', 'city'])
        
        # Reset index
        df = df.reset_index(drop=True)
        
        return df
        
    except FileNotFoundError:
        st.error("Temperature data file not found. Please ensure 'csv/temperature.csv' exists.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading weather data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_egg_price_data(cities: List[str] = None) -> pd.DataFrame:
    """
    Load and process egg price data from CSV file.
    
    Args:
        cities: List of cities to filter for. If None, loads all cities.
        
    Returns:
        DataFrame with processed egg price data
    """
    try:
        # Load egg price data
        df = pd.read_csv('csv/egg prices.csv')
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Rename columns for consistency
        df = df.rename(columns={
            'Location': 'city',
            'Average_Price_Per_Egg_INR_Monthly': 'egg_price'
        })
        
        # Handle missing values
        df['egg_price'] = pd.to_numeric(df['egg_price'], errors='coerce')
        
        # Remove rows with missing price data
        df = df.dropna(subset=['egg_price'])
        
        # Filter by cities if specified
        if cities:
            df = df[df['city'].isin(cities)]
        
        # Sort by date and city
        df = df.sort_values(['Date', 'city'])
        
        # Reset index
        df = df.reset_index(drop=True)
        
        return df
        
    except FileNotFoundError:
        st.error("Egg price data file not found. Please ensure 'csv/egg prices.csv' exists.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading egg price data: {str(e)}")
        return pd.DataFrame()

def merge_datasets(weather_df: pd.DataFrame, price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge weather and egg price datasets on date and city.
    
    Args:
        weather_df: Weather data DataFrame
        price_df: Egg price data DataFrame
        
    Returns:
        Combined DataFrame with both weather and price data
    """
    try:
        if weather_df.empty or price_df.empty:
            st.warning("One or both datasets are empty. Cannot merge.")
            return pd.DataFrame()
        
        # Merge on Date and city
        merged_df = pd.merge(
            weather_df, 
            price_df, 
            on=['Date', 'city', 'Year', 'Month'], 
            how='inner'
        )
        
        # Check if merge was successful
        if merged_df.empty:
            st.warning("No matching data found between weather and price datasets.")
            return pd.DataFrame()
        
        # Sort by date and city
        merged_df = merged_df.sort_values(['Date', 'city'])
        
        # Reset index
        merged_df = merged_df.reset_index(drop=True)
        
        # Add some derived columns for analysis
        merged_df['year'] = merged_df['Date'].dt.year
        merged_df['month_name'] = merged_df['Date'].dt.month_name()
        
        return merged_df
        
    except Exception as e:
        st.error(f"Error merging datasets: {str(e)}")
        return pd.DataFrame()

def filter_by_date_range(df: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
    """
    Filter DataFrame by date range.
    
    Args:
        df: Input DataFrame with 'Date' column
        start_date: Start date for filtering
        end_date: End date for filtering
        
    Returns:
        Filtered DataFrame
    """
    try:
        # Convert dates to datetime for comparison
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)
        
        # Filter by date range
        filtered_df = df[
            (df['Date'] >= start_datetime) & 
            (df['Date'] <= end_datetime)
        ]
        
        return filtered_df
        
    except Exception as e:
        st.error(f"Error filtering by date range: {str(e)}")
        return df

def get_available_cities() -> List[str]:
    """
    Get list of available cities from the data.
    
    Returns:
        List of city names
    """
    return ['Ahmedabad', 'Bengaluru', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune']

def validate_date_range(start_date: date, end_date: date) -> bool:
    """
    Validate that the date range is logical.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        True if valid, False otherwise
    """
    return start_date <= end_date

def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Get summary statistics for the combined dataset.
    
    Args:
        df: Combined DataFrame
        
    Returns:
        Dictionary with summary statistics
    """
    if df.empty:
        return {}
    
    summary = {
        'total_records': len(df),
        'cities_count': df['city'].nunique(),
        'cities': sorted(df['city'].unique().tolist()),
        'date_range': {
            'start': df['Date'].min().strftime('%Y-%m-%d'),
            'end': df['Date'].max().strftime('%Y-%m-%d')
        },
        'temperature_stats': {
            'min': df['temperature'].min(),
            'max': df['temperature'].max(),
            'mean': df['temperature'].mean(),
            'std': df['temperature'].std()
        },
        'price_stats': {
            'min': df['egg_price'].min(),
            'max': df['egg_price'].max(),
            'mean': df['egg_price'].mean(),
            'std': df['egg_price'].std()
        }
    }
    
    return summary

def detect_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect missing data patterns in the dataset.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with missing data analysis
    """
    missing_info = []
    
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        
        # Check for missing months
        date_range = pd.date_range(
            start=city_data['Date'].min(),
            end=city_data['Date'].max(),
            freq='MS'  # Month start
        )
        
        missing_dates = set(date_range) - set(city_data['Date'])
        
        missing_info.append({
            'city': city,
            'total_records': len(city_data),
            'missing_months': len(missing_dates),
            'missing_dates': sorted([d.strftime('%Y-%m') for d in missing_dates])
        })
    
    return pd.DataFrame(missing_info)

def load_and_merge_all_data(cities: List[str] = None, start_date: date = None, end_date: date = None) -> pd.DataFrame:
    """
    Convenience function to load and merge all data with optional filtering.
    
    Args:
        cities: List of cities to include
        start_date: Start date for filtering
        end_date: End date for filtering
        
    Returns:
        Combined and filtered DataFrame
    """
    # Load data
    weather_df = load_weather_data(cities)
    price_df = load_egg_price_data(cities)
    
    # Merge datasets
    merged_df = merge_datasets(weather_df, price_df)
    
    # Apply date filtering if specified
    if start_date and end_date and not merged_df.empty:
        merged_df = filter_by_date_range(merged_df, start_date, end_date)
    
    return merged_df