import pandas as pd


def check_primary_key_uniqueness(df, table_name, pk_column):
    duplicates = df[df.duplicated(subset=[pk_column], keep=False)]

    if duplicates.empty:
        print(f"✅ {table_name}: Primary key uniqueness passed")
    else:
        print(f"❌ {table_name}: Duplicate primary keys found")
        print(duplicates)

def check_composite_key_uniqueness(df, table_name, columns):
    duplicates = df[df.duplicated(subset=columns, keep=False)]

    if duplicates.empty:
        print(f"✅ {table_name}: Composite key uniqueness passed")
    else:
        print(f"❌ {table_name}: Duplicate composite keys found")
        print(duplicates)

def check_composite_key_uniqueness(df, table_name, columns):
    duplicates = df[df.duplicated(subset=columns, keep=False)]

    if duplicates.empty:
        print(f"✅ {table_name}: Composite key uniqueness passed")
    else:
        print(f"❌ {table_name}: Duplicate composite keys found")

        filename = f"output/{table_name}_duplicates.csv"
        duplicates.to_csv(filename, index=False)

        print(f"Saved to {filename}")

def check_foreign_key_integrity(
        child_df,
        parent_df,
        child_column,
        parent_column,
        table_name):

    invalid_keys = child_df[
        ~child_df[child_column].isin(parent_df[parent_column])
    ]

    if invalid_keys.empty:
        print(f"✅ {table_name}: Foreign key integrity passed")
    else:
        print(f"❌ {table_name}: Invalid foreign keys found")

        filename = f"output/{table_name}_invalid_fk.csv"
        invalid_keys.to_csv(filename, index=False)

        print(f"Saved to {filename}")

def check_balance_sheet_equation(df):
    equity = df["equity_capital"] + df["reserves"]
    liabilities = df["borrowings"] + df["other_liabilities"]

    expected_assets = equity + liabilities

    difference_percentage = (
        abs(df["total_assets"] - expected_assets)
        / df["total_assets"]
    )

    invalid_rows = df[difference_percentage > 0.01]

    if invalid_rows.empty:
        print("✅ balancesheet: Balance equation passed")
    else:
        print("❌ balancesheet: Balance equation failed")

        invalid_rows.to_csv(
            "output/balance_sheet_equation_failures.csv",
            index=False
        )

        print(
            "Saved to output/balance_sheet_equation_failures.csv"
        )



def check_opm_consistency(df):
    calculated_opm = (
        df["operating_profit"] / df["sales"]
    ) * 100

    difference = abs(
        calculated_opm - df["opm_percentage"]
    )

    invalid_rows = df[difference > 1]

    if invalid_rows.empty:
        print("✅ profitandloss: OPM consistency passed")
    else:
        print("❌ profitandloss: OPM consistency failed")

        invalid_rows.to_csv(
            "output/opm_consistency_failures.csv",
            index=False
        )

        print(
            "Saved to output/opm_consistency_failures.csv"
        )

def check_positive_sales(df):
    invalid_rows = df[df["sales"] <= 0]

    if invalid_rows.empty:
        print("✅ profitandloss: Positive sales check passed")
    else:
        print("❌ profitandloss: Non-positive sales found")

        invalid_rows.to_csv(
            "output/non_positive_sales.csv",
            index=False
        )

        print(
            "Saved to output/non_positive_sales.csv"
        )


def check_net_cash_flow_consistency(df):
    calculated_net_cash = (
        df["operating_activity"]
        + df["investing_activity"]
        + df["financing_activity"]
    )

    difference = abs(
        calculated_net_cash - df["net_cash_flow"]
    )

    invalid_rows = df[difference > 1]

    if invalid_rows.empty:
        print("✅ cashflow: Net cash flow consistency passed")
    else:
        print("❌ cashflow: Net cash flow consistency failed")

        invalid_rows.to_csv(
            "output/net_cash_flow_failures.csv",
            index=False
        )

        print(
            "Saved to output/net_cash_flow_failures.csv"
        )



def check_tax_rate_validity(df):
    invalid_rows = df[
        (df["tax_percentage"] < 0)
        | (df["tax_percentage"] > 100)
    ]

    if invalid_rows.empty:
        print("✅ profitandloss: Tax rate validity passed")
    else:
        print("❌ profitandloss: Invalid tax rates found")

        invalid_rows.to_csv(
            "output/invalid_tax_rates.csv",
            index=False
        )

        print(
            "Saved to output/invalid_tax_rates.csv"
        )


