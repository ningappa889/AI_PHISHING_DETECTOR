from flask import Flask, render_template, request
import joblib
import math
from scipy.sparse import hstack, csr_matrix

from utils.feature_extractor import clean_url, is_trusted_domain, has_suspicious_domain_pattern, generate_analysis_reasoning
from utils.feature_matrix import build_feature_dataframe

app = Flask(__name__)

# Load model, vectorizer, and scaler only once
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")
scaler = joblib.load("model/scaler.pkl")


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/scan", methods=["GET", "POST"])
def scan():

    prediction = None
    url = ""
    features = None
    risk_score = 0
    risk_level = ""
    risk_class = ""
    risk_icon = ""
    is_trusted = False
    reasons = []

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
                is_trusted = True
                # Dynamic minimal risk percentage between 3% and 12%
                entropy_val = features.get("entropy", 2.0)
                url_len = features.get("url_length", 10)
                risk_score = min(12, max(3, int(3 + (entropy_val * 1.5) + (url_len % 4))))
            elif has_suspicious_domain_pattern(url):
                prediction = "PHISHING"
                is_trusted = False
                # Dynamic threat density score for heuristic phishing
                threat_boost = (features.get("suspicious_keywords", 0) * 8) + \
                               (features.get("hyphen_count", 0) * 6) + \
                               (features.get("subdomain_count", 0) * 7) + \
                               (features.get("contains_ip", 0) * 20) + \
                               (features.get("slash_count", 0) * 3)
                risk_score = min(98, max(72, int(72 + threat_boost)))
            else:
                cleaned_url = clean_url(url)
                tfidf = vectorizer.transform([cleaned_url])
                url_features_scaled = scaler.transform(feature_df.values)
                X = hstack([tfidf, csr_matrix(url_features_scaled)])

                result = model.predict(X)[0]

                if hasattr(model, "decision_function"):
                    raw_score = model.decision_function(X)[0]
                    prob = 1 / (1 + math.exp(-raw_score))
                    base_prob = int(round(prob * 100))
                else:
                    base_prob = 80 if result == 1 else 20

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
                    entropy_val = features.get("entropy", 2.5)
                    risk_score = min(18, max(6, int(6 + (entropy_val * 2.5) + features.get("dot_count", 1))))
                elif result == 1:
                    prediction = "PHISHING"
                    threat_boost = (features.get("suspicious_keywords", 0) * 6) + (features.get("hyphen_count", 0) * 5)
                    risk_score = min(98, max(68, max(base_prob, 68) + threat_boost))
                else:
                    prediction = "SAFE"
                    base = 16 + (features.get("dot_count", 1) * 4) + (features.get("slash_count", 0) * 5) + int(features.get("entropy", 3.0) * 3)
                    risk_score = min(48, max(16, base))

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

            # Generate Explainable AI Reasoning Analysis Points
            reasons = generate_analysis_reasoning(url, prediction, features, is_trusted)

    return render_template(
        "index.html",
        prediction=prediction,
        url=url,
        features=features,
        risk_score=risk_score,
        risk_level=risk_level,
        risk_class=risk_class,
        risk_icon=risk_icon,
        is_trusted=is_trusted,
        reasons=reasons
    )


if __name__ == "__main__":
    app.run(debug=True)