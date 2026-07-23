import pandas as pd

from src.etl.validator import (
    check_primary_key_uniqueness,
    check_composite_key_uniqueness,
    check_foreign_key_integrity,
    check_balance_sheet_equation,
    check_opm_consistency,
    check_positive_sales,
    check_net_cash_flow_consistency,
    check_tax_rate_validity,
    check_dividend_cap,
    check_eps_sign,
    check_url_validity,
    check_sector_availability,
    check_year_coverage,
    check_duplicate_rows,
    check_ticker_normalization,
    check_mandatory_columns,
)


def test_primary_key_uniqueness():
    df = pd.DataFrame({"id": ["A", "B", "C"]})

    check_primary_key_uniqueness(df, "companies", "id")


def test_composite_key_uniqueness():
    df = pd.DataFrame({"company_id": ["A", "A", "B"], "year": [2022, 2023, 2022]})

    check_composite_key_uniqueness(df, "profitandloss", ["company_id", "year"])


def test_foreign_key_integrity():
    parent_df = pd.DataFrame({"id": ["A", "B"]})

    child_df = pd.DataFrame({"company_id": ["A", "B"]})

    check_foreign_key_integrity(
        child_df, parent_df, "company_id", "id", "profitandloss"
    )


def test_balance_sheet_equation():
    df = pd.DataFrame(
        {
            "equity_capital": [100],
            "reserves": [100],
            "borrowings": [50],
            "other_liabilities": [50],
            "total_assets": [300],
        }
    )

    check_balance_sheet_equation(df)


def test_opm_consistency():
    df = pd.DataFrame(
        {"operating_profit": [300], "sales": [1000], "opm_percentage": [30]}
    )

    check_opm_consistency(df)


def test_positive_sales():
    df = pd.DataFrame(
        {
            "sales": [1000],
            "expenses": [500],
            "operating_profit": [300],
            "net_profit": [200],
        }
    )

    check_positive_sales(df)


def test_net_cash_flow_consistency():
    df = pd.DataFrame(
        {
            "operating_activity": [100],
            "investing_activity": [-20],
            "financing_activity": [30],
            "net_cash_flow": [110],
        }
    )

    check_net_cash_flow_consistency(df)


def test_tax_rate_validity():
    df = pd.DataFrame({"tax_percentage": [30]})

    check_tax_rate_validity(df)


def test_dividend_cap():
    df = pd.DataFrame({"dividend_payout": [40]})

    check_dividend_cap(df)


def test_eps_sign():
    df = pd.DataFrame({"net_profit": [100], "eps": [10]})

    check_eps_sign(df)


def test_url_validity():
    df = pd.DataFrame({"website": ["https://example.com"]})

    check_url_validity(df, ["website"], "companies")


def test_sector_availability():
    companies_df = pd.DataFrame({"id": ["A", "B"]})

    sectors_df = pd.DataFrame({"company_id": ["A", "B"]})

    check_sector_availability(companies_df, sectors_df)


def test_year_coverage():
    df = pd.DataFrame({"company_id": ["A"] * 10, "year": list(range(2015, 2025))})

    check_year_coverage(df, "profitandloss")


def test_duplicate_rows():
    df = pd.DataFrame({"company_id": ["A", "B"], "year": [2022, 2023]})

    check_duplicate_rows(df, "profitandloss")
