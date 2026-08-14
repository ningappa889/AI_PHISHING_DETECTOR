import unittest
from utils.feature_extractor import clean_url, entropy, extract_features

class TestFeatureExtractor(unittest.TestCase):

    def test_clean_url(self):
        self.assertEqual(clean_url("https://www.google.com"), "google.com")
        self.assertEqual(clean_url("http://www.google.com"), "google.com")
        self.assertEqual(clean_url("http://google.com"), "google.com")
        self.assertEqual(clean_url("https://sub.domain.com/path"), "sub.domain.com/path")

    def test_entropy(self):
        self.assertEqual(entropy("aaaaa"), 0.0)
        self.assertGreater(entropy("abcdef"), 0.0)

    def test_extract_features_keys(self):
        features = extract_features("https://www.google.com")
        expected_keys = {
            "url_length",
            "domain_length",
            "dot_count",
            "hyphen_count",
            "slash_count",
            "digit_count",
            "contains_at",
            "contains_ip",
            "subdomain_count",
            "suspicious_keywords",
            "entropy"
        }
        self.assertEqual(set(features.keys()), expected_keys)

    def test_extract_features_ip_detection(self):
        features_ip = extract_features("http://192.168.1.1/login")
        self.assertEqual(features_ip["contains_ip"], 1)

        features_domain = extract_features("http://google.com")
        self.assertEqual(features_domain["contains_ip"], 0)

if __name__ == "__main__":
    unittest.main()
