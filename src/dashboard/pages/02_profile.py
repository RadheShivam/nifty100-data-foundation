import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------------------------------
# Add Project Root
# -------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# Database Functions
# -------------------------------------------------

from src.dashboard.utils.db import (
    get_companies,
    get_latest_ratio,
    get_pl,
    get_bs,
    get_cf,
    get_ratios,
    get_valuation,
    get_pros_cons,
    get_sector_info,
)

# -------------------------------------------------
# Page Title
# -------------------------------------------------

st.title("🏢 Company Profile")

st.caption("Search any Nifty 100 company and view its financial profile.")

# -------------------------------------------------
# Load Company Master
# -------------------------------------------------

companies = get_companies()

if companies.empty:
    st.error("Company master data not found.")
    st.stop()

# -------------------------------------------------
# Search Company
# -------------------------------------------------

company_options = (
    companies["id"].astype(str) + " - " + companies["company_name"].astype(str)
)

selected_company = st.selectbox(
    "🔍 Search Company",
    company_options,
)

ticker = selected_company.split(" - ")[0].strip()

company = companies[companies["id"] == ticker]

if company.empty:
    st.error("Ticker not found.")
    st.stop()

company = company.iloc[0]

# -------------------------------------------------
# Sector Information
# -------------------------------------------------

sector_df = get_sector_info(ticker)

sector = "N/A"
sub_sector = "N/A"
market_cap = "N/A"

if not sector_df.empty:

    sector = sector_df.iloc[0].get("broad_sector", "N/A")

    sub_sector = sector_df.iloc[0].get("sub_sector", "N/A")

    market_cap = sector_df.iloc[0].get("market_cap_category", "N/A")

# -------------------------------------------------
# Latest Financial Ratio
# -------------------------------------------------

latest_ratio = get_latest_ratio(ticker)

if latest_ratio.empty:
    st.error("Financial ratios not available.")
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

    if "company_logo" in company.index and pd.notna(company["company_logo"]):
        try:
            st.image(company["company_logo"], width=150)
        except Exception:
            st.info("Logo unavailable")

with col2:

    st.markdown(f"## {company['company_name']}")

    st.write(f"**Ticker:** {ticker}")

    st.write(f"**Sector:** {sector}")

    st.write(f"**Sub-Sector:** {sub_sector}")

    st.write(f"**Market Cap Category:** {market_cap}")

    if "chart_link" in company.index and pd.notna(company["chart_link"]):
        st.markdown(f"[📈 TradingView Chart]({company['chart_link']})")

st.divider()

# -------------------------------------------------
# Financial Highlights
# -------------------------------------------------

st.subheader("📊 Latest Financial KPIs")


def safe_metric(value, suffix=""):

    if pd.isna(value):
        return "N/A"

    try:
        return f"{float(value):.2f}{suffix}"
    except Exception:
        return str(value)


c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

with c1:
    st.metric("ROE", safe_metric(latest_ratio["return_on_equity_pct"], "%"))

with c2:
    st.metric("ROCE", safe_metric(latest_ratio["roce_percentage"], "%"))

with c3:
    st.metric(
        "Net Profit Margin", safe_metric(latest_ratio["net_profit_margin_pct"], "%")
    )

with c4:
    st.metric("Debt / Equity", safe_metric(latest_ratio["debt_to_equity"]))

with c5:
    st.metric("Revenue CAGR (5Y)", safe_metric(latest_ratio["revenue_cagr_5yr"], "%"))

with c6:
    st.metric("Free Cash Flow", safe_metric(latest_ratio["free_cash_flow_cr"], " Cr"))

st.divider()

# -------------------------------------------------
# About Company
# -------------------------------------------------

st.subheader("📖 About Company")

if "about_company" in company.index and pd.notna(company["about_company"]):
    st.info(company["about_company"])
else:
    st.info("Company description unavailable.")

st.divider()

# -------------------------------------------------
# Useful Links
# -------------------------------------------------

st.subheader("🔗 Useful Links")

col1, col2 = st.columns(2)

with col1:

    if pd.notna(company["website"]):
        st.link_button("🌐 Company Website", company["website"])

    if pd.notna(company["chart_link"]):
        st.link_button("📈 TradingView", company["chart_link"])

with col2:

    if pd.notna(company["nse_profile"]):
        st.link_button("🏛 NSE Profile", company["nse_profile"])

    if pd.notna(company["bse_profile"]):
        st.link_button("📄 BSE Profile", company["bse_profile"])

