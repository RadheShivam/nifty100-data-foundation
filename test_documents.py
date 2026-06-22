from src.etl.loader import load_documents

df = load_documents()

print(df.head())
print(df.shape)
print(df.columns)