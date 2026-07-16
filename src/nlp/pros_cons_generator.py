




import os
import sqlite3
import pandas as pd

# ---------------------------------------
# Paths
# ---------------------------------------

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------
# Database Connection
# ---------------------------------------

conn = sqlite3.connect(DB_PATH)

# ---------------------------------------
# Financial Ratios
# ---------------------------------------

ratios_df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)

# ---------------------------------------
# Market Cap
# ---------------------------------------

market_df = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        market_cap_crore,
        pe_ratio,
        pb_ratio,
        dividend_yield_pct
    FROM marketcap
    """,
    conn
)

# ---------------------------------------
# Companies
# ---------------------------------------

companies_df = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    """,
    conn
)

# ---------------------------------------
# Sector Information
# ---------------------------------------

sector_df = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector,
        sub_sector
    FROM sectors
    """,
    conn
)

# ---------------------------------------
# Balance Sheet
# ---------------------------------------

balance_df = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        borrowings,
        total_assets
    FROM balancesheet
    """,
    conn
)

conn.close()

# ---------------------------------------
# Prepare Financial Ratios
# ---------------------------------------

ratios_df["year_num"] = (
    ratios_df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
    .astype(float)
)

# ---------------------------------------
# Historical Annual Data
# ---------------------------------------

history_df = (
    ratios_df[
        ratios_df["year"] != "TTM"
    ]
    .copy()
)

history_df = history_df.sort_values(
    [
        "company_id",
        "year_num"
    ]
)

# ---------------------------------------
# Latest Annual Record
# ---------------------------------------

latest_df = (
    history_df
    .groupby("company_id")
    .tail(1)
)

# ---------------------------------------
# Prepare Balance Sheet History
# ---------------------------------------

balance_df["year_num"] = (
    balance_df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
    .astype(float)
)

balance_df = balance_df.sort_values(
    [
        "company_id",
        "year_num"
    ]
)

# ---------------------------------------
# Merge Latest Data
# ---------------------------------------

latest_df = latest_df.merge(
    market_df,
    on=["company_id", "year"],
    how="left"
)

latest_df = latest_df.merge(
    companies_df,
    on="company_id",
    how="left"
)

latest_df = latest_df.merge(
    sector_df,
    on="company_id",
    how="left"
)


# ---------------------------------------
# Preview
# ---------------------------------------

print("=" * 50)
print("LATEST COMPANY DATA")
print("=" * 50)

print()

print("Companies :", len(latest_df))

print()

print(latest_df.head())

latest_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "latest_company_data.csv"
    ),
    index=False
)

print()

print("Saved : output/latest_company_data.csv")

# --------------------------------------------------
# Initialize Lists
# --------------------------------------------------

pros = []
cons = []

# --------------------------------------------------
# Pro Rules
# --------------------------------------------------

