import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

company = pd.read_csv('data/sp500_companies.csv')
weightage = pd.read_csv('data/weightage.csv')

# Sidebar for user selection
st.sidebar.header("Select Company")
selected_company = st.sidebar.selectbox("Choose a Company", company['Symbol'].unique())

company_info = company[company['Symbol'] == selected_company]
weightage_info = weightage[weightage['Symbol'] == selected_company]

st.subheader(f"Basic Information for {selected_company}")
st.write(f"**Sector:** {company_info['GICS_Sector'].values[0]}")
st.write(f"**Date Added:** {company_info['Date_added'].values[0]}")
st.write(f"**Weightage in S&P 500:** {weightage_info['Weight'].values[0]}")





# Visualization: Pie Chart of Sector Distribution
sector_distribution = company['GICS_Sector'].value_counts()
plt.figure(figsize=(10, 5))
plt.pie(sector_distribution, labels=sector_distribution.index, autopct='%1.1f%%', startangle=140)
plt.title("Sector Distribution of S&P 500 Companies")
st.pyplot(plt)