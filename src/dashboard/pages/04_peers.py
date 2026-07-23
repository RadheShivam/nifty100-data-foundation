import os
import sys
import sqlite3

import pandas as pd
import streamlit as st

import plotly.graph_objects as go

# -------------------------------------------------
# Add Project Root
# -------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.dashboard.utils.db import (
    get_companies,
    get_ratios_by_year,
    get_sectors,
)

# -------------------------------------------------
# Database
# -------------------------------------------------

DB_PATH = "db/nifty100.db"

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Peer Comparison")

st.caption("Compare a company with other companies in the same peer group.")

# -------------------------------------------------
# Load Data
# -------------------------------------------------

companies_df = get_companies()

ratios_df = get_ratios_by_year("Mar 2024")

sectors_df = get_sectors()

# -------------------------------------------------
# Market Data
# -------------------------------------------------

conn = sqlite3.connect(DB_PATH)

market_df = pd.read_sql(
    """
    SELECT
        company_id,
        pe_ratio,
        pb_ratio,
        dividend_yield_pct
    FROM marketcap
    WHERE year = 2024
    """,
    conn,
)

conn.close()

# -------------------------------------------------
# Merge Data
# -------------------------------------------------

peer_df = ratios_df.merge(
    companies_df[
        [
            "id",
            "company_name",
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left",
)

peer_df = peer_df.merge(
    sectors_df[
        [
            "company_id",
            "broad_sector",
            "sub_sector",
        ]
    ],
    on="company_id",
    how="left",
)

peer_df = peer_df.merge(
    market_df,
    on="company_id",
    how="left",
)

# -------------------------------------------------
# Handle Missing Values
# -------------------------------------------------

numeric_cols = peer_df.select_dtypes(include="number").columns

peer_df[numeric_cols] = peer_df[numeric_cols].fillna(0)

# -------------------------------------------------
# Preview
# -------------------------------------------------

st.success(f"{len(peer_df)} companies loaded successfully.")

st.dataframe(
    peer_df.head(),
    use_container_width=True,
    hide_index=True,
)

# -------------------------------------------------
# Select Peer Group
# -------------------------------------------------

st.markdown("---")

st.subheader("🏢 Select Peer Group")

peer_groups = sorted(peer_df["broad_sector"].dropna().unique())

selected_group = st.selectbox("Choose Peer Group", peer_groups)

# -------------------------------------------------
# Filter Companies in Selected Group
# -------------------------------------------------

group_df = peer_df[peer_df["broad_sector"] == selected_group]

st.success(f"{len(group_df)} companies found in {selected_group}")

# -------------------------------------------------
# Select Company
# -------------------------------------------------

company_options = (group_df["company_id"] + " - " + group_df["company_name"]).tolist()

selected_company = st.selectbox("Choose Company", company_options)

selected_ticker = selected_company.split(" - ")[0]

company_data = group_df[group_df["company_id"] == selected_ticker].iloc[0]

# -------------------------------------------------
# Company Card
# -------------------------------------------------

st.markdown("---")

st.subheader("🏆 Selected Company")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Company:** {company_data['company_name']}")
    st.write(f"**Ticker:** {company_data['company_id']}")
    st.write(f"**Sector:** {company_data['broad_sector']}")
    st.write(f"**Sub Sector:** {company_data['sub_sector']}")

with col2:
    st.metric("ROE", f"{company_data['return_on_equity_pct']:.2f}%")

    st.metric("ROCE", f"{company_data['roce_percentage']:.2f}%")

    st.metric("PE", f"{company_data['pe_ratio']:.2f}")

    st.metric("PB", f"{company_data['pb_ratio']:.2f}")


# -------------------------------------------------
# Radar Chart
# -------------------------------------------------

st.markdown("---")

st.subheader("📊 Company vs Peer Group")

metrics = [
    "return_on_equity_pct",
    "roce_percentage",
    "net_profit_margin_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "operating_profit_margin_pct",
    "interest_coverage",
]

labels = [
    "ROE",
    "ROCE",
    "Net Margin",
    "Debt/Equity",
    "Revenue CAGR",
    "PAT CAGR",
    "OPM",
    "ICR",
]

company_values = [float(company_data[m]) for m in metrics]

peer_values = [float(group_df[m].mean()) for m in metrics]

# Close the radar chart
company_values.append(company_values[0])
peer_values.append(peer_values[0])
labels.append(labels[0])

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=labels,
        fill="toself",
        name=company_data["company_name"],
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=labels,
        fill="toself",
        name="Peer Average",
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
        )
    ),
    showlegend=True,
    title="Selected Company vs Peer Average",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# -------------------------------------------------
# Peer Comparison Table
# -------------------------------------------------

st.markdown("---")

st.subheader("📋 Peer Comparison Table")

comparison_columns = [
    "company_id",
    "company_name",
    "return_on_equity_pct",
    "roce_percentage",
    "net_profit_margin_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "operating_profit_margin_pct",
    "interest_coverage",
    "pe_ratio",
    "pb_ratio",
]

available_columns = [col for col in comparison_columns if col in group_df.columns]

comparison_df = group_df[available_columns].copy()

comparison_df = comparison_df.sort_values(
    "return_on_equity_pct",
    ascending=False,
)

comparison_df = comparison_df.round(2)

# -------------------------------------------------
# Highlight Selected Company
# -------------------------------------------------


def highlight_company(row):

    if row["company_id"] == selected_ticker:
        return ["background-color:#0f766e;color:white;font-weight:bold"] * len(row)

    return [""] * len(row)


styled_df = comparison_df.style.apply(
    highlight_company,
    axis=1,
)

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True,
)


# -------------------------------------------------
# Peer Group Statistics
# -------------------------------------------------

st.markdown("---")

st.subheader("📈 Peer Group Statistics")

avg_roe = group_df["return_on_equity_pct"].mean()
avg_roce = group_df["roce_percentage"].mean()
avg_pe = group_df["pe_ratio"].mean()
avg_pb = group_df["pb_ratio"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Peer Avg ROE", f"{avg_roe:.2f}%")

with c2:
    st.metric("Peer Avg ROCE", f"{avg_roce:.2f}%")

with c3:
    st.metric("Peer Avg PE", f"{avg_pe:.2f}")

with c4:
    st.metric("Peer Avg PB", f"{avg_pb:.2f}")

# -------------------------------------------------
# Best Company in Peer Group
# -------------------------------------------------

st.markdown("---")

st.subheader("🏆 Best Company in Peer Group")

best_company = group_df.sort_values("composite_quality_score", ascending=False).iloc[0]

col1, col2 = st.columns([3, 2])

with col1:

    st.success(f"""
### {best_company['company_name']}

**Ticker:** {best_company['company_id']}

**Sector:** {best_company['broad_sector']}

**Sub Sector:** {best_company['sub_sector']}
""")

with col2:

    st.metric("Quality Score", f"{best_company['composite_quality_score']:.2f}")

    st.metric("ROE", f"{best_company['return_on_equity_pct']:.2f}%")

    st.metric("ROCE", f"{best_company['roce_percentage']:.2f}%")

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.markdown("---")
