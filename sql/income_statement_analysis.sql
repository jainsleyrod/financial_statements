CREATE TABLE pnl_analysis (
    symbol VARCHAR(10) NOT NULL PRIMARY KEY,
    declining_gross_profit_margin TEXT,
    rising_sga_expenses TEXT,
    increasing_debt_burden TEXT,
    increasing_ebitda_margin TEXT,
    rising_operating_income TEXT,
    revenue_growth TEXT,
    red_flag_count INT,
    green_flag_count INT
);

INSERT INTO pnl_analysis (symbol, declining_gross_profit_margin, rising_sga_expenses, increasing_debt_burden, increasing_ebitda_margin, rising_operating_income, revenue_growth, red_flag_count, green_flag_count)
WITH latest_data AS (
    SELECT 
        symbol,
        revenue,
        grossProfitRatio,
        sellingGeneralAndAdministrativeExpenses,
        interestExpense,
        ebitdaratio,
        operatingIncome,
        calendarYear
    FROM income_statement
    WHERE (symbol, calendarYear) IN (
        SELECT symbol, MAX(calendarYear) 
        FROM income_statement
        GROUP BY symbol
    )
),
previous_year_data AS (
    SELECT 
        symbol,
        revenue,
        grossProfitRatio,
        sellingGeneralAndAdministrativeExpenses,
        interestExpense,
        ebitdaratio,
        operatingIncome,
        calendarYear
    FROM income_statement
    WHERE (symbol, calendarYear) IN (
        SELECT symbol, MAX(calendarYear) - 1 income_statement
        FROM income_statement
        GROUP BY symbol
    )
)
SELECT
	ld.symbol,
    
	-- Red Flags
    CASE WHEN ld.grossProfitRatio < pd.grossProfitRatio THEN 'Declining Gross Profit Margin' END AS declining_gross_profit_margin,
    CASE WHEN ld.sellingGeneralAndAdministrativeExpenses > pd.sellingGeneralAndAdministrativeExpenses THEN 'Rising SG&A Expenses' END AS rising_sga_expenses,
    CASE WHEN ld.interestExpense > pd.interestExpense THEN 'Increasing Debt Burden' END AS increasing_debt_burden,
    
    -- Green Flags
    CASE WHEN ld.ebitdaratio > pd.ebitdaratio THEN 'Increasing EBITDA Margin' END AS increasing_ebitda_margin,
    CASE WHEN ld.operatingIncome > pd.operatingIncome THEN 'Rising Operating Income' END AS rising_operating_income,
    CASE WHEN ld.revenue > pd.revenue THEN 'Revenue Growth' END AS revenue_growth,
    
    -- Count Red Flags
    (CASE WHEN ld.grossProfitRatio < pd.grossProfitRatio THEN 1 ELSE 0 END +
     CASE WHEN ld.sellingGeneralAndAdministrativeExpenses > pd.sellingGeneralAndAdministrativeExpenses THEN 1 ELSE 0 END +
     CASE WHEN ld.interestExpense > pd.interestExpense THEN 1 ELSE 0 END) AS red_flag_count,
    
    -- Count Green Flags
    (CASE WHEN ld.ebitdaratio > pd.ebitdaratio THEN 1 ELSE 0 END +
     CASE WHEN ld.operatingIncome > pd.operatingIncome THEN 1 ELSE 0 END +
     CASE WHEN ld.revenue > pd.revenue THEN 1 ELSE 0 END) AS green_flag_count
    
FROM latest_data AS ld
JOIN previous_year_data AS pd
ON
	ld.symbol = pd.symbol
;

-- Insert final count column
ALTER TABLE pnl_analysis
ADD COLUMN pnl_final_count INT;

UPDATE pnl_analysis
SET pnl_final_count = green_flag_count - red_flag_count;

SELECT *
FROM pnl_analysis
;

