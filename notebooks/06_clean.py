import re
import pandas as pd
from bs4 import BeautifulSoup

def clean_text(text):
    if not isinstance(text, str) or text.strip() == "":
        return ""
    # Убираем HTML теги
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    # Нижний регистр
    text = text.lower()
    # Убираем спецсимволы, оставляем только буквы и цифры
    text = re.sub(r"[^а-яёa-z0-9\s]", " ", text)
    # Убираем лишние пробелы
    text = re.sub(r"\s+", " ", text).strip()
    return text

df = pd.read_csv("../data/raw/all_labeled.csv")

# Убираем 3 неразмеченных
df = df.dropna(subset=["label"])
df["label"] = df["label"].astype(int)

# Очищаем текстовые колонки
print("Cleaning up texts...")
df["title_clean"] = df["title"].apply(clean_text)
df["description_clean"] = df["description"].apply(clean_text)

# Объединяем title + description в один текст для TF-IDF
df["text"] = df["title_clean"] + " " + df["description_clean"]

print(f"Rows: {len(df)}")
print(f"\nExample of cleared text:")
print(df["text"].iloc[0][:200])

df.to_csv("../data/clean/dataset_clean.csv", index=False)
print("\nSaved to → data/clean/dataset_clean.csv")