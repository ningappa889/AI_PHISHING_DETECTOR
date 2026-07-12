import pandas as pd

df = pd.read_csv("dataset/cleaned_dataset.csv")

exact = df[df["url"] == "https://www.google.com"]

print(exact)

print("\nCount:", len(exact))