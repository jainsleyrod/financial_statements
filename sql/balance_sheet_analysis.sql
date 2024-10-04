CREATE TABLE bs_analysis (
    symbol VARCHAR(10) NOT NULL PRIMARY KEY,
    increasing_current_ratio TEXT,
    green_flag_positive_retained_earnings TEXT,
    increasing_working_capital TEXT,
    red_flag_high_accounts_receivable TEXT,
    increasing_debt_to_equity TEXT,
    decreasing_total_assets TEXT,
    red_flag_count INT,
    green_flag_count INT
);

INSERT INTO bs_analysis (symbol, increasing_current_ratio, green_flag_positive_retained_earnings, increasing_working_capital, red_flag_high_accounts_receivable, increasing_debt_to_equity, decreasing_total_assets, red_flag_count, green_flag_count)
WITH latest_data AS (
    SELECT 
        symbol,
        totalCurrentAssets,
        totalCurrentLiabilities,
        totalDebt,
        totalEquity,
        totalAssets,
        retainedEarnings,
        (totalCurrentAssets - totalCurrentLiabilities) AS workingCapital,
        netReceivables,
        calendarYear
    FROM balance_sheet
    WHERE (symbol, calendarYear) IN (
        SELECT symbol, MAX(calendarYear) 
        FROM balance_sheet
        GROUP BY symbol
    )
),
previous_year_data AS (
    SELECT 
        symbol,
        totalCurrentAssets,
        totalCurrentLiabilities,
        totalDebt,
        totalEquity,
        totalAssets,
        retainedEarnings,
        (totalCurrentAssets - totalCurrentLiabilities) AS workingCapital,
        netReceivables,
        calendarYear
    FROM balance_sheet
    WHERE (symbol, calendarYear) IN (
        SELECT symbol, MAX(calendarYear) - 1 
        FROM balance_sheet
        GROUP BY symbol
    )
)
SELECT
    ld.symbol,
    
    -- Green Flags
    CASE WHEN (ld.totalCurrentAssets / ld.totalCurrentLiabilities) > (pd.totalCurrentAssets / pd.totalCurrentLiabilities) THEN 'Increasing Current Ratio' END AS increasing_current_ratio,
    CASE WHEN ld.retainedEarnings > 0 THEN 'Positive Retained Earnings' END AS green_flag_positive_retained_earnings,
    CASE WHEN ld.workingCapital > pd.workingCapital THEN 'Increasing Working Capital' END AS increasing_working_capital,

    -- Red Flags
    CASE WHEN ld.netReceivables > (ld.totalAssets * 0.2) THEN 'High Accounts Receivable' END AS red_flag_high_accounts_receivable,
    CASE WHEN (ld.totalDebt / ld.totalEquity) > (pd.totalDebt / pd.totalEquity) THEN 'Increasing Debt to Equity Ratio' END AS increasing_debt_to_equity,
    CASE WHEN ld.totalAssets < pd.totalAssets THEN 'Decreasing Total Assets' END AS decreasing_total_assets,

    -- Count Red Flags
    (CASE WHEN ld.netReceivables > (ld.totalAssets * 0.2) THEN 1 ELSE 0 END +
     CASE WHEN (ld.totalDebt / ld.totalEquity) > (pd.totalDebt / pd.totalEquity) THEN 1 ELSE 0 END +
     CASE WHEN ld.totalAssets < pd.totalAssets THEN 1 ELSE 0 END) AS red_flag_count,

    -- Count Green Flags
    (CASE WHEN (ld.totalCurrentAssets / ld.totalCurrentLiabilities) > (pd.totalCurrentAssets / pd.totalCurrentLiabilities) THEN 1 ELSE 0 END +
     CASE WHEN ld.retainedEarnings > 0 THEN 1 ELSE 0 END +
     CASE WHEN ld.workingCapital > pd.workingCapital THEN 1 ELSE 0 END) AS green_flag_count
    
FROM latest_data AS ld
JOIN previous_year_data AS pd
ON ld.symbol = pd.symbol;

-- Insert final count column
ALTER TABLE bs_analysis
ADD COLUMN bs_final_count INT;

UPDATE bs_analysis
SET bs_final_count = green_flag_count - red_flag_count;

SELECT *
FROM bs_analysis;




