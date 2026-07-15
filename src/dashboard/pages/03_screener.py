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
    get_ratios_by_year,
    get_companies,
    get_sectors,
)

DB_PATH = "db/nifty100.db"

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Financial Screener",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Financial Screener")
st.caption("Filter Nifty 100 companies using financial metrics.")

# -------------------------------------------------
# Load Data
# -------------------------------------------------

ratios_df = get_ratios_by_year("Mar 2024")
companies_df = get_companies()
sectors_df = get_sectors()

# Market Valuation Table
conn = sqlite3.connect(DB_PATH)

market_df = pd.read_sql(
    """
    SELECT
        company_id,
        pe_ratio,
        pb_ratio,
        dividend_yield_pct
    FROM marketcap
    WHERE year = (
        SELECT MAX(year)
        FROM marketcap
    )
    """,
    conn,
)

conn.close()

# -------------------------------------------------
# Merge Data
# -------------------------------------------------

screen_df = (
    ratios_df
    .merge(
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
    .merge(
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
    .merge(
        market_df,
        on="company_id",
        how="left",
    )
)

st.write(market_df.head())

st.write(
    screen_df[
        [
            "company_id",
            "pe_ratio",
            "pb_ratio"
        ]
    ].head()
)
# -------------------------------------------------
# Replace Missing Values
# -------------------------------------------------

numeric_cols = screen_df.select_dtypes(include="number").columns
screen_df[numeric_cols] = screen_df[numeric_cols].fillna(0)


# -------------------------------------------------
# Safe Slider Function
# -------------------------------------------------

def safe_slider(label, series, default_value, is_max=False):
    """
    Creates a slider that never crashes even if
    min == max or values contain NaN.
    """

    series = pd.to_numeric(series, errors="coerce").fillna(0)

    min_val = float(series.min())
    max_val = float(series.max())

    if min_val == max_val:
        max_val = min_val + 1

    if is_max:
        default_value = max_val
    else:
        default_value = max(default_value, min_val)
        default_value = min(default_value, max_val)

    return st.sidebar.slider(
        label,
        min_value=min_val,
        max_value=max_val,
        value=default_value,
    )


# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------

st.sidebar.header("📊 Filter Companies")

roe_min = safe_slider(
    "Minimum ROE (%)",
    screen_df["return_on_equity_pct"],
    15.0,
)

de_max = safe_slider(
    "Maximum Debt / Equity",
    screen_df["debt_to_equity"],
    1.0,
    is_max=True,
)

fcf_min = safe_slider(
    "Minimum Free Cash Flow (Cr)",
    screen_df["free_cash_flow_cr"],
    0.0,
)

revenue_min = safe_slider(
    "Revenue CAGR 5Y (%)",
    screen_df["revenue_cagr_5yr"],
    10.0,
)

pat_min = safe_slider(
    "PAT CAGR 5Y (%)",
    screen_df["pat_cagr_5yr"],
    10.0,
)

opm_min = safe_slider(
    "Minimum OPM (%)",
    screen_df["operating_profit_margin_pct"],
    15.0,
)

pe_max = safe_slider(
    "Maximum PE Ratio",
    screen_df["pe_ratio"],
    40.0,
    is_max=True,
)

pb_max = safe_slider(
    "Maximum PB Ratio",
    screen_df["pb_ratio"],
    5.0,
    is_max=True,
)

dividend_min = safe_slider(
    "Minimum Dividend Yield (%)",
    screen_df["dividend_yield_pct"],
    0.0,
)

icr_min = safe_slider(
    "Minimum Interest Coverage",
    screen_df["interest_coverage"],
    2.0,
)


# -------------------------------------------------
# Apply Filters
# -------------------------------------------------

# filtered_df = screen_df.copy()

# filtered_df = filtered_df[
#     (filtered_df["return_on_equity_pct"] >= roe_min)
#     &
#     (filtered_df["debt_to_equity"] <= de_max)
#     &
#     (filtered_df["free_cash_flow_cr"] >= fcf_min)
#     &
#     (filtered_df["revenue_cagr_5yr"] >= revenue_min)
#     &
#     (filtered_df["pat_cagr_5yr"] >= pat_min)
#     &
#     (filtered_df["operating_profit_margin_pct"] >= opm_min)
#     &
#     (filtered_df["pe_ratio"] <= pe_max)
#     &
#     (filtered_df["pb_ratio"] <= pb_max)
#     &
#     (filtered_df["dividend_yield_pct"] >= dividend_min)
#     &
#     (filtered_df["interest_coverage"] >= icr_min)
# ]


filtered_df = screen_df.copy()

st.write("Initial:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["return_on_equity_pct"] >= roe_min
]
st.write("After ROE:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["debt_to_equity"] <= de_max
]
st.write("After D/E:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["free_cash_flow_cr"] >= fcf_min
]
st.write("After FCF:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["revenue_cagr_5yr"] >= revenue_min
]
st.write("After Revenue CAGR:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["pat_cagr_5yr"] >= pat_min
]
st.write("After PAT CAGR:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["operating_profit_margin_pct"] >= opm_min
]
st.write("After OPM:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["pe_ratio"] <= pe_max
]
st.write("After PE:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["pb_ratio"] <= pb_max
]
st.write("After PB:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["dividend_yield_pct"] >= dividend_min
]
st.write("After Dividend:", len(filtered_df))

filtered_df = filtered_df[
    filtered_df["interest_coverage"] >= icr_min
]
st.write("After Interest Coverage:", len(filtered_df))

# -------------------------------------------------
# Sort Results
# -------------------------------------------------

filtered_df = filtered_df.sort_values(
    by="composite_quality_score",
    ascending=False,
)

# -------------------------------------------------
# Screening Results
# -------------------------------------------------

st.markdown("---")

st.subheader("📊 Screening Results")

st.success(
    f"{len(filtered_df)} Companies match your filters."
)

# -------------------------------------------------
# Columns to Display
# -------------------------------------------------

display_columns = [
    "company_id",
    "company_name",
    "broad_sector",
    "sub_sector",
    "return_on_equity_pct",
    "roce_percentage",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "operating_profit_margin_pct",
    "interest_coverage",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "composite_quality_score",
]

available_columns = [
    col
    for col in display_columns
    if col in filtered_df.columns
]

# -------------------------------------------------
# Display Data
# -------------------------------------------------

st.dataframe(
    filtered_df[available_columns],
    use_container_width=True,
    hide_index=True,
)

# -------------------------------------------------
# Download CSV
# -------------------------------------------------

st.markdown("---")

csv = filtered_df[available_columns].to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name="financial_screener_results.csv",
    mime="text/csv",
)

# -------------------------------------------------
# Preset Screeners
# -------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Preset Screeners")

preset = st.sidebar.radio(
    "Choose Preset",
    [
        "Custom",
        "Quality Compounder",
        "Value Pick",
        "Growth Accelerator",
        "Dividend Champion",
        "Debt-Free Blue Chip",
        "Turnaround Watch",
    ],
)

if preset == "Quality Compounder":
    st.sidebar.success(
        "High ROE • High ROCE • Low Debt • Strong Growth"
    )

elif preset == "Value Pick":
    st.sidebar.success(
        "Low PE • Low PB • Reasonable ROE"
    )

elif preset == "Growth Accelerator":
    st.sidebar.success(
        "High Revenue CAGR • High PAT CAGR"
    )

elif preset == "Dividend Champion":
    st.sidebar.success(
        "High Dividend Yield"
    )

elif preset == "Debt-Free Blue Chip":
    st.sidebar.success(
        "Very Low Debt • Stable Business"
    )

elif preset == "Turnaround Watch":
    st.sidebar.success(
        "Improving Fundamentals"
    )

# -------------------------------------------------
# Summary Dashboard
# -------------------------------------------------

st.markdown("---")

st.subheader("📈 Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Companies Found",
        len(filtered_df),
    )

with col2:
    if len(filtered_df):
        st.metric(
            "Highest Quality Score",
            f"{filtered_df['composite_quality_score'].max():.2f}",
        )
    else:
        st.metric(
            "Highest Quality Score",
            "N/A",
        )

with col3:
    if len(filtered_df):
        st.metric(
            "Average ROE",
            f"{filtered_df['return_on_equity_pct'].mean():.2f}%",
        )
    else:
        st.metric(
            "Average ROE",
            "N/A",
        )

with col4:
    if len(filtered_df):
        st.metric(
            "Average PE",
            f"{filtered_df['pe_ratio'].mean():.2f}",
        )
    else:
        st.metric(
            "Average PE",
            "N/A",
        )

# -------------------------------------------------
# Top 10 Companies
# -------------------------------------------------

if len(filtered_df):

    st.markdown("---")

    st.subheader("🏆 Top 10 Ranked Companies")

    top10 = filtered_df.nlargest(
        10,
        "composite_quality_score",
    )

    st.dataframe(
        top10[
            [
                "company_name",
                "broad_sector",
                "return_on_equity_pct",
                "roce_percentage",
                "pe_ratio",
                "composite_quality_score",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.markdown("---")

