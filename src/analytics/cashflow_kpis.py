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
# Helper Functions
# --------------------------------------------------


def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow
    """
    return operating_activity + investing_activity


def cfo_quality_score(operating_cash_flow, net_profit):
    """
    CFO / PAT Ratio
    """

    if pd.isna(net_profit) or net_profit == 0:
        return None, None

    ratio = operating_cash_flow / net_profit

    if ratio > 1:
        label = "High Quality"
    elif ratio >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return ratio, label


def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity %
    """

    if pd.isna(sales) or sales == 0:
        return None, None

    value = abs(investing_activity) / sales * 100

    if value < 3:
        label = "Asset Light"
    elif value <= 8:
        label = "Moderate"
    else:
        label = "Capital Intensive"

    return value, label


def fcf_conversion_rate(free_cash_flow, operating_profit):
    """
    FCF Conversion %
    """

    if pd.isna(operating_profit) or operating_profit == 0:
        return None

    return (free_cash_flow / operating_profit) * 100


def capital_allocation_pattern(
    operating_activity, investing_activity, financing_activity, quality=None
):
    """
    Capital Allocation Pattern
    """

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    if (cfo, cfi, cff) == ("+", "-", "-"):

        if quality == "High Quality":
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    elif (cfo, cfi, cff) == ("+", "+", "-"):
        label = "Liquidating Assets"

    elif (cfo, cfi, cff) == ("-", "+", "+"):
        label = "Distress Signal"

    elif (cfo, cfi, cff) == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    elif (cfo, cfi, cff) == ("+", "+", "+"):
        label = "Cash Accumulator"

    elif (cfo, cfi, cff) == ("-", "-", "-"):
        label = "Pre-Revenue"

    elif (cfo, cfi, cff) == ("+", "-", "+"):
        label = "Mixed"

    else:
        label = "Other"

    return cfo, cfi, cff, label


# --------------------------------------------------
# Load Database
# --------------------------------------------------

conn = sqlite3.connect(DB_PATH)

cashflow_df = pd.read_sql("SELECT * FROM cashflow", conn)

ratios_df = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        free_cash_flow_cr,
        cfo_pat_ratio
    FROM financial_ratios
    """,
    conn,
)

pl_df = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        sales,
        operating_profit,
        net_profit
    FROM profitandloss
    """,
    conn,
)

balance_df = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        borrowings
    FROM balancesheet
    """,
    conn,
)

sector_df = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sectors
    """,
    conn,
)

