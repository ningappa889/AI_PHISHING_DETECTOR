import pandas as pd

# Load original dataset
df = pd.read_csv("dataset/malicious_phish.csv")

print("Original Shape:", df.shape)

# Keep only benign and phishing URLs
df = df[df["type"].isin(["benign", "phishing"])]

# Create binary labels
df["label"] = df["type"].map({
    "benign": 0,
    "phishing": 1
})

# Keep only required columns
df = df[["url", "label"]]

print("\nNew Shape:", df.shape)

print("\nLabel Distribution:")
print(df["label"].value_counts())

# Save cleaned dataset
df.to_csv("dataset/cleaned_dataset.csv", index=False)

print("\nSaved as dataset/cleaned_dataset.csv")