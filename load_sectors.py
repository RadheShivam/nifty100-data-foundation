import sqlite3
import pandas as pd

# Read Excel
df = pd.read_excel("data/supplementry/sectors.xlsx")

# Connect database
conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

# Clear old data
cursor.execute("DELETE FROM sectors")

# Insert rows
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO sectors (
            id,
            company_id,
            broad_sector,
            sub_sector,
            index_weight_pct,
            market_cap_category
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        int(row["id"]),
        row["company_id"],
        row["broad_sector"],
        row["sub_sector"],
        row["index_weight_pct"],
        row["market_cap_category"]
    ))

conn.commit()

count = cursor.execute(
    "SELECT COUNT(*) FROM sectors"
).fetchone()[0]

print(f"✅ Loaded {count} sector records.")

conn.close()