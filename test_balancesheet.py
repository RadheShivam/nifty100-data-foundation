from src.etl.loader import load_balancesheet

df = load_balancesheet()

print(df.head())
print(df.shape)
print(df.columns)