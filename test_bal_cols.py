import pandas as pd

df = pd.read_csv("data/processed/balancesheet.csv")

print(df.columns.tolist())