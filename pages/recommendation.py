import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


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

#finanicial ratios
final = pd.merge(latest_data, ratios, on='symbol')

#weightage in sp500
weightage.columns = ['symbol', 'weightage']
final = pd.merge(final, weightage, on='symbol')
final['weightage'] = final['weightage'].str.replace('%', '').astype(float)

#stock price
stock_data = stock_data.loc[stock_data.groupby('Ticker')['Date'].idxmax()]
stock_data = stock_data[['Ticker', 'Close']]
stock_data.columns = ['symbol', 'stock_price']

#final dataframe with all important columns
final = pd.merge(final, stock_data, on='symbol')

#Feature scaling for numerical columns
scaler = StandardScaler()
features = final.drop(columns=['symbol'])

#Put more weight on stock price
features['stock_price'] = features['stock_price'] * 3
features_scaled = scaler.fit_transform(features)

# Calculate the cosine similarity between companies
similarity_matrix = cosine_similarity(features_scaled)
similarity_df = pd.DataFrame(similarity_matrix, index=final['symbol'], columns=final['symbol'])

# Streamlit title
st.title('S&P 500 Company Recommendation System')

# Streamlit sidebar input for company name
company_name = st.selectbox('Select a Company', final['symbol'])


# Function to recommend similar companies
def recommend_similar(company, similarity_df, num_recommendations=3):
    similar_scores = similarity_df[company].sort_values(ascending=False)
    similar_companies = similar_scores.index[similar_scores.index != company]
    return similar_companies[:num_recommendations]


# If the user selects a company, display recommendations
if company_name:
    recommended_companies = recommend_similar(company_name, similarity_df)
    st.write(f"### Here are some similar stocks you can buy:")
    for i, company in enumerate(recommended_companies):
        stock_price = round(final[final['symbol'] == company]['stock_price'].values[0],2)
        # Display company name and stock price
        st.write(f"{i + 1}. **{company}** - Stock Price: ${stock_price}")
st.write("#### Check out more information about the recommended companies in the other sections!")