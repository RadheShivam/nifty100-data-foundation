import pandas as pd
import os


def create_validation_summary():
    files = [
        "profitandloss_duplicates.csv",
        "balancesheet_duplicates.csv",
        "cashflow_duplicates.csv",
        "profitandloss_invalid_fk.csv",
        "balancesheet_invalid_fk.csv",
        "cashflow_invalid_fk.csv",
        "analysis_invalid_fk.csv",
        "documents_invalid_fk.csv",
        "prosandcons_invalid_fk.csv",
        "balance_sheet_equation_failures.csv",
        "opm_consistency_failures.csv",
        "non_positive_sales.csv",
        "net_cash_flow_failures.csv",
        "invalid_tax_rates.csv",
        "invalid_dividend_payout.csv",
        "eps_sign_failures.csv",
        "documents_invalid_urls.csv",
        "profitandloss_year_coverage_failures.csv",
        "balancesheet_year_coverage_failures.csv",
        "cashflow_year_coverage_failures.csv"
    ]

    data = []

    for file in files:
        path = f"output/{file}"

        if os.path.exists(path):
            df = pd.read_csv(path)

            data.append({
                "file_name": file,
                "records": len(df),
                "severity": "High"
            })

    pd.DataFrame(data).to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print("✅ validation_failures.csv created")