# from src.etl.load_to_sqlite import create_database

# create_database()

# import sqlite3

# conn = sqlite3.connect("db/nifty100.db")

# cursor = conn.cursor()

# cursor.execute("""
# SELECT name
# FROM sqlite_master
# WHERE type='table'
# """)

# tables = cursor.fetchall()

# print(tables)

# conn.close()


# from src.etl.load_to_sqlite import *

# create_database()
# load_data_to_sqlite()



# # import sqlite3

# # conn = sqlite3.connect("db/nifty100.db")

# # cursor = conn.cursor()

# # tables = [
# #     "companies",
# #     "profitandloss",
# #     "balancesheet",
# #     "cashflow",
# #     "analysis",
# #     "documents",
# #     "prosandcons",
# #     "sectors"
# # ]

# # for table in tables:
# #     cursor.execute(f"SELECT COUNT(*) FROM {table}")
# #     count = cursor.fetchone()[0]
# #     print(f"{table}: {count}")

# # conn.close()



# import sqlite3

# conn = sqlite3.connect("db/nifty100.db")

# cursor = conn.cursor()

# cursor.execute(
#     "PRAGMA foreign_key_check;"
# )

# violations = cursor.fetchall()

# print(violations)

# conn.close()







