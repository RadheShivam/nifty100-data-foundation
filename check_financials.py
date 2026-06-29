import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    c.company_name,
    s.broad_sector
FROM companies c
JOIN sectors s
ON c.id = s.company_id
WHERE s.broad_sector = 'Financials'
ORDER BY c.company_name;
"""

df = pd.read_sql(query, conn)

conn.close()

print(df)
print()
print("Total Financial Companies:", len(df))