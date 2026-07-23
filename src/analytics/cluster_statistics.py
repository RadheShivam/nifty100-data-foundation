import os
import warnings
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd


from scipy.stats import zscore
import numpy as np

warnings.filterwarnings("ignore")

# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

cluster_file = os.path.join(OUTPUT_DIR, "cluster_labels.csv")

profile_file = os.path.join(OUTPUT_DIR, "cluster_profile.csv")

# ==========================================================
# LOAD DATA
# ==========================================================

print("=" * 60)
print("Cluster Statistics")
print("=" * 60)

df = pd.read_csv(cluster_file)

print("Companies Loaded :", len(df))

# ==========================================================
# FEATURES
# ==========================================================

FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
]

# ==========================================================
# MEAN
# ==========================================================

mean_stats = df.groupby("cluster")[FEATURES].mean()

mean_stats.columns = [c + "_mean" for c in mean_stats.columns]

# ==========================================================
# MEDIAN
# ==========================================================

median_stats = df.groupby("cluster")[FEATURES].median()

median_stats.columns = [c + "_median" for c in median_stats.columns]

# ==========================================================
# COMPANY COUNT
# ==========================================================

company_count = df.groupby("cluster").size().rename("company_count")

# ==========================================================
# DOMINANT SECTOR
# ==========================================================

dominant_sector = (
    df.groupby("cluster")["broad_sector"]
    .agg(lambda x: x.mode().iloc[0])
    .rename("dominant_sector")
)

# ==========================================================
# MERGE
# ==========================================================

profile = pd.concat([company_count, dominant_sector, mean_stats, median_stats], axis=1)

profile = profile.round(2)

# ==========================================================
# SAVE
# ==========================================================

profile.to_csv(profile_file)

print()

print(profile)

print()

print("Saved")

print(profile_file)

print("=" * 60)


# ==========================================================
# ASSIGN CLUSTER NAMES
# ==========================================================

print("\nAssigning Cluster Names...")
print("=" * 60)

cluster_names = {}

for cluster in profile.index:

    row = profile.loc[cluster]

    roe = row["return_on_equity_pct_mean"]
    de = row["debt_to_equity_mean"]
    growth = row["revenue_cagr_5yr_mean"]
    fcf = row["free_cash_flow_cr_mean"]
    opm = row["operating_profit_margin_pct_mean"]

    # -----------------------------
    # Rule-based naming
    # -----------------------------

    if roe >= 20 and opm >= 30 and fcf > 0:
        name = "High-Quality Compounders"

    elif growth >= 15 and de < 1:
        name = "Emerging Growth"

    elif de >= 3:
        name = "High Leverage"

    elif fcf < 0:
        name = "Distressed / Turnaround"

    elif opm >= 25:
        name = "High Margin Businesses"

    else:
        name = "Value Cyclicals"

    cluster_names[cluster] = name

# ==========================================================
# ADD CLUSTER NAME
# ==========================================================

df["cluster_name"] = df["cluster"].map(cluster_names)

profile["cluster_name"] = profile.index.map(cluster_names)

# Put cluster name first

cols = ["cluster_name"] + [c for c in profile.columns if c != "cluster_name"]

profile = profile[cols]

# ==========================================================
# SAVE UPDATED FILES
# ==========================================================

df.to_csv(cluster_file, index=False)

profile.to_csv(profile_file)

print("\nAssigned Cluster Names")

for cid, name in cluster_names.items():
    print(f"Cluster {cid} -> {name}")

print("\nUpdated")

print(cluster_file)
print(profile_file)

# ==========================================================
# FINAL SUMMARY
# ==========================================================

print("\nCluster Summary")
print("=" * 60)

summary = profile[["cluster_name", "company_count", "dominant_sector"]]

print(summary)

print("=" * 60)


# ==========================================================
# PART 3 : CORRELATION HEATMAP
# ==========================================================

