import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

tables = cursor.fetchall()

print(tables)
print("Total tables:", len(tables))

conn.close()