for _, row in latest_df.iterrows():

    company = row["company_id"]

    # -------------------------------
    # Rule P1 : ROE > 20%
    # -------------------------------

    if (
        pd.notna(row["return_on_equity_pct"])
        and row["return_on_equity_pct"] > 20
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P1",
            "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
            "confidence_pct": 95

        })

    # -------------------------------
    # Rule P2 : Positive Free Cash Flow
    # -------------------------------

    if (
        pd.notna(row["free_cash_flow_cr"])
        and row["free_cash_flow_cr"] > 0
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P2",
            "text": "Strong free cash flow generation indicates healthy business fundamentals.",
            "confidence_pct": 90

        })

    # -------------------------------
    # Rule P3 : Debt Free
    # -------------------------------

    if (
        pd.notna(row["debt_to_equity"])
        and row["debt_to_equity"] == 0
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P3",
            "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",
            "confidence_pct": 92

        })

    # -------------------------------
    # Rule P4 : Revenue CAGR > 15%
    # -------------------------------

    if (
        pd.notna(row["revenue_cagr_5yr"])
        and row["revenue_cagr_5yr"] > 15
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P4",
            "text": "Revenue growing above 15% CAGR over 5 years reflects strong business momentum.",
            "confidence_pct": 88

        })

    # -------------------------------
    # Rule P5 : OPM > 25%
    # -------------------------------

    if (
        pd.notna(row["operating_profit_margin_pct"])
        and row["operating_profit_margin_pct"] > 25
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P5",
            "text": "Operating profit margin above 25% indicates strong pricing power and cost discipline.",
            "confidence_pct": 90

        })

    # -------------------------------
    # Rule P6 : PAT CAGR > 20%
    # -------------------------------

    if (
        pd.notna(row["pat_cagr_5yr"])
        and row["pat_cagr_5yr"] > 20
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P6",
            "text": "Net profit compounding above 20% over 5 years creates significant shareholder value.",
            "confidence_pct": 92

        })

    # -------------------------------
    # Rule P7 : Interest Coverage > 10
    # -------------------------------

    if (
        (
            pd.notna(row["interest_coverage"])
            and row["interest_coverage"] > 10
        )
        or
        (
            pd.notna(row["debt_to_equity"])
            and row["debt_to_equity"] == 0
        )
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P7",
            "text": "Very high interest coverage ratio reflects negligible financial stress from debt servicing.",
            "confidence_pct": 90

        })

    # -------------------------------
    # Rule P8 : Dividend + Positive FCF
    # -------------------------------

    if (
        pd.notna(row["dividend_yield_pct"])
        and row["dividend_yield_pct"] > 2
        and pd.notna(row["free_cash_flow_cr"])
        and row["free_cash_flow_cr"] > 0
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P8",
            "text": "Consistent dividend yield above 2% backed by positive free cash flow.",
            "confidence_pct": 85

        })

    # -------------------------------
    # Rule P9 : EPS CAGR > 15%
    # -------------------------------

    if (
        pd.notna(row["eps_cagr_5yr"])
        and row["eps_cagr_5yr"] > 15
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P9",
            "text": "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding.",
            "confidence_pct": 90

        })

    # -------------------------------
    # Rule P11 : PAT CAGR > Revenue CAGR
    # -------------------------------

    if (
        pd.notna(row["revenue_cagr_5yr"])
        and pd.notna(row["pat_cagr_5yr"])
        and row["pat_cagr_5yr"] > row["revenue_cagr_5yr"]
    ):

        pros.append({

            "company_id": company,
            "type": "pro",
            "rule_id": "P11",
            "text": "Revenue growing slower than profits shows improving operating leverage and scale benefits.",
            "confidence_pct": 86

        })

# --------------------------------------------------
# Con Rules
# --------------------------------------------------

for _, row in latest_df.iterrows():

    company = row["company_id"]

    # -------------------------------
    # Rule C1 : High Debt
    # -------------------------------

    if (
        pd.notna(row["debt_to_equity"])
        and row["debt_to_equity"] > 2
        and row["broad_sector"] != "Financials"
    ):

        cons.append({

            "company_id": company,
            "type": "con",
            "rule_id": "C1",
            "text": f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} is elevated for a non-financial company and warrants monitoring.",
            "confidence_pct": 90

        })

    # -------------------------------
    # Rule C2 : Negative Free Cash Flow
    # -------------------------------

    if (
        pd.notna(row["free_cash_flow_cr"])
        and row["free_cash_flow_cr"] < 0
    ):

        cons.append({

            "company_id": company,
            "type": "con",
            "rule_id": "C2",
            "text": "Negative free cash flow raises concern about cash generation quality.",
            "confidence_pct": 85

        })

    # -------------------------------
    # Rule C3 : Negative Net Profit Margin
    # -------------------------------

    if (
        pd.notna(row["net_profit_margin_pct"])
        and row["net_profit_margin_pct"] < 0
    ):

        cons.append({

            "company_id": company,
            "type": "con",
            "rule_id": "C3",
            "text": "Company reported a negative net profit margin in the latest financial year.",
            "confidence_pct": 95

        })

    # -------------------------------
    # Rule C4 : ROCE < 10%
    # -------------------------------

    if (
        pd.notna(row["roce_percentage"])
        and row["roce_percentage"] < 10
    ):

        cons.append({

            "company_id": company,
            "type": "con",
            "rule_id": "C4",
            "text": "Return on capital employed below 10% suggests weak capital efficiency.",
            "confidence_pct": 88

        })

    # -------------------------------
    # Rule C8 : High Debt
    # -------------------------------

    if (
        pd.notna(row["debt_to_equity"])
        and row["debt_to_equity"] > 1.5
    ):

        cons.append({

            "company_id": company,
            "type": "con",
            "rule_id": "C8",
            "text": "Debt-to-equity ratio is elevated and should be monitored.",
            "confidence_pct": 80

        })

