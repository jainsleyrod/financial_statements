CREATE TABLE final_analysis AS
SELECT 
    pnl.symbol,
    pnl.pnl_final_count AS pnl_final_count,
    bs.bs_final_count AS bs_final_count,
    cf.cf_final_count AS cash_final_count,

    -- Calculate total final count by summing individual final counts
    (COALESCE(pnl.pnl_final_count, 0) +
     COALESCE(bs.bs_final_count, 0) +
     COALESCE(cf.cf_final_count, 0)) AS total_final_count

FROM pnl_analysis pnl
JOIN bs_analysis bs ON pnl.symbol = bs.symbol
JOIN cf_analysis cf ON pnl.symbol = cf.symbol
;

SELECT * FROM final_analysis;