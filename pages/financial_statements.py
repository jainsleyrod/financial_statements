import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go   

balance_sheet = pd.read_csv("data/balance_sheet.csv")
income_statement = pd.read_csv("data/income_statement.csv")
cash_flow = pd.read_csv("data/cash_flow.csv")
bs_analysis = pd.read_csv("data/bs_analysis.csv")
pnl_analysis = pd.read_csv("data/pnl_analysis.csv")
cf_analysis = pd.read_csv("data/cf_analysis.csv")

# Sidebar for user selection
st.sidebar.header("Select Company and Calendar Year")
selected_company = st.sidebar.selectbox("Choose a Company", balance_sheet['symbol'].unique())
selected_year = st.sidebar.selectbox("Choose a Calendar Year", balance_sheet[balance_sheet['symbol'] == selected_company]['calendarYear'].unique())

st.title("Financial Statements Overview")

selected_statement = st.radio("Select a Financial Statement", ["balance_sheet", "income_statement", "cash_flow"])

if selected_statement == "balance_sheet":
    
    st.subheader(f"Balance Sheet for {selected_company} in {selected_year}")
    bs = balance_sheet[(balance_sheet['symbol'] == selected_company) & (balance_sheet['calendarYear'] == selected_year)]
    st.write(bs)
    totalAssets = bs['totalAssets'].values[0]
    totalLiabilities = bs['totalLiabilities'].values[0]
    totalEquity = bs['totalEquity'].values[0]
    st.write(f"""
        A balance sheet provides a snapshot of a company's financial position at a specific point in time. 
        Key components include:
        - **Total Assets:** Everything the company owns. ({totalAssets})
        - **Total Liabilities:** Everything the company owes. ({totalLiabilities})
        - **Equity:** The value that belongs to the shareholders. ({totalEquity})
        
        High total assets and equity compared to liabilities generally indicate a healthy financial position.
        """)
    historical_data = balance_sheet[balance_sheet['symbol'] == selected_company]
    st.subheader("Trend Analysis")
    important_metrics = ['totalAssets', 'totalLiabilities', 'totalEquity']
    for metric in important_metrics:
    # Create a Plotly figure
        fig = go.Figure()
        
        # Add a line trace for the current metric
        fig.add_trace(go.Scatter(
            x=historical_data['calendarYear'],
            y=historical_data[metric],
            mode='lines+markers',
            name=metric
        ))
        
        # Customize layout
        fig.update_layout(
            title=f"Trend of {metric} Over Years",
            xaxis_title="Year",
            yaxis_title=metric,
            xaxis=dict(tickmode='array', tickvals=historical_data['calendarYear'].unique())  # Set x-axis ticks to show full years
        )

        # Display the Plotly chart using Streamlit
        st.plotly_chart(fig)
    st.subheader(f"Green Flags for {selected_company} Balance Sheet")
    df_list = bs_analysis[bs_analysis['symbol'] == selected_company].values.tolist()
    
    for item in df_list[0][1:4]:
        if pd.notna(item):
            st.write(f"- {item}")
        
    st.subheader(f"Red Flags for {selected_company} Balance Sheet")
    for item in df_list[0][4:7]:
        if pd.notna(item):
            st.write(f"- {item}")
        

  
