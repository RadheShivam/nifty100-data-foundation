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
# Import Database Functions
# -------------------------------------------------

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
)

# -------------------------------------------------
# Page Title
# -------------------------------------------------

st.title("📈 Trend Analysis")

st.caption(
    "Analyze financial performance over time."
)

# -------------------------------------------------
# Load Companies
# -------------------------------------------------

companies = get_companies()

if companies.empty:
    st.error("No companies found.")
    st.stop()

# -------------------------------------------------
# Company Search
# -------------------------------------------------

company_options = (
    companies["id"].astype(str)
    + " - "
    + companies["company_name"].astype(str)
)

selected_company = st.selectbox(
    "🔍 Select Company",
    company_options,
)

ticker = selected_company.split(" - ")[0]

# -------------------------------------------------
# Load Financial Ratios
# -------------------------------------------------

ratio_df = get_ratios(ticker)

if ratio_df.empty:
    st.warning("No financial data available.")
    st.stop()

ratio_df = ratio_df.sort_values("year")

st.success(f"Selected Company : {ticker}")


# -------------------------------------------------
# Metric Selection
# -------------------------------------------------

st.markdown("---")

st.subheader("📊 Select Metrics")

available_metrics = {
    "ROE (%)": "return_on_equity_pct",
    "ROCE (%)": "roce_percentage",
    "Net Profit Margin (%)": "net_profit_margin_pct",
    "Operating Profit Margin (%)": "operating_profit_margin_pct",
    "Debt to Equity": "debt_to_equity",
    "Interest Coverage": "interest_coverage",
    "Asset Turnover": "asset_turnover",
    "Free Cash Flow (Cr)": "free_cash_flow_cr",
    "Revenue CAGR 5Y (%)": "revenue_cagr_5yr",
    "PAT CAGR 5Y (%)": "pat_cagr_5yr",
    "EPS CAGR 5Y (%)": "eps_cagr_5yr",
    "Composite Quality Score": "composite_quality_score",
}

selected_metrics = st.multiselect(
    "Choose up to 3 metrics",
    options=list(available_metrics.keys()),
    default=["ROE (%)"],
    max_selections=3,
)

if len(selected_metrics) == 0:
    st.warning("Please select at least one metric.")
    st.stop()

selected_columns = [
    available_metrics[m]
    for m in selected_metrics
]

# -------------------------------------------------
# Prepare Chart Data
# -------------------------------------------------

chart_df = ratio_df[
    ["year"] + selected_columns
].copy()

chart_df = chart_df.sort_values("year")

# -------------------------------------------------
# Trend Chart
# -------------------------------------------------

st.markdown("---")

st.subheader("📈 Financial Trend")

plot_df = chart_df.melt(
    id_vars="year",
    value_vars=selected_columns,
    var_name="Metric",
    value_name="Value"
)

# Replace column names with readable names
reverse_metrics = {
    v: k
    for k, v in available_metrics.items()
}

plot_df["Metric"] = plot_df["Metric"].map(reverse_metrics)

# -------------------------------------------------
# Calculate YoY %
# -------------------------------------------------

plot_df = chart_df.copy()

for col in selected_columns:
    plot_df[col + "_YoY"] = (
        plot_df[col]
        .pct_change() * 100
    ).round(2)

# -------------------------------------------------
# Create Line Chart
# -------------------------------------------------

fig = px.line(
    plot_df,
    x="year",
    y=selected_columns,
    markers=True,
    title="Financial Trend Analysis"
)

# Rename legend labels
reverse_metrics = {
    v: k
    for k, v in available_metrics.items()
}

for trace in fig.data:

    column = trace.name

    trace.name = reverse_metrics[column]

    trace.hovertemplate = (
        "<b>%{x}</b><br>"
        + reverse_metrics[column]
        + ": %{y:.2f}<extra></extra>"
    )

# -------------------------------------------------
# Add YoY Annotation
# -------------------------------------------------

for column in selected_columns:

    for _, row in plot_df.iterrows():

        yoy_col = column + "_YoY"

        if pd.notna(row[yoy_col]):

            fig.add_annotation(

                x=row["year"],

                y=row[column],

                text=f"{row[yoy_col]:.1f}%",

                showarrow=False,

                yshift=15,

                font=dict(
                    size=9
                )

            )

# -------------------------------------------------
# Layout
# -------------------------------------------------

fig.update_layout(

    height=650,

    hovermode="x unified",

    legend_title="Metrics",

    xaxis_title="Financial Year",

    yaxis_title="Metric Value"
)

st.plotly_chart(
    fig,
    use_container_width=True
)