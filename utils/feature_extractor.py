import re
from urllib.parse import urlparse
from collections import Counter
from math import log2

def entropy(text):
    counter = Counter(text)
    total = len(text)

    return -sum(
        (count / total) * log2(count / total)
        for count in counter.values()
    )

def extract_features(url):
    parsed = urlparse(url)

    features = {}

    features["url_length"] = len(url)
    features["domain_length"] = len(parsed.netloc)
    features["dot_count"] = url.count(".")
    features["hyphen_count"] = url.count("-")
    features["slash_count"] = url.count("/")
    features["digit_count"] = sum(c.isdigit() for c in url)

    features["https"] = 1 if parsed.scheme == "https" else 0

    features["contains_at"] = 1 if "@" in url else 0

    ip_pattern = r"\d+\.\d+\.\d+\.\d+"
    features["contains_ip"] = 1 if re.search(ip_pattern, url) else 0

    features["subdomain_count"] = max(len(parsed.netloc.split(".")) - 2, 0)

    keywords = [
        "login",
        "secure",
        "verify",
        "update",
        "account",
        "signin",
        "bank",
        "paypal",
        "free",
        "bonus"
    ]

    features["suspicious_keywords"] = sum(
        word in url.lower() for word in keywords
    )

    features["entropy"] = entropy(url)

    return features