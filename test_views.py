import sqlite3

conn = sqlite3.connect("db/nifty100.db")

with open("sql/views.sql", "r") as f:
    conn.executescript(f.read())

conn.commit()

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='view'
""")

print(cursor.fetchall())

conn.close()