st.divider()

# -------------------------------------------------
# Revenue & Net Profit Trend
# -------------------------------------------------

st.subheader("📈 Revenue & Net Profit (10 Years)")

if not pl_df.empty:

    revenue_col = "sales" if "sales" in pl_df.columns else None
    profit_col = "net_profit" if "net_profit" in pl_df.columns else None

    if revenue_col and profit_col:

        chart_df = pl_df[["year", revenue_col, profit_col]].copy()

        chart_df.rename(
            columns={revenue_col: "Revenue", profit_col: "Net Profit"}, inplace=True
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

        fig.update_layout(xaxis_title="Financial Year", yaxis_title="₹ Crore")

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.warning("Revenue or Net Profit data not available.")

else:

    st.warning("Profit & Loss data unavailable.")

# -------------------------------------------------
# ROE & ROCE Trend
# -------------------------------------------------

st.divider()

st.subheader("📈 ROE & ROCE Trend")

ratio_history = get_ratios(ticker)

if not ratio_history.empty:

    ratio_history = ratio_history.sort_values("year")

    ratio_chart = ratio_history[
        ["year", "return_on_equity_pct", "roce_percentage"]
    ].copy()

    ratio_chart.rename(
        columns={"return_on_equity_pct": "ROE", "roce_percentage": "ROCE"}, inplace=True
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

    fig.update_layout(xaxis_title="Financial Year", yaxis_title="Percentage (%)")

    st.plotly_chart(fig, use_container_width=True)

else:

    st.warning("Financial ratio history unavailable.")

# -------------------------------------------------
# Profit & Loss Statement
# -------------------------------------------------

st.divider()

st.subheader("📑 Profit & Loss Statement")

if not pl_df.empty:

    st.dataframe(pl_df, use_container_width=True, hide_index=True)

else:

    st.warning("Profit & Loss data unavailable.")

# -------------------------------------------------
# Balance Sheet
# -------------------------------------------------

st.divider()

st.subheader("🏦 Balance Sheet")

bs_df = get_bs(ticker)

if not bs_df.empty:

    st.dataframe(bs_df, use_container_width=True, hide_index=True)

else:

    st.warning("Balance Sheet data unavailable.")

# -------------------------------------------------
# Cash Flow Statement
# -------------------------------------------------

st.divider()

st.subheader("💰 Cash Flow Statement")

cf_df = get_cf(ticker)

if not cf_df.empty:

    st.dataframe(cf_df, use_container_width=True, hide_index=True)

else:

    st.warning("Cash Flow data unavailable.")

# -------------------------------------------------
# Company Valuation
# -------------------------------------------------

st.divider()

st.subheader("💎 Company Valuation")

valuation = get_valuation(ticker)

if not valuation.empty:

    row = valuation.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if pd.notna(row["face_value"]):
            st.metric("Face Value", f"₹ {row['face_value']:.2f}")
        else:
            st.metric("Face Value", "N/A")

    with c2:
        if pd.notna(row["book_value"]):
            st.metric("Book Value", f"₹ {row['book_value']:.2f}")
        else:
            st.metric("Book Value", "N/A")

    with c3:
        if pd.notna(row["roe_percentage"]):
            st.metric("ROE", f"{row['roe_percentage']:.2f}%")
        else:
            st.metric("ROE", "N/A")

    with c4:
        if pd.notna(row["roce_percentage"]):
            st.metric("ROCE", f"{row['roce_percentage']:.2f}%")
        else:
            st.metric("ROCE", "N/A")

else:

    st.info("Valuation data unavailable.")

# -------------------------------------------------
# Pros & Cons
# -------------------------------------------------

st.divider()

st.subheader("✅ Pros & ❌ Cons")

pros_cons = get_pros_cons(ticker)

if not pros_cons.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ✅ Pros")

        pros = pros_cons["pros"].dropna().tolist()

        if len(pros) == 0:
            st.info("No Pros available.")
        else:
            for item in pros:
                st.success(item)

    with col2:

        st.markdown("### ❌ Cons")

        cons = pros_cons["cons"].dropna().tolist()

        if len(cons) == 0:
            st.info("No Cons available.")
        else:
            for item in cons:
                st.error(item)

else:

    st.info("Pros & Cons data unavailable.")

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

st.caption("📊 Nifty 100 Analytics Dashboard • Company Profile • Sprint 4")
