


import os
import sys

import streamlit as st
import pandas as pd

# -------------------------------------------------
# Add Project Root
# -------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# Import Database Functions
# -------------------------------------------------

from src.dashboard.utils.db import (
    get_sectors,
    get_ratios_by_year,
)

# -------------------------------------------------
# Page Title
# -------------------------------------------------

st.title("📊 Sector Analysis")

st.caption(
    "Compare companies across different sectors."
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------

sector_df = get_sectors()

ratio_df = get_ratios_by_year("Mar 2024")

if sector_df.empty or ratio_df.empty:
    st.error("Sector data not found.")
    st.stop()

# -------------------------------------------------
# Merge Data
# -------------------------------------------------

df = ratio_df.merge(
    sector_df,
    on="company_id",
    how="left"
)

# -------------------------------------------------
# Load Revenue from Profit & Loss
# -------------------------------------------------

import sqlite3

conn = sqlite3.connect("db/nifty100.db")

sales_df = pd.read_sql(
    """
    SELECT
        company_id,
        sales
    FROM profitandloss
    WHERE year='Mar 2024'
    """,
    conn
)

market_df = pd.read_sql(
    """
    SELECT
        company_id,
        market_cap_crore
    FROM marketcap
    WHERE year=2024
    """,
    conn
)

conn.close()

df = df.merge(
    sales_df,
    on="company_id",
    how="left"
)

df = df.merge(
    market_df,
    on="company_id",
    how="left"
)

# -------------------------------------------------
# Sector Dropdown
# -------------------------------------------------

sector_list = sorted(
    df["broad_sector"].dropna().unique()
)

selected_sector = st.selectbox(
    "🏢 Select Sector",
    sector_list
)

sector_data = df[
    df["broad_sector"] == selected_sector
]

st.success(
    f"{len(sector_data)} companies found in {selected_sector}"
)

import plotly.express as px

st.markdown("---")

st.subheader("🫧 Sector Bubble Chart")

fig = px.scatter(

    sector_data,

    x="sales",

    y="return_on_equity_pct",

    size="market_cap_crore",

    color="sub_sector",

    hover_name="company_id",

    size_max=60,

    title=f"{selected_sector} Sector Analysis"
)

fig.update_layout(

    xaxis_title="Revenue (Cr)",

    yaxis_title="ROE (%)",

    height=700,

    legend_title="Sub Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Sector Median KPI Chart
# -------------------------------------------------

st.markdown("---")

st.subheader("📊 Sector Median KPIs")

median_df = pd.DataFrame({

    "KPI": [

        "ROE",

        "ROCE",

        "Debt/Equity",

        "Revenue CAGR",

        "PAT CAGR",

        "Quality Score"

    ],

    "Median Value": [

        sector_data["return_on_equity_pct"].median(),

        sector_data["roce_percentage"].median(),

        sector_data["debt_to_equity"].median(),

        sector_data["revenue_cagr_5yr"].median(),

        sector_data["pat_cagr_5yr"].median(),

        sector_data["composite_quality_score"].median()

    ]

})

fig = px.bar(

    median_df,

    x="KPI",

    y="Median Value",

    text="Median Value",

    title=f"{selected_sector} Median Financial KPIs"
)

fig.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

fig.update_layout(

    height=500,

    xaxis_title="",

    yaxis_title="Median Value"

)

st.plotly_chart(

    fig,

    use_container_width=True
)