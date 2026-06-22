from src.etl.loader import *
from src.etl.validator import *

sectors_df = load_sectors()



# Load tables
companies_df = load_companies()
profit_df = load_profitandloss()
balance_df = load_balancesheet()
cashflow_df = load_cashflow()

analysis_df = load_analysis()
documents_df = load_documents()
pros_df = load_prosandcons()

# DQ-01
check_primary_key_uniqueness(
    companies_df,
    "companies",
    "id"
)

# DQ-02
check_composite_key_uniqueness(
    profit_df,
    "profitandloss",
    ["company_id", "year"]
)

check_composite_key_uniqueness(
    balance_df,
    "balancesheet",
    ["company_id", "year"]
)

check_composite_key_uniqueness(
    cashflow_df,
    "cashflow",
    ["company_id", "year"]
)

# DQ-03 Foreign Key Integrity

check_foreign_key_integrity(
    profit_df,
    companies_df,
    "company_id",
    "id",
    "profitandloss"
)

check_foreign_key_integrity(
    balance_df,
    companies_df,
    "company_id",
    "id",
    "balancesheet"
)

check_foreign_key_integrity(
    cashflow_df,
    companies_df,
    "company_id",
    "id",
    "cashflow"
)

check_foreign_key_integrity(
    analysis_df,
    companies_df,
    "company_id",
    "id",
    "analysis"
)

check_foreign_key_integrity(
    documents_df,
    companies_df,
    "company_id",
    "id",
    "documents"
)

check_foreign_key_integrity(
    pros_df,
    companies_df,
    "company_id",
    "id",
    "prosandcons"
)

check_balance_sheet_equation(balance_df)




check_opm_consistency(profit_df)

check_positive_sales(profit_df)


check_net_cash_flow_consistency(cashflow_df)

check_tax_rate_validity(profit_df)

check_dividend_cap(profit_df)

check_eps_sign(profit_df)


check_url_validity(
    companies_df,
    [
        "company_logo",
        "website",
        "nse_profile",
        "bse_profile"
    ],
    "companies"
)

check_url_validity(
    documents_df,
    [
        "Annual_Report"
    ],
    "documents"
)

check_sector_availability(
    companies_df,
    sectors_df
)

# sectors_df = load_sectors()




# DQ-13

check_year_coverage(
    profit_df,
    "profitandloss"
)

check_year_coverage(
    balance_df,
    "balancesheet"
)

check_year_coverage(
    cashflow_df,
    "cashflow"
)


# DQ-14

check_duplicate_rows(
    profit_df,
    "profitandloss"
)

check_duplicate_rows(
    balance_df,
    "balancesheet"
)

check_duplicate_rows(
    cashflow_df,
    "cashflow"
)


# DQ-15

check_ticker_normalization(
    companies_df,
    "id",
    "companies"
)

check_ticker_normalization(
    profit_df,
    "company_id",
    "profitandloss"
)

check_ticker_normalization(
    balance_df,
    "company_id",
    "balancesheet"
)

check_ticker_normalization(
    cashflow_df,
    "company_id",
    "cashflow"
)



# DQ-16

check_mandatory_columns(
    companies_df,
    [
        "id",
        "company_logo",
        "company_name"
    ],
    "companies"
)

check_mandatory_columns(
    profit_df,
    [
        "company_id",
        "year",
        "sales",
        "net_profit"
    ],
    "profitandloss"
)

check_mandatory_columns(
    balance_df,
    [
        "company_id",
        "year",
        "total_assets"
    ],
    "balancesheet"
)

check_mandatory_columns(
    cashflow_df,
    [
        "company_id",
        "year",
        "net_cash_flow"
    ],
    "cashflow"
)

check_mandatory_columns(
    analysis_df,
    [
        "company_id",
        "roe"
    ],
    "analysis"
)

check_mandatory_columns(
    documents_df,
    [
        "company_id",
        "Annual_Report"
    ],
    "documents"
)

check_mandatory_columns(
    pros_df,
    [
        "company_id",
        "pros",
        "cons"
    ],
    "prosandcons"
)

check_mandatory_columns(
    sectors_df,
    [
        "company_id",
        "broad_sector"
    ],
    "sectors"
)