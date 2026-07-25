from fastapi import APIRouter, Query, HTTPException
import sqlite3
import os

router = APIRouter(prefix="/companies", tags=["Companies"])

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
# GET ALL COMPANIES
# ==========================================================


@router.get("/")
def get_companies(
    search: str | None = Query(default=None),
    sector: str | None = Query(default=None),
    market_cap_category: str | None = Query(default=None),
):

    conn = get_connection()

    query = """
    SELECT
        id,
        company_name,
        broad_sector,
        sub_sector,
        roe_percentage,
        roce_percentage,
        market_cap_category,
        website,
        company_logo
    FROM companies
    WHERE 1=1
    """

    params = []

    if search:
        query += """
        AND (
            company_name LIKE ?
            OR id LIKE ?
        )
        """
        params.extend([f"%{search}%", f"%{search}%"])

    if sector:
        query += """
        AND broad_sector = ?
        """
        params.append(sector)

    if market_cap_category:
        query += """
        AND market_cap_category = ?
        """
        params.append(market_cap_category)

    query += """
    ORDER BY company_name
    """

    rows = conn.execute(query, params).fetchall()
    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# GET PROFIT & LOSS HISTORY
# ==========================================================


@router.get("/{ticker}/pl")
def get_profit_loss(
    ticker: str,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):

    conn = get_connection()

    company = conn.execute(
        """
        SELECT id
        FROM companies
        WHERE UPPER(id)=UPPER(?)
        """,
        (ticker,),
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id = ?
    """

    params = [ticker]

    if from_year:
        query += """
        AND (
            year='TTM'
            OR CAST(substr(year,-4) AS INTEGER) >= ?
        )
        """
        params.append(int(from_year))

    if to_year:
        query += """
        AND (
            year='TTM'
            OR CAST(substr(year,-4) AS INTEGER) <= ?
        )
        """
        params.append(int(to_year))

    query += """
    ORDER BY
        CASE
            WHEN year='TTM' THEN 9999
            ELSE CAST(substr(year,-4) AS INTEGER)
        END DESC
    """

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# GET BALANCE SHEET HISTORY
# ==========================================================


@router.get("/{ticker}/bs")
def get_balance_sheet(
    ticker: str,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):

    conn = get_connection()

    company = conn.execute(
        """
        SELECT id
        FROM companies
        WHERE UPPER(id)=UPPER(?)
        """,
        (ticker,),
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    query = """
    SELECT *
    FROM balancesheet
    WHERE company_id = ?
    """

    params = [ticker]

    if from_year:
        query += """
        AND (
            year='TTM'
            OR CAST(substr(year,-4) AS INTEGER) >= ?
        )
        """
        params.append(int(from_year))

    if to_year:
        query += """
        AND (
            year='TTM'
            OR CAST(substr(year,-4) AS INTEGER) <= ?
        )
        """
        params.append(int(to_year))

    query += """
    ORDER BY
        CASE
            WHEN year='TTM' THEN 9999
            ELSE CAST(substr(year,-4) AS INTEGER)
        END DESC
    """

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# GET CASH FLOW HISTORY
# ==========================================================


@router.get("/{ticker}/cashflow")
def get_cashflow(
    ticker: str,
    from_year: str | None = Query(default=None),
    to_year: str | None = Query(default=None),
):

    conn = get_connection()

    company = conn.execute(
        """
        SELECT id
        FROM companies
        WHERE UPPER(id)=UPPER(?)
        """,
        (ticker,),
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    query = """
    SELECT *
    FROM cashflow
    WHERE company_id = ?
    """

    params = [ticker]

    if from_year:
        query += """
        AND (
            year='TTM'
            OR CAST(substr(year,-4) AS INTEGER) >= ?
        )
        """
        params.append(int(from_year))

    if to_year:
        query += """
        AND (
            year='TTM'
            OR CAST(substr(year,-4) AS INTEGER) <= ?
        )
        """
        params.append(int(to_year))

    query += """
    ORDER BY
        CASE
            WHEN year='TTM' THEN 9999
            ELSE CAST(substr(year,-4) AS INTEGER)
        END DESC
    """

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# GET FINANCIAL RATIOS
# ==========================================================


@router.get("/{ticker}/ratios")
def get_financial_ratios(
    ticker: str,
    year: str | None = Query(default=None),
):

    conn = get_connection()

    company = conn.execute(
        """
        SELECT id
        FROM companies
        WHERE UPPER(id)=UPPER(?)
        """,
        (ticker,),
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    """

    params = [ticker]

    if year:
        query += """
        AND year = ?
        """
        params.append(year)

    query += """
    ORDER BY
        CASE
            WHEN year='TTM' THEN 9999
            ELSE CAST(substr(year,-4) AS INTEGER)
        END DESC
    """

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# GET COMPANY TEARSHEET
# ==========================================================


@router.get("/{ticker}/tearsheet")
def get_tearsheet(ticker: str):

    conn = get_connection()

    company = conn.execute(
        """
        SELECT *
        FROM companies
        WHERE UPPER(id)=UPPER(?)
        """,
        (ticker,),
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    company = dict(company)

    latest_ratio = conn.execute(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY
            CASE
                WHEN year='TTM' THEN 9999
                ELSE CAST(substr(year,-4) AS INTEGER)
            END DESC
        LIMIT 1
        """,
        (ticker,),
    ).fetchone()

    latest_pl = conn.execute(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY
            CASE
                WHEN year='TTM' THEN 9999
                ELSE CAST(substr(year,-4) AS INTEGER)
            END DESC
        LIMIT 1
        """,
        (ticker,),
    ).fetchone()

    latest_bs = conn.execute(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        ORDER BY
            CASE
                WHEN year='TTM' THEN 9999
                ELSE CAST(substr(year,-4) AS INTEGER)
            END DESC
        LIMIT 1
        """,
        (ticker,),
    ).fetchone()

    latest_cf = conn.execute(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        ORDER BY
            CASE
                WHEN year='TTM' THEN 9999
                ELSE CAST(substr(year,-4) AS INTEGER)
            END DESC
        LIMIT 1
        """,
        (ticker,),
    ).fetchone()

    conn.close()

    return {
        "company": company,
        "financial_ratios": dict(latest_ratio) if latest_ratio else None,
        "profit_loss": dict(latest_pl) if latest_pl else None,
        "balance_sheet": dict(latest_bs) if latest_bs else None,
        "cash_flow": dict(latest_cf) if latest_cf else None,
    }


# ==========================================================
# GET COMPANY PROFILE
# (KEEP THIS ROUTE LAST)
# ==========================================================


@router.get("/{ticker}")
def get_company(ticker: str):

    conn = get_connection()

    company = conn.execute(
        """
        SELECT *
        FROM companies
        WHERE UPPER(id)=UPPER(?)
        """,
        (ticker,),
    ).fetchone()

    if company is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")

    company = dict(company)

    latest_ratio = conn.execute(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY
            CASE
                WHEN year='TTM' THEN 9999
                ELSE CAST(substr(year,-4) AS INTEGER)
            END DESC
        LIMIT 1
        """,
        (ticker,),
    ).fetchone()

    conn.close()

    company["latest_ratios"] = dict(latest_ratio) if latest_ratio else None

    return company
