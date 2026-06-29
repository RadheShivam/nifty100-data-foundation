import sqlite3
import pandas as pd

from src.analytics.ratios import return_on_equity

conn = sqlite3.connect("db/nifty100.db")

profit = pd.read_sql("""
SELECT
company_id,
year,
net_profit
FROM profitandloss
""", conn)

balance = pd.read_sql("""
SELECT
company_id,
year,
equity_capital,
reserves
FROM balancesheet
""", conn)

companies = pd.read_sql("""
SELECT
id,
company_name,
roe_percentage
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

    roe = return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    )

    if roe is None:
        continue

    if pd.isna(row["roe_percentage"]):
        continue

    difference = abs(roe - row["roe_percentage"])

    if difference > 5:

        log.append([
            row["company_name"],
            row["year"],
            round(roe, 2),
            row["roe_percentage"],
            round(difference, 2)
        ])

log_df = pd.DataFrame(
    log,
    columns=[
        "Company",
        "Year",
        "Computed ROE",
        "Source ROE",
        "Difference"
    ]
)

log_df.to_csv(
    "output/roe_edge_cases.csv",
    index=False
)

print(log_df.head())
print()
print("Total ROE anomalies:", len(log_df))