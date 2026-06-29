import sqlite3
import pandas as pd

from src.analytics.ratios import return_on_capital_employed

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

print(df.head())
print()
print("Rows:", len(df))