"""
Statistical Analysis Module for Data Weaver Dashboard
Calculates correlations and statistical insights between weather and egg price data.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import List, Tuple, Dict
import streamlit as st

def calculate_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate correlations between weather metrics and egg prices for each city.
    
    Args:
        df: Combined DataFrame with weather and price data
        
    Returns:
        DataFrame with correlation results
    """
    results = []
    
    # Weather metrics to analyze
    weather_metrics = ['temperature']
    
    # Calculate correlations for each city and metric
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        
        for metric in weather_metrics:
            if metric in city_data.columns and len(city_data) > 1:
                # Calculate Pearson correlation
                correlation, p_value = stats.pearsonr(
                    city_data[metric].dropna(), 
                    city_data['egg_price'].dropna()
                )
                
                results.append({
                    'city': city,
                    'weather_metric': metric,
                    'correlation': correlation,
                    'p_value': p_value,
                    'sample_size': len(city_data.dropna()),
                    'is_significant': p_value < 0.05
                })
    
    return pd.DataFrame(results)

def find_significant_correlations(correlations: pd.DataFrame, alpha: float = 0.05) -> pd.DataFrame:
    """
    Filter correlations to find statistically significant relationships.
    
    Args:
        correlations: DataFrame with correlation results
        alpha: Significance level (default: 0.05)
        
    Returns:
        DataFrame with only significant correlations
    """
    return correlations[correlations['p_value'] < alpha]

def generate_insights(df: pd.DataFrame, correlations: pd.DataFrame) -> List[str]:
    """
    Generate automated insights from correlation analysis.
    
    Args:
        df: Combined DataFrame with weather and price data
        correlations: DataFrame with correlation results
        
    Returns:
        List of insight strings
    """
    insights = []
    
    # Overall correlation insight
    overall_corr = df['temperature'].corr(df['egg_price'])
    if abs(overall_corr) > 0.5:
        direction = "positive" if overall_corr > 0 else "negative"
        insights.append(f"🔍 Strong {direction} correlation ({overall_corr:.3f}) between temperature and egg prices across all cities.")
    elif abs(overall_corr) > 0.3:
        direction = "positive" if overall_corr > 0 else "negative"
        insights.append(f"📊 Moderate {direction} correlation ({overall_corr:.3f}) between temperature and egg prices.")
    else:
        insights.append(f"📈 Weak correlation ({overall_corr:.3f}) between temperature and egg prices overall.")
    
    # City-specific insights
    if not correlations.empty:
        # Strongest correlation
        strongest = correlations.loc[correlations['correlation'].abs().idxmax()]
        direction = "positive" if strongest['correlation'] > 0 else "negative"
        insights.append(f"🏆 Strongest correlation found in {strongest['city']}: {direction} relationship ({strongest['correlation']:.3f})")
        
        # Significant correlations count
        significant_count = len(correlations[correlations['is_significant']])
        total_count = len(correlations)
        insights.append(f"📋 {significant_count} out of {total_count} city correlations are statistically significant (p < 0.05)")
        
        # Temperature range insight
        temp_range = df['temperature'].max() - df['temperature'].min()
        price_range = df['egg_price'].max() - df['egg_price'].min()
        insights.append(f"🌡️ Temperature varies by {temp_range:.1f}°C while egg prices vary by ₹{price_range:.2f} across the dataset")
    
    return insights

def detect_extreme_weather_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect extreme weather events and their impact on egg prices.
    
    Args:
        df: Combined DataFrame with weather and price data
        
    Returns:
        DataFrame with extreme weather events
    """
    # Define thresholds for extreme weather
    temp_high_threshold = df['temperature'].quantile(0.95)
    temp_low_threshold = df['temperature'].quantile(0.05)
    
    # Identify extreme events
    extreme_events = df[
        (df['temperature'] >= temp_high_threshold) | 
        (df['temperature'] <= temp_low_threshold)
    ].copy()
    
    # Add event type
    extreme_events['event_type'] = 'Normal'
    extreme_events.loc[extreme_events['temperature'] >= temp_high_threshold, 'event_type'] = 'Extreme Heat'
    extreme_events.loc[extreme_events['temperature'] <= temp_low_threshold, 'event_type'] = 'Extreme Cold'
    
    return extreme_events

def calculate_price_volatility(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    """
    Calculate egg price volatility indices.
    
    Args:
        df: DataFrame with egg price data
        window: Rolling window size for volatility calculation
        
    Returns:
        DataFrame with volatility metrics
    """
    volatility_results = []
    
    for city in df['city'].unique():
        city_data = df[df['city'] == city].sort_values('Date')
        
        if len(city_data) >= window:
            # Calculate rolling standard deviation
            city_data['price_volatility'] = city_data['egg_price'].rolling(window=window).std()
            
            # Calculate price change percentage
            city_data['price_change_pct'] = city_data['egg_price'].pct_change() * 100
            
            volatility_results.append({
                'city': city,
                'avg_volatility': city_data['price_volatility'].mean(),
                'max_volatility': city_data['price_volatility'].max(),
                'avg_price_change': city_data['price_change_pct'].mean(),
                'max_price_change': city_data['price_change_pct'].abs().max()
            })
    
    return pd.DataFrame(volatility_results)

def perform_statistical_tests(df: pd.DataFrame) -> Dict:
    """
    Perform various statistical tests on the data.
    
    Args:
        df: Combined DataFrame with weather and price data
        
    Returns:
        Dictionary with test results
    """
    results = {}
    
    # Normality tests
    temp_shapiro = stats.shapiro(df['temperature'].dropna())
    price_shapiro = stats.shapiro(df['egg_price'].dropna())
    
    results['normality'] = {
        'temperature_normal': temp_shapiro.pvalue > 0.05,
        'price_normal': price_shapiro.pvalue > 0.05,
        'temp_p_value': temp_shapiro.pvalue,
        'price_p_value': price_shapiro.pvalue
    }
    
    # Correlation test
    corr_test = stats.pearsonr(df['temperature'].dropna(), df['egg_price'].dropna())
    results['correlation_test'] = {
        'correlation': corr_test.statistic,
        'p_value': corr_test.pvalue,
        'is_significant': corr_test.pvalue < 0.05
    }
    
    # ANOVA test for city differences
    city_groups = [group['egg_price'].values for name, group in df.groupby('city')]
    if len(city_groups) > 1:
        anova_result = stats.f_oneway(*city_groups)
        results['anova'] = {
            'f_statistic': anova_result.statistic,
            'p_value': anova_result.pvalue,
            'cities_differ': anova_result.pvalue < 0.05
        }
    
    return results

def format_correlation_value(correlation: float) -> str:
    """
    Format correlation value with descriptive text.
    
    Args:
        correlation: Correlation coefficient
        
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