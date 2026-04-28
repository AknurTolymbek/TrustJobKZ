import pandas as pd

hh = pd.read_csv("../data/raw/hh_raw.csv")
olx = pd.read_csv("../data/raw/olx_raw.csv")

print("HH.KZ")
print(f"Строк: {len(hh)}")
print(hh[["title", "company_name", "has_salary", "has_company_name"]].head(3))

print("\nOLX.KZ")
print(f"Строк: {len(olx)}")
print(olx[["title", "company_name", "has_salary", "has_company_name"]].head(3))

print("\nALL")
print(f"Together: {len(hh) + len(olx)}")
print(f"hh.kz with company : {hh['has_company_name'].sum()} из {len(hh)}")
print(f"olx.kz with company: {olx['has_company_name'].sum()} из {len(olx)}")
print(f"hh.kz with salary: {hh['has_salary'].sum()} из {len(hh)}")
print(f"olx.kz with salary: {olx['has_salary'].sum()} из {len(olx)}")