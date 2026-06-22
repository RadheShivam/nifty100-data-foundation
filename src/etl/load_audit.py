import sqlite3
import pandas as pd


def generate_load_audit():
    conn = sqlite3.connect("db/nifty100.db")

    tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "sectors"
    ]

    data = []

    cursor = conn.cursor()

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")

        count = cursor.fetchone()[0]

        data.append({
            "table_name": table,
            "row_count": count
        })

    audit_df = pd.DataFrame(data)

    audit_df.to_csv(
        "output/load_audit.csv",
        index=False
    )

    conn.close()

    print("✅ load_audit.csv created")