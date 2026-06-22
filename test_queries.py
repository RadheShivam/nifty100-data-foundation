import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    company_id,
    sales
FROM profitandloss
WHERE year='Mar 2024'
ORDER BY sales DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()