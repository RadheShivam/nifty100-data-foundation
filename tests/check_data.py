import pandas as pd

files = [
    "data/core/profitandloss.xlsx",
    "data/core/balancesheet.xlsx",
    "data/core/cashflow.xlsx",
    "data/core/analysis.xlsx",
]

for file in files:
    print("\n" + "=" * 60)
    print(file)
    print("=" * 60)

    df = pd.read_excel(file)

    if "company_id" in df.columns:
        result = df[df["company_id"].isin(["ATGL", "SBIN"])]

        if result.empty:
            print("❌ No records found")
        else:
            print(result)

    else:
        print("❌ company_id column not found")