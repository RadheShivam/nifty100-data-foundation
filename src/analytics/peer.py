import sqlite3
import pandas as pd

from src.etl.loader import load_peer_groups

# -----------------------------
# Load Peer Groups
# -----------------------------

peer_df = load_peer_groups()

# -----------------------------
# Load Financial Ratios
# -----------------------------

conn = sqlite3.connect("db/nifty100.db")

ratio_df = pd.read_sql("SELECT * FROM financial_ratios", conn)

conn.close()

print("Peer Groups:", peer_df.shape)
print("Financial Ratios:", ratio_df.shape)

print(peer_df.head())
print(ratio_df.head())

# -----------------------------
# Merge Peer Groups
# -----------------------------

peer_ratio_df = ratio_df.merge(
    peer_df[["company_id", "peer_group_name", "is_benchmark"]],
    on="company_id",
    how="left",
)

# -----------------------------
# Handle companies with no peer group
# -----------------------------

peer_ratio_df["peer_group_name"] = peer_ratio_df["peer_group_name"].fillna(
    "No peer group assigned"
)

print("\nMerged Shape:", peer_ratio_df.shape)

print(peer_ratio_df[["company_id", "peer_group_name", "is_benchmark"]].head(20))

# -----------------------------
# Metrics to Rank
# -----------------------------

metrics = {
    "ROE": "return_on_equity_pct",
    "ROCE": "roce_percentage",
    "Net Profit Margin": "net_profit_margin_pct",
    "Debt to Equity": "debt_to_equity",
    "Free Cash Flow": "free_cash_flow_cr",
    "PAT CAGR 5Y": "pat_cagr_5yr",
    "Revenue CAGR 5Y": "revenue_cagr_5yr",
    "EPS CAGR 5Y": "eps_cagr_5yr",
    "Interest Coverage": "interest_coverage",
    "Asset Turnover": "asset_turnover",
}

print(metrics)

# -----------------------------
# Calculate Peer Percentiles
# -----------------------------

peer_results = []

for peer_group in peer_ratio_df["peer_group_name"].unique():

    if peer_group == "No peer group assigned":
        print("No peer group assigned")
        continue

    group_df = peer_ratio_df[peer_ratio_df["peer_group_name"] == peer_group].copy()

    for metric_name, column in metrics.items():

        if column not in group_df.columns:
            continue

        percentile = group_df[column].rank(pct=True, method="average")

        # Lower D/E is better
        if metric_name == "Debt to Equity":
            percentile = 1 - percentile

        group_df["percentile_rank"] = (percentile * 100).round(2)

        for _, row in group_df.iterrows():

            peer_results.append(
                {
                    "company_id": row["company_id"],
                    "peer_group_name": peer_group,
                    "metric": metric_name,
                    "value": row[column],
                    "percentile_rank": row["percentile_rank"],
                    "year": row["year"],
                }
            )

peer_percentile_df = pd.DataFrame(peer_results)

print(peer_percentile_df.head(20))

print("\nTotal Rankings:", len(peer_percentile_df))

# -----------------------------
# Save Peer Percentiles
# -----------------------------

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("""
DROP TABLE IF EXISTS peer_percentiles
""")

cursor.execute("""
CREATE TABLE peer_percentiles (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    peer_group_name TEXT,
    metric TEXT,
    value REAL,
    percentile_rank REAL,
    year TEXT

)
""")

peer_percentile_df.to_sql("peer_percentiles", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print(f"✅ peer_percentiles table created with {len(peer_percentile_df)} rows.")
