import pandas as pd
import numpy as np

def analyze_high_low(df):
    """Core analysis logic for breakout and range-bound stocks."""
    # Clean data
    df = df.replace('-', np.nan)
    numeric_cols = ['Adjusted_52_Week_High', 'Adjusted_52_Week_Low']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    # Calculate metrics
    df['Price_Range_Pct'] = (
        (df['Adjusted_52_Week_High'] - df['Adjusted_52_Week_Low']) / 
        df['Adjusted_52_Week_Low']
    ) * 100
    df['Current_To_High_Pct'] = (
        (df['Adjusted_52_Week_High'] - df['Adjusted_52_Week_Low']) / 
        df['Adjusted_52_Week_High']
    ) * 100

    # Breakout candidates (within 5% of high, min 20% annual range)
    breakout = df[
        (df['Current_To_High_Pct'] <= 5) & 
        (df['Price_Range_Pct'] >= 20)
    ].sort_values('Current_To_High_Pct')

    # Range-bound stocks (low volatility)
    range_bound = df[
        (df['Price_Range_Pct'] <= 15)
    ].sort_values('Price_Range_Pct')

    return {
        'breakout': breakout,
        'range_bound': range_bound,
        'all_data': df
    }
