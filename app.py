import pandas as pd
import streamlit as st
import plotly.express as px
from analyzer import analyze_high_low

# Configure the app
st.set_page_config(
    page_title="Stock Breakout Analyzer", 
    page_icon="📈", 
    layout="wide"
)

# Custom CSS for better visuals
st.markdown("""
    <style>
    .stDataFrame { width: 100% !important; }
    .stAlert { padding: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

def load_data(uploaded_file):
    """Load and validate uploaded file."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(
                uploaded_file,
                encoding='utf-8',
                on_bad_lines='skip',
                dtype={
                    'Adjusted_52_Week_High': float,
                    'Adjusted_52_Week_Low': float
                }
            )
        else:
            df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Failed to load file: {str(e)}")
        return None

# UI Components
st.title("🚀 Stock Breakout & Range-Bound Analyzer")
st.markdown("Upload a 52-week High/Low CSV or Excel file to identify trading opportunities.")

# File Upload
uploaded_file = st.file_uploader(
    "Choose a file", 
    type=["csv", "xlsx"],
    help="Ensure columns: SYMBOL, SERIES, Adjusted_52_Week_High, 52_Week_High_Date, Adjusted_52_Week_Low, 52_Week_Low_DT"
)

if uploaded_file:
    df = load_data(uploaded_file)
    
    if df is not None:
        # Analysis
        results = analyze_high_low(df)
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs([
            "📊 Breakout Candidates", 
            "🔄 Range-Bound Stocks", 
            "🔥 Volatility Analysis"
        ])

        with tab1:
            st.subheader("Stocks Near 52-Week High (Breakout Potential)")
            if not results['breakout'].empty:
                st.dataframe(
                    results['breakout'].style.highlight_max(
                        subset=['Current_To_High_Pct'], 
                        color='lightgreen'
                    ),
                    use_container_width=True
                )
                fig = px.bar(
                    results['breakout'].head(20),
                    x='SYMBOL',
                    y='Current_To_High_Pct',
                    title="Top Breakout Candidates (% from 52-Week High)",
                    color='Price_Range_Pct',
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No breakout candidates found. Try adjusting thresholds.")

        with tab2:
            st.subheader("Low-Volatility (Range-Bound) Stocks")
            if not results['range_bound'].empty:
                st.dataframe(
                    results['range_bound'].style.highlight_min(
                        subset=['Price_Range_Pct'], 
                        color='lightblue'
                    ),
                    use_container_width=True
                )
                fig = px.line(
                    results['range_bound'].head(20),
                    x='SYMBOL',
                    y=['Adjusted_52_Week_High', 'Adjusted_52_Week_Low'],
                    title="Price Range of Stable Stocks",
                    markers=True
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No range-bound stocks detected.")

        with tab3:
            st.subheader("Volatility Heatmap")
            if not df.empty:
                fig = px.imshow(
                    df.pivot_table(
                        values='Price_Range_Pct',
                        index='SYMBOL',
                        columns=None
                    ).head(50),
                    color_continuous_scale='Reds',
                    title="Stock Volatility Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("ℹ️ Upload a properly formatted CSV/XLSX file with 52-week high/low data.")
