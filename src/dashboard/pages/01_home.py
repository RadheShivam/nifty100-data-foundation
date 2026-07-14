import os
import sys

import streamlit as st
import plotly.express as px
import pandas as pd

# -------------------------------------------------
# Add project root to Python path
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

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide"
)

# -------------------------------------------------
# Page Title
# -------------------------------------------------

st.title("🏠 Home Dashboard")
st.caption(
    "Financial summary of the Nifty 100 companies for the selected financial year."
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

years = [
    "Mar 2019",
    "Mar 2020",
    "Mar 2021",
    "Mar 2022",
    "Mar 2023",
    "Mar 2024",
]

selected_year = st.sidebar.selectbox(
    "📅 Select Financial Year",
    years,
    index=len(years) - 1,
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------

companies = get_companies()
sectors = get_sectors()
ratios = get_ratios_by_year(selected_year)

# -------------------------------------------------
# Selected Year
# -------------------------------------------------

st.markdown(f"### Financial Year : **{selected_year}**")

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------

st.subheader("📊 Key Performance Indicators")

valid_roe = ratios[
    (ratios["return_on_equity_pct"] >= -100)
    &
    (ratios["return_on_equity_pct"] <= 100)
]

avg_roe = valid_roe["return_on_equity_pct"].mean()

median_de = ratios["debt_to_equity"].median()

median_revenue_cagr = ratios["revenue_cagr_5yr"].median()

debt_free = (ratios["debt_to_equity"] == 0).sum()

total_companies = ratios["company_id"].nunique()

# Day 26
median_pe = "N/A"

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric(
    "Average ROE",
    f"{avg_roe:.2f}%"
)

col2.metric(
    "Median D/E",
    f"{median_de:.2f}"
)

col3.metric(
    "Total Companies",
    total_companies
)

col4.metric(
    "Median Revenue CAGR (5Y)",
    f"{median_revenue_cagr:.2f}%"
)

col5.metric(
    "Debt-Free Companies",
    debt_free
)

col6.metric(
    "Median P/E",
    median_pe
)

st.divider()

# -------------------------------------------------
# Sector Distribution
# -------------------------------------------------

st.subheader("📊 Sector Distribution")

sector_count = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    values="Companies",
    names="broad_sector",
    hole=0.45,
    title="Companies by Broad Sector",
)

fig.update_traces(
    textinfo="percent+label"
)

fig.update_layout(
    height=550,
    legend_title="Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# Top 5 Companies
# -------------------------------------------------

st.subheader("🏆 Top 5 Companies by Composite Quality Score")

top5 = (
    ratios[
        [
            "company_id",
            "composite_quality_score",
            "return_on_equity_pct",
            "roce_percentage",
        ]
    ]
    .sort_values(
        by="composite_quality_score",
        ascending=False
    )
    .head(5)
)

top5 = top5.rename(
    columns={
        "company_id": "Company",
        "composite_quality_score": "Composite Score",
        "return_on_equity_pct": "ROE (%)",
        "roce_percentage": "ROCE (%)",
    }
)

top5 = top5.round(
    {
        "Composite Score": 2,
        "ROE (%)": 2,
        "ROCE (%)": 2,
    }
)

st.dataframe(
    top5,
    hide_index=True,
    use_container_width=True,
)