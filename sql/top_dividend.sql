SELECT
    company_id,
    dividend_payout
FROM profitandloss
WHERE year='Mar 2024'
ORDER BY dividend_payout DESC
LIMIT 10;