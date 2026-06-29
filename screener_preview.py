import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    f.company_id,
    f.year,
    f.return_on_equity_pct,
    f.debt_to_equity
FROM financial_ratios f
JOIN (
    SELECT
        company_id,
        MAX(year) AS latest_year
    FROM financial_ratios
    GROUP BY company_id
) latest
ON f.company_id = latest.company_id
AND f.year = latest.latest_year
WHERE
    f.return_on_equity_pct > 15
    AND f.debt_to_equity < 1
ORDER BY
    f.return_on_equity_pct DESC;
"""

df = pd.read_sql(query, conn)

conn.close()

print(df)

print("\n----------------------------")
print("Companies found :", df["company_id"].nunique())
print("Rows found      :", len(df))
print("----------------------------")