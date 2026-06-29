import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT *
FROM financial_ratios
WHERE company_id IN (
    'TCS',
    'INFY',
    'RELIANCE',
    'ITC',
    'HDFCBANK'
)
ORDER BY company_id, year DESC;
"""

df = pd.read_sql(query, conn)

conn.close()

print(df)