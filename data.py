import requests
import json
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

with open('config.json') as f:
    config = json.load(f)
api_key = config['api_key']


#function that returns the balance sheet, cash flow statement, and income statement for a given company and number of years

def get_financial_statements(company, years, api_key):
    balance_sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit={years}&apikey={api_key}").json()
    cash_flow = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?limit={years}&apikey={api_key}").json()
    income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{company}?limit={years}&apikey={api_key}").json()
    return balance_sheet, cash_flow, income_statement


def get_stock_data(ticker):
    '''
    This function fetches the stock data for a single ticker
    '''
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Fetch the data, date is the index
    data = yf.download(ticker, start=start_date, end=end_date, interval='1mo')
    data['Ticker'] = ticker

    # Add date as a column and reset index
    data.reset_index(inplace=True)

    # Rearrange columns to match the desired schema
    data = data[['Ticker', 'Date', 'Open', 'High', 'Low', 'Close']]
    return data


#get tickers of S&P 500 companies
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
companies = pd.read_html(url, header = 0)[0]
#companies.to_csv('data/sp500_companies.csv', index=False)

tickers = list(companies['Symbol'])

'''
#Get stock data for each ticker
stock_data = pd.DataFrame()
for ticker in tickers:
    stock_data = pd.concat([stock_data, get_stock_data(ticker)], ignore_index=True)

stock_data.to_csv('data/stock_data.csv', index=False)
'''


# Initialize DataFrames
balance_sheet_df = pd.DataFrame()
income_statement_df = pd.DataFrame()
cash_flow_df = pd.DataFrame()

# Define essential columns
essential_bs = [
    'date', 'symbol', 'cashAndCashEquivalents', 'totalCurrentAssets',
    'propertyPlantEquipmentNet', 'totalNonCurrentAssets', 'totalAssets',
    'totalCurrentLiabilities', 'longTermDebt', 'totalLiabilities',
    'totalStockholdersEquity', 'retainedEarnings', 'totalDebt', 'netDebt', 'finalLink'
]

essential_is = [
    'date', 'symbol', 'revenue', 'costOfRevenue', 'grossProfit',
    'researchAndDevelopmentExpenses', 'generalAndAdministrativeExpenses',
    'sellingAndMarketingExpenses', 'operatingExpenses', 'ebitda',
    'operatingIncome', 'incomeBeforeTax', 'netIncome', 'eps', 'epsdiluted', 'finalLink'
]

essential_cf = [
    'date', 'symbol', 'netCashProvidedByOperatingActivities',
    'netCashUsedForInvestingActivites',
    'netCashUsedProvidedByFinancingActivities',
    'netChangeInCash', 'finalLink'
]

#financial modelling prep api only allows 250 requests per day, ~80 companies per day, around 7 days to get all data

for ticker in tickers[80:160]:
    try:
        # Fetch financial statements
        balance_sheet, cash_flow, income_statement = get_financial_statements(ticker, 1, api_key)
        
        # Convert to DataFrames
        balance_sheet = pd.DataFrame(balance_sheet)
        income_statement = pd.DataFrame(income_statement)
        cash_flow = pd.DataFrame(cash_flow)
        
        # Filter essential columns
        balance_sheet = balance_sheet[essential_bs]
        income_statement = income_statement[essential_is]
        cash_flow = cash_flow[essential_cf]
        
        # Append to main DataFrames
        balance_sheet_df = pd.concat([balance_sheet_df, balance_sheet], ignore_index=True)
        income_statement_df = pd.concat([income_statement_df, income_statement], ignore_index=True)
        cash_flow_df = pd.concat([cash_flow_df, cash_flow], ignore_index=True)
    
    except Exception as e:
        # Log the error and skip the current ticker
        print(f"Error processing data for {ticker}: {e}")
        continue  # Skip the row and move to the next ticker

# Save DataFrames to CSV
balance_sheet_df.to_csv('data/balance_sheet.csv', index=False)
income_statement_df.to_csv('data/income_statement.csv', index=False)
cash_flow_df.to_csv('data/cash_flow.csv', index=False)