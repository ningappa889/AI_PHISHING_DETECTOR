import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/malicious_phish.csv")

# Display the first 5 rows
print("First 5 Rows:")
print(df.head())

# Display information about the dataset
print("\nDataset Information:")
print(df.info())

# Display the dataset shape
print("\nShape of Dataset:")
print(df.shape)

# Display column names
print("\nColumn Names:")
print(df.columns)

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Display class distribution
print("\nLabel Distribution:")
print(df["type"].value_counts())