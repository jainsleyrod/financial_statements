import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

balance_sheet = pd.read_csv("data/balance_sheet.csv")
income_statement = pd.read_csv("data/income_statement.csv")
cash_flow = pd.read_csv("data/cash_flow.csv")

# Sidebar for user selection
st.sidebar.header("Select Company and Calendar Year")
selected_company = st.sidebar.selectbox("Choose a Company", balance_sheet['symbol'].unique())
selected_year = st.sidebar.selectbox("Choose a Calendar Year", balance_sheet[balance_sheet['symbol'] == selected_company]['calendarYear'].unique())

st.title("Financial Statements Overview")

selected_statement = st.radio("Select a Financial Statement", ["balance_sheet", "income_statement", "cash_flow"])

if selected_statement == "balance_sheet":
    
    st.subheader(f"Balance Sheet for {selected_company} in {selected_year}")
    st.write(balance_sheet[(balance_sheet['symbol'] == selected_company) & (balance_sheet['calendarYear'] == selected_year)])
    st.write("""
        A balance sheet provides a snapshot of a company's financial position at a specific point in time. 
        Key components include:
        - **Total Assets:** Everything the company owns.
        - **Total Liabilities:** Everything the company owes.
        - **Equity:** The value that belongs to the shareholders.
        
        High total assets and equity compared to liabilities generally indicate a healthy financial position.
        """)
    historical_data = balance_sheet[balance_sheet['symbol'] == selected_company]
    st.subheader("Trend Analysis")
    important_metrics = ['totalAssets', 'totalLiabilities', 'totalEquity']
    for metric in important_metrics:
        plt.figure(figsize=(10, 5))
        plt.plot(historical_data['calendarYear'], historical_data[metric], marker='o', label=metric.replace('total', 'Total '))
        plt.title(f"Trend of {metric.replace('total', 'Total ')} Over Years")
        plt.xlabel("Year")
        plt.ylabel(metric.replace('total', 'Total '))
        st.pyplot(plt)
    
elif selected_statement == "income_statement":
    st.subheader(f"Income Statement for {selected_company} in {selected_year}")
    st.write(income_statement[(income_statement['symbol'] == selected_company) & (income_statement['calendarYear'] == selected_year)])

else:
    st.subheader(f"Cash Flow Statement for {selected_company} in {selected_year}")
    st.write(cash_flow[(cash_flow['symbol'] == selected_company) & (cash_flow['calendarYear'] == selected_year)])
    