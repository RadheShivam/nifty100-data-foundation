import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


# --------------------------------------------------
# Companies
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_companies():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    conn.close()
    return df


# --------------------------------------------------
# Financial Ratios (Single Company)
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    conn = sqlite3.connect(DB_PATH)

    if year:

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        AND year = ?
        """

        df = pd.read_sql(
            query,
            conn,
            params=(ticker, year)
        )

    else:

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        """

        df = pd.read_sql(
            query,
            conn,
            params=(ticker,)
        )

    conn.close()
    return df


# --------------------------------------------------
# Financial Ratios (All Companies)
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_ratios_by_year(year):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM financial_ratios
    WHERE year = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=(year,)
    )

    conn.close()
    return df


# --------------------------------------------------
# Profit & Loss
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        """,
        conn,
        params=(ticker,)
    )

    conn.close()
    return df


# --------------------------------------------------
# Balance Sheet
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        """,
        conn,
        params=(ticker,)
    )

    conn.close()
    return df


# --------------------------------------------------
# Cash Flow
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        """,
        conn,
        params=(ticker,)
    )

    conn.close()
    return df


# --------------------------------------------------
# Sector Information
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_sectors():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()
    return df


# --------------------------------------------------
# Peer Groups
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM peer_groups
    WHERE peer_group_name = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=(group_name,)
    )

    conn.close()
    return df

# --------------------------------------------------
# Valuation
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        company_name,
        face_value,
        book_value,
        roe_percentage,
        roce_percentage
    FROM companies
    WHERE id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=(ticker,)
    )

    conn.close()
    return df


# --------------------------------------------------
# Latest Financial Ratio
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_latest_ratio(ticker):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1
    """

    df = pd.read_sql(
        query,
        conn,
        params=(ticker,)
    )

    conn.close()
    return df


# --------------------------------------------------
# Pros & Cons
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_pros_cons(ticker):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        pros,
        cons
    FROM prosandcons
    WHERE company_id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=(ticker,)
    )

    conn.close()
    return df


# --------------------------------------------------
# Sector Information
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_sector_info(ticker):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        broad_sector,
        sub_sector,
        market_cap_category
    FROM sectors
    WHERE company_id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=(ticker,)
    )

    conn.close()
    return df