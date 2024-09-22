import requests
import json
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

with open('config.json') as f:
    config = json.load(f)
api_key = config['api_key']


#function that returns the balance sheet, cash flow statement, and income statement for a given company and number of years

def get_financial_statements(company, years, api_key):
    balance_sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit={years}&apikey={api_key}").json()
    income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{company}?limit={years}&apikey={api_key}").json()
    cash_flow = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?limit={years}&apikey={api_key}").json()
    return balance_sheet,  income_statement, cash_flow

#function that returns the stock data for a given ticker for the past 3 years at monthly intervals

def get_stock_data(ticker):
    '''
    This function fetches the stock data for a single ticker
    '''
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)

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
companies.columns = companies.columns.str.strip().str.replace(' ', '_')
companies.to_csv('data/sp500_companies.csv', index=False)

tickers = list(companies['Symbol'])


#Get the weightage of each ticker in the S&P 500 index
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
})

response = session.get(url)
if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    #get the table
    table = soup.find('table')
    weightage = pd.read_html(str(table))[0]
    weightage = weightage[['Symbol', 'Weight']]
    weightage.columns = weightage.columns.str.strip().str.replace(' ', '_')
    weightage.to_csv('data/weightage.csv', index=False)
    
else:
    print(f"Failed to retrieve data: {response.status_code}")
    
    
#Get stock data for each ticker
stock_data = pd.DataFrame()
for ticker in tickers:
    stock_data = pd.concat([stock_data, get_stock_data(ticker)], ignore_index=True)

stock_data.columns = stock_data.columns.str.strip().str.replace(' ', '_')

stock_data.to_csv('data/stock_data.csv', index=False)


# Initialize DataFrames
balance_sheet_df = pd.DataFrame()
income_statement_df = pd.DataFrame()
cash_flow_df = pd.DataFrame()

#Get financial statements for each ticker
#financial modelling prep api only allows 250 requests per day, ~80 companies per day as each function call makes 3 requests 
for ticker in tickers[:80]:
    try:
        # Fetch financial statements for the past 3 years
        balance_sheet, income_statement, cash_flow = get_financial_statements(ticker, 3, api_key)
        
        # Convert to DataFrames
        balance_sheet = pd.DataFrame(balance_sheet)
        income_statement = pd.DataFrame(income_statement)
        cash_flow = pd.DataFrame(cash_flow)
        
        # Append to main DataFrames
        balance_sheet_df = pd.concat([balance_sheet_df, balance_sheet], ignore_index=True)
        income_statement_df = pd.concat([income_statement_df, income_statement], ignore_index=True)
        cash_flow_df = pd.concat([cash_flow_df, cash_flow], ignore_index=True)
    
    except Exception as e:
        # Log the error and skip the current ticker
        print(f"Error processing data for {ticker}: {e}")
        continue  # Skip the row and move to the next ticker


balance_sheet_df.columns = balance_sheet_df.columns.str.strip().str.replace(' ', '_')
income_statement_df.columns = income_statement_df.columns.str.strip().str.replace(' ', '_')
cash_flow_df.columns = cash_flow_df.columns.str.strip().str.replace(' ', '_')

# Save DataFrames to CSV
balance_sheet_df.to_csv('data/balance_sheet.csv', index=False)
income_statement_df.to_csv('data/income_statement.csv', index=False)
cash_flow_df.to_csv('data/cash_flow.csv', index=False)
