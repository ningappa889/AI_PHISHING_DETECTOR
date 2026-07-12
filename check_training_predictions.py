import pandas as pd
import joblib
from scipy.sparse import hstack
from utils.feature_matrix import build_feature_dataframe

# Load training data
df = pd.read_csv("dataset/cleaned_dataset.csv")

# Load model
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# Test on REAL training samples
samples = df.sample(10, random_state=42)

urls = samples["url"]
labels = samples["label"]

tfidf = vectorizer.transform(urls)
features = build_feature_dataframe(urls)

X = hstack([tfidf, features.values])

predictions = model.predict(X)

for url, actual, pred in zip(urls, labels, predictions):
    print("-" * 80)
    print(url)
    print(f"Actual    : {actual}")
    print(f"Predicted : {pred}")