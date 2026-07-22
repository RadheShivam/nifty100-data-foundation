import sqlite3
import os

# Project root
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

    # Create portfolios table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create portfolio holdings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio_holdings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        portfolio_id INTEGER NOT NULL,
        company_id TEXT NOT NULL,
        quantity REAL NOT NULL,
        average_price REAL NOT NULL,

        FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
        FOREIGN KEY (company_id) REFERENCES companies(id)
    )
    """)

    conn.commit()

    print("✅ Portfolio tables created successfully!")

    # Verify tables
    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """)

    print("\nTables in database:\n")

    for table in cursor.fetchall():
        print(table[0])

    conn.close()


if __name__ == "__main__":
    create_tables()