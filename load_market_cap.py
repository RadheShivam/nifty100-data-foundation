import sqlite3
import pandas as pd

# Read Excel
df = pd.read_excel("data/supplementry/market_cap.xlsx")

# Connect SQLite
conn = sqlite3.connect("db/nifty100.db")

# Save as table
df.to_sql("marketcap", conn, if_exists="replace", index=False)

conn.close()

print("✅ market_cap table created")

print(df.head())
