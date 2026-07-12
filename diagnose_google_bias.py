import pandas as pd
import joblib

df = pd.read_csv("dataset/cleaned_dataset.csv")

# 1. How many URLs contain "google" and what are their labels?
contains_google = df[df["url"].str.contains("google", case=False, na=False)]

print("Total rows containing 'google':", len(contains_google))
print("\nLabel distribution among 'google' URLs:")
print(contains_google["label"].value_counts())

print("\nSample rows:")
print(contains_google[["url", "label"]].head(20).to_string())

# 2. Overall dataset label balance (sanity check)
print("\nOverall label distribution:")
print(df["label"].value_counts())

# 3. Check what the TF-IDF vectorizer learned for the token "google"
vectorizer = joblib.load("model/vectorizer.pkl")
model = joblib.load("model/phishing_model.pkl")

vocab = vectorizer.vocabulary_

if "google" in vocab:
    idx = vocab["google"]
    print(f"\n'google' token index in vocabulary: {idx}")
    print("IDF weight for 'google':", vectorizer.idf_[idx])

    # If model has coefficients (Logistic Regression / Linear SVM)
    if hasattr(model, "coef_"):
        coef = model.coef_[0][idx]
        print("Model coefficient for 'google' token:", coef)
        print("(Positive = pushes toward PHISHING, Negative = pushes toward SAFE)")
else:
    print("\n'google' not found as a standalone token in vocabulary (check ngrams like 'google com', 'www google').")
    # check for any vocab entries containing 'google'
    matches = {k: v for k, v in vocab.items() if "google" in k}
    print("Vocab entries containing 'google':", matches)
    if hasattr(model, "coef_"):
        for token, idx in matches.items():
            print(f"  coef for '{token}':", model.coef_[0][idx])