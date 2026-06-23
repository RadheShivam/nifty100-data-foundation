import sqlite3


def test_companies_not_empty():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM companies")
    count = cursor.fetchone()[0]

    assert count > 0

    conn.close()


def test_profitandloss_not_empty():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM profitandloss")
    count = cursor.fetchone()[0]

    assert count > 0

    conn.close()


def test_balancesheet_not_empty():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM balancesheet")
    count = cursor.fetchone()[0]

    assert count > 0

    conn.close()


def test_cashflow_not_empty():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cashflow")
    count = cursor.fetchone()[0]

    assert count > 0

    conn.close()


def test_marketcap_not_empty():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM marketcap")

    assert cursor.fetchone()[0] > 0

    conn.close()


def test_stockprices_not_empty():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM stockprices")

    assert cursor.fetchone()[0] > 0

    conn.close()