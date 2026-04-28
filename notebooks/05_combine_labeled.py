import pandas as pd

part1 = pd.read_csv("../data/raw/part_ayaulym_done.csv", sep=";")
part2 = pd.read_csv("../data/raw/part_aknur_done.csv", sep=";")
part3 = pd.read_csv("../data/raw/part_aruzhan_done.csv", sep=";")

df = pd.concat([part1, part2, part3], ignore_index=True)

print(f"All: {len(df)}")
print(f"Labeled: {df['label'].notna().sum()}")
print(f"Unlabeled: {df['label'].isna().sum()}")
print(f"Distribution of labels:\n:")
print(df['label'].value_counts())

df.to_csv("../data/raw/all_labeled.csv", index=False)
print("\nСохранено → data/raw/all_labeled.csv")