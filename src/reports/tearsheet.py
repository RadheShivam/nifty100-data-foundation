import os
import sqlite3
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle

from reportlab.lib.units import inch
from reportlab.lib.units import cm

from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

import matplotlib.pyplot as plt

# --------------------------------------------------
# Paths
# --------------------------------------------------

DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "reports/tearsheets"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# --------------------------------------------------
# Database Connection
# --------------------------------------------------

conn = sqlite3.connect(DB_PATH)

# --------------------------------------------------
# Load Companies
# --------------------------------------------------

companies_df = pd.read_sql(
    """
    SELECT
        id,
        company_name
    FROM companies
    """,
    conn
)

# --------------------------------------------------
# Load Financial Ratios
# --------------------------------------------------

ratios_df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)

# --------------------------------------------------
# Load Profit & Loss
# --------------------------------------------------

profit_df = pd.read_sql(
    """
    SELECT *
    FROM profitandloss
    """,
    conn
)

# --------------------------------------------------
# Load Balance Sheet
# --------------------------------------------------

balance_df = pd.read_sql(
    """
    SELECT *
    FROM balancesheet
    """,
    conn
)

# --------------------------------------------------
# Load Cash Flow
# --------------------------------------------------

cashflow_df = pd.read_sql(
    """
    SELECT *
    FROM cashflow
    """,
    conn
)

# --------------------------------------------------
# Load Pros & Cons
# --------------------------------------------------

pros_cons_df = pd.read_csv(
    "output/pros_cons_generated.csv"
)

# --------------------------------------------------
# Load Cash Flow Intelligence
# --------------------------------------------------

cashflow_intelligence_df = pd.read_excel(
    "output/cashflow_intelligence.xlsx"
)

conn.close()

# --------------------------------------------------
# Extract Numeric Year
# --------------------------------------------------

for dataframe in [
    ratios_df,
    profit_df,
    balance_df,
    cashflow_df
]:

    dataframe["year_num"] = (
        dataframe["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(float)
    )

# --------------------------------------------------
# Styles
# --------------------------------------------------

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    textColor=colors.white,
    fontSize=20,
    spaceAfter=10
)

heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading2"],
    textColor=HexColor("#0A2E5C"),
    spaceAfter=6
)

normal_style = styles["BodyText"]

print("=" * 50)
print("DAY 33")
print("=" * 50)
print()
print("Companies Loaded :", len(companies_df))
print("Financial Ratios :", len(ratios_df))
print("Profit Records   :", len(profit_df))
print("Balance Records  :", len(balance_df))
print("Cash Flow        :", len(cashflow_df))
print("Pros/Cons        :", len(pros_cons_df))
print("Cash Intelligence:", len(cashflow_intelligence_df))


# --------------------------------------------------
# Generate Tearsheet
# --------------------------------------------------

def generate_tearsheet(company_id):

    company = companies_df[
        companies_df["id"] == company_id
    ]

    if company.empty:
        print("Company not found:", company_id)
        return

    company_name = company.iloc[0]["company_name"]

    latest_ratio = (
        ratios_df[
            ratios_df["company_id"] == company_id
        ]
        .sort_values("year_num")
        .tail(1)
    )

    latest_profit = (
        profit_df[
            profit_df["company_id"] == company_id
        ]
        .sort_values("year_num")
        .tail(1)
    )

    latest_cash = (
        cashflow_intelligence_df[
            cashflow_intelligence_df["company_id"] == company_id
        ]
    )

    if latest_ratio.empty:
        print("No ratio data:", company_id)
        return

    latest_ratio = latest_ratio.iloc[0]

    if not latest_profit.empty:
        latest_profit = latest_profit.iloc[0]

    if not latest_cash.empty:
        latest_cash = latest_cash.iloc[0]

    pdf_file = os.path.join(
        OUTPUT_DIR,
        f"{company_id}_tearsheet.pdf"
    )

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4
    )

    elements = []

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    header = Table(
        [[
            Paragraph(
                f"<b>{company_name}</b><br/>{company_id}",
                title_style
            )
        ]],
        colWidths=[18 * cm]
    )

    header.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#0A2E5C")),

            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),

            ("TOPPADDING", (0, 0), (-1, -1), 12)

        ])

    )

    elements.append(header)

    elements.append(Spacer(1, 0.4 * cm))

    # --------------------------------------------------
    # KPI Tiles
    # --------------------------------------------------

    kpi_data = [

        [
            "ROE",
            f"{latest_ratio['return_on_equity_pct']:.2f}%"
        ],

        [
            "ROCE",
            f"{latest_ratio['roce_percentage']:.2f}%"
        ],

        [
            "Debt/Equity",
            f"{latest_ratio['debt_to_equity']:.2f}"
        ],

        [
            "FCF",
            f"{latest_ratio['free_cash_flow_cr']:.2f}"
        ],

        [
            "EPS",
            f"{latest_ratio['earnings_per_share']:.2f}"
        ],

        [
            "Quality",
            latest_cash["cfo_quality_label"]
            if not latest_cash.empty
            else "-"
        ]

    ]

    kpi_table = Table(

        [
            [Paragraph("<b>"+x[0]+"</b>", heading_style)
             for x in kpi_data],

            [Paragraph(str(x[1]), normal_style)
             for x in kpi_data]

        ],

        colWidths=[3 * cm] * 6

    )

    kpi_table.setStyle(

        TableStyle([

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND", (0,0), (-1,0), HexColor("#DCE6F2")),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("TOPPADDING", (0,0), (-1,-1), 8)

        ])

    )

    elements.append(kpi_table)

    elements.append(Spacer(1,0.5*cm))

    # --------------------------------------------------
    # Placeholder
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "<b>Charts will be added in Part 3</b>",
            heading_style
        )
    )

    doc.build(elements)

    print("Generated :", pdf_file)


# --------------------------------------------------
# Test
# --------------------------------------------------

generate_tearsheet("TCS")