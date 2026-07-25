from fastapi import APIRouter, Query
import sqlite3
import os

router = APIRouter(prefix="/screener", tags=["Screener"])

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

DB_PATH = os.path.join(PROJECT_ROOT, "db", "nifty100.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/")
def screener(min_roe: float | None = Query(default=None)):

    conn = get_connection()

    query = """
    SELECT
        id,
        company_name,
        roe_percentage,
        roce_percentage
    FROM companies
    WHERE 1=1
    """

    params = []

    if min_roe is not None:
        query += " AND roe_percentage >= ? "
        params.append(min_roe)

    query += " ORDER BY company_name "

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]
