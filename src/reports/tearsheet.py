import os
import sqlite3
import warnings

import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

warnings.filterwarnings("ignore")

# ==================================================
# PATHS
# ==================================================

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DB_PATH = os.path.join(PROJECT_ROOT, "db", "nifty100.db")

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "reports", "tearsheets")

OUTPUT_IMAGE_DIR = os.path.join(OUTPUT_DIR, "charts")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)

# ==================================================
# DATABASE
# ==================================================

conn = sqlite3.connect(DB_PATH)

companies_df = pd.read_sql("SELECT id, company_name FROM companies", conn)

ratios_df = pd.read_sql("SELECT * FROM financial_ratios", conn)

profit_df = pd.read_sql("SELECT * FROM profitandloss", conn)

balance_df = pd.read_sql("SELECT * FROM balancesheet", conn)

cashflow_df = pd.read_sql("SELECT * FROM cashflow", conn)

conn.close()

# ==================================================
# OPTIONAL FILES
# ==================================================

pros_cons_path = os.path.join(PROJECT_ROOT, "output", "pros_cons_generated.csv")

cash_intelligence_path = os.path.join(
    PROJECT_ROOT, "output", "cashflow_intelligence.xlsx"
)

if os.path.exists(pros_cons_path):
    pros_cons_df = pd.read_csv(pros_cons_path)
else:
    pros_cons_df = pd.DataFrame()

if os.path.exists(cash_intelligence_path):
    cashflow_intelligence_df = pd.read_excel(cash_intelligence_path)
else:
    cashflow_intelligence_df = pd.DataFrame()

# ==================================================
# PREPROCESSING
# ==================================================

for df in (
    ratios_df,
    profit_df,
    balance_df,
    cashflow_df,
):
    if "year" in df.columns:

        df["year_num"] = df["year"].astype(str).str.extract(r"(\d{4})")[0].astype(float)

# ==================================================
# REPORTLAB STYLES
# ==================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    fontSize=20,
    textColor=colors.white,
    spaceAfter=8,
)

heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading2"],
    textColor=HexColor("#0A2E5C"),
    fontSize=14,
    spaceAfter=8,
)

normal_style = ParagraphStyle(
    "Normal", parent=styles["BodyText"], fontSize=10, leading=14
)

small_style = ParagraphStyle("Small", parent=styles["BodyText"], fontSize=8)

# ==================================================
# HELPER FUNCTIONS
# ==================================================


def safe_value(value, digits=2, suffix=""):
    """
    Convert NaN values into 'N/A'
    """

    if pd.isna(value):
        return "N/A"

    if isinstance(value, (int, float)):
        return f"{value:.{digits}f}{suffix}"

    return str(value)


def latest_record(df, company_id):
    """
    Return latest yearly record for a company.
    """

    temp = df[df["company_id"] == company_id].sort_values("year_num")

    if temp.empty:
        return None

    return temp.iloc[-1]


print("=" * 50)
print("DAY 33 - Tearsheet Generator")
print("=" * 50)
print()

print(f"Companies Loaded : {len(companies_df)}")
print(f"Financial Ratios : {len(ratios_df)}")
print(f"Profit Records   : {len(profit_df)}")
print(f"Balance Records  : {len(balance_df)}")
print(f"Cash Flow        : {len(cashflow_df)}")
print(f"Pros & Cons      : {len(pros_cons_df)}")
print(f"Cash Intelligence: {len(cashflow_intelligence_df)}")

# ==================================================
# TEARSHEET GENERATOR
# ==================================================


