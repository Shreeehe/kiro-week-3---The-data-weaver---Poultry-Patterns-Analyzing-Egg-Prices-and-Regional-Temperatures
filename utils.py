"""
Utility Module for Data Weaver Dashboard
Helper functions for data formatting, validation, and export functionality.
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import List, Optional
import streamlit as st
import io
import base64

def format_correlation_value(correlation: float) -> str:
    """
    Format correlation value with descriptive text and color coding.
    
    Args:
        correlation: Correlation coefficient (-1 to 1)
        
    Returns:
        Formatted string with correlation description
    """
    abs_corr = abs(correlation)
    
    if abs_corr >= 0.7:
        strength = "Strong"
    elif abs_corr >= 0.5:
        strength = "Moderate"
    elif abs_corr >= 0.3:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    direction = "Positive" if correlation > 0 else "Negative"
    
    return f"{strength} {direction} ({correlation:.3f})"

def validate_date_range(start_date: date, end_date: date) -> bool:
    """
    Validate that the date range is logical and within data bounds.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        True if valid, False otherwise
    """
    # Check if start date is before end date
    if start_date > end_date:
        return False
    
    # Check if date range is reasonable (not too large)
    date_diff = (end_date - start_date).days
    if date_diff > 3650:  # More than 10 years
        return False
    
    return True

def get_available_cities() -> List[str]:
    """
    Get list of available cities from the data.
    
    Returns:
        List of city names
    """
    return ['Ahmedabad', 'Bengaluru', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune']

def export_data_to_csv(df: pd.DataFrame, filename: str = "weather_egg_data") -> str:
    """
    Export DataFrame to CSV format for download.
    
    Args:
        df: DataFrame to export
        filename: Base filename (without extension)
        
    Returns:
        CSV string for download
    """
    # Create CSV string
    csv_string = df.to_csv(index=False)
    
    # Create download link
    b64 = base64.b64encode(csv_string.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV File</a>'
    
    return href

def format_number(value: float, decimal_places: int = 2) -> str:
    """
    Format numbers for display with appropriate decimal places.
    
    Args:
        value: Number to format
        decimal_places: Number of decimal places
        
    Returns:
        Formatted string
    """
    if pd.isna(value):
        return "N/A"
    
    return f"{value:.{decimal_places}f}"

def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics for the dataset.
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Dictionary with summary statistics
    """
    summary = {
        'total_records': len(df),
        'date_range': {
            'start': df['Date'].min().strftime('%Y-%m-%d') if not df.empty else 'N/A',
            'end': df['Date'].max().strftime('%Y-%m-%d') if not df.empty else 'N/A'
        },
        'cities_count': df['city'].nunique() if 'city' in df.columns else 0,
        'temperature': {
            'min': df['temperature'].min() if 'temperature' in df.columns else None,
            'max': df['temperature'].max() if 'temperature' in df.columns else None,
            'mean': df['temperature'].mean() if 'temperature' in df.columns else None
        },
        'egg_price': {
            'min': df['egg_price'].min() if 'egg_price' in df.columns else None,
            'max': df['egg_price'].max() if 'egg_price' in df.columns else None,
            'mean': df['egg_price'].mean() if 'egg_price' in df.columns else None
        }
    }
    
    return summary

def create_download_link(df: pd.DataFrame, filename: str, file_format: str = 'csv') -> str:
    """
    Create a download link for the DataFrame.
    
    Args:
        df: DataFrame to download
        filename: Name of the file
        file_format: Format ('csv' or 'excel')
        
    Returns:
        HTML download link
    """
    if file_format.lower() == 'csv':
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">📥 Download CSV</a>'
    elif file_format.lower() == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        excel_data = output.getvalue()
        b64 = base64.b64encode(excel_data).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">📥 Download Excel</a>'
    else:
        href = "Unsupported format"
    
    return href

def filter_outliers(df: pd.DataFrame, column: str, method: str = 'iqr') -> pd.DataFrame:
    """
    Filter outliers from a DataFrame column.
    
    Args:
        df: Input DataFrame
        column: Column name to filter outliers from
        method: Method to use ('iqr' or 'zscore')
        
    Returns:
        DataFrame with outliers removed
    """
    if column not in df.columns:
        return df
    
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    elif method == 'zscore':
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        return df[z_scores < 3]
    
    return df

def calculate_percentage_change(df: pd.DataFrame, column: str, periods: int = 1) -> pd.DataFrame:
    """
    Calculate percentage change for a column.
    
    Args:
        df: Input DataFrame
        column: Column to calculate percentage change for
        periods: Number of periods to shift for calculation
        
    Returns:
        DataFrame with percentage change column added
    """
    df_copy = df.copy()
    df_copy[f'{column}_pct_change'] = df_copy[column].pct_change(periods=periods) * 100
    
    return df_copy

def get_color_palette(n_colors: int) -> List[str]:
    """
    Get a color palette for visualizations.
    
    Args:
        n_colors: Number of colors needed
        
    Returns:
        List of color hex codes
    """
    # Predefined color palette
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    
    # Repeat colors if more are needed
    while len(colors) < n_colors:
        colors.extend(colors)
    
    return colors[:n_colors]

def format_date_range(start_date: date, end_date: date) -> str:
    """
    Format date range for display.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Formatted date range string
    """
    return f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"

def check_data_quality(df: pd.DataFrame) -> dict:
    """
    Check data quality and return quality metrics.
    
    Args:
        df: DataFrame to check
        
    Returns:
        Dictionary with data quality metrics
    """
    quality_report = {
        'total_rows': len(df),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.to_dict(),
        'memory_usage': df.memory_usage(deep=True).sum(),
        'completeness': (1 - df.isnull().sum() / len(df)).to_dict()
    }
    
    return quality_report