from fastapi import APIRouter
import sqlite3
import os
import time

router = APIRouter(prefix="/health", tags=["Health"])

# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

DB_PATH = os.path.join(PROJECT_ROOT, "db", "nifty100.db")

API_START_TIME = time.time()

# ==========================================================
# DATABASE CONNECTION
# ==========================================================


def get_connection():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================================
# HEALTH ENDPOINT
# ==========================================================


@router.get("/")
def health():
    """
    Health check endpoint.

    Returns:
        dict: API status information.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
        """)

    tables = [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]

    row_counts = {}

    for table in tables:

        try:

            cursor.execute(f"SELECT COUNT(*) FROM {table}")

            row_counts[table] = cursor.fetchone()[0]

        except Exception:

            row_counts[table] = "Error"

    conn.close()

    return {
        "status": "ok",
        "db_row_counts": row_counts,
        "uptime_seconds": round(time.time() - API_START_TIME, 2),
        "version": "1.0.0",
    }
