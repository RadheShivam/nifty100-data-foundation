import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

balance_df = pd.read_sql(
    "SELECT * FROM balancesheet LIMIT 5",
    conn
)

conn.close()

print(balance_df.columns.tolist())
print(balance_df.head())