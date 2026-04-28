import pandas as pd

df = pd.read_csv("../data/raw/all_raw.csv")

# Добавляем id
df["id"] = range(1, len(df) + 1)

# Перемешиваем случайно но одинаково каждый раз (random_state фиксирует результат)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Делим на 3 части
n = len(df)
part1 = df.iloc[0:n//3]
part2 = df.iloc[n//3:2*n//3]
part3 = df.iloc[2*n//3:]

part1.to_csv("../data/raw/part_ayaulym.csv", index=False)
part2.to_csv("../data/raw/part_aknur.csv", index=False)
part3.to_csv("../data/raw/part_aruzhan.csv", index=False)

print(f"All: {n} vacancies")
print(f"\nAyaulym:  {len(part1)} vacancies")
print(f"  hh.kz:  {(part1['source']=='hh.kz').sum()}")
print(f"  olx.kz: {(part1['source']=='olx.kz').sum()}")
print(f"\nAknur:   {len(part2)}vacancies")
print(f"  hh.kz:  {(part2['source']=='hh.kz').sum()}")
print(f"  olx.kz: {(part2['source']=='olx.kz').sum()}")
print(f"\nAruzhan:  {len(part3)} vacancies")
print(f"  hh.kz:  {(part3['source']=='hh.kz').sum()}")
print(f"  olx.kz: {(part3['source']=='olx.kz').sum()}")