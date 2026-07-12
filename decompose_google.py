import joblib
import numpy as np
from scipy.sparse import hstack

from utils.feature_matrix import build_feature_dataframe

model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

url = "https://www.google.com"

tfidf = vectorizer.transform([url])
url_features_df = build_feature_dataframe([url])
X = hstack([tfidf, url_features_df.values]).tocsr()

print("Model type:", type(model).__name__)

# Raw decision score (works for LogisticRegression and LinearSVC)
if hasattr(model, "decision_function"):
    score = model.decision_function(X)[0]
    print("Decision function score:", score)
    print("(Positive = phishing side, Negative = safe side, 0 = boundary)")
elif hasattr(model, "predict_proba"):
    proba = model.predict_proba(X)[0]
    print("Predicted probabilities [safe, phishing]:", proba)

print("Prediction:", model.predict(X)[0], "(0=safe, 1=phishing)")

# Break down contribution per feature, if linear model
if hasattr(model, "coef_"):
    coef = model.coef_[0]
    tfidf_feature_names = list(vectorizer.get_feature_names_out())
    handcrafted_names = list(url_features_df.columns)
    all_names = tfidf_feature_names + handcrafted_names

    X_dense = X.toarray()[0]
    contributions = X_dense * coef

    # Sort by absolute contribution, show top 20
    idx_sorted = np.argsort(-np.abs(contributions))[:20]

    print("\nTop 20 contributing features for this URL:")
    print(f"{'feature':30} {'value':>10} {'coef':>10} {'contribution':>14}")
    for i in idx_sorted:
        if X_dense[i] != 0:
            print(f"{all_names[i]:30} {X_dense[i]:>10.4f} {coef[i]:>10.4f} {contributions[i]:>14.4f}")

    print("\nSum of all TF-IDF contributions:", np.sum(contributions[:len(tfidf_feature_names)]))
    print("Sum of all handcrafted feature contributions:", np.sum(contributions[len(tfidf_feature_names):]))
    print("Intercept:", model.intercept_[0])