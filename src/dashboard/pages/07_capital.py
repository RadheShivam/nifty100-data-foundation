import os
import sys

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Add Project Root
# -------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# Import DB
# -------------------------------------------------

from src.dashboard.utils.db import (
    get_ratios_by_year,
)

# -------------------------------------------------
# Page Title
# -------------------------------------------------

st.title("🌳 Capital Allocation Map")

st.caption(
    "Visualize companies based on capital allocation patterns."
)

# -------------------------------------------------
# Load Data
# -------------------------------------------------

df = get_ratios_by_year("Mar 2024")

if df.empty:
    st.error("No financial data found.")
    st.stop()

# -------------------------------------------------
# Capital Allocation Pattern
# -------------------------------------------------

def classify_company(row):

    roe = row["return_on_equity_pct"]
    debt = row["debt_to_equity"]
    fcf = row["free_cash_flow_cr"]
    growth = row["revenue_cagr_5yr"]

    if roe >= 20 and debt < 0.5:
        return "Compounders"

    elif debt > 1.5:
        return "Highly Leveraged"

    elif growth >= 20:
        return "High Growth"

    elif fcf > 0:
        return "Cash Generators"

    elif fcf < 0:
        return "Capex Heavy"

    elif roe < 10:
        return "Low Return"

    elif debt == 0:
        return "Debt Free"

    else:
        return "Balanced"


df["capital_pattern"] = df.apply(
    classify_company,
    axis=1
)


# -------------------------------------------------
# Treemap
# -------------------------------------------------

st.markdown("---")

st.subheader("🌳 Capital Allocation Treemap")

fig = px.treemap(

    df,

    path=[
        "capital_pattern",
        "company_id"
    ],

    values="composite_quality_score",

    color="return_on_equity_pct",

    color_continuous_scale="RdYlGn",

    hover_data={
        "return_on_equity_pct":":.2f",
        "debt_to_equity":":.2f",
        "revenue_cagr_5yr":":.2f",
        "free_cash_flow_cr":":,.0f"
    },

    title="Capital Allocation Patterns"
)

fig.update_layout(
    height=750
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Companies by Capital Allocation Pattern
# -------------------------------------------------

st.markdown("---")

st.subheader("📋 Companies by Capital Allocation Pattern")

patterns = sorted(
    df["capital_pattern"].unique()
)

selected_pattern = st.selectbox(
    "Select Capital Allocation Pattern",
    patterns
)

pattern_df = (
    df[df["capital_pattern"] == selected_pattern]
    .sort_values(
        "composite_quality_score",
        ascending=False
    )
)

st.success(
    f"{len(pattern_df)} companies found in '{selected_pattern}'"
)

display_df = pattern_df[
    [
        "company_id",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "composite_quality_score"
    ]
].rename(
    columns={
        "company_id": "Company",
        "return_on_equity_pct": "ROE (%)",
        "debt_to_equity": "Debt/Equity",
        "free_cash_flow_cr": "Free Cash Flow",
        "revenue_cagr_5yr": "Revenue CAGR (5Y)",
        "composite_quality_score": "Quality Score"
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)