import streamlit as st

# Main page setup
st.set_page_config(page_title="S&P 500 Financial Health Dashboard", layout="wide")
st.title("S&P 500 Financial Health Dashboard")
st.write("""
Welcome to the S&P 500 Financial Health Dashboard. This application provides an in-depth view of the financial statements and overall health of companies within the S&P 500 index.
Explore the following sections:
- **Company Overview**: Get insights into individual company financials.
- **Financial Health Analysis**: See a breakdown of financial health indicators.
- **Investment Insights**: View company trends and investment potential.
- **S&P 500 Overview**: Analyze overall trends and performance of the S&P 500 index.
""")

# Sidebar navigation note
st.sidebar.title("Navigation")
st.sidebar.write("Use the sidebar to select a page to explore specific sections.")