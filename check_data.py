import pandas as pd

files = [
    "data/core/profitandloss.xlsx",
    "data/core/balancesheet.xlsx",
    "data/core/cashflow.xlsx",
    "data/core/analysis.xlsx",
]

for file in files:

    print("\n" + "=" * 70)
    print(file)
    print("=" * 70)

    df = pd.read_excel(file, header=1)

    result = df[df["company_id"].isin(["ATGL", "SBIN"])]

    if result.empty:
        print("❌ No records found")
    else:
        print(result)
