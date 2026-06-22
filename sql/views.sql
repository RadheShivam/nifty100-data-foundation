CREATE VIEW IF NOT EXISTS vw_top_sales AS
SELECT
    company_id,
    sales
FROM profitandloss
WHERE year='Mar 2024'
ORDER BY sales DESC
LIMIT 10;


CREATE VIEW IF NOT EXISTS vw_top_roe AS
SELECT
    company_id,
    roe
FROM analysis
ORDER BY roe DESC
LIMIT 10;


CREATE VIEW IF NOT EXISTS vw_sector_distribution AS
SELECT
    broad_sector,
    COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;