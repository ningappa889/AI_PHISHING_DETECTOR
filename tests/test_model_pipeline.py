import unittest
import os
import joblib
from scipy.sparse import hstack, csr_matrix
from utils.feature_extractor import clean_url, is_trusted_domain
from utils.feature_matrix import build_feature_dataframe

class TestModelPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model_path = "model/phishing_model.pkl"
        cls.vectorizer_path = "model/vectorizer.pkl"
        cls.scaler_path = "model/scaler.pkl"

        assert os.path.exists(cls.model_path), "Model file missing"
        assert os.path.exists(cls.vectorizer_path), "Vectorizer file missing"
        assert os.path.exists(cls.scaler_path), "Scaler file missing"

        cls.model = joblib.load(cls.model_path)
        cls.vectorizer = joblib.load(cls.vectorizer_path)
        cls.scaler = joblib.load(cls.scaler_path)

    def predict_url(self, url):
        if is_trusted_domain(url):
            return 0
        cleaned_url = clean_url(url)
        tfidf = self.vectorizer.transform([cleaned_url])
        raw_features = build_feature_dataframe([url])
        scaled_features = self.scaler.transform(raw_features.values)
        X = hstack([tfidf, csr_matrix(scaled_features)])
        return self.model.predict(X)[0]

    def test_safe_url_prediction(self):
        pred = self.predict_url("https://www.google.com")
        self.assertEqual(pred, 0, "google.com should be predicted as safe (0)")

    def test_phishing_url_prediction(self):
        pred = self.predict_url("http://paypal-login-security.xyz")
        self.assertEqual(pred, 1, "paypal-login-security.xyz should be predicted as phishing (1)")

if __name__ == "__main__":
    unittest.main()
