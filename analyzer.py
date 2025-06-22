import pandas as pd
import numpy as np

def analyze_high_low(df):
    """
    Identifies breakout candidates, range-bound stocks, and sector trends.
    Args:
        df (DataFrame): Columns = [SYMBOL, SERIES, Adjusted_52_Week_High, 
                          52_Week_High_Date, Adjusted_52_Week_Low, 52_Week_Low_DT]
    Returns:
        dict: Analysis results with DataFrames and sector stats.
    """
    # Clean data
    df = df.replace('-', np.nan)
    df['Adjusted_52_Week_High'] = pd.to_numeric(df['Adjusted_52_Week_High'], errors='coerce')
    df['Adjusted_52_Week_Low'] = pd.to_numeric(df['Adjusted_52_Week_Low'], errors='coerce')
    
    # Calculate metrics
    df['Price_Range_Pct'] = ((df['Adjusted_52_Week_High'] - df['Adjusted_52_Week_Low']) / 
                             df['Adjusted_52_Week_Low']) * 100
    df['Current_To_High_Pct'] = ((df['Adjusted_52_Week_High'] - df['Adjusted_52_Week_Low']) / 
                                 df['Adjusted_52_Week_High']) * 100
    
    # Breakout Candidates (within 5% of 52-week high, min 20% annual range)
    breakout = df[
        (df['Current_To_High_Pct'] <= 5) & 
        (df['Price_Range_Pct'] >= 20)
    ].sort_values('Current_To_High_Pct')
    
    # Range-Bound Stocks (low volatility, narrow range)
    range_bound = df[
        (df['Price_Range_Pct'] <= 15)
    ].sort_values('Price_Range_Pct')
    
    # Sector Analysis (assuming sector column exists)
    if 'SECTOR' in df.columns:
        sector_stats = df.groupby('SECTOR').agg({
            'Adjusted_52_Week_High': 'mean',
            'Price_Range_Pct': 'mean'
        }).rename(columns={
            'Adjusted_52_Week_High': 'Avg_High',
            'Price_Range_Pct': 'Avg_Volatility'
        }).sort_values('Avg_Volatility', ascending=False)
    else:
        sector_stats = pd.DataFrame()
    
    return {
        'breakout': breakout,
        'range_bound': range_bound,
        'sector_stats': sector_stats,
        'all_data': df  # Raw data for heatmaps
    }
