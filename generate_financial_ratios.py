import sqlite3
import pandas as pd

from src.etl.loader import (
    load_profitandloss,
    load_balancesheet,
    load_cashflow
)

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover
)

from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity
)

# -----------------------------
# Load data
# -----------------------------

profit_df = load_profitandloss()
balance_df = load_balancesheet()
cashflow_df = load_cashflow()

# -----------------------------
# Merge Profit & Balance Sheet
# -----------------------------

merged_df = profit_df.merge(
    balance_df,
    on=["company_id", "year"],
    how="inner",
    suffixes=("_pl", "_bs")
)

# -----------------------------
# Merge Cash Flow
# -----------------------------

merged_df = merged_df.merge(
    cashflow_df,
    on=["company_id", "year"],
    how="inner"
)

# -----------------------------
# Sort data
# -----------------------------

merged_df = merged_df.sort_values(
    ["company_id", "year"]
).reset_index(drop=True)

# -----------------------------
# Create CAGR columns
# -----------------------------

merged_df["revenue_cagr_5yr"] = None
merged_df["revenue_cagr_5yr_flag"] = None

merged_df["pat_cagr_5yr"] = None
merged_df["pat_cagr_5yr_flag"] = None

merged_df["eps_cagr_5yr"] = None
merged_df["eps_cagr_5yr_flag"] = None

print("Merged rows:", len(merged_df))
print(merged_df.columns.tolist())


# ----------------------------------------
# Calculate 5-Year CAGR for each company
# ----------------------------------------

for company, group in merged_df.groupby("company_id"):

    group = group.sort_values("year").reset_index()

    for i in range(5, len(group)):

        # Revenue CAGR
        revenue_value, revenue_flag = revenue_cagr(
            group.loc[i - 5, "sales"],
            group.loc[i, "sales"],
            5
        )

        merged_df.loc[
            group.loc[i, "index"],
            "revenue_cagr_5yr"
        ] = revenue_value

        merged_df.loc[
            group.loc[i, "index"],
            "revenue_cagr_5yr_flag"
        ] = revenue_flag

        # PAT CAGR
        pat_value, pat_flag = pat_cagr(
            group.loc[i - 5, "net_profit"],
            group.loc[i, "net_profit"],
            5
        )

        merged_df.loc[
            group.loc[i, "index"],
            "pat_cagr_5yr"
        ] = pat_value

        merged_df.loc[
            group.loc[i, "index"],
            "pat_cagr_5yr_flag"
        ] = pat_flag

        # EPS CAGR
        eps_value, eps_flag = eps_cagr(
            group.loc[i - 5, "eps"],
            group.loc[i, "eps"],
            5
        )

        merged_df.loc[
            group.loc[i, "index"],
            "eps_cagr_5yr"
        ] = eps_value

        merged_df.loc[
            group.loc[i, "index"],
            "eps_cagr_5yr_flag"
        ] = eps_flag


rows = []

