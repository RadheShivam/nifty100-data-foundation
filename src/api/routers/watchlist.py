from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
import os

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

DB_PATH = os.path.join(PROJECT_ROOT, "db", "nifty100.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================================
# REQUEST MODEL
# ==========================================================


class WatchlistCreate(BaseModel):
    name: str


# ==========================================================
# CREATE WATCHLIST
# ==========================================================


@router.post("/")
def create_watchlist(data: WatchlistCreate):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO watchlists(name)
        VALUES(?)
        """,
        (data.name,),
    )

    conn.commit()

    watchlist_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Watchlist created successfully",
        "watchlist_id": watchlist_id,
        "name": data.name,
    }


# ==========================================================
# GET ALL WATCHLISTS
# ==========================================================


@router.get("/")
def get_watchlists():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id,
            name,
            created_at
        FROM watchlists
        ORDER BY id
        """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# REQUEST MODEL - WATCHLIST ITEM
# ==========================================================


class WatchlistItemCreate(BaseModel):
    company_id: str


# ==========================================================
# ADD STOCK TO WATCHLIST
# ==========================================================


@router.post("/{watchlist_id}/stocks")
def add_stock(watchlist_id: int, item: WatchlistItemCreate):

    conn = get_connection()
    cursor = conn.cursor()

    # Check watchlist exists
    watchlist = cursor.execute(
        """
        SELECT id
        FROM watchlists
        WHERE id = ?
        """,
        (watchlist_id,),
    ).fetchone()

    if watchlist is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Watchlist not found")

    # Check company exists
    company = cursor.execute(
        """
        SELECT id
        FROM companies
        WHERE UPPER(id)=UPPER(?)
        """,
        (item.company_id,),
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    # Prevent duplicate entries
    existing = cursor.execute(
        """
        SELECT id
        FROM watchlist_items
        WHERE watchlist_id = ?
        AND company_id = ?
        """,
        (watchlist_id, item.company_id.upper()),
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=400, detail="Company already exists in watchlist"
        )

    cursor.execute(
        """
        INSERT INTO watchlist_items
        (
            watchlist_id,
            company_id
        )
        VALUES (?, ?)
        """,
        (watchlist_id, item.company_id.upper()),
    )

    conn.commit()

    item_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Stock added successfully",
        "item_id": item_id,
        "watchlist_id": watchlist_id,
        "company_id": item.company_id.upper(),
    }


# ==========================================================
# GET WATCHLIST DETAILS
# ==========================================================


@router.get("/{watchlist_id}")
def get_watchlist(watchlist_id: int):

    conn = get_connection()

    # Check watchlist exists
    watchlist = conn.execute(
        """
        SELECT *
        FROM watchlists
        WHERE id = ?
        """,
        (watchlist_id,),
    ).fetchone()

    if watchlist is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Watchlist not found")

    stocks = conn.execute(
        """
        SELECT
            wi.id,
            wi.company_id,
            c.company_name,
            c.website,
            c.roce_percentage,
            c.roe_percentage
        FROM watchlist_items wi
        JOIN companies c
            ON wi.company_id = c.id
        WHERE wi.watchlist_id = ?
        ORDER BY c.company_name
        """,
        (watchlist_id,),
    ).fetchall()

    conn.close()

    return {"watchlist": dict(watchlist), "stocks": [dict(stock) for stock in stocks]}


# ==========================================================
# REMOVE STOCK FROM WATCHLIST
# ==========================================================


@router.delete("/{watchlist_id}/stocks/{company_id}")
def remove_stock(watchlist_id: int, company_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    # Check watchlist exists
    watchlist = cursor.execute(
        """
        SELECT id
        FROM watchlists
        WHERE id = ?
        """,
        (watchlist_id,),
    ).fetchone()

    if watchlist is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Watchlist not found")

    # Check stock exists in watchlist
    stock = cursor.execute(
        """
        SELECT id
        FROM watchlist_items
        WHERE watchlist_id = ?
        AND company_id = ?
        """,
        (watchlist_id, company_id.upper()),
    ).fetchone()

    if stock is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Stock not found in watchlist")

    cursor.execute(
        """
        DELETE FROM watchlist_items
        WHERE watchlist_id = ?
        AND company_id = ?
        """,
        (watchlist_id, company_id.upper()),
    )

    conn.commit()

    conn.close()

    return {
        "message": "Stock removed successfully",
        "watchlist_id": watchlist_id,
        "company_id": company_id.upper(),
    }
