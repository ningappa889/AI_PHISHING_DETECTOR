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


TRUSTED_DOMAINS = {
    "google.com", "google.co.in", "google.co.uk",
    "amazon.com", "github.com", "microsoft.com",
    "apple.com", "paypal.com", "openai.com", "facebook.com",
    "twitter.com", "linkedin.com", "youtube.com", "instagram.com",
    "wikipedia.org", "yahoo.com", "netflix.com"
}


def is_trusted_domain(url):
    cleaned = clean_url(url)
    try:
        netloc = urlparse("http://" + cleaned).netloc
    except Exception:
        netloc = cleaned.split("/")[0].split(":")[0]
    parts = netloc.lower().split(".")
    if len(parts) >= 2:
        reg_domain = ".".join(parts[-2:])
    else:
        reg_domain = netloc.lower()
    return reg_domain in TRUSTED_DOMAINS


def has_suspicious_domain_pattern(url):
    if is_trusted_domain(url):
        return False
    feats = extract_features(url)
    if feats["suspicious_keywords"] >= 2 or (feats["suspicious_keywords"] >= 1 and feats["hyphen_count"] >= 1):
        return True
    return False


def extract_features(url):

    cleaned = clean_url(url)

    # Prepend a dummy scheme so urlparse can correctly split netloc/path
    # for ANY input. Handle malformed URLs gracefully if urlparse raises ValueError (e.g. invalid IPv6 brackets).
    try:
        parsed = urlparse("http://" + cleaned)
        netloc = parsed.netloc
    except Exception:
        netloc = cleaned.split("/")[0].split(":")[0]

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
        "bonus",
        "benefits",
        "access",
        "claim",
        "portal",
        "support",
        "service",
        "billing",
        "help",
        "info",
        "confirm",
        "admin",
        "security",
        "wallet"
    ]

    return {

        "url_length": len(cleaned),

        "domain_length": len(netloc),

        "dot_count": cleaned.count("."),

        "hyphen_count": cleaned.count("-"),

        "slash_count": cleaned.count("/"),

        "digit_count": sum(c.isdigit() for c in cleaned),

        "contains_at": 1 if "@" in cleaned else 0,

        "contains_ip": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", netloc) else 0,

        "subdomain_count": max(len(netloc.split(".")) - 2, 0),

        "suspicious_keywords":
            sum(word in cleaned.lower() for word in keywords),

        "entropy": entropy(cleaned)
    }