elif selected_statement == "income_statement":
    st.subheader(f"Income Statement for {selected_company} in {selected_year}")
    pnl = income_statement[(income_statement['symbol'] == selected_company) & (income_statement['calendarYear'] == selected_year)]
    st.write(pnl)
    revenue = pnl['revenue'].values[0]
    costOfRevenue = pnl['costOfRevenue'].values[0]
    netIncome = pnl['netIncome'].values[0]
    
    # Income Statement Overview
    st.write(f"""
        An income statement shows the company's revenue, expenses, and profits over a specific period. 
        Key components include:
        - **Revenue:** Total income from sales. ({revenue})
        - **Cost of Goods Sold (COGS):** Direct costs related to production. ({costOfRevenue})
        - **Net Income:** Profit or loss after all expenses. ({netIncome})
        
        Growing revenue and positive net income are signs of a company's good financial health.
        """)
    
    # Trend Analysis
    historical_data = income_statement[income_statement['symbol'] == selected_company]
    st.subheader("Trend Analysis")
    important_metrics = ['revenue', 'costOfRevenue', 'netIncome']
    for metric in important_metrics:
    # Create a Plotly figure
        fig = go.Figure()
        
        # Add a line trace for the current metric
        fig.add_trace(go.Scatter(
            x=historical_data['calendarYear'],
            y=historical_data[metric],
            mode='lines+markers',
            name=metric
        ))
        
        # Customize layout
        fig.update_layout(
            title=f"Trend of {metric} Over Years",
            xaxis_title="Year",
            yaxis_title=metric,
            xaxis=dict(tickmode='array', tickvals=historical_data['calendarYear'].unique())  # Set x-axis ticks to show full years
        )

        # Display the Plotly chart using Streamlit
        st.plotly_chart(fig)
    
    # Green Flags
    st.subheader(f"Green Flags for {selected_company} Income Statement")
    df_list = pnl_analysis[pnl_analysis['symbol'] == selected_company].values.tolist()
    for item in df_list[0][4:7]:
        if pd.notna(item):
            st.write(f"- {item}")
    
    # Red Flags
    st.subheader(f"Red Flags for {selected_company} Income Statement")
    for item in df_list[0][1:4]:
        if pd.notna(item):
            st.write(f"- {item}")

### Cash Flow Statement
else:
    
    st.subheader(f"Cash Flow Statement for {selected_company} in {selected_year}")
    cf = cash_flow[(cash_flow['symbol'] == selected_company) & (cash_flow['calendarYear'] == selected_year)]
    st.write(cf)
    operatingCashFlow = cf['operatingCashFlow'].values[0]
    investingCashFlow = cf['netCashUsedForInvestingActivites'].values[0]
    financingCashFlow = cf['netCashUsedProvidedByFinancingActivities'].values[0]
    
    # Cash Flow Overview
    st.write(f"""
        A cash flow statement provides an overview of how cash is generated and used in operating, investing, and financing activities. 
        Key components include:
        - **Operating Cash Flow:** Cash generated from core business operations. ({operatingCashFlow})
        - **Investing Cash Flow:** Cash used or generated from investments. ({investingCashFlow})
        - **Financing Cash Flow:** Cash raised or returned to investors. ({financingCashFlow})
        
        Positive cash flows from operations indicate that a company can generate enough cash to maintain and grow its operations.
        """)
    
    # Trend Analysis
    historical_data = cash_flow[cash_flow['symbol'] == selected_company]
    st.subheader("Trend Analysis")
    important_metrics = ['operatingCashFlow', 'netCashUsedForInvestingActivites', 'netCashUsedProvidedByFinancingActivities']
    for metric in important_metrics:
    # Create a Plotly figure
        fig = go.Figure()
        
        # Add a line trace for the current metric
        fig.add_trace(go.Scatter(
            x=historical_data['calendarYear'],
            y=historical_data[metric],
            mode='lines+markers',
            name=metric
        ))
        
        # Customize layout
        fig.update_layout(
            title=f"Trend of {metric} Over Years",
            xaxis_title="Year",
            yaxis_title=metric,
            xaxis=dict(tickmode='array', tickvals=historical_data['calendarYear'].unique())  # Set x-axis ticks to show full years
        )

        # Display the Plotly chart using Streamlit
        st.plotly_chart(fig)
    
    # Green Flags
    st.subheader(f"Green Flags for {selected_company} Cash Flow Statement")
    df_list = cf_analysis[cf_analysis['symbol'] == selected_company].values.tolist()
    for item in df_list[0][4:7]:
        if pd.notna(item):
            st.write(f"- {item}")
    
    # Red Flags
    st.subheader(f"Red Flags for {selected_company} Cash Flow Statement")
    for item in df_list[0][1:4]:
        if pd.notna(item):
            st.write(f"- {item}")
