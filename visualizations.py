"""
Visualization Module for Data Weaver Dashboard
Creates interactive Plotly charts and graphs for weather and egg price analysis.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

def create_correlation_scatter(df: pd.DataFrame, x_col: str = 'temperature', y_col: str = 'egg_price') -> go.Figure:
    """
    Create correlation scatter plot between weather and egg price data.
    
    Args:
        df: Combined DataFrame with weather and price data
        x_col: Column name for x-axis (default: 'temperature')
        y_col: Column name for y-axis (default: 'egg_price')
        
    Returns:
        Plotly Figure object
    """
    fig = px.scatter(
        df, 
        x=x_col, 
        y=y_col, 
        color='city',
        title=f'{x_col.title()} vs {y_col.replace("_", " ").title()} Correlation',
        labels={
            x_col: f'{x_col.replace("_", " ").title()}' + (' (°C)' if 'temp' in x_col else ''),
            y_col: 'Price (INR per egg)'
        },
        hover_data=['Date', 'city']
    )
    
    # Add trend line
    try:
        # Calculate correlation coefficient
        correlation = df[x_col].corr(df[y_col])
        
        # Add trend line using numpy polyfit
        z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
        p = np.poly1d(z)
        
        x_trend = np.linspace(df[x_col].min(), df[x_col].max(), 100)
        y_trend = p(x_trend)
        
        fig.add_trace(go.Scatter(
            x=x_trend, 
            y=y_trend,
            mode='lines',
            name=f'Trend Line (r={correlation:.3f})',
            line=dict(color='red', dash='dash')
        ))
        
    except Exception as e:
        print(f"Could not add trend line: {e}")
    
    # Update layout for better appearance
    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=60, b=80),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        title=dict(
            x=0.5,
            xanchor='center'
        )
    )
    
    return fig

def create_time_series_chart(df: pd.DataFrame, cities: list, metric: str = 'temperature') -> go.Figure:
    """
    Create time series chart for weather or price data.
    
    Args:
        df: DataFrame with time series data
        cities: List of cities to include
        metric: Metric to plot ('temperature' or 'egg_price')
        
    Returns:
        Plotly Figure object
    """
    # Filter data for selected cities
    filtered_df = df[df['city'].isin(cities)]
    
    # Create appropriate labels
    if metric == 'temperature':
        title = 'Temperature Trends Over Time'
        y_label = 'Temperature (°C)'
        color_scale = 'Reds'
    else:
        title = 'Egg Price Trends Over Time'
        y_label = 'Price (INR per egg)'
        color_scale = 'Blues'
    
    fig = px.line(
        filtered_df, 
        x='Date', 
        y=metric, 
        color='city',
        title=title,
        labels={metric: y_label, 'Date': 'Date'}
    )
    
    # Update layout for better spacing
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=80),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        ),
        title=dict(
            x=0.5,
            xanchor='center'
        )
    )
    
    return fig

def create_correlation_heatmap(correlations: pd.DataFrame) -> go.Figure:
    """
    Create correlation heatmap for multiple weather metrics vs egg prices.
    
    Args:
        correlations: DataFrame with correlation results
        
    Returns:
        Plotly Figure object
    """
    # Pivot the correlations data for heatmap
    heatmap_data = correlations.pivot(index='city', columns='weather_metric', values='correlation')
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='RdBu',
        zmid=0,
        text=heatmap_data.values,
        texttemplate="%{text:.3f}",
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Weather-Price Correlation Heatmap',
        xaxis_title='Weather Metrics',
        yaxis_title='Cities',
        height=400,
        title_x=0.5
    )
    
    return fig

def create_extreme_weather_analysis(df: pd.DataFrame) -> go.Figure:
    """
    Create visualization for extreme weather events and their impact on prices.
    
    Args:
        df: Combined DataFrame with weather and price data
        
    Returns:
        Plotly Figure object
    """
    # Define extreme weather thresholds
    temp_threshold_high = df['temperature'].quantile(0.9)
    temp_threshold_low = df['temperature'].quantile(0.1)
    
    # Create categories
    df_copy = df.copy()
    df_copy['weather_category'] = 'Normal'
    df_copy.loc[df_copy['temperature'] >= temp_threshold_high, 'weather_category'] = 'Extreme Hot'
    df_copy.loc[df_copy['temperature'] <= temp_threshold_low, 'weather_category'] = 'Extreme Cold'
    
    # Create box plot
    fig = px.box(
        df_copy,
        x='weather_category',
        y='egg_price',
        color='weather_category',
        title='Egg Prices During Different Weather Conditions',
        labels={'egg_price': 'Price (INR per egg)', 'weather_category': 'Weather Condition'}
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_x=0.5
    )
    
    return fig

def create_dual_axis_chart(df: pd.DataFrame, city: str) -> go.Figure:
    """
    Create dual-axis chart showing temperature and egg prices for a specific city.
    
    Args:
        df: Combined DataFrame with weather and price data
        city: City name to filter for
        
    Returns:
        Plotly Figure object
    """
    city_data = df[df['city'] == city].sort_values('Date')
    
    fig = go.Figure()
    
    # Add temperature line
    fig.add_trace(go.Scatter(
        x=city_data['Date'],
        y=city_data['temperature'],
        name='Temperature',
        line=dict(color='red'),
        yaxis='y'
    ))
    
    # Add egg price line
    fig.add_trace(go.Scatter(
        x=city_data['Date'],
        y=city_data['egg_price'],
        name='Egg Price',
        line=dict(color='blue'),
        yaxis='y2'
    ))
    
    # Update layout with dual y-axes
    fig.update_layout(
        title=f'Temperature and Egg Price Trends - {city}',
        xaxis_title='Date',
        yaxis=dict(
            title='Temperature (°C)',
            side='left',
            color='red'
        ),
        yaxis2=dict(
            title='Price (INR per egg)',
            side='right',
            overlaying='y',
            color='blue'
        ),
        height=400,
        title_x=0.5,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig