import os
import sqlite3
import warnings
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)

warnings.filterwarnings("ignore")

# ======================================================
# PATHS
# ======================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

DB_PATH = os.path.join(
    PROJECT_ROOT,
    "db",
    "nifty100.db"
)

SECTOR_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "supplementry",
    "sectors.xlsx"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "reports",
    "sector"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======================================================
# DATABASE
# ======================================================

conn = sqlite3.connect(DB_PATH)

companies_df = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios_df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

# ======================================================
# LOAD SECTOR FILE
# ======================================================

sectors_df = pd.read_excel(SECTOR_FILE)

# ======================================================
# PREPROCESSING
# ======================================================

ratios_df["year_num"] = (
    ratios_df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
    .astype(float)
)

latest_ratios = (
    ratios_df
    .sort_values("year_num")
    .groupby("company_id")
    .tail(1)
)

# ======================================================
# MERGE DATA
# ======================================================

sector_df = (
    companies_df
    .merge(
        sectors_df[
            [
                "company_id",
                "broad_sector",
                "sub_sector",
                "market_cap_category"
            ]
        ],
        left_on="id",
        right_on="company_id",
        how="left"
    )
    .merge(
        latest_ratios,
        left_on="id",
        right_on="company_id",
        how="left",
        suffixes=("_company", "")
    )
)

# Remove duplicate company_id column
sector_df = sector_df.loc[:, ~sector_df.columns.duplicated()]

# ======================================================
# REPORTLAB STYLES
# ======================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    textColor=colors.white,
    fontSize=18
)

heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading2"],
    textColor=HexColor("#123A6D"),
    fontSize=14
)

normal_style = styles["BodyText"]

# ======================================================
# STARTUP INFO
# ======================================================

print("=" * 50)
print("Sector Report Generator")
print("=" * 50)

print(f"Companies Loaded : {len(companies_df)}")
print(f"Financial Ratios : {len(ratios_df)}")
print(f"Broad Sectors    : {sector_df['broad_sector'].nunique()}")

print("\nSector List:")
print(sorted(sector_df["broad_sector"].dropna().unique()))

print("\nMerged Columns:\n")
print(sector_df.columns.tolist())

# ======================================================
# HELPER FUNCTIONS
# ======================================================

def safe(value):
    if pd.isna(value):
        return "N/A"

    if isinstance(value, (int, float)):
        return f"{value:.2f}"

    return str(value)


def build_sector_report(sector_name):

    df = sector_df[
        sector_df["broad_sector"] == sector_name
    ].copy()

    if df.empty:
        return

    pdf_path = os.path.join(
        OUTPUT_DIR,
        f"{sector_name.replace(' ', '_')}_report.pdf"
    )

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=0.8 * cm,
        leftMargin=0.8 * cm,
        topMargin=0.8 * cm,
        bottomMargin=0.8 * cm,
    )

    elements = []

    # ======================================================
    # HEADER
    # ======================================================

    header = Table(
        [[Paragraph(f"<b>{sector_name}</b>", title_style)]],
        colWidths=[18 * cm],
    )

    header.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#123A6D")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    elements.append(header)
    elements.append(Spacer(1, 0.5 * cm))

    # ======================================================
    # SUMMARY
    # ======================================================

    elements.append(
        Paragraph(
            "<b>Sector Summary</b>",
            heading_style
        )
    )

    summary_data = [
        ["Metric", "Value"],
        ["Companies", len(df)],
        ["Median ROE", safe(df["return_on_equity_pct"].median())],
        ["Median ROCE", safe(df["roce_percentage"].median())],
        ["Median Debt/Equity", safe(df["debt_to_equity"].median())],
        ["Median EPS", safe(df["earnings_per_share"].median())],
        ["Median Free Cash Flow", safe(df["free_cash_flow_cr"].median())],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[8 * cm, 8 * cm],
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#123A6D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    )

    elements.append(summary_table)
    elements.append(Spacer(1, 0.5 * cm))

    # ======================================================
    # COMPANY TABLE
    # ======================================================

    elements.append(
        Paragraph(
            "<b>Company Metrics</b>",
            heading_style
        )
    )

    elements.append(Spacer(1, 0.2 * cm))

    company_data = [[
        "Company",
        "ROE",
        "ROCE",
        "D/E",
        "EPS",
        "FCF",
        "Quality"
    ]]

    df = df.sort_values("company_name")

    for _, row in df.iterrows():

        company_data.append([
            row["company_name"],
            safe(row["return_on_equity_pct"]),
            safe(row["roce_percentage"]),
            safe(row["debt_to_equity"]),
            safe(row["earnings_per_share"]),
            safe(row["free_cash_flow_cr"]),
            safe(row["composite_quality_score"]),
        ])

    company_table = Table(
        company_data,
        repeatRows=1,
        colWidths=[
            6 * cm,
            1.6 * cm,
            1.6 * cm,
            1.6 * cm,
            1.6 * cm,
            2.2 * cm,
            2.2 * cm,
        ],
    )

    company_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#123A6D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ])
    )

    elements.append(company_table)

    doc.build(elements)

    print(f"Generated : {os.path.basename(pdf_path)}")


# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    print("\nGenerating Sector Reports...\n")

    sectors = sorted(
        sector_df["broad_sector"]
        .dropna()
        .unique()
    )

    for sector in sectors:
        build_sector_report(sector)

    print("\n" + "=" * 50)
    print("Sector Report Generation Complete")
    print("=" * 50)
    print(f"Total Reports : {len(sectors)}")
    print(f"Output Folder : {OUTPUT_DIR}")