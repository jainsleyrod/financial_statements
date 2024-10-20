import streamlit as st

# Main page setup
st.set_page_config(page_title="S&P 500 Financial Health Dashboard", layout="wide")
st.title("S&P 500 Financial Health Dashboard")
st.write("""
Welcome to the S&P 500 Financial Health Dashboard. This application provides an in-depth view of the financial statements and overall health of companies within the S&P 500 index.
Explore the following sections:
- **Company Overview**: Get insights into individual company details.
- **Financial Ratio Analysis**: See a breakdown of financial health ratios.
- **Financial Statements Analysis**: Dive into the balance sheet, income statement, and cash flow statement.
- **Recommendation**: Discover companies with similar financial health.
""")

