"""
Simple test script to verify data loading functionality
"""

import pandas as pd
from data_processor import load_weather_data, load_egg_price_data, merge_datasets

def test_data_loading():
    """Test basic data loading functionality"""
    print("Testing data loading...")
    
    # Test weather data loading
    print("\n1. Loading weather data...")
    weather_df = load_weather_data(['Delhi', 'Mumbai'])
    print(f"Weather data shape: {weather_df.shape}")
    print(f"Weather columns: {list(weather_df.columns)}")
    print(f"Weather data sample:")
    print(weather_df.head())
    
    # Test egg price data loading
    print("\n2. Loading egg price data...")
    price_df = load_egg_price_data(['Delhi', 'Mumbai'])
    print(f"Price data shape: {price_df.shape}")
    print(f"Price columns: {list(price_df.columns)}")
    print(f"Price data sample:")
    print(price_df.head())
    
    # Test data merging
    print("\n3. Merging datasets...")
    merged_df = merge_datasets(weather_df, price_df)
    print(f"Merged data shape: {merged_df.shape}")
    print(f"Merged columns: {list(merged_df.columns)}")
    print(f"Merged data sample:")
    print(merged_df.head())
    
    print("\n✅ Data loading test completed successfully!")
    return merged_df

if __name__ == "__main__":
    test_data_loading()