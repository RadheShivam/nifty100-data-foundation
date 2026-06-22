from src.etl.loader import load_profitandloss

df = load_profitandloss()

print(df.head())
print(df.shape)
print(df.columns)