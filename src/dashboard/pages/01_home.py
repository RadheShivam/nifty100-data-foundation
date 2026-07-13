import streamlit as st
import plotly.express as px

import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.dashboard.utils.db import (
    get_companies,
    get_sectors,
    get_ratios,
)

st.title("🏠 Home Dashboard")

# -----------------------------
# Load Data
# -----------------------------

companies = get_companies()
sectors = get_sectors()

ratios = get_ratios("TCS")  # temporary test

# -----------------------------
# Sidebar
# -----------------------------

year = st.sidebar.selectbox(
    "Select Year",
    [
        "Mar 2019",
        "Mar 2020",
        "Mar 2021",
        "Mar 2022",
        "Mar 2023",
        "Mar 2024",
    ],
    index=5,
)

# -----------------------------
# KPI Cards
# -----------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Companies",
    len(companies)
)

c2.metric(
    "Total Sectors",
    sectors["broad_sector"].nunique()
)

c3.metric(
    "Financial Ratio Rows",
    len(ratios)
)

# -----------------------------
# Sector Distribution
# -----------------------------

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
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Companies Preview
# -----------------------------

st.subheader("Companies")

st.dataframe(
    companies.head(10),
    use_container_width=True,
)