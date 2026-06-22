import sqlite3
import os


def test_database_exists():
    assert os.path.exists("db/nifty100.db")


def test_companies_row_count():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM companies")
    count = cursor.fetchone()[0]

    assert count == 92

    conn.close()


def test_profitandloss_row_count():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM profitandloss")
    count = cursor.fetchone()[0]

    assert count == 1276

    conn.close()


def test_balancesheet_row_count():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM balancesheet")
    count = cursor.fetchone()[0]

    assert count == 1312

    conn.close()


def test_cashflow_row_count():
    conn = sqlite3.connect("db/nifty100.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cashflow")
    count = cursor.fetchone()[0]

    assert count == 1187

    conn.close()