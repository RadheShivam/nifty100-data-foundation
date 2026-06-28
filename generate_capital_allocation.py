import pandas as pd

from src.etl.loader import load_cashflow
from src.analytics.cashflow_kpis import capital_allocation_pattern

# Load cashflow table
cashflow_df = load_cashflow()

rows = []

for _, row in cashflow_df.iterrows():

    cfo_sign, cfi_sign, cff_sign, label = capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    )

    rows.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": cfo_sign,
        "cfi_sign": cfi_sign,
        "cff_sign": cff_sign,
        "pattern_label": label
    })

output_df = pd.DataFrame(rows)

output_df.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print("✅ output/capital_allocation.csv created successfully")