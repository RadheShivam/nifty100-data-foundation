import os
import sqlite3
import warnings

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    SimpleDocTemplate,
    PageBreak,
)

warnings.filterwarnings("ignore")

# =====================================================
# PATHS
# =====================================================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DB_PATH = os.path.join(PROJECT_ROOT, "db", "nifty100.db")

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "reports", "portfolio")

os.makedirs(OUTPUT_DIR, exist_ok=True)

PDF_PATH = os.path.join(OUTPUT_DIR, "portfolio_summary.pdf")

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect(DB_PATH)

companies_df = pd.read_sql("SELECT * FROM companies", conn)

ratios_df = pd.read_sql("SELECT * FROM financial_ratios", conn)

conn.close()

# =====================================================
# PREPROCESSING
# =====================================================

ratios_df["year_num"] = (
    ratios_df["year"].astype(str).str.extract(r"(\d{4})")[0].astype(float)
)

companies_df = companies_df.sort_values("id")

# =====================================================
# STYLES
# =====================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    fontSize=18,
    textColor=colors.white,
)

heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading2"],
    textColor=HexColor("#0A2E5C"),
    fontSize=13,
)

normal_style = ParagraphStyle(
    "Normal",
    parent=styles["BodyText"],
    fontSize=10,
)

small_style = ParagraphStyle(
    "Small",
    parent=styles["BodyText"],
    fontSize=8,
)

# =====================================================
# HELPERS
# =====================================================


def safe(v):

    if pd.isna(v):
        return "N/A"

    if isinstance(v, float):
        return f"{v:.2f}"

    return str(v)


print("=" * 50)
print("Portfolio Summary Generator")
print("=" * 50)
print(f"Companies : {len(companies_df)}")
print(f"Ratios    : {len(ratios_df)}")


# =====================================================
# HELPER FUNCTIONS
# =====================================================


def latest_record(company_id):
    """
    Return latest financial ratio record for a company.
    """

    df = ratios_df[ratios_df["company_id"] == company_id].sort_values("year_num")

    if df.empty:
        return None

    return df.iloc[-1]


def trend_arrow(company_id, column):
    """
    Compare latest value with previous year.
    ↑ Improved
    ↓ Declined
    → Flat (within 2%)
    """

    df = ratios_df[ratios_df["company_id"] == company_id].sort_values("year_num")

    if len(df) < 2:
        return "→"

    latest = df.iloc[-1].get(column)
    previous = df.iloc[-2].get(column)

    if pd.isna(latest) or pd.isna(previous):
        return "→"

    if previous == 0:
        return "→"

    change = ((latest - previous) / abs(previous)) * 100

    if change > 2:
        return "↑"

    if change < -2:
        return "↓"

    return "→"


# =====================================================
# PDF
# =====================================================

doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=A4,
    rightMargin=0.8 * cm,
    leftMargin=0.8 * cm,
    topMargin=0.8 * cm,
    bottomMargin=0.8 * cm,
)

elements = []


# =====================================================
# GENERATOR
# =====================================================


def generate_portfolio_summary():

    global elements

    for _, company in companies_df.iterrows():

        company_id = company["id"]
        company_name = company["company_name"]

        ratio = latest_record(company_id)

        if ratio is None:
            continue

        sector = company.get("sector", "N/A")

        # Header

        header = Table(
            [[Paragraph(f"<b>{company_name}</b><br/>{company_id}", title_style)]],
            colWidths=[18 * cm],
        )

        header.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), HexColor("#123A6D")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )

        elements.append(header)

        elements.append(Spacer(1, 0.4 * cm))

        elements.append(Paragraph(f"<b>Sector:</b> {sector}", normal_style))

        elements.append(Spacer(1, 0.4 * cm))

        # =====================================================
        # TOP 6 KPIs
        # =====================================================

        elements.append(Paragraph("<b>Top 6 KPIs</b>", heading_style))

        elements.append(Spacer(1, 0.2 * cm))

        kpi_table = [
            ["Metric", "Value"],
            ["ROE", safe(ratio.get("return_on_equity_pct"))],
            ["ROCE", safe(ratio.get("roce_percentage"))],
            ["Debt / Equity", safe(ratio.get("debt_to_equity"))],
            ["EPS", safe(ratio.get("earnings_per_share"))],
            ["P/E Ratio", safe(ratio.get("price_to_earnings"))],
            ["Free Cash Flow", safe(ratio.get("free_cash_flow_cr"))],
        ]

        table = Table(kpi_table, colWidths=[8 * cm, 8 * cm])

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#123A6D")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(table)

        elements.append(Spacer(1, 0.5 * cm))

        # =====================================================
        # KPI Trends
        # =====================================================

        elements.append(Paragraph("<b>KPI Trends</b>", heading_style))

        elements.append(Spacer(1, 0.2 * cm))

        trend_data = [
            ["Metric", "Trend"],
            ["ROE", trend_arrow(company_id, "return_on_equity_pct")],
            ["ROCE", trend_arrow(company_id, "roce_percentage")],
            ["Debt / Equity", trend_arrow(company_id, "debt_to_equity")],
            ["EPS", trend_arrow(company_id, "earnings_per_share")],
            ["P/E Ratio", trend_arrow(company_id, "price_to_earnings")],
            ["Free Cash Flow", trend_arrow(company_id, "free_cash_flow_cr")],
        ]

        trend_table = Table(trend_data, colWidths=[8 * cm, 8 * cm])

        trend_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0A2E5C")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(trend_table)

        # New page for next company
        elements.append(PageBreak())


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("\nGenerating Portfolio Summary...\n")

    generate_portfolio_summary()

    doc.build(elements)

    print("=" * 50)
    print("Portfolio Summary Generated Successfully")
    print("=" * 50)
    print(f"Output: {PDF_PATH}")