def generate_tearsheet(company_id):

    # ----------------------------------------------
    # Company Information
    # ----------------------------------------------

    company = companies_df[companies_df["id"] == company_id]

    if company.empty:
        print(f"{company_id} not found.")
        return

    company_name = company.iloc[0]["company_name"]

    ratio = latest_record(ratios_df, company_id)

    profit = latest_record(profit_df, company_id)

    balance = latest_record(balance_df, company_id)

    cash = latest_record(cashflow_df, company_id)

    if ratio is None:
        print(f"No financial ratios found for {company_id}")
        return

    cash_intelligence = None

    if (
        not cashflow_intelligence_df.empty
        and "company_id" in cashflow_intelligence_df.columns
    ):

        temp = cashflow_intelligence_df[
            cashflow_intelligence_df["company_id"] == company_id
        ]

        if not temp.empty:
            cash_intelligence = temp.iloc[0]

    # ----------------------------------------------
    # Output PDF
    # ----------------------------------------------

    pdf_path = os.path.join(OUTPUT_DIR, f"{company_id}_tearsheet.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=0.6 * cm,
        leftMargin=0.6 * cm,
        topMargin=0.7 * cm,
        bottomMargin=0.7 * cm,
    )

    elements = []

    # ----------------------------------------------
    # HEADER
    # ----------------------------------------------

    header = Table(
        [[Paragraph(f"<b>{company_name}</b><br/>{company_id}", title_style)]],
        colWidths=[18.2 * cm],
    )

    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#123A6D")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 14),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                ("BOX", (0, 0), (-1, -1), 1, HexColor("#123A6D")),
            ]
        )
    )

    elements.append(header)

    elements.append(Spacer(1, 0.45 * cm))

    # ----------------------------------------------
    # Basic Information
    # ----------------------------------------------

    latest_year = ratio["year"] if "year" in ratio.index else "-"

    info_table = Table(
        [
            [
                Paragraph(
                    f"<b>Latest Financial Year :</b> {latest_year}", normal_style
                ),
                Paragraph(f"<b>Company ID :</b> {company_id}", normal_style),
            ]
        ],
        colWidths=[9 * cm, 9 * cm],
    )

    info_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F5F7FA")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(info_table)

    elements.append(Spacer(1, 0.4 * cm))

    # ----------------------------------------------
    # KPI Section Heading
    # ----------------------------------------------

    elements.append(Paragraph("<b>Key Financial Indicators</b>", heading_style))

    elements.append(Spacer(1, 0.2 * cm))

    # ==================================================
    # KPI DASHBOARD
    # ==================================================

    quality = "N/A"

    if cash_intelligence is not None and "cfo_quality_label" in cash_intelligence.index:
        quality = cash_intelligence["cfo_quality_label"]

    market_cap = "N/A"

    if profit is not None and "market_cap" in profit.index:
        market_cap = safe_value(profit["market_cap"], digits=2)

    pe_ratio = "N/A"

    if "price_to_earnings" in ratio.index:
        pe_ratio = safe_value(ratio["price_to_earnings"], digits=2)

    kpi_data = [
        ["ROE", safe_value(ratio.get("return_on_equity_pct"), suffix="%")],
        ["ROCE", safe_value(ratio.get("roce_percentage"), suffix="%")],
        ["Debt / Equity", safe_value(ratio.get("debt_to_equity"))],
        ["Free Cash Flow", safe_value(ratio.get("free_cash_flow_cr"))],
        ["EPS", safe_value(ratio.get("earnings_per_share"))],
        ["P/E Ratio", pe_ratio],
        ["Market Cap", market_cap],
        ["CFO Quality", quality],
    ]

    row1 = []
    row2 = []

    for title, value in kpi_data:

        card = Table(
            [
                [Paragraph(f"<b>{title}</b>", heading_style)],
                [Paragraph(str(value), normal_style)],
            ],
            colWidths=[4.3 * cm],
        )

        card.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#DCE6F2")),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )

        if len(row1) < 4:
            row1.append(card)
        else:
            row2.append(card)

    elements.append(Table([row1], colWidths=[4.4 * cm] * 4))

    elements.append(Spacer(1, 0.2 * cm))

    elements.append(Table([row2], colWidths=[4.4 * cm] * 4))

    elements.append(Spacer(1, 0.5 * cm))

    # ==================================================
    # FINANCIAL CHARTS HEADING
    # ==================================================

    elements.append(Paragraph("<b>Financial Performance</b>", heading_style))

    elements.append(Spacer(1, 0.25 * cm))

    # ==================================================
    # REVENUE HISTORY
    # ==================================================

    profit_history = (
        profit_df[profit_df["company_id"] == company_id]
        .sort_values("year_num")
        .tail(10)
        .copy()
    )

    if not profit_history.empty:

        # ------------------------------------------
        # Revenue Chart
        # ------------------------------------------

        revenue_chart = os.path.join(OUTPUT_IMAGE_DIR, f"{company_id}_revenue.png")

        plt.figure(figsize=(5, 3))

        plt.bar(profit_history["year"].astype(str), profit_history["sales"])

        plt.title("Revenue")

        plt.xticks(rotation=45, fontsize=8)

        plt.tight_layout()

        plt.savefig(revenue_chart, dpi=180, bbox_inches="tight")

        plt.close()

        # ------------------------------------------
        # Net Profit Chart
        # ------------------------------------------

        profit_chart = os.path.join(OUTPUT_IMAGE_DIR, f"{company_id}_profit.png")

        plt.figure(figsize=(5, 3))

        plt.bar(profit_history["year"].astype(str), profit_history["net_profit"])

        plt.title("Net Profit")

        plt.xticks(rotation=45, fontsize=8)

        plt.tight_layout()

        plt.savefig(profit_chart, dpi=180, bbox_inches="tight")

        plt.close()

    # ==================================================
    # ROE vs ROCE
    # ==================================================

    ratio_history = (
        ratios_df[ratios_df["company_id"] == company_id]
        .sort_values("year_num")
        .tail(10)
        .copy()
    )

    roe_chart = os.path.join(OUTPUT_IMAGE_DIR, f"{company_id}_roe.png")

    if not ratio_history.empty:

        plt.figure(figsize=(6, 3))

        plt.plot(
            ratio_history["year"].astype(str),
            ratio_history["return_on_equity_pct"],
            marker="o",
            linewidth=2,
            label="ROE",
        )

        plt.plot(
            ratio_history["year"].astype(str),
            ratio_history["roce_percentage"],
            marker="s",
            linewidth=2,
            label="ROCE",
        )

        plt.legend()

        plt.grid(alpha=0.3)

        plt.xticks(rotation=45, fontsize=8)

        plt.title("ROE vs ROCE")

        plt.tight_layout()

        plt.savefig(roe_chart, dpi=180, bbox_inches="tight")

        plt.close()

    # ==================================================
    # ADD CHARTS TO PDF
    # ==================================================

    chart_table = Table(
        [
            [
                Image(revenue_chart, width=3.2 * inch, height=2.3 * inch),
                Image(profit_chart, width=3.2 * inch, height=2.3 * inch),
            ],
            [Image(roe_chart, width=6.5 * inch, height=2.6 * inch), ""],
        ],
        colWidths=[3.4 * inch, 3.4 * inch],
    )

    chart_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    elements.append(chart_table)

    elements.append(Spacer(1, 0.4 * cm))

    # ==================================================
    # PAGE 2
    # ==================================================

    elements.append(PageBreak())

    elements.append(Paragraph("<b>Balance Sheet Analysis</b>", heading_style))

    elements.append(Spacer(1, 0.3 * cm))

    # ==================================================
    # BALANCE SHEET SNAPSHOT
    # ==================================================

    balance_data = [
        [
            "Total Assets",
            safe_value(balance.get("total_assets") if balance is not None else None),
        ],
        [
            "Total Liabilities",
            safe_value(
                balance.get("total_liabilities") if balance is not None else None
            ),
        ],
        [
            "Equity Capital",
            safe_value(
                balance.get("equity_share_capital") if balance is not None else None
            ),
        ],
        [
            "Reserves",
            safe_value(balance.get("reserves") if balance is not None else None),
        ],
        [
            "Borrowings",
            safe_value(balance.get("borrowings") if balance is not None else None),
        ],
        [
            "Cash & Investments",
            safe_value(
                balance.get("cash_equivalents") if balance is not None else None
            ),
        ],
    ]

    table_data = [["Metric", "Value"]]

    table_data.extend(balance_data)

    balance_table = Table(table_data, colWidths=[8 * cm, 8 * cm])

    balance_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#123A6D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(balance_table)

    elements.append(Spacer(1, 0.5 * cm))

    # ==================================================
    # ASSETS vs LIABILITIES CHART
    # ==================================================

    assets_chart = os.path.join(OUTPUT_IMAGE_DIR, f"{company_id}_balance.png")

    if balance is not None:

        labels = ["Assets", "Liabilities"]

        values = [balance.get("total_assets", 0), balance.get("total_liabilities", 0)]

        plt.figure(figsize=(5, 3))

        plt.bar(labels, values)

        plt.title("Assets vs Liabilities")

        plt.tight_layout()

        plt.savefig(assets_chart, dpi=180, bbox_inches="tight")

        plt.close()

        elements.append(Image(assets_chart, width=5.5 * inch, height=3.0 * inch))

    elements.append(Spacer(1, 0.4 * cm))

    # ==================================================
    # CASH FLOW INTELLIGENCE
    # ==================================================

    elements.append(Paragraph("<b>Cash Flow Intelligence</b>", heading_style))

    elements.append(Spacer(1, 0.2 * cm))

    operating_cf = "N/A"
    investing_cf = "N/A"
    financing_cf = "N/A"
    free_cash_flow = "N/A"
    cash_quality = "N/A"

    if cash is not None:

        operating_cf = safe_value(cash.get("cash_from_operating_activity"))

        investing_cf = safe_value(cash.get("cash_from_investing_activity"))

        financing_cf = safe_value(cash.get("cash_from_financing_activity"))

        free_cash_flow = safe_value(cash.get("free_cash_flow"))

    if cash_intelligence is not None:

        if "cfo_quality_label" in cash_intelligence.index:
            cash_quality = str(cash_intelligence["cfo_quality_label"])

    cash_table_data = [
        ["Operating Cash Flow", operating_cf],
        ["Investing Cash Flow", investing_cf],
        ["Financing Cash Flow", financing_cf],
        ["Free Cash Flow", free_cash_flow],
        ["Cash Flow Quality", cash_quality],
    ]

    cash_table = Table(
        [["Metric", "Value"]] + cash_table_data, colWidths=[8 * cm, 8 * cm]
    )

    cash_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1E8449")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(cash_table)

    elements.append(Spacer(1, 0.3 * cm))

    # ==================================================
    # CASH FLOW SUMMARY
    # ==================================================

    summary_text = f"""
    <b>Cash Flow Summary</b><br/><br/>

    <b>Operating Cash Flow:</b> {operating_cf}<br/>
    <b>Investing Cash Flow:</b> {investing_cf}<br/>
    <b>Financing Cash Flow:</b> {financing_cf}<br/>
    <b>Free Cash Flow:</b> {free_cash_flow}<br/><br/>

    <b>Overall Cash Flow Quality:</b> {cash_quality}
    """

    summary_box = Table(
        [[Paragraph(summary_text, normal_style)]], colWidths=[17.5 * cm]
    )

    summary_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F8F9F9")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    elements.append(summary_box)

    elements.append(Spacer(1, 0.5 * cm))

    # ==================================================
    # PROS & CONS
    # ==================================================

    elements.append(Paragraph("<b>Pros & Cons</b>", heading_style))

    elements.append(Spacer(1, 0.2 * cm))

    pros_text = "No information available."
    cons_text = "No information available."

    if not pros_cons_df.empty and "company_id" in pros_cons_df.columns:

        pc = pros_cons_df[pros_cons_df["company_id"] == company_id]

        if not pc.empty:

            row = pc.iloc[0]

            if "pros" in row.index and pd.notna(row["pros"]):
                pros_text = str(row["pros"]).replace("|", "<br/>• ")

            if "cons" in row.index and pd.notna(row["cons"]):
                cons_text = str(row["cons"]).replace("|", "<br/>• ")

    pros_para = Paragraph("<b>Pros</b><br/>• " + pros_text, normal_style)

    cons_para = Paragraph("<b>Cons</b><br/>• " + cons_text, normal_style)

    pros_cons_table = Table([[pros_para, cons_para]], colWidths=[8.8 * cm, 8.8 * cm])

    pros_cons_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("BACKGROUND", (0, 0), (0, 0), HexColor("#E8F5E9")),
                ("BACKGROUND", (1, 0), (1, 0), HexColor("#FDEDEC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(pros_cons_table)

    elements.append(Spacer(1, 0.4 * cm))

    # ==================================================
    # INVESTMENT SUMMARY
    # ==================================================

    elements.append(Paragraph("<b>Investment Summary</b>", heading_style))

    recommendation = "Neutral"

    try:
        roe = ratio.get("return_on_equity_pct", 0)
        debt = ratio.get("debt_to_equity", 999)

        if pd.notna(roe) and pd.notna(debt):
            if roe >= 20 and debt < 1:
                recommendation = "Strong Candidate"
            elif roe >= 15 and debt < 2:
                recommendation = "Good Candidate"
            else:
                recommendation = "Needs Further Analysis"
    except Exception:
        recommendation = "Not Available"

    summary = f"""
    <b>Company:</b> {company_name}<br/><br/>

    This report summarizes the company's latest financial
    performance using profitability, balance sheet,
    cash flow and valuation metrics.

    <b>Overall Assessment:</b> {recommendation}
    """

    summary_table = Table([[Paragraph(summary, normal_style)]], colWidths=[17.5 * cm])

    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#F8F9FA")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    elements.append(summary_table)

    # ==================================================
    # BUILD PDF
    # ==================================================

    doc.build(elements)

    print(f"Generated: {pdf_path}")


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    print("\nGenerating Tearsheets...\n")

    success = 0
    failed = 0

    for company_id in companies_df["id"]:

        try:
            generate_tearsheet(company_id)
            success += 1

        except Exception as e:
            failed += 1
            print(f"Failed: {company_id}")
            print(e)
            print("-" * 50)

    print("\n" + "=" * 50)
    print("Generation Complete")
    print("=" * 50)
    print(f"Successful : {success}")
    print(f"Failed     : {failed}")
    print(f"Output Dir : {OUTPUT_DIR}")
