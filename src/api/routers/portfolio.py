from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3
import os

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

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


class PortfolioCreate(BaseModel):
    name: str


# ==========================================================
# CREATE PORTFOLIO
# ==========================================================


@router.post("/")
def create_portfolio(data: PortfolioCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO portfolios(name)
        VALUES(?)
        """,
        (data.name,),
    )

    conn.commit()

    portfolio_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Portfolio created successfully",
        "portfolio_id": portfolio_id,
        "name": data.name,
    }


# ==========================================================
# GET ALL PORTFOLIOS
# ==========================================================


@router.get("/")
def get_portfolios():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id,
            name,
            created_at
        FROM portfolios
        ORDER BY id
        """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# REQUEST MODEL - HOLDINGS
# ==========================================================


class HoldingCreate(BaseModel):
    company_id: str
    quantity: float
    average_price: float


# ==========================================================
# ADD HOLDING TO PORTFOLIO
# ==========================================================


@router.post("/{portfolio_id}/holdings")
def add_holding(portfolio_id: int, holding: HoldingCreate):

    conn = get_connection()
    cursor = conn.cursor()

    # Check portfolio exists
    portfolio = cursor.execute(
        """
        SELECT id
        FROM portfolios
        WHERE id = ?
        """,
        (portfolio_id,),
    ).fetchone()

    if portfolio is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Check company exists
    company = cursor.execute(
        """
        SELECT id
        FROM companies
        WHERE UPPER(id)=UPPER(?)
        """,
        (holding.company_id,),
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    cursor.execute(
        """
        INSERT INTO portfolio_holdings
        (
            portfolio_id,
            company_id,
            quantity,
            average_price
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            portfolio_id,
            holding.company_id.upper(),
            holding.quantity,
            holding.average_price,
        ),
    )

    conn.commit()

    holding_id = cursor.lastrowid

    conn.close()

    return {
        "message": "Holding added successfully",
        "holding_id": holding_id,
        "portfolio_id": portfolio_id,
        "company_id": holding.company_id.upper(),
        "quantity": holding.quantity,
        "average_price": holding.average_price,
    }


# ==========================================================
# GET PORTFOLIO DETAILS
# ==========================================================


@router.get("/{portfolio_id}")
def get_portfolio(portfolio_id: int):

    conn = get_connection()

    # Check portfolio exists
    portfolio = conn.execute(
        """
        SELECT *
        FROM portfolios
        WHERE id = ?
        """,
        (portfolio_id,),
    ).fetchone()

    if portfolio is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Get all holdings
    holdings = conn.execute(
        """
        SELECT
            ph.id,
            ph.company_id,
            c.company_name,
            ph.quantity,
            ph.average_price
        FROM portfolio_holdings ph
        JOIN companies c
            ON ph.company_id = c.id
        WHERE ph.portfolio_id = ?
        ORDER BY c.company_name
        """,
        (portfolio_id,),
    ).fetchall()

    conn.close()

    return {"portfolio": dict(portfolio), "holdings": [dict(row) for row in holdings]}


# ==========================================================
# PORTFOLIO SUMMARY
# ==========================================================


@router.get("/{portfolio_id}/summary")
def get_portfolio_summary(portfolio_id: int):

    conn = get_connection()

    # Check portfolio exists
    portfolio = conn.execute(
        """
        SELECT *
        FROM portfolios
        WHERE id = ?
        """,
        (portfolio_id,),
    ).fetchone()

    if portfolio is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Portfolio not found")

    holdings = conn.execute(
        """
        SELECT
            ph.company_id,
            ph.quantity,
            ph.average_price,
            sp.close_price
        FROM portfolio_holdings ph
        LEFT JOIN stock_prices sp
            ON ph.company_id = sp.company_id
        WHERE ph.portfolio_id = ?
        """,
        (portfolio_id,),
    ).fetchall()

    total_investment = 0
    current_value = 0

    for row in holdings:

        investment = row["quantity"] * row["average_price"]

        current_price = row["close_price"] if row["close_price"] else 0

        value = row["quantity"] * current_price

        total_investment += investment
        current_value += value

    profit_loss = current_value - total_investment

    return_percent = 0

    if total_investment > 0:
        return_percent = (profit_loss / total_investment) * 100

    conn.close()

    return {
        "portfolio_id": portfolio_id,
        "total_investment": round(total_investment, 2),
        "current_value": round(current_value, 2),
        "profit_loss": round(profit_loss, 2),
        "return_percentage": round(return_percent, 2),
    }


# ==========================================================
# PORTFOLIO ALLOCATION
# ==========================================================


@router.get("/{portfolio_id}/allocation")
def get_portfolio_allocation(portfolio_id: int):

    conn = get_connection()

    portfolio = conn.execute(
        """
        SELECT id
        FROM portfolios
        WHERE id = ?
        """,
        (portfolio_id,),
    ).fetchone()

    if portfolio is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Portfolio not found")

    rows = conn.execute(
        """
        SELECT
            ph.company_id,
            c.company_name,
            ph.quantity,
            ph.average_price,
            (ph.quantity * ph.average_price) AS investment
        FROM portfolio_holdings ph
        JOIN companies c
            ON ph.company_id = c.id
        WHERE ph.portfolio_id = ?
        ORDER BY investment DESC
        """,
        (portfolio_id,),
    ).fetchall()

    total = sum(row["investment"] for row in rows)

    allocation = []

    for row in rows:

        percent = 0

        if total > 0:
            percent = (row["investment"] / total) * 100

        allocation.append(
            {
                "company_id": row["company_id"],
                "company_name": row["company_name"],
                "investment": round(row["investment"], 2),
                "allocation_percentage": round(percent, 2),
            }
        )

    conn.close()

    return {
        "portfolio_id": portfolio_id,
        "total_investment": round(total, 2),
        "allocation": allocation,
    }


# ==========================================================
# TEST ROUTE
# ==========================================================


@router.get("/")
def get_portfolios():
    return {"message": "Portfolio API is working"}
