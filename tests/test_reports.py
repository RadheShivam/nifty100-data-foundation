import os


def test_load_audit_exists():
    assert os.path.exists("output/load_audit.csv")


def test_top_sales_exists():
    assert os.path.exists("output/top_sales.csv")


def test_top_roe_exists():
    assert os.path.exists("output/top_roe.csv")


def test_sector_distribution_exists():
    assert os.path.exists("output/sector_distribution.csv")


def test_top_cashflow_exists():
    assert os.path.exists("output/top_cashflow.csv")


def test_kpi_summary_exists():
    assert os.path.exists("output/kpi_summary.csv")