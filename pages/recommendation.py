import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt
import seaborn as sns

bs = pd.read_csv('data/balance_sheet.csv')
is_ = pd.read_csv('data/income_statement.csv')
cf = pd.read_csv('data/cash_flow.csv')
ratios = pd.read_csv('data/financial_ratio.csv')
weightage = pd.read_csv('data/weightage.csv')
stock_data = pd.read_csv('data/stock_data.csv')


def get_latest_data(df):
    # Filter the DataFrame to include only the latest year for each company
    return df.loc[df.groupby('symbol')['calendarYear'].idxmax()]

# Get latest year for each financial statement
latest_bs = get_latest_data(bs)
latest_is = get_latest_data(is_)
latest_cf = get_latest_data(cf)


#select relevant columns
latest_bs = latest_bs[['symbol', 'totalAssets', 'totalLiabilities', 'totalEquity']]
latest_is = latest_is[['symbol', 'revenue', 'costOfRevenue', 'netIncome']]
latest_cf = latest_cf[['symbol', 'operatingCashFlow', 'netCashUsedForInvestingActivites', 'netCashUsedProvidedByFinancingActivities']]

#merge the dataframes
latest_data = pd.merge(latest_bs, latest_is, on='symbol')
latest_data = pd.merge(latest_data, latest_cf, on='symbol')

weightage.columns = ['symbol', 'weightage']
final = pd.merge(latest_data, ratios, on='symbol')
final = pd.merge(final, weightage, on='symbol')

stock_data = stock_data.loc[stock_data.groupby('Ticker')['Date'].idxmax()]

stock_data = stock_data[['Ticker', 'Close']]
stock_data.columns = ['symbol', 'stock_price']

#final dataframe
final = pd.merge(final, stock_data, on='symbol')

final['weightage'] = final['weightage'].str.replace('%', '').astype(float)

#Feature scaling
scaler = StandardScaler()
scaled = scaler.fit_transform(final.drop(columns=['symbol']))

# Fit K-Means model
k = 5  # Choose a suitable number of clusters
kmeans = KMeans(n_clusters=k, random_state=42)
final['Cluster'] = kmeans.fit_predict(scaled)  # Assign clusters to the final DataFrame

# Streamlit UI
st.title("Company Recommendation System with K-Means")

# User selects a company
selected_company = st.selectbox("Select a company you like:", final['symbol'].unique())

if st.button("Get Recommendations"):
    # Find the cluster of the selected company
    selected_cluster = final[final['symbol'] == selected_company]['Cluster'].values[0]
    selected_features = final[final['symbol'] == selected_company].drop(columns=['symbol', 'Cluster']).values
    
    # Get companies in the same cluster
    recommendations = final[final['Cluster'] == selected_cluster]

    # Calculate distances from the selected company
    distances = pairwise_distances(recommendations.drop(columns=['symbol', 'Cluster']), selected_features)

    # Add distances to recommendations DataFrame
    recommendations['Distance'] = distances

    # Set a threshold for distance (you can adjust this value)
    distance_threshold = 20.0  # Adjust this value based on your dataset
    strict_recommendations = recommendations[recommendations['Distance'] < distance_threshold]['symbol'].tolist()
    
    # Remove the selected company from recommendations
    strict_recommendations = [company for company in strict_recommendations if company != selected_company]
    
    st.write("You might also like:")
    if strict_recommendations:
        for company in strict_recommendations:
            st.write(company)
    else:
        st.write("No similar companies found in the same cluster.")




