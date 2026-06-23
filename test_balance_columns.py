from src.etl.load_to_sqlite import *

# or however balance_df is created in your code
import pandas as pd

balance_df = pd.read_csv("data/processed/balancesheet.csv")

print(balance_df.columns.tolist())