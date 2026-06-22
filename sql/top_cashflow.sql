SELECT
    company_id,
    net_cash_flow
FROM cashflow
WHERE year='Mar 2024'
ORDER BY net_cash_flow DESC
LIMIT 10;