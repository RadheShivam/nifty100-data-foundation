

from src.etl.loader import *

def test_companies_columns():
    df = load_companies()

    expected_columns = [
        "id",
        "company_logo",
        "company_name",
        "chart_link",
        "about_company",
        "website",
        "nse_profile",
        "bse_profile",
        "face_value",
        "book_value",
        "roce_percentage",
        "roe_percentage"
    ]

    assert list(df.columns) == expected_columns








def test_companies_columns():
    df = load_companies()
    assert "id" in df.columns
    assert "company_name" in df.columns


def test_profitandloss_columns():
    df = load_profitandloss()
    assert "company_id" in df.columns
    assert "sales" in df.columns


def test_balancesheet_columns():
    df = load_balancesheet()
    assert "company_id" in df.columns
    assert "total_assets" in df.columns


def test_cashflow_columns():
    df = load_cashflow()
    assert "company_id" in df.columns
    assert "net_cash_flow" in df.columns


def test_analysis_columns():
    df = load_analysis()
    assert "company_id" in df.columns
    assert "roe" in df.columns


def test_documents_columns():
    df = load_documents()
    assert "company_id" in df.columns
    assert "Annual_Report" in df.columns


def test_prosandcons_columns():
    df = load_prosandcons()
    assert "company_id" in df.columns
    assert "pros" in df.columns


def test_sectors_columns():
    df = load_sectors()
    assert "company_id" in df.columns
    assert "broad_sector" in df.columns