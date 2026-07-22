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
)