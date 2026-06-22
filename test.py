from src.etl.loader import load_companies

df = load_companies()

print(df.head())
print(df.shape)