import joblib
import pandas as pd
from scipy.sparse import hstack
from utils.feature_matrix import build_feature_dataframe

# Load model and vectorizer
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# Test URLs
urls = [
    "https://www.google.com",
    "http://paypal-login-security.xyz"
]

# Build features
tfidf = vectorizer.transform(urls)
features = build_feature_dataframe(urls)

X = hstack([tfidf, features.values])

print("Prediction:", model.predict(X))

print("Decision Function:", model.decision_function(X))