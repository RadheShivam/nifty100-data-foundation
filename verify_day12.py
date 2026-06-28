import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    p.company_id,
    p.year,
    p.net_profit,
    b.equity_capital,
    b.reserves,
    p.sales,
    f.return_on_equity_pct,
    f.revenue_cagr_5yr
FROM profitandloss p
JOIN balancesheet b
    ON p.company_id = b.company_id
   AND p.year = b.year
JOIN financial_ratios f
    ON p.company_id = f.company_id
   AND p.year = f.year
WHERE p.company_id IN ('TCS','INFY','RELIANCE')
ORDER BY p.company_id, p.year;
"""

df = pd.read_sql(query, conn)

conn.close()

print(df.head(20))