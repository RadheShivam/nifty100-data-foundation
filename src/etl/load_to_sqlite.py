import sqlite3
import pandas as pd
from src.etl.loader import *


def create_database():
    conn = sqlite3.connect("db/nifty100.db")

    with open("db/schema.sql", "r") as f:
        schema = f.read()

    conn.executescript(schema)

    conn.commit()
    conn.close()

    print("✅ Database and tables created successfully")


def load_data_to_sqlite():
    conn = sqlite3.connect("db/nifty100.db")

    # Core tables
    companies_df = load_companies()
    profit_df = load_profitandloss()
    balance_df = load_balancesheet()
    cashflow_df = load_cashflow()
    analysis_df = load_analysis()
    documents_df = load_documents()
    pros_df = load_prosandcons()
    sectors_df = load_sectors()

    # Supplementary tables
    marketcap_df = pd.read_excel(
        "data/supplementry/market_cap.xlsx"
    )

    stockprices_df = pd.read_excel(
        "data/supplementry/stock_prices.xlsx"
    )

    # Debug columns
    print("\nCompanies columns:")
    print(companies_df.columns.tolist())

    print("\nProfit & Loss columns:")
    print(profit_df.columns.tolist())

    print("\nBalance Sheet columns:")
    print(balance_df.columns.tolist())

    print("\nCash Flow columns:")
    print(cashflow_df.columns.tolist())

    print("\nAnalysis columns:")
    print(analysis_df.columns.tolist())

    print("\nMarket Cap columns:")
    print(marketcap_df.columns.tolist())

    print("\nStock Prices columns:")
    print(stockprices_df.columns.tolist())

    # Load core tables
    companies_df.to_sql(
        "companies",
        conn,
        if_exists="append",
        index=False
    )

    profit_df.to_sql(
        "profitandloss",
        conn,
        if_exists="append",
        index=False
    )

    balance_df.to_sql(
        "balancesheet",
        conn,
        if_exists="append",
        index=False
    )

    cashflow_df.to_sql(
        "cashflow",
        conn,
        if_exists="append",
        index=False
    )

    analysis_df.to_sql(
        "analysis",
        conn,
        if_exists="append",
        index=False
    )

    documents_df.to_sql(
        "documents",
        conn,
        if_exists="append",
        index=False
    )

    pros_df.to_sql(
        "prosandcons",
        conn,
        if_exists="append",
        index=False
    )

    sectors_df.to_sql(
        "sectors",
        conn,
        if_exists="append",
        index=False
    )

    # Load supplementary tables
    marketcap_df.to_sql(
        "marketcap",
        conn,
        if_exists="append",
        index=False
    )

    stockprices_df.to_sql(
        "stockprices",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()
    conn.close()

    print("\n✅ Data loaded successfully")