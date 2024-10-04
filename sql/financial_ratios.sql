-- create new table for financial ratios

DROP TABLE IF EXISTS financial_ratios;

CREATE TABLE financial_ratios (
    symbol VARCHAR(10) NOT NULL,
    quick_ratio DECIMAL(10, 4),
    debt_to_equity DECIMAL(10, 4),
    working_capital_ratio DECIMAL(10, 4),
    price_to_earnings_ratio DECIMAL(10, 4),
    earnings_per_share DECIMAL(10, 4),
    return_on_equity DECIMAL(10, 4),
    profit_margin DECIMAL(10, 4)
);

-- create temporary tables which contain only latest data for the year 2023 for each symbol
CREATE TEMPORARY TABLE latest_balance_sheet AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) AS rn
    FROM balance_sheet
) AS ranked
WHERE rn = 1;

CREATE TEMPORARY TABLE latest_income_statement AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) AS rn
    FROM income_statement
) AS ranked
WHERE rn = 1;

CREATE TEMPORARY TABLE latest_cash_flow AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) AS rn
    FROM cash_flow
) AS ranked
WHERE rn = 1;

CREATE TEMPORARY TABLE latest_stock_data AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY Ticker ORDER BY date DESC) AS rn
    FROM stock_data
) AS ranked
WHERE rn = 1;

-- Insert data into table

INSERT INTO financial_ratios (
    symbol, 
    quick_ratio, 
    debt_to_equity, 
    working_capital_ratio, 
    price_to_earnings_ratio, 
    earnings_per_share, 
    return_on_equity, 
    profit_margin
)
SELECT
	bs.symbol,
    ((bs.totalCurrentAssets - bs.inventory) / bs.totalCurrentLiabilities) AS quick_ratio,
    (bs.totalLiabilities / bs.totalEquity ) AS debt_to_equity,
    (bs.totalCurrentAssets / bs.totalCurrentLiabilities) AS working_capital_ratio,
    (sd.Close / pnl.eps) AS price_to_earnings_ratio,
    pnl.eps AS earnings_per_share,
    (pnl.netIncome / bs.totalEquity) AS return_on_equity,
    (pnl.netIncome / pnl.revenue) AS profit_margin
FROM
	latest_balance_sheet as bs
JOIN
	latest_income_statement pnl ON bs.symbol = pnl.symbol
JOIN 
	latest_cash_flow cf ON bs.symbol = cf.symbol
JOIN
	latest_stock_data sd on bs.symbol = sd.Ticker
;