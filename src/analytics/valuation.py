import os
import sqlite3
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# Database Connection
# --------------------------------------------------

conn = sqlite3.connect(DB_PATH)

# --------------------------------------------------
# Load Financial Ratios
# --------------------------------------------------

ratios_df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)

# --------------------------------------------------
# Normalize Financial Ratio Year
# Example:
# Mar 2024 -> 2024
# Dec 2023 -> 2023
# TTM -> NaN
# --------------------------------------------------

ratios_df["year_num"] = (
    ratios_df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

ratios_df["year_num"] = pd.to_numeric(
    ratios_df["year_num"],
    errors="coerce"
)

# --------------------------------------------------
# Load Market Cap
# --------------------------------------------------

market_df = pd.read_sql(
    """
    SELECT *
    FROM marketcap
    """,
    conn
)

market_df["year"] = pd.to_numeric(
    market_df["year"],
    errors="coerce"
)

# --------------------------------------------------
# Load Companies
# --------------------------------------------------

companies_df = pd.read_sql(
    """
    SELECT *
    FROM companies
    """,
    conn
)

# --------------------------------------------------
# Load Sector Information
# --------------------------------------------------

sector_df = pd.read_sql(
    """
    SELECT *
    FROM sectors
    """,
    conn
)

conn.close()

# --------------------------------------------------
# Keep Required Columns Only
# --------------------------------------------------

market_df = market_df[
    [
        "company_id",
        "year",
        "market_cap_crore",
        "enterprise_value_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "dividend_yield_pct"
    ]
]

companies_df = companies_df[
    [
        "id",
        "company_name"
    ]
]

sector_df = (
    sector_df[
        [
            "company_id",
            "broad_sector",
            "sub_sector"
        ]
    ]
    .drop_duplicates(subset="company_id")
)

# --------------------------------------------------
# Merge Data
# --------------------------------------------------

valuation_df = ratios_df.merge(
    market_df,
    left_on=["company_id", "year_num"],
    right_on=["company_id", "year"],
    how="left"
)

valuation_df.rename(
    columns={
        "year_x": "year"
    },
    inplace=True
)

if "year_y" in valuation_df.columns:
    valuation_df.drop(columns=["year_y"], inplace=True)

valuation_df = valuation_df.merge(
    sector_df,
    on="company_id",
    how="left"
)

valuation_df = valuation_df.merge(
    companies_df,
    left_on="company_id",
    right_on="id",
    how="left"
)

if "id" in valuation_df.columns:
    valuation_df.drop(columns=["id"], inplace=True)



# --------------------------------------------------
# Verification
# --------------------------------------------------

print("Financial Ratios :", len(ratios_df))
print("Market Cap       :", len(market_df))
print("Companies        :", len(companies_df))
print("Sectors          :", len(sector_df))

print("\nMerged Rows :", len(valuation_df))



# --------------------------------------------------
# Keep Annual Results Only
# Remove TTM and partial-year records
# --------------------------------------------------

valuation_df = valuation_df[
    ~valuation_df["year"].isin(["TTM"])
].copy()

valuation_df = valuation_df[
    ~valuation_df["year"].str.contains(
        "9m|15",
        case=False,
        na=False
    )
]

valuation_df["year_num"] = pd.to_numeric(
    valuation_df["year"]
        .str.extract(r"(\d{4})")[0],
    errors="coerce"
)

valuation_df = (
    valuation_df
    .sort_values("year_num")
    .groupby("company_id", as_index=False)
    .tail(1)
)

print("\nLatest Company Records :", len(valuation_df))


# --------------------------------------------------
# Calculate FCF Yield
# --------------------------------------------------

valuation_df["fcf_yield_pct"] = (
    valuation_df["free_cash_flow_cr"]
    / valuation_df["market_cap_crore"]
) * 100

valuation_df["fcf_yield_pct"] = (
    valuation_df["fcf_yield_pct"]
    .round(2)
)

print("\nFCF Yield Preview")

print(
    valuation_df[
        [
            "company_id",
            "free_cash_flow_cr",
            "market_cap_crore",
            "fcf_yield_pct"
        ]
    ].head(10)
)

# --------------------------------------------------
# Calculate Sector Median PE
# --------------------------------------------------

sector_pe = (
    valuation_df
    .groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
)

sector_pe.rename(
    columns={
        "pe_ratio": "sector_median_pe"
    },
    inplace=True
)

valuation_df = valuation_df.merge(
    sector_pe,
    on="broad_sector",
    how="left"
)

# --------------------------------------------------
# PE vs Sector Median %
# --------------------------------------------------

valuation_df["pe_vs_sector_median_pct"] = (
    (
        valuation_df["pe_ratio"]
        - valuation_df["sector_median_pe"]
    )
    /
    valuation_df["sector_median_pe"]
) * 100

valuation_df["pe_vs_sector_median_pct"] = (
    valuation_df["pe_vs_sector_median_pct"]
    .round(2)
)

# --------------------------------------------------
# Valuation Flag
# --------------------------------------------------

def valuation_flag(row):

    if pd.isna(row["pe_ratio"]):
        return "Fair"

    if pd.isna(row["sector_median_pe"]):
        return "Fair"

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    if row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    return "Fair"


valuation_df["flag"] = valuation_df.apply(
    valuation_flag,
    axis=1
)

# --------------------------------------------------
# Prepare Final Output
# --------------------------------------------------

valuation_summary = valuation_df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "fcf_yield_pct",
        "sector_median_pe",
        "pe_vs_sector_median_pct",
        "flag"
    ]
].copy()

valuation_summary.rename(
    columns={
        "broad_sector": "sector",
        "pe_ratio": "P/E",
        "pb_ratio": "P/B",
        "ev_ebitda": "EV/EBITDA",
        "fcf_yield_pct": "FCF_yield_pct",
        "sector_median_pe": "5yr_median_PE",
        "pe_vs_sector_median_pct": "PE_vs_sector_median_pct"
    },
    inplace=True
)

# --------------------------------------------------
# Preview
# --------------------------------------------------

print("\nValuation Summary Preview")

print(valuation_summary.head(10))

print("\nFlag Counts")

print(
    valuation_summary["flag"].value_counts()
)

# --------------------------------------------------
# Save valuation_summary.xlsx
# --------------------------------------------------

summary_file = os.path.join(
    OUTPUT_DIR,
    "valuation_summary.xlsx"
)

valuation_summary.to_excel(
    summary_file,
    index=False
)

# --------------------------------------------------
# Generate valuation_flags.csv
# --------------------------------------------------

valuation_flags = valuation_summary[
    valuation_summary["flag"].isin(
        [
            "Caution",
            "Discount"
        ]
    )
].copy()

flags_file = os.path.join(
    OUTPUT_DIR,
    "valuation_flags.csv"
)

valuation_flags.to_csv(
    flags_file,
    index=False
)

# --------------------------------------------------
# Final Validation
# --------------------------------------------------

print("\n========================================")
print("VALUATION MODULE COMPLETED")
print("========================================")

print(f"Total Companies : {len(valuation_summary)}")

print("\nFlag Distribution")
print(
    valuation_summary["flag"].value_counts()
)

print("\nOutput Files")

print(summary_file)
print(flags_file)

print("\nFirst 10 Companies")

print(
    valuation_summary[
        [
            "company_id",
            "company_name",
            "sector",
            "P/E",
            "P/B",
            "EV/EBITDA",
            "FCF_yield_pct",
            "5yr_median_PE",
            "PE_vs_sector_median_pct",
            "flag"
        ]
    ].head(10)
)

print("\nDone.")