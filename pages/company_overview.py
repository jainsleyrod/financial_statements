import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

company = pd.read_csv('data/sp500_companies.csv')
weightage = pd.read_csv('data/weightage.csv')
stock_data = pd.read_csv('data/stock_data.csv')

# Sidebar for user selection
st.sidebar.header("Select Company")
selected_company = st.sidebar.selectbox("Choose a Company", company['Symbol'].unique())

company_info = company[company['Symbol'] == selected_company]
weightage_info = weightage[weightage['Symbol'] == selected_company]

st.subheader(f"Basic Information for {selected_company}")
st.write(f"**Sector:** {company_info['GICS_Sector'].values[0]}")
st.write(f"**Date Added:** {company_info['Date_added'].values[0]}")
st.write(f"**Weightage in S&P 500:** {weightage_info['Weight'].values[0]}")

# Visualization: Stock Price Line Chart
stock_data = stock_data[stock_data['Ticker'] == selected_company]
# Plotly Line Chart
fig = px.line(stock_data, x='Date', y='Close', title=f"Stock Price for {selected_company}")
st.plotly_chart(fig)



# Visualization: Pie Chart of Sector Distribution
sector_distribution = company['GICS_Sector'].value_counts()

# Plotly Pie Chart
fig = px.pie(values=sector_distribution, 
             names=sector_distribution.index, 
             title="Sector Distribution of S&P 500 Companies", 
             hole=0.4,  # Creates a donut chart
             labels={'label': 'Sector', 'value': 'Count'},
             color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig)

#Get company name fron ticker
selected_name = company[company['Symbol'] == selected_company]['Security'].values[0]

with open('config.json') as f:
    config = json.load(f)
api_key = config['serpi_api_key']

url = f'https://serpapi.com/search.json?engine=google&q={selected_name}&api_key={api_key}'
# Fetch articles from SerpAPI
response = requests.get(url)
data = response.json()

# Display latest news articles
st.subheader(f"Latest News Articles about {selected_name} (Qualtitative Analysis)")

if response.status_code == 200 and 'organic_results' in data:
    articles = data['organic_results'][:3]  # Get the first 3 articles

    if articles:
        for article in articles:
            title = article.get('title')
            link = article.get('link')
            st.write(f"**Title:** {title}")
            st.write(f"**URL:** {link}")
            st.write("----")
    else:
        st.write("No news articles found for this company.")
else:
    st.write("Error fetching articles:", data.get('error', 'Unknown error'))