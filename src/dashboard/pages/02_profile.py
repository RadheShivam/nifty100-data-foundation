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

from src.dashboard.utils.db import (
    get_companies,
    get_latest_ratio,
    get_pl,
    get_ratios,
    get_bs,
    get_cf,
    get_valuation,
    get_pros_cons,
    get_sector_info,
)

# -------------------------------------------------
# Page Title
# -------------------------------------------------

st.title("🏢 Company Profile")

st.caption(
    "Search any Nifty 100 company and view its financial profile."
)

# -------------------------------------------------
# Load Companies
# -------------------------------------------------

companies = get_companies()

# -------------------------------------------------
# Company Search
# -------------------------------------------------

company_options = (
    companies["id"]
    + " - "
    + companies["company_name"]
).tolist()

selected_company = st.selectbox(
    "🔍 Search Company",
    company_options
)

ticker = selected_company.split(" - ")[0]

company = companies[
    companies["id"] == ticker
].iloc[0]

sector_df = get_sector_info(ticker)

if not sector_df.empty:
    sector = sector_df.iloc[0]["broad_sector"]
    sub_sector = sector_df.iloc[0]["sub_sector"]
    market_cap = sector_df.iloc[0]["market_cap_category"]
else:
    sector = "N/A"
    sub_sector = "N/A"
    market_cap = "N/A"

latest_ratio = get_latest_ratio(ticker)

if latest_ratio.empty:
    st.error("No financial ratio data available.")
    st.stop()

latest_ratio = latest_ratio.iloc[0]

# -------------------------------------------------
# Profit & Loss History
# -------------------------------------------------

pl_df = get_pl(ticker)

if not pl_df.empty:
    pl_df = pl_df.sort_values("year")

st.success(f"Selected Company : {ticker}")

st.divider()

# -------------------------------------------------
# Company Information
# -------------------------------------------------

st.subheader("🏢 Company Information")

col1, col2 = st.columns([1, 3])

with col1:

    if (
        "company_logo" in company.index
        and pd.notna(company["company_logo"])
    ):

        try:
            st.image(
                company["company_logo"],
                width=150
            )

        except Exception:
            st.info("Logo unavailable")

with col2:

    st.markdown(f"## {company['company_name']}")

    st.write(f"**Ticker :** {company['id']}")

    st.write(f"**Sector :** {sector}")

    st.write(f"**Sub-Sector :** {sub_sector}")

    st.write(f"**Market Cap :** {market_cap}")

    st.markdown(
        f"[📈 TradingView Chart]({company['chart_link']})"
    )

st.divider()

# -------------------------------------------------
# Financial Highlights
# -------------------------------------------------

st.subheader("📊 Latest Financial KPIs")

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

with c1:
    st.metric(
        "ROE",
        f"{latest_ratio['return_on_equity_pct']:.2f}%"
    )

with c2:
    st.metric(
        "ROCE",
        f"{latest_ratio['roce_percentage']:.2f}%"
    )

with c3:
    st.metric(
        "Net Profit Margin",
        f"{latest_ratio['net_profit_margin_pct']:.2f}%"
    )

with c4:
    st.metric(
        "Debt / Equity",
        f"{latest_ratio['debt_to_equity']:.2f}"
    )

with c5:
    st.metric(
        "Revenue CAGR (5Y)",
        f"{latest_ratio['revenue_cagr_5yr']:.2f}%"
    )

with c6:
    st.metric(
        "Free Cash Flow",
        f"₹ {latest_ratio['free_cash_flow_cr']:.2f} Cr"
    )

st.divider()

# -------------------------------------------------
# About Company
# -------------------------------------------------

st.subheader("📖 About Company")

st.info(
    company["about_company"]
)

st.divider()

# -------------------------------------------------
# Useful Links
# -------------------------------------------------

st.subheader("🔗 Useful Links")

c1, c2 = st.columns(2)

with c1:

    st.link_button(
        "🌐 Company Website",
        company["website"]
    )

    st.link_button(
        "📈 TradingView",
        company["chart_link"]
    )

with c2:

    st.link_button(
        "🏛 NSE Profile",
        company["nse_profile"]
    )

    st.link_button(
        "📄 BSE Profile",
        company["bse_profile"]
    )

# -------------------------------------------------
# Revenue & Net Profit Trend
# -------------------------------------------------

st.divider()

st.subheader("📈 Revenue & Net Profit (10 Years)")

