import pandas as pd
import numpy as np

def analyze_high_low(df, high_col='52_Week_High', low_col='52_Week_Low'):
    """
    Analyze 52-week high/low stock data
    
    Args:
        df (pd.DataFrame): Input dataframe with stock data
        high_col (str): Column name for 52-week high
        low_col (str): Column name for 52-week low
    
    Returns:
        dict: Dictionary containing analysis results with keys:
              - 'summary': Summary statistics
              - 'near_lows': Stocks near 52-week lows
              - 'full_data': Full analysis dataframe
    """
    # Validate columns exist
    missing_cols = [col for col in [high_col, low_col] if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns not found in dataframe: {missing_cols}")
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Clean data - replace common missing value indicators
    df_clean = df_clean.replace(['-', 'NA', 'N/A', ''], np.nan)
    
    # Convert to numeric
    df_clean[high_col] = pd.to_numeric(df_clean[high_col], errors='coerce')
    df_clean[low_col] = pd.to_numeric(df_clean[low_col], errors='coerce')
    
    # Calculate metrics
    df_clean['Current_Price'] = pd.to_numeric(df_clean.get('Current_Price', df_clean.get('Price', np.nan)), errors='coerce')
    df_clean['Price_Range_Pct'] = (df_clean[high_col] - df_clean[low_col]) / df_clean[low_col] * 100
    df_clean['Current_vs_Low_Pct'] = (df_clean['Current_Price'] - df_clean[low_col]) / df_clean[low_col] * 100
    df_clean['Current_vs_High_Pct'] = (df_clean['Current_Price'] - df_clean[high_col]) / df_clean[high_col] * 100
    
    # Identify stocks near lows (within 5% of 52-week low)
    near_lows = df_clean[df_clean['Current_vs_Low_Pct'] <= 5].sort_values('Current_vs_Low_Pct')
    
    # Create summary statistics
    summary = {
        'Total Stocks': len(df_clean),
        'Stocks Near Lows': len(near_lows),
        'Avg Price Range (%)': df_clean['Price_Range_Pct'].mean(),
        'Median Current vs Low (%)': df_clean['Current_vs_Low_Pct'].median(),
        'Stocks >50% Below High': len(df_clean[df_clean['Current_vs_High_Pct'] < -50])
    }
    
    return {
        'summary': pd.DataFrame.from_dict(summary, orient='index', columns=['Value']),
        'near_lows': near_lows,
        'full_data': df_clean
    }
