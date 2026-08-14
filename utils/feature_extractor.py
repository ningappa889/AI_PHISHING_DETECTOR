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
    u = url.strip()
    # Handle defanged URL notations like hxxps:// or [.]
    u = re.sub(r"\[\.\]|\(\.\)", ".", u)
    # Recursively strip schemes in case of double prefixes like https://hxxps://
    while re.match(r"^(https?://|h[xt]{2}ps?://)", u, flags=re.IGNORECASE):
        u = re.sub(r"^(https?://|h[xt]{2}ps?://)", "", u, flags=re.IGNORECASE)
    u = re.sub(r"^www\.", "", u, flags=re.IGNORECASE)
    return u


# Reserved institutional & government suffixes that CANNOT be registered by unauthorized individuals
TRUSTED_TLD_SUFFIXES = (
    ".gov", ".gov.in", ".gov.uk", ".gov.au", ".gov.ca",
    ".nic.in", ".edu", ".edu.in", ".ac.in", ".mil", ".res.in", ".org.in"
)

# Known 2-part TLD suffixes to properly extract registered domains (e.g. sbi.co.in -> sbi.co.in, not co.in)
TWO_PART_TLDS = {
    "co.in", "gov.in", "net.in", "org.in", "edu.in", "ac.in", "nic.in", "res.in",
    "co.uk", "gov.uk", "org.uk", "ac.uk",
    "com.au", "gov.au", "edu.au", "org.au",
    "co.jp", "ne.jp", "ac.jp"
}

TRUSTED_DOMAINS = {
    # Indian Banking, Digital Payments & Financial Services
    "phonepe.com", "paytm.com", "bhimupi.org.in", "npci.org.in", "gpay.com",
    "sbi.co.in", "onlinesbi.sbi", "sbi.sbi", "hdfcbank.com", "icicibank.com",
    "axisbank.com", "kotak.com", "pnbindia.in", "bankofbaroda.in", "canarabank.com",
    "cred.club", "razorpay.com", "zerodha.com", "groww.in", "upstox.com", "paytm.in",

    # Indian Official Portals & E-Commerce / Services
    "uidai.gov.in", "irctc.co.in", "flipkart.com", "myntra.com", "meesho.com",
    "swiggy.com", "zomato.com", "zepto.com", "blinkit.com", "bigbasket.com",
    "bookmyshow.com", "makemytrip.com", "redbus.in", "licindia.in", "epfindia.gov.in",
    "incometax.gov.in", "passportindia.gov.in", "parivahan.gov.in", "digilocker.gov.in",
    "airtel.in", "jio.com", "tataplay.com", "hotstar.com",

    # Global Tech, News, Social, Search & AI Platforms
    "google.com", "google.co.in", "google.co.uk", "youtube.com", "gmail.com",
    "amazon.com", "amazon.in", "apple.com", "microsoft.com", "github.com", "gitlab.com",
    "openai.com", "chatgpt.com", "claude.ai", "anthropic.com", "perplexity.ai",
    "facebook.com", "instagram.com", "whatsapp.com", "twitter.com", "x.com",
    "linkedin.com", "reddit.com", "netflix.com", "spotify.com", "wikipedia.org",
    "geeksforgeeks.org", "stackoverflow.com", "medium.com", "coursera.org",
    "udemy.com", "quora.com", "canva.com", "figma.com", "adobe.com", "zoom.us",
    "notion.so", "paypal.com", "yahoo.com", "bbc.com", "cnn.com", "nytimes.com",
    "theguardian.com", "reuters.com", "bloomberg.com", "forbes.com", "ndtv.com",
    "indiatimes.com", "hindustantimes.com", "thehindu.com", "indianexpress.com"
}


