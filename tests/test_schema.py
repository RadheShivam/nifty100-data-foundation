import sqlite3


def test_companies_table_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='companies'"
    )

    assert cursor.fetchone() is not None

    conn.close()


def test_profitandloss_table_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='profitandloss'"
    )

    assert cursor.fetchone() is not None

    conn.close()


def test_balancesheet_table_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='balancesheet'"
    )

    assert cursor.fetchone() is not None

    conn.close()


def test_cashflow_table_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='cashflow'"
    )

    assert cursor.fetchone() is not None

    conn.close()


def test_marketcap_table_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='marketcap'
    """)

    assert cursor.fetchone() is not None

    conn.close()


def test_stockprices_table_exists():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='stockprices'
    """)

    assert cursor.fetchone() is not None

    conn.close()

    