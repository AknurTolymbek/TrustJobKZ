import pandas as pd

hh = pd.read_csv("../data/raw/hh_raw.csv")
olx = pd.read_csv("../data/raw/olx_raw.csv")

olx = olx.drop(columns=["location"], errors="ignore")

df = pd.concat([hh, olx], ignore_index=True)

print(f"Before removing duplicates: {len(df)}")

# Удаляем дубликаты по url — одна ссылка = одна вакансия
df = df.drop_duplicates(subset=["url"], keep="first")

print(f"After removing duplicates: {len(df)}")
print(f"\nBy Source:")
print(df["source"].value_counts())

df.to_csv("../data/raw/all_raw.csv", index=False)
print("\nСохранено → data/raw/all_raw.csv")