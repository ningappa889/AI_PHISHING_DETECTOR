import re
from urllib.parse import urlparse
from collections import Counter
from math import log2

def entropy(text):
    counter = Counter(text)
    total = len(text)

    if total == 0:
        return 0

    return -sum(
        (count / total) * log2(count / total)
        for count in counter.values()
    )


def clean_url(url):
    """
    Canonicalize a URL by stripping the scheme (http/https) and a leading
    'www.' so that URLs are represented consistently regardless of how the
    original data source formatted them.

    This matters because the training dataset mixes sources that format
    URLs differently (some with scheme+www, some bare domain-only), and
    that formatting difference - not actual maliciousness - was leaking
    into both the TF-IDF text and the handcrafted features. Normalizing
    here removes that shortcut so the model has to learn from real
    content instead.
    """
    u = url.strip()
    u = re.sub(r"^https?://", "", u, flags=re.IGNORECASE)
    u = re.sub(r"^www\.", "", u, flags=re.IGNORECASE)
    return u


def extract_features(url):

    has_https = 1 if re.match(r"^https://", url.strip(), re.IGNORECASE) else 0

    cleaned = clean_url(url)

    # Prepend a dummy scheme so urlparse can correctly split netloc/path
    # for ANY input, whether or not the original URL had a scheme. Without
    # this, urlparse silently returns an empty netloc for schemeless URLs,
    # which was previously causing domain_length/subdomain_count to be
    # wrongly computed as 0 for a large share of the dataset.
    parsed = urlparse("http://" + cleaned)

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

    return {

        "url_length": len(cleaned),

        "domain_length": len(parsed.netloc),

        "dot_count": cleaned.count("."),

        "hyphen_count": cleaned.count("-"),

        "slash_count": cleaned.count("/"),

        "digit_count": sum(c.isdigit() for c in cleaned),

        "https": has_https,

        "contains_at": 1 if "@" in cleaned else 0,

        "contains_ip": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", parsed.netloc) else 0,

        "subdomain_count": max(len(parsed.netloc.split(".")) - 2, 0),

        "suspicious_keywords":
            sum(word in cleaned.lower() for word in keywords),

        "entropy": entropy(cleaned)
    }