import os
import sqlite3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.etl.loader import load_peer_groups

# -----------------------------
# Load Peer Groups
# -----------------------------

peer_df = load_peer_groups()

# -----------------------------
# Load Financial Ratios
# -----------------------------

conn = sqlite3.connect("db/nifty100.db")

ratio_df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

print("Peer Groups:", peer_df.shape)
print("Financial Ratios:", ratio_df.shape)

# -----------------------------
# Merge Peer Groups
# -----------------------------

radar_df = ratio_df.merge(
    peer_df[
        [
            "company_id",
            "peer_group_name",
            "is_benchmark"
        ]
    ],
    on="company_id",
    how="left"
)

radar_df["peer_group_name"] = (
    radar_df["peer_group_name"]
    .fillna("No peer group assigned")
)

print("\nMerged Shape:", radar_df.shape)

print(
    radar_df[
        [
            "company_id",
            "peer_group_name",
            "year"
        ]
    ].head(20)
)

# -----------------------------
# Radar Metrics
# -----------------------------

radar_metrics = [
    "return_on_equity_pct",
    "roce_percentage",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score"
]

print("\nRadar Metrics:")
print(radar_metrics)

# -----------------------------
# Companies List
# -----------------------------

companies = sorted(
    radar_df["company_id"].unique()
)

print("\nTotal Companies:", len(companies))

# -----------------------------
# Create Output Folder
# -----------------------------

os.makedirs(
    "reports/radar_charts",
    exist_ok=True
)

# -----------------------------
# Generate Radar Chart For Every Company
# -----------------------------

for test_company in companies:

    company_df = radar_df[
        radar_df["company_id"] == test_company
    ].sort_values("year")

    if company_df.empty:
        continue

    latest_company = company_df.iloc[-1]

    peer_group = latest_company["peer_group_name"]

    # -----------------------------
    # Peer Average
    # -----------------------------

    if peer_group == "No peer group assigned":

        peer_latest = radar_df[
            radar_df["year"] == latest_company["year"]
        ]

    else:

        peer_latest = radar_df[
            (radar_df["peer_group_name"] == peer_group)
            &
            (radar_df["year"] == latest_company["year"])
        ]

    company_values = (
        latest_company[radar_metrics]
        .fillna(0)
        .astype(float)
        .tolist()
    )

    peer_average = (
        peer_latest[radar_metrics]
        .mean()
        .fillna(0)
        .tolist()
    )

    print(f"\nGenerating radar for {test_company}")

        # -----------------------------
    # Radar Labels
    # -----------------------------

    labels = [
        "ROE",
        "ROCE",
        "NPM",
        "D/E",
        "FCF",
        "PAT CAGR",
        "Revenue CAGR",
        "Composite"
    ]

    # -----------------------------
    # Create Angles
    # -----------------------------

    num_vars = len(labels)

    angles = np.linspace(
        0,
        2 * np.pi,
        num_vars,
        endpoint=False
    ).tolist()

    angles += angles[:1]

    # -----------------------------
    # Close the Polygon
    # -----------------------------

    company_plot = company_values + [company_values[0]]
    peer_plot = peer_average + [peer_average[0]]

    # -----------------------------
    # Create Figure
    # -----------------------------

    fig = plt.figure(figsize=(8, 8))

    ax = plt.subplot(
        111,
        polar=True
    )

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(
        angles[:-1],
        labels,
        fontsize=10
    )

    # -----------------------------
    # Plot Company
    # -----------------------------

    ax.plot(
        angles,
        company_plot,
        linewidth=2,
        label=test_company
    )

    ax.fill(
        angles,
        company_plot,
        alpha=0.25
    )

    # -----------------------------
    # Plot Peer Average
    # -----------------------------

    ax.plot(
        angles,
        peer_plot,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
    )

    # -----------------------------
    # Title
    # -----------------------------

    plt.title(
        f"{test_company} Radar Chart ({peer_group})",
        pad=20
    )

    plt.legend(
        loc="upper right",
        bbox_to_anchor=(1.3, 1.1)
    )

    # -----------------------------
    # Save Chart
    # -----------------------------

    output_file = os.path.join(
        "reports",
        "radar_charts",
        f"{test_company}_radar.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"✅ {test_company} radar chart saved.")

# -----------------------------
# Finished
# -----------------------------

print("\n🎉 All radar charts generated successfully.")