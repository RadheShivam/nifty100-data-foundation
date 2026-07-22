import sqlite3
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

DB_PATH = os.path.join(
    PROJECT_ROOT,
    "db",
    "nifty100.db"
)


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watchlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watchlist_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        watchlist_id INTEGER NOT NULL,
        company_id TEXT NOT NULL,

        FOREIGN KEY (watchlist_id)
            REFERENCES watchlists(id),

        FOREIGN KEY (company_id)
            REFERENCES companies(id)
    )
    """)

    conn.commit()

    print("✅ Watchlist tables created successfully!")

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """)

    print("\nTables:\n")

    for table in cursor.fetchall():
        print(table[0])

    conn.close()


if __name__ == "__main__":
    create_tables()