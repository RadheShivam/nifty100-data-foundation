import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

# Top Sales View
cursor.execute("""
CREATE VIEW IF NOT EXISTS vw_top_sales AS
SELECT company_id, sales
FROM profitandloss
WHERE year='Mar 2024'
ORDER BY sales DESC
LIMIT 10
""")

# Top ROE View
cursor.execute("""
CREATE VIEW IF NOT EXISTS vw_top_roe AS
SELECT company_id, roe
FROM analysis
ORDER BY roe DESC
LIMIT 10
""")

# Sector Distribution View
cursor.execute("""
CREATE VIEW IF NOT EXISTS vw_sector_distribution AS
SELECT broad_sector,
       COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
""")

conn.commit()
conn.close()

print("✅ Views created successfully")