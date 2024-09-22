import pandas as pd
from sqlalchemy import create_engine
import json

with open('config.json') as f:
    config = json.load(f)
password = config['password']

#Read the data
sp500_companies = pd.read_csv('data/sp500_companies.csv')
weightage = pd.read_csv('data/weightage.csv')
stock_data = pd.read_csv('data/stock_data.csv')
balance_sheet_df = pd.read_csv('data/balance_sheet.csv')
income_statement_df = pd.read_csv('data/income_statement.csv')
cash_flow_df = pd.read_csv('data/cash_flow.csv')


# Save the data to MySQL sp500 database
engine = create_engine(f'mysql+pymysql://root:{password}@localhost/sp500')

sp500_companies.to_sql('sp500_companies', con=engine, if_exists='replace', index=False)
weightage.to_sql('weightage', con=engine, if_exists='replace', index=False)
stock_data.to_sql('stock_data', con=engine, if_exists='replace', index=False)
balance_sheet_df.to_sql('balance_sheet', con=engine, if_exists='append', index=False)
income_statement_df.to_sql('income_statement', con=engine, if_exists='append', index=False)
cash_flow_df.to_sql('cash_flow', con=engine, if_exists='append', index=False)


