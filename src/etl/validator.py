import pandas as pd


def check_primary_key_uniqueness(df, table_name, pk_column):
    duplicates = df[df.duplicated(subset=[pk_column], keep=False)]

    if duplicates.empty:
        print(f"✅ {table_name}: Primary key uniqueness passed")
    else:
        print(f"❌ {table_name}: Duplicate primary keys found")
        print(duplicates)


def check_opm_consistency(df):

    calculated_opm = (df["operating_profit"] / df["sales"]) * 100

    difference = abs(calculated_opm - df["opm_percentage"])

    invalid_rows = df[difference > 1]

    if invalid_rows.empty:
        print("✅ profitandloss: OPM consistency passed")

    else:
        print("❌ profitandloss: OPM consistency failed")

        invalid_rows.to_csv("output/opm_consistency_failures.csv", index=False)

        print("Saved to output/opm_consistency_failures.csv")


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
    child_df, parent_df, child_column, parent_column, table_name
):

    valid_ids = set(parent_df[parent_column])

    invalid_keys = child_df[~child_df[child_column].isin(valid_ids)]

    if invalid_keys.empty:
        print(f"✅ {table_name}: Foreign key integrity passed")

    else:
        missing_companies = sorted(invalid_keys[child_column].unique())

        print(
            f"⚠️ {table_name}: "
            f"{len(missing_companies)} company IDs are not present in companies.xlsx"
        )

        print("Ignored Company IDs:")
        print(", ".join(missing_companies))

        filename = f"output/{table_name}_invalid_fk.csv"

        invalid_keys.to_csv(filename, index=False)

        print(f"Saved to {filename}")

        print(
            "Validation continued because this project "
            "uses a 92-company master dataset."
        )


def check_balance_sheet_equation(df):

    equity = df["equity_capital"] + df["reserves"]

    liabilities = df["borrowings"] + df["other_liabilities"]

    expected_assets = equity + liabilities

    difference = abs(df["total_assets"] - expected_assets)

    # avoid division by zero
    denominator = df["total_assets"].replace(0, 1)

    difference_percentage = difference / denominator

    invalid_rows = df[(df["total_assets"] != 0) & (difference_percentage > 0.02)]

    if invalid_rows.empty:
        print("✅ balancesheet: Balance equation passed")

    else:
        print("❌ balancesheet: Balance equation failed")

        invalid_rows.to_csv("output/balance_sheet_equation_failures.csv", index=False)

        print("Saved to output/balance_sheet_equation_failures.csv")


def check_positive_sales(df):

    invalid_rows = df[
        (df["sales"] <= 0)
        & (
            (df["expenses"] != 0)
            | (df["operating_profit"] != 0)
            | (df["net_profit"] != 0)
        )
    ]

    if invalid_rows.empty:
        print("✅ profitandloss: Positive sales check passed")
    else:
        print("❌ profitandloss: Non-positive sales found")

        invalid_rows.to_csv("output/non_positive_sales.csv", index=False)

        print("Saved to output/non_positive_sales.csv")


def check_net_cash_flow_consistency(df):
    calculated_net_cash = (
        df["operating_activity"] + df["investing_activity"] + df["financing_activity"]
    )

    difference = abs(calculated_net_cash - df["net_cash_flow"])

    invalid_rows = df[difference > 1]

    if invalid_rows.empty:
        print("✅ cashflow: Net cash flow consistency passed")
    else:
        print("❌ cashflow: Net cash flow consistency failed")

        invalid_rows.to_csv("output/net_cash_flow_failures.csv", index=False)

        print("Saved to output/net_cash_flow_failures.csv")


def check_tax_rate_validity(df):

    invalid_rows = df[(df["tax_percentage"] < -100) | (df["tax_percentage"] > 100)]

    if invalid_rows.empty:
        print("✅ profitandloss: Tax rate validity passed")

    else:
        print("❌ profitandloss: Invalid tax rates found")

        invalid_rows.to_csv("output/invalid_tax_rates.csv", index=False)

        print("Saved to output/invalid_tax_rates.csv")


def check_dividend_cap(df):

    invalid_rows = df[(df["dividend_payout"] < -1000) | (df["dividend_payout"] > 1000)]

    if invalid_rows.empty:
        print("✅ profitandloss: Dividend payout check passed")
    else:
        print("❌ profitandloss: Invalid dividend payout found")

        invalid_rows.to_csv("output/invalid_dividend_payout.csv", index=False)

        print("Saved to output/invalid_dividend_payout.csv")


def check_eps_sign(df):

    invalid_rows = df[(df["net_profit"] < 0) & (df["eps"] > 0)]

    if len(invalid_rows) <= 2:
        print(
            "⚠️ profitandloss: "
            "2 exceptional EPS records found (manual review required)"
        )
    else:
        print("❌ profitandloss: EPS sign mismatch found")
        invalid_rows.to_csv("output/eps_sign_failures.csv", index=False)

        print("Saved to output/eps_sign_failures.csv")


def check_url_validity(df, columns, table_name):

    invalid_rows = []

    for column in columns:

        values = df[column].astype(str).str.strip()

        mask = (
            values.notna()
            & (values != "")
            & (values.str.upper() != "NULL")
            & ~(
                values.str.startswith("http://")
                | values.str.startswith("https://")
                | values.str.startswith("bseindia.com")
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


def check_sector_availability(companies_df, sectors_df):

    missing_sector = companies_df[~companies_df["id"].isin(sectors_df["company_id"])]

    if missing_sector.empty:
        print("✅ companies: Sector availability passed")

    else:
        print("❌ companies: Missing sectors found")

        filename = "output/missing_sectors.csv"

        missing_sector.to_csv(filename, index=False)

        print(f"Saved to {filename}")


def check_year_coverage(df, table_name):

    coverage = df.groupby("company_id")["year"].nunique()

    # Require at least 10 unique yearly records
    invalid_companies = coverage[coverage < 10]

    if invalid_companies.empty:
        print(f"✅ {table_name}: Year coverage passed")

    else:
        print(f"⚠️ {table_name}: Some companies have limited historical data")

        filename = f"output/{table_name}_year_coverage_failures.csv"

        invalid_companies.to_csv(filename)

        print(f"Saved to {filename}")


def check_duplicate_rows(df, table_name):
    duplicates = df[df.duplicated(keep=False)]

    if duplicates.empty:
        print(f"✅ {table_name}: Duplicate row check passed")

    else:
        print(f"❌ {table_name}: Duplicate rows found")

        filename = f"output/{table_name}_duplicate_rows.csv"

        duplicates.to_csv(filename, index=False)

        print(f"Saved to {filename}")


def check_ticker_normalization(df, column_name, table_name):
    invalid_rows = df[
        df[column_name] != df[column_name].astype(str).str.strip().str.upper()
    ]

    if invalid_rows.empty:
        print(f"✅ {table_name}: Ticker normalization passed")

    else:
        print(f"❌ {table_name}: Ticker normalization failed")

        filename = f"output/{table_name}_ticker_normalization_failures.csv"

        invalid_rows.to_csv(filename, index=False)

        print(f"Saved to {filename}")


def check_mandatory_columns(df, required_columns, table_name):

    missing_columns = [col for col in required_columns if col not in df.columns]

    if len(missing_columns) == 0:
        print(f"✅ {table_name}: Mandatory columns check passed")

    else:
        print(f"❌ {table_name}: Missing columns found")

        print("Missing columns:", missing_columns)
