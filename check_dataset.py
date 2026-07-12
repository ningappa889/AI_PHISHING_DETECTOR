import pandas as pd

# Load dataset
df = pd.read_csv("dataset/cleaned_dataset.csv")

# Websites to search
websites = [
    "google",
    "github",
    "chatgpt",
    "openai",
    "microsoft",
    "amazon",
    "facebook",
    "paypal"
]

for site in websites:
    result = df[df["url"].str.contains(site, case=False, na=False)]

    print("\n" + "=" * 60)
    print(f"{site.upper()}")

    if len(result) == 0:
        print("❌ Not found in dataset")
    else:
        print(f"Found {len(result)} URLs")
        print(result.head(5))