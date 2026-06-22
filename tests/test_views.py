import sqlite3


def test_vw_top_sales_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='view'
        AND name='vw_top_sales'
    """)

    assert cursor.fetchone() is not None

    conn.close()


def test_vw_top_roe_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='view'
        AND name='vw_top_roe'
    """)

    assert cursor.fetchone() is not None

    conn.close()


def test_vw_sector_distribution_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='view'
        AND name='vw_sector_distribution'
    """)

    assert cursor.fetchone() is not None

    conn.close()