if not pl_df.empty:

    revenue_col = None
    profit_col = None

    for col in pl_df.columns:

        c = col.lower()

        if revenue_col is None and (
            "sales" in c or "revenue" in c
        ):
            revenue_col = col

        if profit_col is None and (
            "net profit" in c
            or "net_profit" in c
            or "profit after tax" in c
            or c == "pat"
        ):
            profit_col = col

    if revenue_col and profit_col:

        chart_df = pl_df[
            [
                "year",
                revenue_col,
                profit_col,
            ]
        ].copy()

        chart_df.rename(
            columns={
                revenue_col: "Revenue",
                profit_col: "Net Profit",
            },
            inplace=True,
        )

        chart_df = chart_df.melt(
            id_vars="year",
            value_vars=["Revenue", "Net Profit"],
            var_name="Metric",
            value_name="Value",
        )

        fig = px.bar(
            chart_df,
            x="year",
            y="Value",
            color="Metric",
            barmode="group",
            title="Revenue vs Net Profit",
        )

        fig.update_layout(
            xaxis_title="Financial Year",
            yaxis_title="₹ Crore",
            legend_title="Metric",
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "Revenue or Net Profit columns not found."
        )

else:

    st.warning(
        "Profit & Loss data unavailable."
    )

# -------------------------------------------------
# ROE & ROCE Trend
# -------------------------------------------------

st.divider()

st.subheader("📈 ROE & ROCE Trend")

ratio_history = get_ratios(ticker)

if not ratio_history.empty:
    

    ratio_history = ratio_history.sort_values("year")

    ratio_chart = ratio_history[
        [
            "year",
            "return_on_equity_pct",
            "roce_percentage",
        ]
    ].copy()

    ratio_chart.rename(
        columns={
            "return_on_equity_pct": "ROE",
            "roce_percentage": "ROCE",
        },
        inplace=True,
    )

    ratio_chart = ratio_chart.melt(
        id_vars="year",
        value_vars=["ROE", "ROCE"],
        var_name="Metric",
        value_name="Percentage",
    )

    fig = px.line(
        ratio_chart,
        x="year",
        y="Percentage",
        color="Metric",
        markers=True,
        title="ROE vs ROCE",
    )

    fig.update_layout(
        legend_title="Metrics",
        xaxis_title="Financial Year",
        yaxis_title="Percentage (%)",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "Financial ratio history unavailable."
    )


# -------------------------------------------------
# Profit & Loss Statement
# -------------------------------------------------

st.divider()

st.subheader("📑 Profit & Loss Statement")

pl_df = get_pl(ticker)

if not pl_df.empty:

    st.dataframe(
        pl_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.warning(
        "Profit & Loss data unavailable."
    )


# -------------------------------------------------
# Balance Sheet
# -------------------------------------------------

st.divider()

st.subheader("🏦 Balance Sheet")

bs_df = get_bs(ticker)

if not bs_df.empty:

    st.dataframe(
        bs_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.warning(
        "Balance Sheet data unavailable."
    )


# -------------------------------------------------
# Cash Flow Statement
# -------------------------------------------------

st.divider()

st.subheader("💰 Cash Flow Statement")

cf_df = get_cf(ticker)

if not cf_df.empty:

    st.dataframe(
        cf_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.warning(
        "Cash Flow data unavailable."
    )

# -------------------------------------------------
# Company Valuation
# -------------------------------------------------

st.divider()

st.markdown("---")
st.subheader("💎 Company Valuation")

valuation = get_valuation(ticker)

if not valuation.empty:

    row = valuation.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Face Value",
            f"₹ {row['face_value']:.0f}"
        )

    with c2:
        st.metric(
            "Book Value",
            f"₹ {row['book_value']:,.0f}"
        )

    with c3:
        st.metric(
            "ROE",
            f"{row['roe_percentage']:.2f}%"
        )

    with c4:
        st.metric(
            "ROCE",
            f"{row['roce_percentage']:.2f}%"
        )

else:
    st.info("Valuation data unavailable.")

# st.write(company)

# st.write(companies.columns.tolist())



st.divider()

st.subheader("✅ Pros & ❌ Cons")

pros_cons = get_pros_cons(ticker)
st.write("Ticker =", ticker)
st.write(pros_cons)

if not pros_cons.empty:

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Pros")

        for item in pros_cons["pros"].dropna():
            st.success(item)

    with col2:
        st.markdown("### ❌ Cons")

        for item in pros_cons["cons"].dropna():
            st.error(item)

else:
    st.info("No Pros & Cons available.")