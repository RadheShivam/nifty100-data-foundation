import os
import sys
import sqlite3

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
# Merge Sector + Ratios
# -------------------------------------------------

df = ratio_df.merge(
    sector_df,
    on="company_id",
    how="left"
)

# -------------------------------------------------
# Load Revenue & Market Cap
# -------------------------------------------------

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

companies_df = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    """,
    conn
)

conn.close()

# -------------------------------------------------
# Merge All Data
# -------------------------------------------------

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

df = df.merge(
    companies_df,
    on="company_id",
    how="left"
)

# -------------------------------------------------
# Convert Numeric Columns
# -------------------------------------------------

numeric_columns = [
    "sales",
    "return_on_equity_pct",
    "market_cap_crore",
    "roce_percentage",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "composite_quality_score"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# -------------------------------------------------
# Remove Invalid Rows
# -------------------------------------------------

df = df.dropna(
    subset=[
        "broad_sector"
    ]
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
].copy()

# -------------------------------------------------
# DEBUG THE MERGED DATA
# -------------------------------------------------



st.markdown("---")

st.subheader("Companies in Selected Sector")



st.dataframe(
    sector_data[
        [
            "company_id",
            "company_name",
            "sub_sector"
        ]
    ].fillna("N/A"),
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------
# Bubble Chart
# -------------------------------------------------

st.markdown("---")

st.subheader("🫧 Sector Bubble Chart")

bubble_df = sector_data.dropna(
    subset=[
        "sales",
        "return_on_equity_pct",
        "market_cap_crore"
    ]
)



if bubble_df.empty:

    st.warning(
        "No financial data available for this sector."
    )


else:

    

    fig = px.scatter(

        bubble_df,

        x="sales",

        y="return_on_equity_pct",

        size="market_cap_crore",

        color="sub_sector",

        hover_name="company_name",

        hover_data={
            "company_id": True,
            "sales": ":,.0f",
            "market_cap_crore": ":,.0f",
            "return_on_equity_pct": ":.2f"
        },

        size_max=60,

        title=f"{selected_sector} Sector Analysis"
    )



    


    fig.update_layout(

        xaxis_title="Revenue (₹ Cr)",

        yaxis_title="ROE (%)",

        height=650,

        legend_title="Sub Sector",

        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40
        )
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

median_df["Median Value"] = median_df["Median Value"].fillna(0)

fig = px.bar(

    median_df,

    x="KPI",

    y="Median Value",

    text="Median Value",

    title=f"{selected_sector} Sector Median Financial KPIs"

)

fig.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

fig.update_layout(

    height=500,

    xaxis_title="",

    yaxis_title="Median Value",

    margin=dict(
        l=40,
        r=40,
        t=60,
        b=40
    )

)

st.plotly_chart(

    fig,

    use_container_width=True

)