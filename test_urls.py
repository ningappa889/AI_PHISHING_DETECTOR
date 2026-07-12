import joblib
from scipy.sparse import hstack
from utils.feature_matrix import build_feature_dataframe

model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

urls = [
    "https://www.google.com",
    "https://google.com",
    "https://www.amazon.com",
    "https://github.com",
    "https://www.microsoft.com",
    "http://paypal-login-security.xyz",
    "http://drive-google-com.fanalav.com",
    "https://openai.com"
]

for url in urls:

    tfidf = vectorizer.transform([url])
    features = build_feature_dataframe([url])

    X = hstack([tfidf, features.values])

    prediction = model.predict(X)[0]

    result = "SAFE" if prediction == 0 else "PHISHING"

    print(f"{url}\n→ {result}\n")