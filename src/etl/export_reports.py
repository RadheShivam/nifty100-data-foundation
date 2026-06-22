import sqlite3
import pandas as pd


def export_reports():
    conn = sqlite3.connect("db/nifty100.db")

    queries = {
        "top_sales": """
        SELECT company_id, sales
        FROM profitandloss
        WHERE year='Mar 2024'
        ORDER BY sales DESC
        LIMIT 10
        """,

        "top_roe": """
        SELECT company_id, roe
        FROM analysis
        ORDER BY roe DESC
        LIMIT 10
        """,

        "sector_distribution": """
        SELECT broad_sector,
               COUNT(*) AS company_count
        FROM sectors
        GROUP BY broad_sector
        ORDER BY company_count DESC
        """
    }

    for name, query in queries.items():
        df = pd.read_sql(query, conn)
        df.to_csv(
            f"output/{name}.csv",
            index=False
        )

        print(f"✅ output/{name}.csv created")

    conn.close()