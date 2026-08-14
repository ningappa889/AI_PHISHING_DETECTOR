import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack, csr_matrix
from utils.feature_extractor import clean_url
from utils.feature_matrix import build_feature_dataframe

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ================================
# Load Dataset
# ================================
print("\nLoading dataset...")

df = pd.read_csv("dataset/cleaned_dataset.csv")

raw_urls = df["url"]
cleaned_urls = raw_urls.apply(clean_url)

y = df["label"]

print("Building TF-IDF Matrix...")

vectorizer = TfidfVectorizer(
    max_features=100000,
    ngram_range=(1, 2),
    min_df=2
)

tfidf_features = vectorizer.fit_transform(cleaned_urls)

print("Building URL Feature Matrix...")

url_features = build_feature_dataframe(raw_urls)

# ================================
# Scale handcrafted features
# ================================
# Handcrafted features (domain_length, url_length, dot_count, etc.) are on
# very different numeric scales than TF-IDF weights (0-1 range). Without
# scaling, large raw counts like domain_length can dominate the decision
# function just because of their magnitude, not because they're actually
# more predictive. StandardScaler fixes this.
print("Scaling handcrafted features...")

scaler = StandardScaler()
url_features_scaled = scaler.fit_transform(url_features.values)

print("Combining Features...")

X = hstack([tfidf_features, csr_matrix(url_features_scaled)])

# ================================
# Train-Test Split
# ================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n==============================================")
print("Training Samples :", X_train.shape)
print("Testing Samples  :", X_test.shape)
print("==============================================")

# ================================
# Models
# ================================
# class_weight="balanced" compensates for the ~82/18 safe/phishing
# imbalance in the dataset so the model doesn't just lean toward
# predicting the majority class.
models = {

    "Logistic Regression":
        LogisticRegression(
    solver="liblinear",
    max_iter=2000,
    random_state=42,
    class_weight="balanced"
),

    "Multinomial Naive Bayes":
        MultinomialNB(),

    "Linear SVM":
        LinearSVC(
            class_weight="balanced",
            max_iter=10000
        )
}

best_model = None
best_name = ""
best_accuracy = 0

results = []

# ================================
# Train Models
# ================================
for name, model in models.items():

    print(f"\nTraining {name}...")

    # MultinomialNB requires non-negative input; scaled features can be
    # negative, so skip scaling issues by only feeding it TF-IDF if needed.
    if name == "Multinomial Naive Bayes":
        # Naive Bayes assumes non-negative counts, so give it the
        # unscaled, non-negative version instead of the standardized one.
        X_nb = hstack([tfidf_features, url_features.values])
        X_train_nb, X_test_nb, _, _ = train_test_split(
            X_nb, y, test_size=0.20, random_state=42, stratify=y
        )
        model.fit(X_train_nb, y_train)
        y_pred = model.predict(X_test_nb)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    results.append((name, accuracy))

    print(f"Accuracy : {accuracy:.4f}")
    print(classification_report(y_test, y_pred))

    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_name = name

# ================================
# Results
# ================================
print("\n")
print("=" * 50)
print("MODEL COMPARISON")
print("=" * 50)

for name, accuracy in results:
    print(f"{name:<30} {accuracy:.4f}")

print("=" * 50)

print(f"\nBest Model : {best_name}")
print(f"Accuracy   : {best_accuracy:.4f}")

# ================================
# Evaluation
# ================================
print("\nClassification Report\n")

if best_name == "Multinomial Naive Bayes":
    X_nb = hstack([tfidf_features, url_features.values])
    _, X_test_final, _, y_test_final = train_test_split(
        X_nb, y, test_size=0.20, random_state=42, stratify=y
    )
else:
    X_test_final, y_test_final = X_test, y_test

y_pred = best_model.predict(X_test_final)

print(classification_report(y_test_final, y_pred))

print("Confusion Matrix\n")

print(confusion_matrix(y_test_final, y_pred))

# ================================
# Save Best Model + Scaler + Vectorizer
# ================================
joblib.dump(best_model, "model/phishing_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("\n==============================================")
print("Best model saved successfully!")
print("Saved Model :", best_name)
print("Scaler saved to model/scaler.pkl")
print("==============================================")