def is_trusted_domain(url):
    cleaned = clean_url(url)
    try:
        netloc = urlparse("http://" + cleaned).netloc
    except Exception:
        netloc = cleaned.split("/")[0].split(":")[0]

    netloc_lower = netloc.lower()

    # 1. Government and official education TLDs are inherently trusted
    if netloc_lower.endswith(TRUSTED_TLD_SUFFIXES):
        return True

    parts = netloc_lower.split(".")

    # 2. Handle 2-part TLDs (like sbi.co.in -> sbi.co.in)
    if len(parts) >= 3 and ".".join(parts[-2:]) in TWO_PART_TLDS:
        reg_domain = ".".join(parts[-3:])
    elif len(parts) >= 2:
        reg_domain = ".".join(parts[-2:])
    else:
        reg_domain = netloc_lower

    return reg_domain in TRUSTED_DOMAINS


SUSPICIOUS_TLDS = {
    ".top", ".online", ".cfd", ".xyz", ".site", ".icu", ".tk", ".ml", ".ga",
    ".cf", ".gq", ".zip", ".mov", ".bid", ".click", ".monster", ".fit", ".buzz",
    ".rest", ".work", ".beauty", ".hair", ".quest", ".live", ".shop", ".vip",
    ".space", ".vu", ".cyou", ".casa", ".cam", ".best", ".cc", ".to"
}


FREE_HOSTING_DOMAINS = (
    "workers.dev", "pages.dev", "herokuapp.com", "firebaseapp.com",
    "web.app", "glitch.me", "onrender.com", "surge.sh"
)


def has_suspicious_domain_pattern(url):
    if is_trusted_domain(url):
        return False

    cleaned = clean_url(url).lower()
    netloc = cleaned.split("/")[0].split(":")[0]

    # 1. Check for high-risk abused phishing TLDs or free hosting subdomains
    for tld in SUSPICIOUS_TLDS:
        if netloc.endswith(tld):
            return True

    if netloc.endswith(FREE_HOSTING_DOMAINS) and len(netloc.split(".")) >= 3:
        return True

    feats = extract_features(url)

    # 2. Check for DGA / alphanumeric scam domain pattern (e.g. flfwc26.com, 24benefits, win99)
    domain_name = netloc.split(".")[0]
    if re.search(r"[a-zA-Z]{3,}\d+", domain_name) or re.search(r"\d+[a-zA-Z]{3,}", domain_name):
        return True

    # 3. Check for suspicious keywords & structural traits
    if feats["suspicious_keywords"] >= 1:
        if feats["hyphen_count"] >= 1 or feats["subdomain_count"] >= 1 or "/" in cleaned:
            return True
        if feats["suspicious_keywords"] >= 2:
            return True

    # 4. Check for hyphenated domain names on non-trusted TLDs
    if feats["hyphen_count"] >= 1 and (feats["domain_length"] >= 12 or feats["suspicious_keywords"] >= 1):
        return True

    # 5. Check for suspicious path patterns (/v/index.html, /goldclie/new, /gRB0qs)
    parts = cleaned.split("/")
    if len(parts) > 1:
        path = "/".join(parts[1:])
        if any(token in path for token in ["/v/", "index.html", "login", "secure", "verify", "new", "gold"]):
            return True
        if len(parts[1]) >= 5 and re.match(r"^[a-zA-Z0-9_-]+$", parts[1]) and not parts[1].endswith((".html", ".php", ".htm")):
            return True

    return False


def extract_features(url):

    cleaned = clean_url(url)

    try:
        parsed = urlparse("http://" + cleaned)
        netloc = parsed.netloc
    except Exception:
        netloc = cleaned.split("/")[0].split(":")[0]

    keywords = [
        "login", "secure", "verify", "update", "account", "signin", "bank",
        "paypal", "free", "bonus", "benefits", "access", "claim", "portal",
        "support", "service", "billing", "help", "info", "confirm", "admin",
        "security", "wallet", "remote", "domain", "sav", "save", "prune",
        "client", "gold", "clie", "direct", "express", "token", "auth",
        "connect", "mail", "banking", "office", "webmail", "genthis", "eplus",
        "fwc", "fifa", "ticket", "cup", "lottery", "promo", "event", "deal"
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
        "suspicious_keywords": sum(word in cleaned.lower() for word in keywords),
        "entropy": entropy(cleaned)
    }