from src.etl.loader import load_cashflow

df = load_cashflow()

print(df.head())
print(df.shape)
print(df.columns)