import joblib
from scipy.sparse import hstack, csr_matrix

from utils.feature_extractor import clean_url
from utils.feature_matrix import build_feature_dataframe

# Load model, vectorizer, and scaler
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")
scaler = joblib.load("model/scaler.pkl")

while True:

    url = input("\nEnter URL (or type 'exit' to quit): ")

    if url.lower() == "exit":
        break

    # TF-IDF Features
    cleaned_url = clean_url(url)
    tfidf = vectorizer.transform([cleaned_url])

    # Handcrafted URL Features
    url_features = build_feature_dataframe([url])

    # Scale handcrafted features using the SAME scaler fit during training.
    # This must match train_model.py exactly, or the feature magnitudes
    # won't line up with what the model learned.
    url_features_scaled = scaler.transform(url_features.values)

    # Combine Features
    X = hstack([tfidf, csr_matrix(url_features_scaled)])

    # Prediction
    prediction = model.predict(X)[0]

    print("\n" + "=" * 40)

    if prediction == 0:
        print("[SAFE] SAFE WEBSITE")
    else:
        print("[WARNING] PHISHING WEBSITE")

    print("=" * 40)

    print("\nExtracted Features (raw, before scaling)\n")

    for feature, value in url_features.iloc[0].items():
        print(f"{feature:25} : {value}")

    print("\n")