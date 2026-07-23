from fastapi import APIRouter, HTTPException
import sqlite3
import os

router = APIRouter(prefix="/sectors", tags=["Sectors"])

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

DB_PATH = os.path.join(PROJECT_ROOT, "db", "nifty100.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/")
def get_sectors():

    conn = get_connection()

    rows = conn.execute("""
        SELECT DISTINCT broad_sector
        FROM sectors
        ORDER BY broad_sector
    """).fetchall()

    conn.close()

    return [row["broad_sector"] for row in rows]


@router.get("/{sector}")
def get_sector_companies(sector: str):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            c.id,
            c.company_name,
            s.broad_sector
        FROM companies c
        JOIN sectors s
            ON c.id = s.company_id
        WHERE UPPER(s.broad_sector)=UPPER(?)
        ORDER BY c.company_name
    """,
        (sector,),
    ).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Sector not found")

    result = []

    for row in rows:
        item = dict(row)
        item["sector"] = item.pop("broad_sector")
        result.append(item)

    return result
