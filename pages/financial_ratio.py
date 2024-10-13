import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(pd.read_csv("data/financial_ratio.csv"))


st.title("Financial Health Analysis")

st.write("This section provides a snapshot of the company's financial health using key financial ratios.")

symbols = df['symbol'].unique().tolist()

selected_symbol = st.selectbox("Select a Company symbol:", symbols)

company_data = df[df['symbol'] == selected_symbol].iloc[0]

st.subheader(f"Financial Health Analysis for {selected_symbol}")

# Display the company's financial ratios
ratios = company_data.drop('symbol') 
horizontal_df = pd.DataFrame([ratios.index, ratios.values]).T
horizontal_df.columns = ['Metric', 'Value'] 

# Display the DataFrame in Streamlit
st.dataframe(horizontal_df)
# Mapping of ratio details with simplified descriptions
ratio_details = {
    'quick_ratio': {
        "description": "The Quick Ratio tells us if a company can quickly pay off its short-term bills using its most liquid assets (like cash). A higher number means better short-term financial health.",
        "calculation": "Quick Ratio = (Current Assets - Inventory) / Current Liabilities",
        "threshold": 1,  # Good value if above this
        "good_message": "This indicates that the company has enough liquid assets to cover its short-term liabilities.",
        "bad_message": "This suggests that the company may struggle to meet its short-term obligations."
    },
    'debt_to_equity': {
        "description": "The Debt-to-Equity Ratio shows how much debt a company has compared to its own money (equity). A lower number suggests less risk.",
        "calculation": "Debt-to-Equity Ratio = Total Liabilities / Shareholders' Equity",
        "threshold": 1,  # Good value if below this
        "good_message": "This indicates a balanced approach to leveraging debt and equity.",
        "bad_message": "A high ratio may indicate that the company is heavily reliant on debt for financing."
    },
    'working_capital_ratio': {
        "description": "The Working Capital Ratio measures if a company can cover its short-term debts with its short-term assets. A value above 1 is generally good.",
        "calculation": "Working Capital Ratio = Current Assets / Current Liabilities",
        "threshold": 1,  # Good value if above this
        "good_message": "This shows that the company is in a healthy liquidity position.",
        "bad_message": "A low ratio may signal potential liquidity issues."
    },
    'price_to_earnings_ratio': {
        "description": "The Price-to-Earnings (P/E) Ratio tells us how much investors are willing to pay for $1 of a company’s earnings. A very high P/E can mean that the stock is overvalued.",
        "calculation": "P/E Ratio = Market Value per Share / Earnings per Share",
        "threshold": 25,  # Good value if below this
        "good_message": "This suggests the stock is fairly valued or potentially undervalued.",
        "bad_message": "A high P/E may indicate that the stock is overvalued."
    },
    'earnings_per_share': {
        "description": "Earnings Per Share (EPS) shows how much money a company makes for each share of stock. Higher EPS usually indicates a more profitable company.",
        "calculation": "EPS = (Net Income - Dividends on Preferred Stock) / Average Outstanding Shares",
        "threshold": 0,  # Good value if above this
        "good_message": "This indicates the company is profitable, which is a good sign for investors.",
        "bad_message": "A negative EPS indicates the company is not making money, which is a concern."
    },
    'return_on_equity': {
        "description": "Return on Equity (ROE) shows how effectively a company uses its owners' money to make profit. A higher percentage is usually better.",
        "calculation": "ROE = Net Income / Shareholder's Equity",
        "threshold": 0.1,  # Good value if above this
        "good_message": "A higher ROE indicates efficient use of equity investments.",
        "bad_message": "A low ROE may indicate inefficiencies in generating profit."
    },
    'profit_margin': {
        "description": "Profit Margin tells us what percentage of sales is profit. A higher percentage means the company keeps more of its sales as profit.",
        "calculation": "Profit Margin = Net Income / Revenue",
        "threshold": 0.1,  # Good value if above this
        "good_message": "A higher profit margin indicates effective cost management and strong profitability.",
        "bad_message": "A lower margin may suggest challenges in controlling costs."
    }
}

# Select a specific ratio to view details
selected_ratio = st.selectbox("Select a Financial Ratio:", list(ratio_details.keys()))
ratio_info = ratio_details[selected_ratio]


# Display ratio information
st.subheader(f"{selected_ratio.replace('_', ' ').title()} for {selected_symbol}")
st.write(f"**Description:** {ratio_info['description']}")
st.write(f"**How to Calculate:** {ratio_info['calculation']}")

ratio_value = company_data[selected_ratio]

if (selected_ratio in ["debt_to_equity", "price_to_earnings_ratio"] and ratio_value <= ratio_info['threshold']) or \
       (selected_ratio in ["quick_ratio", "working_capital_ratio", "return_on_equity", "profit_margin", "earnings_per_share"] and ratio_value >= ratio_info['threshold']):
        color = 'green'
        message = ratio_info['good_message']
else:
    color = 'red'
    message = ratio_info['bad_message']

# Display the ratio value with the appropriate color
st.markdown(f"**Value:** <span style='color: {color}; font-weight: bold'>{ratio_value:.4f}</span>", unsafe_allow_html=True)
st.write(message)
if color == 'green':
    st.image("images/happy.jpg", width=200)
else:
    st.image("images/sad.jpg", width=200)