def check_dividend_cap(df):
    invalid_rows = df[
        (df["dividend_payout"] < 0)
        | (df["dividend_payout"] > 100)
    ]

    if invalid_rows.empty:
        print("✅ profitandloss: Dividend payout check passed")
    else:
        print("❌ profitandloss: Invalid dividend payout found")

        invalid_rows.to_csv(
            "output/invalid_dividend_payout.csv",
            index=False
        )

        print(
            "Saved to output/invalid_dividend_payout.csv"
        )

def check_eps_sign(df):
    invalid_rows = df[
        (df["net_profit"] < 0)
        & (df["eps"] >= 0)
    ]

    if invalid_rows.empty:
        print("✅ profitandloss: EPS sign check passed")
    else:
        print("❌ profitandloss: EPS sign mismatch found")

        invalid_rows.to_csv(
            "output/eps_sign_failures.csv",
            index=False
        )

        print(
            "Saved to output/eps_sign_failures.csv"
        )


def check_url_validity(df, columns, table_name):
    invalid_rows = []

    for column in columns:
        mask = (
            df[column].notna()
            & ~df[column].astype(str).str.startswith(
                ("http://", "https://")
            )
        )

        invalid = df[mask]

        if not invalid.empty:
            invalid_rows.append(invalid)

    if len(invalid_rows) == 0:
        print(f"✅ {table_name}: URL validation passed")
    else:
        invalid_df = pd.concat(invalid_rows)

        print(f"❌ {table_name}: Invalid URLs found")

        filename = f"output/{table_name}_invalid_urls.csv"

        invalid_df.to_csv(filename, index=False)

        print(f"Saved to {filename}")

def check_sector_availability(
        companies_df,
        sectors_df):

    missing_sector = companies_df[
        ~companies_df["id"].isin(
            sectors_df["company_id"]
        )
    ]

    if missing_sector.empty:
        print(
            "✅ companies: Sector availability passed"
        )

    else:
        print(
            "❌ companies: Missing sectors found"
        )

        filename = "output/missing_sectors.csv"

        missing_sector.to_csv(
            filename,
            index=False
        )

        print(
            f"Saved to {filename}"
        )


def check_year_coverage(df, table_name):
    expected_years = {
        "Mar 2013",
        "Mar 2014",
        "Mar 2015",
        "Mar 2016",
        "Mar 2017",
        "Mar 2018",
        "Mar 2019",
        "Mar 2020",
        "Mar 2021",
        "Mar 2022",
        "Mar 2023",
        "Mar 2024",
        "TTM"
    }

    coverage = df.groupby("company_id")["year"].apply(set)

    invalid_companies = coverage[
        coverage.apply(
            lambda years: not expected_years.issubset(years)
        )
    ]

    if invalid_companies.empty:
        print(f"✅ {table_name}: Year coverage passed")

    else:
        print(f"❌ {table_name}: Incomplete year coverage")

        invalid_companies.to_csv(
            f"output/{table_name}_year_coverage_failures.csv"
        )

        print(
            f"Saved to output/{table_name}_year_coverage_failures.csv"
        )

def check_duplicate_rows(df, table_name):
    duplicates = df[df.duplicated(keep=False)]

    if duplicates.empty:
        print(f"✅ {table_name}: Duplicate row check passed")

    else:
        print(f"❌ {table_name}: Duplicate rows found")

        filename = (
            f"output/{table_name}_duplicate_rows.csv"
        )

        duplicates.to_csv(
            filename,
            index=False
        )

        print(
            f"Saved to {filename}"
        )


def check_ticker_normalization(df, column_name, table_name):
    invalid_rows = df[
        df[column_name] !=
        df[column_name].astype(str).str.strip().str.upper()
    ]

    if invalid_rows.empty:
        print(f"✅ {table_name}: Ticker normalization passed")

    else:
        print(f"❌ {table_name}: Ticker normalization failed")

        filename = (
            f"output/{table_name}_ticker_normalization_failures.csv"
        )

        invalid_rows.to_csv(
            filename,
            index=False
        )

        print(
            f"Saved to {filename}"
        )



def check_mandatory_columns(
        df,
        required_columns,
        table_name):

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if len(missing_columns) == 0:
        print(
            f"✅ {table_name}: Mandatory columns check passed"
        )

    else:
        print(
            f"❌ {table_name}: Missing columns found"
        )

        print(
            "Missing columns:",
            missing_columns
        )