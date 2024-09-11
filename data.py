import requests
import json
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

with open('config.json') as f:
    config = json.load(f)
api_key = config['api_key']


#get ticker symbols for S&P 500 companies from wikipedia

def get_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df = pd.read_html(url, header = 0)[0]
    tickers = list(df['Symbol'])
    return tickers

#function that returns the balance sheet, cash flow statement, and income statement for a given company and number of years

def get_financial_statements(company, years, api_key):
    balance_sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit={years}&apikey={api_key}").json()
    cash_flow = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?limit={years}&apikey={api_key}").json()
    income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{company}?limit={years}&apikey={api_key}").json()
    return balance_sheet, cash_flow, income_statement


#function that returns the stock data for a list of tickers

def get_stock_data(tickers):
    '''
    This function fetches the stock data for a list of tickers
    '''
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Create an empty DataFrame to store the data
    stock_data = pd.DataFrame()

    # Loop through each ticker and fetch the data
    for ticker in tickers:
        # Fetch the data, date is the index
        data = yf.download(ticker, start=start_date, end=end_date, interval='1mo')
        data['Ticker'] = ticker
        #add date as a column
        data.reset_index(inplace=True)
        stock_data = pd.concat([stock_data, data], ignore_index=True)
        stock_data

    # Rearrange columns to match the desired schema
    stock_data = stock_data[['Ticker', 'Date', 'Open', 'High', 'Low', 'Close']]
    return stock_data
    

   