# --------------------------------------------------
# Historical Rules
# --------------------------------------------------

for company in latest_df["company_id"]:

    hist = (
        history_df[
            history_df["company_id"] == company
        ]
        .sort_values("year_num")
        .tail(3)
    )

# --------------------------------------------------
# Default Pro Rule
# --------------------------------------------------

companies_with_pro = {x["company_id"] for x in pros}

for company in latest_df["company_id"]:

    if company not in companies_with_pro:

        pros.append({

            "company_id": company,

            "type": "pro",

            "rule_id": "P0",

            "text": "Business demonstrates stable financial performance with balanced operating metrics.",

            "confidence_pct": 65

        })

# --------------------------------------------------
# Default Con Rule
# --------------------------------------------------

companies_with_con = {x["company_id"] for x in cons}

for company in latest_df["company_id"]:

    if company not in companies_with_con:

        cons.append({

            "company_id": company,

            "type": "con",

            "rule_id": "C0",

            "text": "Some financial metrics require continued monitoring despite overall business stability.",

            "confidence_pct": 65

        })



    # -------------------------------
    # Rule P10 : ROE Improving
    # -------------------------------

    if len(hist) == 3:

        roe = hist["return_on_equity_pct"].tolist()

        if (
            pd.notna(roe[0])
            and pd.notna(roe[1])
            and pd.notna(roe[2])
            and roe[0] < roe[1] < roe[2]
        ):

            pros.append({

                "company_id": company,
                "type": "pro",
                "rule_id": "P10",
                "text": "Return on equity improving for three consecutive years shows strengthening business quality.",
                "confidence_pct": 90

            })

    # -------------------------------
    # Rule C9 : EPS Declining
    # -------------------------------

    if len(hist) == 3:

        eps = hist["earnings_per_share"].tolist()

        if (
            pd.notna(eps[0])
            and pd.notna(eps[1])
            and pd.notna(eps[2])
            and eps[0] > eps[1] > eps[2]
        ):

            cons.append({

                "company_id": company,
                "type": "con",
                "rule_id": "C9",
                "text": "Earnings per share declining for three consecutive years reflects deteriorating profitability.",
                "confidence_pct": 92

            })

    # -------------------------------
    # Rule P12 : Assets ↑ Borrowings ↓
    # -------------------------------

    bs = (
        balance_df[
            balance_df["company_id"] == company
        ]
        .sort_values("year_num")
        .tail(3)
    )

    if len(bs) == 3:

        assets = bs["total_assets"].tolist()
        debt = bs["borrowings"].tolist()

        if (
            assets[0] < assets[1] < assets[2]
            and debt[0] > debt[1] > debt[2]
        ):

            pros.append({

                "company_id": company,
                "type": "pro",
                "rule_id": "P12",
                "text": "Growing asset base funded by declining borrowings reflects self-sustaining growth.",
                "confidence_pct": 92

            })

# --------------------------------------------------
# Save Output
# --------------------------------------------------

pros_df = pd.DataFrame(pros)
cons_df = pd.DataFrame(cons)

final_df = pd.concat(
    [pros_df, cons_df],
    ignore_index=True
)

final_df = final_df.sort_values(
    ["company_id", "type", "rule_id"]
)

output_file = os.path.join(
    OUTPUT_DIR,
    "pros_cons_generated.csv"
)

final_df.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# Summary
# --------------------------------------------------

print()
print("=" * 50)
print("PROS & CONS GENERATED")
print("=" * 50)

print("Total Pros  :", len(pros_df))
print("Total Cons  :", len(cons_df))
print("Total Rules :", len(final_df))

print()
print(final_df.head(20))

print()
print("Output Saved :", output_file)