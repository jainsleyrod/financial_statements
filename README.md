## Steamlit dashboard to display financial statements of S&P 500 Companies
* Many individuals find it difficult to read and understand financial statements, which can hinder their ability to make informed investment decisions
* This project aims to create a user-friendly dashboard using Streamlit to present financial information for S&P 500 companies clearly and concisely, enhancing users' understanding of financial statements
* By offering both quantitative and qualitative insights, the dashboard empowers them to make more informed investment decisions
* Link to Dashboard: https://financial-statements-james.streamlit.app/

## Features of Dashboard
* Company Overview: General information of Companies
* Financial Ratios Analysis: Important financial ratios and their definitions
* Financial Statements Analysis: Breakdown of balance sheet, income statement, and cash flow statement
* Recommendation: Recommend similar companies using the similarity matrix based on selected metrics like netIncome, stockPrice...

## Resources Used
**Python Version**: 3.10
**Packages**: pandas, streamlit, numpy, matplotlib, plotly, requests, lxml, yfinance, mysql-connector-python, sqlalchemy, pymysql, beautifulsoup4, scikit-learn, seaborn

## Data Collection
* Collected financial statements data from Financial Modelling Prep API: https://site.financialmodelingprep.com/
* Data was stored in a mySQL database

## Exploratory Data Analysis
Further analysis was done on the financial statements using SQL
* Calculating financial ratios
* Identifying green and red flags


