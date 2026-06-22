import sqlite3
import pandas as pd


def generate_kpi_summary():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    tables = {
        "Total Companies": "companies",
        "Total Profit Records": "profitandloss",
        "Total Balance Sheet Records": "balancesheet",
        "Total Cash Flow Records": "cashflow",
        "Total Analysis Records": "analysis",
        "Total Documents": "documents",
        "Total Pros & Cons Records": "prosandcons",
        "Total Sectors": "sectors"
    }

    data = []

    for kpi, table in tables.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]

        data.append({
            "KPI": kpi,
            "Value": count
        })

    kpi_df = pd.DataFrame(data)

    kpi_df.to_csv(
        "output/kpi_summary.csv",
        index=False
    )

    conn.close()

    print("✅ kpi_summary.csv created")