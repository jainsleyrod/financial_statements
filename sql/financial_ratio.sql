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

-- Insert data into financial_ratios table
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
WITH latest_balance_sheet AS (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) AS rn
        FROM balance_sheet
    ) AS ranked
    WHERE rn = 1
),
latest_income_statement AS (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) AS rn
        FROM income_statement
    ) AS ranked
    WHERE rn = 1
),
latest_cash_flow AS (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) AS rn
        FROM cash_flow
    ) AS ranked
    WHERE rn = 1
),
latest_stock_data AS (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY Ticker ORDER BY date DESC) AS rn
        FROM stock_data
    ) AS ranked
    WHERE rn = 1
)

SELECT
    bs.symbol,
    (bs.totalCurrentAssets - bs.inventory) / NULLIF(bs.totalCurrentLiabilities, 0) AS quick_ratio,
    bs.totalLiabilities / NULLIF(bs.totalEquity, 0) AS debt_to_equity,
    bs.totalCurrentAssets / NULLIF(bs.totalCurrentLiabilities, 0) AS working_capital_ratio,
    CASE 
        WHEN pnl.eps = 0 THEN NULL 
        ELSE sd.Close / pnl.eps bs_analysis
    END AS price_to_earnings_ratio,
    pnl.eps AS earnings_per_share,
    pnl.netIncome / NULLIF(bs.totalEquity, 0) AS return_on_equity,
    pnl.netIncome / NULLIF(pnl.revenue, 0) AS profit_margin
FROM
    latest_balance_sheet AS bs
JOIN
    latest_income_statement AS pnl ON bs.symbol = pnl.symbol
JOIN 
    latest_cash_flow AS cf ON bs.symbol = cf.symbol
JOIN
    latest_stock_data AS sd ON bs.symbol = sd.Ticker;


SELECT *
FROM financial_ratios;