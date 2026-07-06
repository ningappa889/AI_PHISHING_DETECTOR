import joblib

# Load model and vectorizer
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

while True:
    url = input("\nEnter URL (or type 'exit' to quit): ")

    if url.lower() == "exit":
        break

    # Convert URL into numerical features
    url_vector = vectorizer.transform([url])

    # Predict
    prediction = model.predict(url_vector)[0]

    # Confidence
    confidence = model.predict_proba(url_vector)[0]

    if prediction == 0:
        print(f"\n✅ Safe Website")
        print(f"Confidence: {confidence[0]*100:.2f}%")
    else:
        print(f"\n⚠️ Phishing Website")
        print(f"Confidence: {confidence[1]*100:.2f}%")