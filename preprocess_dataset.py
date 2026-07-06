import pandas as pd

# Load dataset
df = pd.read_csv("dataset/malicious_phish.csv")

print("Original Shape:", df.shape)

# Convert labels
df["label"] = df["type"].apply(
    lambda x: 0 if x == "benign" else 1
)

# Keep only required columns
df = df[["url", "label"]]

print("\nFirst 5 Rows:")
print(df.head())

print("\nNew Label Distribution:")
print(df["label"].value_counts())

# Save cleaned dataset
df.to_csv("dataset/cleaned_dataset.csv", index=False)

print("\nDataset saved as cleaned_dataset.csv")
