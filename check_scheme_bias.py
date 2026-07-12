import pandas as pd

df = pd.read_csv("dataset/cleaned_dataset.csv")

df["has_scheme"] = df["url"].str.contains(r"^https?://", regex=True, na=False)

print("Cross-tab of has_scheme vs label:\n")
print(pd.crosstab(df["has_scheme"], df["label"], margins=True))

print("\nPercent phishing WITH scheme:",
      round(df[df["has_scheme"]]["label"].mean() * 100, 2), "%")

print("Percent phishing WITHOUT scheme:",
      round(df[~df["has_scheme"]]["label"].mean() * 100, 2), "%")

print("\nBreakdown by www prefix too:")
df["has_www"] = df["url"].str.contains(r"^https?://www\.|^www\.", regex=True, na=False)
print(pd.crosstab(df["has_www"], df["label"], margins=True))