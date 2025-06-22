import streamlit as st
import pandas as pd
import plotly.express as px
from analyzer import analyze_high_low

# Page Config
st.set_page_config(
    page_title="Stock Breakout Analyzer", 
    page_icon="📈", 
    layout="wide"
)

# Title
st.title("📊 Stock Breakout & Range-Bound Dashboard")
st.markdown("Upload a 52-week High/Low CSV/XLSX to identify trading opportunities.")

# File Upload
uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("✅ File uploaded successfully!")
    
    # Analyze Data
    results = analyze_high_low(df)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "Breakout Candidates", 
        "Range-Bound Stocks", 
        "Sector Trends", 
        "Volatility Heatmap"
    ])
    
    # Tab 1: Breakout Candidates
    with tab1:
        st.subheader("🚀 Breakout Candidates (Near 52-Week High)")
        st.dataframe(
            results['breakout'][['SYMBOL', 'Adjusted_52_Week_High', 
                               'Current_To_High_Pct', 'Price_Range_Pct']],
            height=400
        )
        
        # Bar Chart: Top Breakout Candidates
        fig = px.bar(
            results['breakout'].head(20),
            x='SYMBOL',
            y='Current_To_High_Pct',
            title="% Distance from 52-Week High",
            color='Price_Range_Pct',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Range-Bound Stocks
    with tab2:
        st.subheader("🔄 Range-Bound Stocks (Low Volatility)")
        st.dataframe(
            results['range_bound'][['SYMBOL', 'Adjusted_52_Week_High', 
                                  'Adjusted_52_Week_Low', 'Price_Range_Pct']],
            height=400
        )
        
        # Line Chart: Price Range
        fig = px.line(
            results['range_bound'].head(20),
            x='SYMBOL',
            y=['Adjusted_52_Week_High', 'Adjusted_52_Week_Low'],
            title="52-Week High vs. Low Prices",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Sector Trends
    with tab3:
        if not results['sector_stats'].empty:
            st.subheader("📊 Sector-Wise Performance")
            st.dataframe(results['sector_stats'], height=400)
            
            # Pie Chart: Sector Volatility
            fig = px.pie(
                results['sector_stats'],
                names=results['sector_stats'].index,
                values='Avg_Volatility',
                title="Sector Volatility Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No sector data found. Add a 'SECTOR' column to enable this feature.")
    
    # Tab 4: Volatility Heatmap
    with tab4:
        st.subheader("🔥 Price Range Heatmap")
        fig = px.imshow(
            pd.pivot_table(
                results['all_data'].head(50),
                values='Price_Range_Pct',
                index='SYMBOL',
                columns='SECTOR' if 'SECTOR' in df.columns else None
            ),
            color_continuous_scale='Reds',
            title="Volatility (Price Range %) Across Stocks"
        )
        st.plotly_chart(fig, use_container_width=True)
