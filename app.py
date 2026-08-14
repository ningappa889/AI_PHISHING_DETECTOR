from flask import Flask, render_template, request
import joblib
import math
from scipy.sparse import hstack, csr_matrix

from utils.feature_extractor import clean_url, is_trusted_domain, has_suspicious_domain_pattern
from utils.feature_matrix import build_feature_dataframe

app = Flask(__name__)

# Load model, vectorizer, and scaler only once
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")
scaler = joblib.load("model/scaler.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    url = ""
    features = None
    risk_score = 0
    risk_level = ""
    risk_class = ""
    risk_icon = ""
    is_trusted = False

    if request.method == "POST":

        url = request.form.get("url", "").strip()

        if url:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            print("Scanning URL:", repr(url))

            # Build feature table for UI rendering
            feature_df = build_feature_dataframe([url])
            features = feature_df.iloc[0].to_dict()

            if is_trusted_domain(url):
                prediction = "SAFE"
                risk_score = 5
                is_trusted = True
            elif has_suspicious_domain_pattern(url):
                prediction = "PHISHING"
                risk_score = 92
                is_trusted = False
            else:
                cleaned_url = clean_url(url)
                tfidf = vectorizer.transform([cleaned_url])
                url_features_scaled = scaler.transform(feature_df.values)
                X = hstack([tfidf, csr_matrix(url_features_scaled)])

                result = model.predict(X)[0]

                if hasattr(model, "decision_function"):
                    raw_score = model.decision_function(X)[0]
                    prob = 1 / (1 + math.exp(-raw_score))
                    risk_score = int(round(prob * 100))
                else:
                    risk_score = 85 if result == 1 else 15

                is_structurally_clean = (
                    features.get("suspicious_keywords", 0) == 0 and
                    features.get("hyphen_count", 0) == 0 and
                    features.get("contains_ip", 0) == 0 and
                    features.get("subdomain_count", 0) <= 1 and
                    features.get("domain_length", 0) <= 30 and
                    features.get("slash_count", 0) <= 1
                )

                if is_structurally_clean and not has_suspicious_domain_pattern(url):
                    prediction = "SAFE"
                    risk_score = min(risk_score, 12)
                elif result == 1:
                    prediction = "PHISHING"
                    risk_score = max(risk_score, 75)
                else:
                    prediction = "SAFE"
                    risk_score = min(risk_score, 45)

            # Categorize into 5 explicit risk tiers with icons & colors
            if risk_score <= 15:
                risk_level = "Minimal Risk"
                risk_class = "risk-minimal"
                risk_icon = "shield-check"
            elif risk_score <= 35:
                risk_level = "Low Risk"
                risk_class = "risk-low"
                risk_icon = "info"
            elif risk_score <= 60:
                risk_level = "Moderate Risk"
                risk_class = "risk-moderate"
                risk_icon = "alert-triangle"
            elif risk_score <= 84:
                risk_level = "High Risk"
                risk_class = "risk-high"
                risk_icon = "alert-octagon"
            else:
                risk_level = "Critical Risk"
                risk_class = "risk-critical"
                risk_icon = "skull"

    return render_template(
        "index.html",
        prediction=prediction,
        url=url,
        features=features,
        risk_score=risk_score,
        risk_level=risk_level,
        risk_class=risk_class,
        risk_icon=risk_icon,
        is_trusted=is_trusted
    )


if __name__ == "__main__":
    app.run(debug=True)