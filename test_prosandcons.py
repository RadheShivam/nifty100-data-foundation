from src.etl.loader import load_prosandcons

df = load_prosandcons()

print(df.head())
print(df.shape)
print(df.columns)