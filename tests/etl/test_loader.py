import pandas as pd

from src.etl.loader import (
    load_companies,
    load_profitandloss,
    load_balancesheet,
    load_cashflow,
    load_analysis,
    load_documents,
    load_prosandcons,
    load_peer_groups,
    load_sectors,
    load_stock_prices,
)


# ======================================
# Companies
# ======================================

def test_load_companies():
    df = load_companies()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "company_name" in df.columns


# ======================================
# Profit & Loss
# ======================================

def test_load_profitandloss():
    df = load_profitandloss()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "sales" in df.columns
    assert "operating_profit" in df.columns
    assert "opm_percentage" in df.columns


# ======================================
# Balance Sheet
# ======================================

def test_load_balancesheet():
    df = load_balancesheet()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


# ======================================
# Cash Flow
# ======================================

def test_load_cashflow():
    df = load_cashflow()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


# ======================================
# Analysis
# ======================================

def test_load_analysis():
    df = load_analysis()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


# ======================================
# Documents
# ======================================

def test_load_documents():
    df = load_documents()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


# ======================================
# Pros & Cons
# ======================================

def test_load_prosandcons():
    df = load_prosandcons()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0





# ======================================
# Peer Groups
# ======================================

def test_load_peer_groups():
    df = load_peer_groups()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


# ======================================
# Sectors
# ======================================

def test_load_sectors():
    df = load_sectors()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


# ======================================
# Stock Prices
# ======================================

def test_load_stock_prices():
    df = load_stock_prices()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0