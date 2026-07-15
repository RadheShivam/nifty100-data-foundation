import os
import sys
import sqlite3

import pandas as pd
import streamlit as st

# -------------------------------------------------
# Add Project Root
# -------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.dashboard.utils.db import (
    get_companies,
    get_sectors,
    get_ratios_by_year,
)

DB_PATH = "db/nifty100.db"

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.title("📊 Sector Analytics")

st.caption(
    "Analyze Nifty 100 sectors using financial metrics."
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------

companies_df = get_companies()

sectors_df = get_sectors()

ratios_df = get_ratios_by_year("Mar 2024")

# -------------------------------------------------
# Load Market Cap Data
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
    WHERE year = '2024'
    """,
    conn,
)

conn.close()

# -------------------------------------------------
# Merge Data
# -------------------------------------------------

sector_df = ratios_df.merge(
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

sector_df = sector_df.merge(
    sectors_df[
        [
            "company_id",
            "broad_sector",
            "sub_sector",
            "market_cap_category",
        ]
    ],
    on="company_id",
    how="left",
)

sector_df = sector_df.merge(
    market_df,
    on="company_id",
    how="left",
)

# -------------------------------------------------
# Preview
# -------------------------------------------------

st.subheader("Merged Dataset")

st.dataframe(
    sector_df.head(10),
    use_container_width=True,
    hide_index=True,
)

st.success(
    f"Loaded {len(sector_df)} companies successfully."
)




# -------------------------------------------------
# Sector Selection
# -------------------------------------------------

st.markdown("---")

st.subheader("🏢 Select Sector")

sector_list = sorted(
    sector_df["broad_sector"]
    .dropna()
    .unique()
)

selected_sector = st.selectbox(
    "Choose a Sector",
    sector_list
)

# -------------------------------------------------
# Filter Selected Sector
# -------------------------------------------------

filtered_sector = sector_df[
    sector_df["broad_sector"] == selected_sector
]

st.success(
    f"{len(filtered_sector)} companies found in {selected_sector}"
)

# -------------------------------------------------
# Show Sector Companies
# -------------------------------------------------

display_columns = [
    "company_id",
    "company_name",
    "broad_sector",
    "sub_sector",
    "return_on_equity_pct",
    "roce_percentage",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "composite_quality_score",
]

available_columns = [
    col
    for col in display_columns
    if col in filtered_sector.columns
]

filtered_sector = filtered_sector.sort_values(
    "composite_quality_score",
    ascending=False
)

st.dataframe(
    filtered_sector[available_columns],
    use_container_width=True,
    hide_index=True,
)

# -------------------------------------------------
# Sector Summary
# -------------------------------------------------

st.markdown("---")

st.subheader("📈 Sector Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Companies",
        len(filtered_sector)
    )

with col2:
    st.metric(
        "Average ROE",
        f"{filtered_sector['return_on_equity_pct'].mean():.2f}%"
    )

with col3:
    st.metric(
        "Average ROCE",
        f"{filtered_sector['roce_percentage'].mean():.2f}%"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Average PE",
        f"{filtered_sector['pe_ratio'].mean():.2f}"
    )

with col5:
    st.metric(
        "Average PB",
        f"{filtered_sector['pb_ratio'].mean():.2f}"
    )

with col6:
    st.metric(
        "Highest Quality Score",
        f"{filtered_sector['composite_quality_score'].max():.2f}"
    )

