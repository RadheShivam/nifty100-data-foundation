import sqlite3
import pandas as pd
import os

from src.analytics.ratios import return_on_capital_employed

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")

profit = pd.read_sql("""
SELECT
    company_id,
    year,
    operating_profit,
    depreciation
FROM profitandloss
""", conn)

balance = pd.read_sql("""
SELECT
    company_id,
    year,
    equity_capital,
    reserves,
    borrowings
FROM balancesheet
""", conn)

companies = pd.read_sql("""
SELECT
    id,
    company_name,
    roce_percentage
FROM companies
""", conn)

conn.close()

df = profit.merge(
    balance,
    on=["company_id", "year"]
)

df = df.merge(
    companies,
    left_on="company_id",
    right_on="id"
)

log = []

for _, row in df.iterrows():

    ebit = row["operating_profit"] + row["depreciation"]

    roce, _ = return_on_capital_employed(
        ebit,
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    )

    if roce is None:
        continue

    source = row["roce_percentage"]

    if pd.isna(source):
        continue

    difference = abs(roce - source)

    if difference > 5:

        if difference > 20:
            category = "Data source issue"
        elif difference > 10:
            category = "Version difference"
        else:
            category = "Formula discrepancy"

        log.append([
            row["company_name"],
            row["year"],
            round(roce, 2),
            source,
            round(difference, 2),
            category
        ])

log_df = pd.DataFrame(
    log,
    columns=[
        "Company",
        "Year",
        "Computed ROCE",
        "Source ROCE",
        "Difference",
        "Category"
    ]
)

log_df.to_csv(
    "output/ratio_edge_cases.log",
    index=False
)

print(log_df.head())
print()
print("Total anomalies:", len(log_df))