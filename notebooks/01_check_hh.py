import pandas as pd

df = pd.read_csv("../data/raw/hh_raw.csv")

print(f"rows: {len(df)}")
print(f"columns: {df.columns.tolist()}")
print(f"\nАFirst 3vacancies:")
print(df[["title", "company_name", "has_salary", "has_company_name"]].head(3))
print(f"\nEmpty:")
print(df.isnull().sum())