for _, row in merged_df.iterrows():

    # -------------------------
    # Profitability Ratios
    # -------------------------

    npm = net_profit_margin(
        row["net_profit"],
        row["sales"]
    )

    opm, _ = operating_profit_margin(
        row["operating_profit"],
        row["sales"],
        row["opm_percentage"]
    )

    roe = return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    )

    # -------------------------
    # Leverage & Efficiency
    # -------------------------

    de = debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"]
    )

    interest_cov, _, _ = interest_coverage_ratio(
        row["operating_profit"],
        row["other_income"],
        row["interest"]
    )

    turnover = asset_turnover(
        row["sales"],
        row["total_assets"]
    )

    # -------------------------
    # Cash Flow KPIs
    # -------------------------

    fcf = free_cash_flow(
        row["operating_activity"],
        row["investing_activity"]
    )

    capex, _ = capex_intensity(
        row["investing_activity"],
        row["sales"]
    )

    # -------------------------
    # Other KPIs
    # -------------------------

    eps = row["eps"]

    if row["equity_capital"] != 0:
        book_value = (
            row["equity_capital"] +
            row["reserves"]
        ) / row["equity_capital"]
    else:
        book_value = None

    dividend = row["dividend_payout"]

    total_debt = row["borrowings"]

    cfo = row["operating_activity"]

    # -------------------------
    # CAGR (Already Calculated)
    # -------------------------

    revenue_5yr = row["revenue_cagr_5yr"]
    revenue_5yr_flag = row["revenue_cagr_5yr_flag"]

    pat_5yr = row["pat_cagr_5yr"]
    pat_5yr_flag = row["pat_cagr_5yr_flag"]

    eps_5yr = row["eps_cagr_5yr"]
    eps_5yr_flag = row["eps_cagr_5yr_flag"]

    # -------------------------
    # Composite Quality Score
    # -------------------------

    quality_score = 0

    if roe is not None and roe > 15:
        quality_score += 1

    if de is not None and de < 1:
        quality_score += 1

    if interest_cov is not None and interest_cov > 3:
        quality_score += 1

    if npm is not None and npm > 10:
        quality_score += 1

    rows.append({

        "company_id": row["company_id"],
        "year": row["year"],

        "net_profit_margin_pct": npm,
        "operating_profit_margin_pct": opm,
        "return_on_equity_pct": roe,

        "debt_to_equity": de,
        "interest_coverage": interest_cov,
        "asset_turnover": turnover,

        "free_cash_flow_cr": fcf,
        "capex_cr": capex,

        "earnings_per_share": eps,
        "book_value_per_share": book_value,
        "dividend_payout_ratio_pct": dividend,

        "total_debt_cr": total_debt,
        "cash_from_operations_cr": cfo,

        "revenue_cagr_5yr": revenue_5yr,
        "revenue_cagr_5yr_flag": revenue_5yr_flag,

        "pat_cagr_5yr": pat_5yr,
        "pat_cagr_5yr_flag": pat_5yr_flag,

        "eps_cagr_5yr": eps_5yr,
        "eps_cagr_5yr_flag": eps_5yr_flag,

        "composite_quality_score": quality_score
    })

ratio_df = pd.DataFrame(rows)

print(ratio_df.head())
print("Generated KPI rows:", len(ratio_df))








# -------------------------------
# Save KPIs into SQLite
# -------------------------------

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

# Clear existing data
cursor.execute("DELETE FROM financial_ratios")

for _, row in ratio_df.iterrows():

    cursor.execute("""
    INSERT INTO financial_ratios (
        company_id,
        year,

        net_profit_margin_pct,
        operating_profit_margin_pct,
        return_on_equity_pct,

        debt_to_equity,
        interest_coverage,
        asset_turnover,

        free_cash_flow_cr,
        capex_cr,

        earnings_per_share,
        book_value_per_share,
        dividend_payout_ratio_pct,

        total_debt_cr,
        cash_from_operations_cr,

        revenue_cagr_5yr,
        revenue_cagr_5yr_flag,

        pat_cagr_5yr,
        pat_cagr_5yr_flag,

        eps_cagr_5yr,
        eps_cagr_5yr_flag,

        composite_quality_score
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["company_id"],
        row["year"],

        row["net_profit_margin_pct"],
        row["operating_profit_margin_pct"],
        row["return_on_equity_pct"],

        row["debt_to_equity"],
        row["interest_coverage"],
        row["asset_turnover"],

        row["free_cash_flow_cr"],
        row["capex_cr"],

        row["earnings_per_share"],
        row["book_value_per_share"],
        row["dividend_payout_ratio_pct"],

        row["total_debt_cr"],
        row["cash_from_operations_cr"],

        row["revenue_cagr_5yr"],
        row["revenue_cagr_5yr_flag"],

        row["pat_cagr_5yr"],
        row["pat_cagr_5yr_flag"],

        row["eps_cagr_5yr"],
        row["eps_cagr_5yr_flag"],

        row["composite_quality_score"]
    ))

conn.commit()

count = cursor.execute(
    "SELECT COUNT(*) FROM financial_ratios"
).fetchone()[0]

print(f"✅ financial_ratios table populated with {count} rows")

conn.close()