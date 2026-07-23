import os
import sqlite3
import pandas as pd

# ---------------------------------------
# Paths
# ---------------------------------------

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------
# Connect Database
# ---------------------------------------

conn = sqlite3.connect(DB_PATH)

# ---------------------------------------
# Load Analysis Table
# ---------------------------------------

analysis_df = pd.read_sql(
    """
    SELECT *
    FROM analysis
    """,
    conn,
)

conn.close()

# --------------------------------------------------
# Regex Parser
# --------------------------------------------------

import re

pattern = re.compile(
    r"(TTM|Last Year|\d+\s*Years?|\d+\s*Year)" r"\s*:?\s*(-?[\d.]+)%", re.IGNORECASE
)

parsed_rows = []

failed_rows = []

target_columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

for _, row in analysis_df.iterrows():

    company = row["company_id"]

    for column in target_columns:

        text = str(row[column]).strip()

        match = pattern.search(text)

        if match:

            period = match.group(1).strip().lower()

            if period == "ttm":
                period_years = 0

            elif period == "last year":
                period_years = 1

            else:
                period_years = int(re.search(r"\d+", period).group())

            parsed_rows.append(
                {
                    "company_id": company,
                    "metric_type": column,
                    "period_years": period_years,
                    "value_pct": float(match.group(2)),
                }
            )

        else:

            failed_rows.append(
                {"company_id": company, "metric_type": column, "raw_text": text}
            )

# --------------------------------------------------
# Save Outputs
# --------------------------------------------------

parsed_df = pd.DataFrame(parsed_rows)

failed_df = pd.DataFrame(failed_rows)

parsed_df.to_csv(os.path.join(OUTPUT_DIR, "analysis_parsed.csv"), index=False)

failed_df.to_csv(os.path.join(OUTPUT_DIR, "parse_failures.csv"), index=False)

print("\n===============================")
print("Parsing Completed")
print("===============================")

print("Parsed Records :", len(parsed_df))

print("Failed Records :", len(failed_df))

print("\nParsed Preview")

print(parsed_df.head(15))

print("\nFailed Preview")

print(failed_df.head(15))

# --------------------------------------------------
# Cross Validation with Ratio Engine
# --------------------------------------------------

conn = sqlite3.connect(DB_PATH)

ratio_df = pd.read_sql(
    """
    SELECT
        company_id,
        revenue_cagr_3yr,
        revenue_cagr_5yr,
        revenue_cagr_10yr,
        pat_cagr_3yr,
        pat_cagr_5yr,
        pat_cagr_10yr
    FROM financial_ratios
    """,
    conn,
)

conn.close()

review_rows = []

for _, row in parsed_df.iterrows():

    company = row["company_id"]
    metric = row["metric_type"]
    period = row["period_years"]
    parsed_value = row["value_pct"]

    ratio = ratio_df[ratio_df["company_id"] == company]

    if ratio.empty:
        continue

    ratio = ratio.iloc[-1]

    db_value = None

    # Revenue CAGR
    if metric == "compounded_sales_growth":

        if period == 3:
            db_value = ratio["revenue_cagr_3yr"]

        elif period == 5:
            db_value = ratio["revenue_cagr_5yr"]

        elif period == 10:
            db_value = ratio["revenue_cagr_10yr"]

    # PAT CAGR
    elif metric == "compounded_profit_growth":

        if period == 3:
            db_value = ratio["pat_cagr_3yr"]

        elif period == 5:
            db_value = ratio["pat_cagr_5yr"]

        elif period == 10:
            db_value = ratio["pat_cagr_10yr"]

    if db_value is None or pd.isna(db_value):
        continue

    difference = abs(parsed_value - db_value)

    if difference > 5:

        review_rows.append(
            {
                "company_id": company,
                "metric": metric,
                "period": period,
                "parsed_value": parsed_value,
                "ratio_engine_value": round(db_value, 2),
                "difference": round(difference, 2),
            }
        )

manual_review_df = pd.DataFrame(review_rows)

manual_review_df.to_csv(os.path.join(OUTPUT_DIR, "manual_review.csv"), index=False)

print("\n===============================")
print("Cross Validation Completed")
print("===============================")

print("Manual Review Rows :", len(manual_review_df))

print(manual_review_df.head(20))
