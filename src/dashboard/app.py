import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 Nifty 100 Analytics")

st.markdown("""
Welcome to the **Nifty 100 Analytics Dashboard**.

Use the **left sidebar** to navigate between the dashboard pages.

Available modules:

- 🏠 Home
- 🏢 Company Profile
- 🔍 Financial Screener
- 🤝 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Annual Reports
""")
