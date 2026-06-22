from src.etl.loader import load_analysis

df = load_analysis()

print(df.head())
print(df.shape)
print(df.columns)