import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    c.company_name,
    s.broad_sector,
    f.debt_to_equity
FROM financial_ratios f
JOIN companies c
ON f.company_id = c.id
JOIN sectors s
ON c.id = s.company_id
ORDER BY company_name;
"""

df = pd.read_sql(query, conn)

conn.close()

df["high_leverage_flag"] = (
    (df["debt_to_equity"] > 5) &
    (df["broad_sector"] != "Financials")
)

print(df.head(20))