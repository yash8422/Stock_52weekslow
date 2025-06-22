import streamlit as st
import pandas as pd
import numpy as np
from analyzer import analyze_high_low

# App title and description
st.title("Stock 52-Week High/Low Analyzer")
st.write("Upload a CSV or Excel file containing stock data to analyze 52-week high/low performance.")

# File uploader
uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])

df = None
results = None

if uploaded_file:
    try:
        # Read file based on extension
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, on_bad_lines='warn')
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("File successfully loaded!")
        
        # Show raw data preview
        with st.expander("Show raw data"):
            st.dataframe(df.head())
            
        # Column mapping if needed
        st.subheader("Column Mapping")
        cols = df.columns.tolist()
        
        # Try to automatically detect common column names
        high_col = next((col for col in cols if 'high' in col.lower()), cols[0])
        low_col = next((col for col in cols if 'low' in col.lower()), cols[1])
        
        # Let user confirm or change column mappings
        high_col = st.selectbox(
            "Select 52-week high column", 
            cols, 
            index=cols.index(high_col) if high_col in cols else 0
        )
        low_col = st.selectbox(
            "Select 52-week low column", 
            cols, 
            index=cols.index(low_col) if low_col in cols else 1
        )
        
        # Analysis
        if st.button("Analyze Data"):
            try:
                results = analyze_high_low(df, high_col=high_col, low_col=low_col)
                
                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(["Summary", "Stocks Near Lows", "Full Data"])
                
                with tab1:
                    st.subheader("Analysis Summary")
                    st.dataframe(results['summary'])
                    
                with tab2:
                    st.subheader("Stocks Near 52-Week Lows")
                    st.dataframe(results['near_lows'])
                    
                with tab3:
                    st.subheader("Full Analysis Data")
                    st.dataframe(results['full_data'])
                    
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.error("Please check your column mappings and data format.")
                
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        st.error("Please check your file format and try again.")