companies_df = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    """,
    conn,
)

conn.close()

# --------------------------------------------------
# Prepare Year Column
# --------------------------------------------------

for df in [cashflow_df, ratios_df, pl_df, balance_df]:

    df["year_num"] = df["year"].astype(str).str.extract(r"(\d{4})")[0].astype(float)

# --------------------------------------------------
# Merge Tables
# --------------------------------------------------

merged_df = (
    cashflow_df.merge(pl_df, on=["company_id", "year"], how="inner")
    .merge(ratios_df, on=["company_id", "year"], how="left")
    .merge(sector_df, on="company_id", how="left")
    .merge(companies_df, on="company_id", how="left")
)

merged_df = merged_df[merged_df["company_id"].isin(companies_df["company_id"])].copy()

merged_df = merged_df.sort_values(["company_id", "year_num"])

print("=" * 50)
print("DATA LOADED")
print("=" * 50)

print("Cash Flow :", len(cashflow_df))
print("Financial Ratios :", len(ratios_df))
print("Profit & Loss :", len(pl_df))
print("Companies :", len(companies_df))
print("Sectors :", len(sector_df))

results = []

valid_companies = companies_df["company_id"].tolist()

# --------------------------------------------------
# Process All Companies
# --------------------------------------------------

for company in valid_companies:

    temp = merged_df[merged_df["company_id"] == company].sort_values("year_num").tail(5)

    if temp.empty:
        continue

    latest = temp.iloc[-1]

    # ------------------------------------------
    # CFO Quality Score (Average of last 5 years)
    # ------------------------------------------

    ratios = []

    for _, row in temp.iterrows():

        ratio, _ = cfo_quality_score(row["operating_activity"], row["net_profit"])

        if ratio is not None:
            ratios.append(ratio)

    if len(ratios):

        avg_ratio = sum(ratios) / len(ratios)

        if avg_ratio > 1:
            quality = "High Quality"

        elif avg_ratio >= 0.5:
            quality = "Moderate"

        else:
            quality = "Accrual Risk"

    else:

        avg_ratio = None
        quality = None

    # ------------------------------------------
    # FCF CAGR (5 Years)
    # ------------------------------------------

    fcf_cagr = None

    fcf_history = temp["free_cash_flow_cr"].dropna().tolist()

    if len(fcf_history) >= 5:

        first = abs(fcf_history[0])
        last = abs(fcf_history[-1])

        if first > 0 and last > 0:

            fcf_cagr = (((last / first) ** (1 / 4)) - 1) * 100

    # ------------------------------------------
    # FCF Conversion
    # ------------------------------------------

    fcf_conversion = fcf_conversion_rate(
        latest["free_cash_flow_cr"], latest["operating_profit"]
    )

    # ------------------------------------------
    # CapEx Intensity
    # ------------------------------------------

    capex_pct, capex_label = capex_intensity(
        latest["investing_activity"], latest["sales"]
    )

    # ------------------------------------------
    # Distress Signal
    # ------------------------------------------

    distress_flag = (
        latest["operating_activity"] < 0 and latest["financing_activity"] > 0
    )

    # ------------------------------------------
    # Deleveraging Flag
    # ------------------------------------------

    bs = balance_df[balance_df["company_id"] == company].sort_values("year_num").tail(2)

    deleveraging_flag = False

    if len(bs) == 2:

        old_borrowing = bs.iloc[0]["borrowings"]
        new_borrowing = bs.iloc[1]["borrowings"]

        if latest["financing_activity"] < 0 and new_borrowing < old_borrowing:

            deleveraging_flag = True

    # ------------------------------------------
    # Capital Allocation Pattern
    # ------------------------------------------

    _, _, _, capital_label = capital_allocation_pattern(
        latest["operating_activity"],
        latest["investing_activity"],
        latest["financing_activity"],
        quality,
    )

    # ------------------------------------------
    # Save Company Result
    # ------------------------------------------

    results.append(
        {
            "company_id": company,
            "company_name": latest["company_name"],
            "sector": latest["broad_sector"],
            "cfo_quality_score": round(avg_ratio, 2) if avg_ratio is not None else None,
            "cfo_quality_label": quality,
            "capex_intensity_pct": (
                round(capex_pct, 2) if capex_pct is not None else None
            ),
            "capex_label": capex_label,
            "fcf_cagr_5yr": round(fcf_cagr, 2) if fcf_cagr is not None else None,
            "fcf_conversion_pct": (
                round(fcf_conversion, 2) if fcf_conversion is not None else None
            ),
            "distress_flag": distress_flag,
            "deleveraging_flag": deleveraging_flag,
            "capital_allocation_label": capital_label,
        }
    )

# --------------------------------------------------
# Create Result DataFrame
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values("company_id").reset_index(drop=True)

# --------------------------------------------------
# Preview
# --------------------------------------------------

print()
print("Total Companies Processed :", len(results_df))

print()
print("=" * 50)
print("CASH FLOW INTELLIGENCE")
print("=" * 50)

print(
    results_df[
        [
            "company_id",
            "cfo_quality_label",
            "capex_label",
            "capital_allocation_label",
            "distress_flag",
            "deleveraging_flag",
        ]
    ].head(20)
)

# --------------------------------------------------
# Save Cash Flow Intelligence Excel
# --------------------------------------------------

excel_file = os.path.join(OUTPUT_DIR, "cashflow_intelligence.xlsx")

results_df.to_excel(excel_file, index=False)

print()
print("Saved :", excel_file)

# --------------------------------------------------
# Distress Alerts
# --------------------------------------------------

distress_df = results_df[results_df["distress_flag"] == True].copy()

distress_file = os.path.join(OUTPUT_DIR, "distress_alerts.csv")

distress_df.to_csv(distress_file, index=False)

print("Saved :", distress_file)

print("Distress Companies :", len(distress_df))

# --------------------------------------------------
# CFO Quality Distribution
# --------------------------------------------------

print()
print("=" * 50)
print("CFO QUALITY DISTRIBUTION")
print("=" * 50)

print(results_df["cfo_quality_label"].value_counts(dropna=False))

# --------------------------------------------------
# CapEx Distribution
# --------------------------------------------------

print()
print("=" * 50)
print("CAPEX DISTRIBUTION")
print("=" * 50)

print(results_df["capex_label"].value_counts(dropna=False))

# --------------------------------------------------
# Capital Allocation Distribution
# --------------------------------------------------

print()
print("=" * 50)
print("CAPITAL ALLOCATION DISTRIBUTION")
print("=" * 50)

print(results_df["capital_allocation_label"].value_counts(dropna=False))

# --------------------------------------------------
# Summary
# --------------------------------------------------

print()
print("=" * 50)
print("SUMMARY")
print("=" * 50)

print("Companies :", len(results_df))

print("High Quality :", (results_df["cfo_quality_label"] == "High Quality").sum())

print("Moderate :", (results_df["cfo_quality_label"] == "Moderate").sum())

print("Accrual Risk :", (results_df["cfo_quality_label"] == "Accrual Risk").sum())

print("Distress Companies :", results_df["distress_flag"].sum())

print("Deleveraging Companies :", results_df["deleveraging_flag"].sum())

print()

# --------------------------------------------------
# Pattern Changes Report
# --------------------------------------------------

capital_df = pd.read_csv("output/capital_allocation.csv")

capital_df["year_num"] = capital_df["year"].astype(str).str.extract(r"(\d{4}|\d{2})")[0]


def convert_year(y):
    if pd.isna(y):
        return None

    y = str(y)

    if len(y) == 2:
        return 2000 + int(y)

    return int(y)


capital_df["year_num"] = capital_df["year_num"].apply(convert_year)

capital_df = capital_df.sort_values(["company_id", "year_num"])

changes = []

for company, group in capital_df.groupby("company_id"):

    if len(group) < 2:
        continue

    previous = group.iloc[-2]
    latest = group.iloc[-1]

    if previous["pattern_label"] != latest["pattern_label"]:

        changes.append(
            {
                "company_id": company,
                "previous_year": previous["year"],
                "previous_pattern": previous["pattern_label"],
                "latest_year": latest["year"],
                "latest_pattern": latest["pattern_label"],
            }
        )

changes_df = pd.DataFrame(changes)

changes_df.to_csv("output/pattern_changes.csv", index=False)

print()
print("=" * 50)
print("PATTERN CHANGES")
print("=" * 50)

print("Companies Changed :", len(changes_df))

print()

print(changes_df.head(20))

print()

print("Saved : output/pattern_changes.csv")
