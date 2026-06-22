# import sqlite3


# def create_database():
#     conn = sqlite3.connect("db/nifty100.db")

#     with open("db/schema.sql", "r") as f:
#         schema = f.read()

#     conn.executescript(schema)

#     conn.commit()
#     conn.close()

#     print("✅ Database and tables created successfully")


# import sqlite3
# from src.etl.loader import *


# def load_data_to_sqlite():
#     conn = sqlite3.connect("db/nifty100.db")

#     companies_df = load_companies()
#     profit_df = load_profitandloss()
#     balance_df = load_balancesheet()
#     cashflow_df = load_cashflow()
#     analysis_df = load_analysis()
#     documents_df = load_documents()
#     pros_df = load_prosandcons()
#     sectors_df = load_sectors()

#     companies_df.to_sql(
#         "companies",
#         conn,
#         if_exists="append",
#         index=False
#     )

#     profit_df.to_sql(
#         "profitandloss",
#         conn,
#         if_exists="append",
#         index=False
#     )

#     balance_df.to_sql(
#         "balancesheet",
#         conn,
#         if_exists="append",
#         index=False
#     )

#     cashflow_df.to_sql(
#         "cashflow",
#         conn,
#         if_exists="append",
#         index=False
#     )

#     analysis_df.to_sql(
#         "analysis",
#         conn,
#         if_exists="append",
#         index=False
#     )

#     documents_df.to_sql(
#         "documents",
#         conn,
#         if_exists="append",
#         index=False
#     )

#     pros_df.to_sql(
#         "prosandcons",
#         conn,
#         if_exists="append",
#         index=False
#     )

#     sectors_df.to_sql(
#         "sectors",
#         conn,
#         if_exists="append",
#         index=False
#     )

#     conn.commit()
#     conn.close()

#     print("✅ Data loaded successfully")



import sqlite3
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

    companies_df = load_companies()
    profit_df = load_profitandloss()
    balance_df = load_balancesheet()
    cashflow_df = load_cashflow()
    analysis_df = load_analysis()
    documents_df = load_documents()
    pros_df = load_prosandcons()
    sectors_df = load_sectors()

    companies_df.to_sql("companies", conn, if_exists="append", index=False)
    profit_df.to_sql("profitandloss", conn, if_exists="append", index=False)
    balance_df.to_sql("balancesheet", conn, if_exists="append", index=False)
    cashflow_df.to_sql("cashflow", conn, if_exists="append", index=False)
    analysis_df.to_sql("analysis", conn, if_exists="append", index=False)
    documents_df.to_sql("documents", conn, if_exists="append", index=False)
    pros_df.to_sql("prosandcons", conn, if_exists="append", index=False)
    sectors_df.to_sql("sectors", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()

    print("✅ Data loaded successfully")