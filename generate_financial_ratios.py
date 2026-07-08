import sqlite3
import pandas as pd

from src.etl.loader import (
    load_companies,
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

companies_df = load_companies()

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
# Merge Company Data
# -----------------------------

merged_df = merged_df.merge(
    companies_df[
        [
            "id",
            "roce_percentage",
            "roe_percentage",
            "book_value"
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left",
    suffixes=("", "_company")
)

merged_df.drop(columns=["id_company"], inplace=True)



# -----------------------------
# Sort data
# -----------------------------

merged_df = merged_df.sort_values(
    ["company_id", "year"]
).reset_index(drop=True)


# -----------------------------
# Sort data
# -----------------------------

merged_df = merged_df.sort_values(
    ["company_id", "year"]
).reset_index(drop=True)

# -----------------------------
# Create CAGR columns
# -----------------------------


merged_df["revenue_cagr_3yr"] = None
merged_df["revenue_cagr_3yr_flag"] = None

merged_df["pat_cagr_3yr"] = None
merged_df["pat_cagr_3yr_flag"] = None

merged_df["eps_cagr_3yr"] = None
merged_df["eps_cagr_3yr_flag"] = None

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

    # ----------------------------------------
# Calculate 3-Year CAGR
# ----------------------------------------

    for i in range(3, len(group)):

        # Revenue CAGR
        revenue_value, revenue_flag = revenue_cagr(
            group.loc[i - 3, "sales"],
            group.loc[i, "sales"],
            3
        )

        merged_df.loc[
            group.loc[i, "index"],
            "revenue_cagr_3yr"
        ] = revenue_value

        merged_df.loc[
            group.loc[i, "index"],
            "revenue_cagr_3yr_flag"
        ] = revenue_flag

        # PAT CAGR
        pat_value, pat_flag = pat_cagr(
            group.loc[i - 3, "net_profit"],
            group.loc[i, "net_profit"],
            3
        )

        merged_df.loc[
            group.loc[i, "index"],
            "pat_cagr_3yr"
        ] = pat_value

        merged_df.loc[
            group.loc[i, "index"],
            "pat_cagr_3yr_flag"
        ] = pat_flag

        # EPS CAGR
        eps_value, eps_flag = eps_cagr(
            group.loc[i - 3, "eps"],
            group.loc[i, "eps"],
            3
        )

        merged_df.loc[
            group.loc[i, "index"],
            "eps_cagr_3yr"
        ] = eps_value

        merged_df.loc[
            group.loc[i, "index"],
            "eps_cagr_3yr_flag"
        ] = eps_flag

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

    # -------------------------
# Normalize Metric
# -------------------------

def normalize_metric(series, higher_is_better=True):
    """
    Normalize a metric to a 0–100 score using P10/P90 winsorisation.
    """

    p10 = series.quantile(0.10)
    p90 = series.quantile(0.90)

    clipped = series.clip(lower=p10, upper=p90)

    score = (clipped - p10) / (p90 - p10)

    if not higher_is_better:
        score = 1 - score

    return score.fillna(0) * 100


# -------------------------
# Main Processing
# -------------------------



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
    # CFO / PAT Ratio
    # -------------------------

    if row["net_profit"] is not None and row["net_profit"] != 0:
        cfo_pat_ratio = cfo / row["net_profit"]
    else:
        cfo_pat_ratio = None

    # -------------------------
    # CAGR (Already Calculated)
    # -------------------------
    revenue_3yr = row["revenue_cagr_3yr"]
    revenue_3yr_flag = row["revenue_cagr_3yr_flag"]

    pat_3yr = row["pat_cagr_3yr"]
    pat_3yr_flag = row["pat_cagr_3yr_flag"]

    eps_3yr = row["eps_cagr_3yr"]
    eps_3yr_flag = row["eps_cagr_3yr_flag"]

    revenue_5yr = row["revenue_cagr_5yr"]
    revenue_5yr_flag = row["revenue_cagr_5yr_flag"]

    pat_5yr = row["pat_cagr_5yr"]
    pat_5yr_flag = row["pat_cagr_5yr_flag"]

    eps_5yr = row["eps_cagr_5yr"]
    eps_5yr_flag = row["eps_cagr_5yr_flag"]

    # -------------------------
    # Composite Quality Score (Weighted)
    # -------------------------




    




    rows.append({

        "company_id": row["company_id"],
        "year": row["year"],

        "net_profit_margin_pct": npm,
        "operating_profit_margin_pct": opm,
        "return_on_equity_pct": roe,
        "roce_percentage": row["roce_percentage"],

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
        "cfo_pat_ratio": cfo_pat_ratio,

        # 3-Year CAGR
        "revenue_cagr_3yr": revenue_3yr,
        "revenue_cagr_3yr_flag": revenue_3yr_flag,

        "pat_cagr_3yr": pat_3yr,
        "pat_cagr_3yr_flag": pat_3yr_flag,

        "eps_cagr_3yr": eps_3yr,
        "eps_cagr_3yr_flag": eps_3yr_flag,

        # 5-Year CAGR
        "revenue_cagr_5yr": revenue_5yr,
        "revenue_cagr_5yr_flag": revenue_5yr_flag,

        "pat_cagr_5yr": pat_5yr,
        "pat_cagr_5yr_flag": pat_5yr_flag,

        "eps_cagr_5yr": eps_5yr,
        "eps_cagr_5yr_flag": eps_5yr_flag,

        # "composite_quality_score": None
        "composite_quality_score": 0,
        
    })

ratio_df = pd.DataFrame(rows)

print(ratio_df.columns.tolist())
rows = ratio_df.to_dict("records")

# -----------------------------
# Merge Sector Information
# -----------------------------

sector_df = pd.read_excel("data/supplementry/sectors.xlsx")

ratio_df = ratio_df.merge(
    sector_df[
        [
            "company_id",
            "broad_sector",
            "sub_sector"
        ]
    ],
    on="company_id",
    how="left"
)

print(
    ratio_df[
        [
            "company_id",
            "broad_sector",
            "sub_sector"
        ]
    ].head(10)
)


# -------------------------
# Normalize Metrics
# -------------------------

# -------------------------
# Normalize Metrics
# -------------------------

ratio_df["roe_score"] = normalize_metric(
    ratio_df["return_on_equity_pct"]
)

ratio_df["roce_score"] = normalize_metric(
    ratio_df["roce_percentage"]
)

ratio_df["npm_score"] = normalize_metric(
    ratio_df["net_profit_margin_pct"]
)

ratio_df["de_score"] = normalize_metric(
    ratio_df["debt_to_equity"],
    higher_is_better=False
)

ratio_df["interest_score"] = normalize_metric(
    ratio_df["interest_coverage"]
)

ratio_df["revenue_score"] = normalize_metric(
    ratio_df["revenue_cagr_5yr"]
)

ratio_df["pat_score"] = normalize_metric(
    ratio_df["pat_cagr_5yr"]
)

ratio_df["fcf_score"] = normalize_metric(
    ratio_df["free_cash_flow_cr"]
)

ratio_df["cfo_pat_score"] = normalize_metric(
    ratio_df["cfo_pat_ratio"]
)

# ==========================
# PASTE THE COMPOSITE SCORE HERE
# ==========================

ratio_df["composite_quality_score"] = (
    # Profitability (35%)
    ratio_df["roe_score"] * 0.15 +
    ratio_df["roce_score"] * 0.10 +
    ratio_df["npm_score"] * 0.10 +

    # Cash Quality (30%)
    ratio_df["fcf_score"] * 0.15 +
    ratio_df["cfo_pat_score"] * 0.10 +
    (ratio_df["free_cash_flow_cr"] > 0).astype(int) * 100 * 0.05 +

    # Growth (20%)
    ratio_df["revenue_score"] * 0.10 +
    ratio_df["pat_score"] * 0.10 +

    # Leverage (15%)
    ratio_df["de_score"] * 0.10 +
    ratio_df["interest_score"] * 0.05
).round(2)

# -----------------------------
# Sector Relative Composite Score
# -----------------------------

ratio_df["sector_relative_score"] = (
    ratio_df.groupby("broad_sector")["composite_quality_score"]
    .transform(
        lambda x: (
            (x - x.min()) /
            (x.max() - x.min())
        ) * 100
        if x.max() != x.min()
        else 50
    )
)

ratio_df["sector_relative_score"] = (
    ratio_df["sector_relative_score"].round(2)
)


print(
    ratio_df[
        [
            "company_id",
            "roe_score",
            "npm_score",
            "fcf_score",
            "revenue_score",
            "de_score",
            "interest_score",
            "composite_quality_score"
        ]
    ].head(10)
)

print(ratio_df[
    [
        "cfo_pat_ratio"
    ]
].describe())

print(ratio_df.head())
print("Generated KPI rows:", len(ratio_df))

print(merged_df[
    ["company_id", "year", "revenue_cagr_3yr"]
].tail(20))







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
        roce_percentage,

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
        cfo_pat_ratio,
        
        revenue_cagr_5yr,
        revenue_cagr_5yr_flag,

        pat_cagr_5yr,
        pat_cagr_5yr_flag,

        eps_cagr_5yr,
        eps_cagr_5yr_flag,
        
        revenue_cagr_3yr,
        revenue_cagr_3yr_flag,

        pat_cagr_3yr,
        pat_cagr_3yr_flag,

        eps_cagr_3yr,
        eps_cagr_3yr_flag,

        composite_quality_score,
        sector_relative_score
    )
    VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """, (
        row["company_id"],
        row["year"],

        row["net_profit_margin_pct"],
        row["operating_profit_margin_pct"],
        row["return_on_equity_pct"],
        row["roce_percentage"],

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
        row["cfo_pat_ratio"],

        row["revenue_cagr_5yr"],
        row["revenue_cagr_5yr_flag"],

        row["pat_cagr_5yr"],
        row["pat_cagr_5yr_flag"],

        row["eps_cagr_5yr"],
        row["eps_cagr_5yr_flag"],

        row["revenue_cagr_3yr"],
        row["revenue_cagr_3yr_flag"],

        row["pat_cagr_3yr"],
        row["pat_cagr_3yr_flag"],

        row["eps_cagr_3yr"],
        row["eps_cagr_3yr_flag"],

        row["composite_quality_score"],
        row["sector_relative_score"]
    ))

conn.commit()

count = cursor.execute(
    "SELECT COUNT(*) FROM financial_ratios"
).fetchone()[0]

print(f"✅ financial_ratios table populated with {count} rows")

conn.close()