import os
import sys

import requests

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
# Database
# -------------------------------------------------

from src.dashboard.utils.db import get_companies

import sqlite3

# -------------------------------------------------
# Page
# -------------------------------------------------

st.title("📑 Annual Reports")

st.caption(
    "Browse annual reports for every company."
)

# -------------------------------------------------
# Load Companies
# -------------------------------------------------

companies = get_companies()

company_options = (
    companies["id"]
    + " - "
    + companies["company_name"]
)

selected = st.selectbox(

    "🔍 Select Company",

    company_options
)

ticker = selected.split(" - ")[0]

# -------------------------------------------------
# Load Reports
# -------------------------------------------------

conn = sqlite3.connect("db/nifty100.db")

reports = pd.read_sql(

    """
    SELECT *
    FROM documents
    WHERE company_id=?
    ORDER BY year DESC
    """,

    conn,

    params=(ticker,)
)

conn.close()

if reports.empty:

    st.warning("No annual reports available.")

    st.stop()

st.success(
    f"{len(reports)} reports found."
)


# -------------------------------------------------
# Available Reports
# -------------------------------------------------

st.markdown("---")

st.subheader("📄 Available Annual Reports")

import requests

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}

for _, row in reports.iterrows():

    col1, col2 = st.columns([1, 4])

    with col1:
        st.write(f"**{row['year']}**")

    with col2:

        url = row["annual_report"]

        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=8,
                allow_redirects=True,
                stream=True
            )

            if response.status_code == 200:
                st.link_button(
                    "📥 Open Report",
                    url
                )
            else:
                st.error("🔴 Report Unavailable")

        except requests.RequestException:
            st.error("🔴 Report Unavailable")