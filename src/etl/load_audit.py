import sqlite3
import pandas as pd
import os


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
        "sectors",
        "marketcap",
        "stockprices",
        "financial_ratios",
        "peer_percentiles"
    ]

    audit = []

    for table in tables:

        try:

            count = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            audit.append({
                "table_name": table,
                "row_count": count
            })

        except Exception:

            audit.append({
                "table_name": table,
                "row_count": 0
            })

    conn.close()

    audit_df = pd.DataFrame(audit)

    os.makedirs(
        "output",
        exist_ok=True
    )

    audit_df.to_csv(
        "output/load_audit.csv",
        index=False
    )

    print("✅ load_audit.csv created")

    print(audit_df)


if __name__ == "__main__":
    generate_load_audit()