print("\nGenerating Correlation Heatmap...")
print("=" * 60)

DB_PATH = os.path.join(PROJECT_ROOT, "db", "nifty100.db")

REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")

os.makedirs(REPORT_DIR, exist_ok=True)

print(DB_PATH)
print(os.path.exists(DB_PATH))

conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn,
)

conn.close()

# ----------------------------------------------------------
# Latest Annual Record Only
# ----------------------------------------------------------

annual = ratios[~ratios["year"].astype(str).str.upper().eq("TTM")].copy()

annual["year_num"] = annual["year"].astype(str).str.extract(r"(\d{4})")[0].astype(float)

latest = annual.sort_values("year_num").groupby("company_id").tail(1)

# ----------------------------------------------------------
# 10 KPI Columns
# ----------------------------------------------------------

KPI_COLUMNS = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "debt_to_equity",
    "current_ratio",
    "interest_coverage_ratio",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
]

available = [c for c in KPI_COLUMNS if c in latest.columns]

corr = latest[available].corr(method="pearson")

plt.figure(figsize=(10, 8))

sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)

plt.title("Pearson Correlation Matrix")

plt.tight_layout()

heatmap_path = os.path.join(REPORT_DIR, "correlation_heatmap.png")

plt.savefig(heatmap_path, dpi=300)

plt.close()

print("Saved:", heatmap_path)
print("=" * 60)


# ==========================================================
# PART 4 : OUTLIER DETECTION & PORTFOLIO STATISTICS
# ==========================================================


print("\nGenerating Outlier Report...")
print("=" * 60)


# ----------------------------------------------------------
# Load company information from cluster_labels.csv
# ----------------------------------------------------------

cluster_info = pd.read_csv(cluster_file)[["company_id", "company_name", "broad_sector"]]

analysis_df = latest.merge(cluster_info, on="company_id", how="left")
# ----------------------------------------------------------
# KPIs for Analysis
# ----------------------------------------------------------

KPI_COLUMNS = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "debt_to_equity",
    "current_ratio",
    "interest_coverage_ratio",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
]

available = [c for c in KPI_COLUMNS if c in analysis_df.columns]

# ----------------------------------------------------------
# Sector-wise Z-score
# ----------------------------------------------------------

zscore_cols = []

for col in available:

    z_col = col + "_z"

    analysis_df[z_col] = analysis_df.groupby("broad_sector")[col].transform(
        lambda x: zscore(x, nan_policy="omit") if len(x) > 1 else np.nan
    )

    zscore_cols.append(z_col)

# ----------------------------------------------------------
# Outlier Flag
# ----------------------------------------------------------

analysis_df["is_outlier"] = analysis_df[zscore_cols].abs().gt(3).any(axis=1)

outliers = analysis_df[analysis_df["is_outlier"]].copy()

outlier_file = os.path.join(OUTPUT_DIR, "outlier_report.csv")

outliers.to_csv(outlier_file, index=False)

print("Outliers Found :", len(outliers))
print("Saved :", outlier_file)

# ==========================================================
# PORTFOLIO STATISTICS
# ==========================================================

print("\nGenerating Portfolio Statistics...")
print("=" * 60)

stats = []

for col in available:

    s = analysis_df[col].dropna()

    stats.append(
        {
            "KPI": col,
            "P10": s.quantile(0.10),
            "P25": s.quantile(0.25),
            "P50": s.quantile(0.50),
            "P75": s.quantile(0.75),
            "P90": s.quantile(0.90),
            "Mean": s.mean(),
            "Std": s.std(),
        }
    )

portfolio_stats = pd.DataFrame(stats)

portfolio_stats = portfolio_stats.round(2)

portfolio_file = os.path.join(OUTPUT_DIR, "portfolio_stats.csv")

portfolio_stats.to_csv(portfolio_file, index=False)

print("Saved :", portfolio_file)

print("\nDay 37 Completed Successfully!")
print("=" * 60)
