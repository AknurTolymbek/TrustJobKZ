import pandas as pd
import pickle
import re
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack, csr_matrix

df = pd.read_csv("../data/raw/all_labeled.csv")
df = df.dropna(subset=["label"])
df["label"] = df["label"].astype(int)

def clean_text(text):
    if not isinstance(text, str) or text.strip() == "":
        return ""
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    text = text.lower()
    text = re.sub(r"[^а-яёa-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["text"] = (df["title"].apply(clean_text) + " " +
              df["description"].apply(clean_text))

print("Running TF-IDF vectorization...")
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=5000,
    min_df=2
)

X_tfidf = vectorizer.fit_transform(df["text"])
print(f"TF-IDF matrix shape: {X_tfidf.shape}")

df["has_company_name"] = df["has_company_name"].fillna(0).astype(int)
df["has_salary"] = df["has_salary"].fillna(0).astype(int)

binary_features = csr_matrix(
    df[["has_company_name", "has_salary"]].values
)

X = hstack([X_tfidf, binary_features])
y = df["label"].values

print(f"Final feature matrix shape: {X.shape}")
print(f"Total samples: {len(y)}")
print(f"Real vacancies (0): {(y==0).sum()}")
print(f"Fake vacancies (1): {(y==1).sum()}")

with open("../data/clean/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("../data/clean/X.pkl", "wb") as f:
    pickle.dump(X, f)

with open("../data/clean/y.pkl", "wb") as f:
    pickle.dump(y, f)

df.to_csv("../data/clean/dataset_clean.csv", index=False)

print("\nDone! Saved to data/clean/:")
print("  tfidf_vectorizer.pkl  <- vectorizer")
print("  X.pkl                 <- feature matrix")
print("  y.pkl                 <- labels")
print("  dataset_clean.csv     <- clean dataset")