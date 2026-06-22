from src.etl.loader import *

companies_df = load_companies()

print(companies_df.tail(15)[["id", "company_name"]])
print("Rows:", len(companies_df))