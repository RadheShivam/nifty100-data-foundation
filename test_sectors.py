from src.etl.loader import *

sectors_df = load_sectors()

print(sectors_df.columns)
print(sectors_df.head())
print(sectors_df.shape)

print(sectors_df.columns)