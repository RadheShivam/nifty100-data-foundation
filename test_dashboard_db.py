from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_pl,
    get_bs,
    get_cf,
    get_sectors,
)

print("=" * 50)
print("Testing Dashboard Database Utility")
print("=" * 50)

companies = get_companies()
print(f"Companies: {len(companies)}")

print("\nFirst 5 Companies:")
print(companies[["id", "company_name"]].head())

ticker = "TCS"

ratios = get_ratios(ticker)
print(f"\nFinancial Ratios ({ticker}): {len(ratios)}")

pl = get_pl(ticker)
print(f"Profit & Loss Rows: {len(pl)}")

bs = get_bs(ticker)
print(f"Balance Sheet Rows: {len(bs)}")

cf = get_cf(ticker)
print(f"Cash Flow Rows: {len(cf)}")

sectors = get_sectors()
print(f"Sectors: {len(sectors)}")

print("\n✅ Dashboard DB utility working successfully!")