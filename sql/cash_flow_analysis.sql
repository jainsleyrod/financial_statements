CREATE TABLE cf_analysis (
    symbol VARCHAR(10) NOT NULL PRIMARY KEY,
    declining_operating_cash_flow TEXT,
    increased_capital_expenditures TEXT,
    increasing_debt_repayment TEXT,
    rising_free_cash_flow TEXT,
    decreasing_capital_expenditures TEXT,
    positive_net_change_in_cash TEXT,
    red_flag_count INT,
    green_flag_count INT
);

-- Inserting cash flow data into the new table
INSERT INTO cf_analysis (symbol, declining_operating_cash_flow, increased_capital_expenditures, increasing_debt_repayment, rising_free_cash_flow, decreasing_capital_expenditures, positive_net_change_in_cash, red_flag_count, green_flag_count)
WITH latest_data AS (
    SELECT 
        symbol,
        netCashProvidedByOperatingActivities,
        capitalExpenditure,
        debtRepayment,
        freeCashFlow,
        netChangeInCash,
        calendarYear
    FROM cash_flow
    WHERE (symbol, calendarYear) IN (
        SELECT symbol, MAX(calendarYear) 
        FROM cash_flow
        GROUP BY symbol
    )
),
previous_year_data AS (
    SELECT 
        symbol,
        netCashProvidedByOperatingActivities,
        capitalExpenditure,
        debtRepayment,
        freeCashFlow,
        netChangeInCash,
        calendarYear
    FROM cash_flow
    WHERE (symbol, calendarYear) IN (
        SELECT symbol, MAX(calendarYear) - 1 
        FROM cash_flow
        GROUP BY symbol
    )
)
SELECT
    ld.symbol,

    -- Red Flags
    CASE WHEN ld.netCashProvidedByOperatingActivities < pd.netCashProvidedByOperatingActivities THEN 'Declining Operating Cash Flow' ELSE NULL END AS declining_operating_cash_flow,
    CASE WHEN ld.capitalExpenditure > pd.capitalExpenditure THEN 'Increased Capital Expenditures' ELSE NULL END AS increased_capital_expenditures,
    CASE WHEN ld.debtRepayment > pd.debtRepayment THEN 'Increasing Debt Repayment' ELSE NULL END AS increasing_debt_repayment,
    
    -- Green Flags
    CASE WHEN ld.freeCashFlow > pd.freeCashFlow THEN 'Rising Free Cash Flow' ELSE NULL END AS rising_free_cash_flow,
    CASE WHEN ld.capitalExpenditure < pd.capitalExpenditure THEN 'Decreasing Capital Expenditures' ELSE NULL END AS decreasing_capital_expenditures,
    CASE WHEN ld.netChangeInCash > pd.netChangeInCash THEN 'Positive Net Change in Cash' ELSE NULL END AS positive_net_change_in_cash,
    
    -- Count Red Flags
    (CASE WHEN ld.netCashProvidedByOperatingActivities < pd.netCashProvidedByOperatingActivities THEN 1 ELSE 0 END +
     CASE WHEN ld.capitalExpenditure > pd.capitalExpenditure THEN 1 ELSE 0 END +
     CASE WHEN ld.debtRepayment > pd.debtRepayment THEN 1 ELSE 0 END) AS red_flag_count,
    
    -- Count Green Flags
    (CASE WHEN ld.freeCashFlow > pd.freeCashFlow THEN 1 ELSE 0 END +
     CASE WHEN ld.capitalExpenditure < pd.capitalExpenditure THEN 1 ELSE 0 END +
     CASE WHEN ld.netChangeInCash > pd.netChangeInCash THEN 1 ELSE 0 END) AS green_flag_count

FROM latest_data AS ld
JOIN previous_year_data AS pd
ON ld.symbol = pd.symbol;


-- Insert final count column
ALTER TABLE cf_analysis
ADD COLUMN cf_final_count INT;

UPDATE cf_analysis
SET cf_final_count = green_flag_count - red_flag_count;

SELECT *
FROM cf_analysis
;
