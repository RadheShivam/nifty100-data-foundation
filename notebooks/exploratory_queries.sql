-- 1 Top Sales Companies
SELECT company_id, sales
FROM profitandloss
WHERE year='Mar 2024'
ORDER BY sales DESC
LIMIT 10;

-- 2 Top ROE Companies
SELECT company_id, roe
FROM analysis
ORDER BY roe DESC
LIMIT 10;

-- 3 Top Cash Flow Companies
SELECT company_id, net_cash_flow
FROM cashflow
WHERE year='Mar 2024'
ORDER BY net_cash_flow DESC
LIMIT 10;

-- 4 Top Dividend Companies
SELECT company_id, dividend_payout
FROM profitandloss
WHERE year='Mar 2024'
ORDER BY dividend_payout DESC
LIMIT 10;

-- 5 Sector Distribution
SELECT broad_sector, COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector;

-- 6 Highest Net Profit
SELECT company_id, net_profit
FROM profitandloss
WHERE year='Mar 2024'
ORDER BY net_profit DESC
LIMIT 10;

-- 7 Highest EPS
SELECT company_id, eps
FROM profitandloss
WHERE year='Mar 2024'
ORDER BY eps DESC
LIMIT 10;

-- 8 Average ROE
SELECT AVG(roe) AS avg_roe
FROM analysis;

-- 9 Highest Sales Growth
SELECT company_id, compounded_sales_growth
FROM analysis
ORDER BY compounded_sales_growth DESC
LIMIT 10;

-- 10 Highest OPM
SELECT company_id, opm_percentage
FROM profitandloss
WHERE year='Mar 2024'
ORDER BY opm_percentage DESC
LIMIT 10;