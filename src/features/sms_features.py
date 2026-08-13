import re
from urllib.parse import urlparse


def extract_url(text):
    """Extract the first URL from an SMS message."""
    
    if not isinstance(text, str):
        return None
    
    pattern = r"https?://[^\s\]\)]+|www\.[^\s\]\)]+"
    match = re.search(pattern, text)
    
    if not match:
        return None
    
    return match.group(0).rstrip(".,;:)]")


def extract_url_features(url):
    """Extract basic numerical features from a URL."""
    
    if not url:
        return {
            "url_length": 0,
            "https": 0,
            "domain_length": 0,
            "path_length": 0,
            "num_dots": 0,
            "num_hyphens": 0,
            "num_digits": 0,
            "has_ip": 0
        }
    
    parsed = urlparse(url)
    
    return {
        "url_length": len(url),
        "https": int(parsed.scheme == "https"),
        "domain_length": len(parsed.netloc),
        "path_length": len(parsed.path),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_digits": sum(c.isdigit() for c in url),
        "has_ip": int(
            bool(re.fullmatch(
                r"\d{1,3}(\.\d{1,3}){3}",
                parsed.netloc
            ))
        )
    }
def clean_sms_text(text):
    """Clean SMS text while preserving multilingual characters."""

    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text
URGENCY_KEYWORDS = [
    "urgent",
    "immediately",
    "now",
    "today",
    "within 24 hours",
    "act now",
    "last chance",
    "expire",
    "expired",
    "blocked",
    "suspended",
    "disconnect",
]

SENSITIVE_KEYWORDS = [
    "otp",
    "kyc",
    "upi",
    "pin",
    "password",
    "cvv",
    "account",
    "bank",
    "verify",
    "verification",
    "refund",
    "payment",
]

ACTION_KEYWORDS = [
    "click",
    "pay",
    "verify",
    "confirm",
    "activate",
    "update",
    "apply",
    "register",
    "login",
    "secure",
]


def count_keywords(text, keywords):
    """Count keyword occurrences in text."""

    text = clean_sms_text(text)

    return sum(
        text.count(keyword.lower())
        for keyword in keywords
    )


def extract_sms_text_features(text):
    """Extract handcrafted phishing-related SMS features."""

    cleaned = clean_sms_text(text)

    return {
        "text_length": len(cleaned),
        "word_count": len(cleaned.split()),
        "urgency_keyword_count": count_keywords(
            cleaned,
            URGENCY_KEYWORDS
        ),
        "sensitive_keyword_count": count_keywords(
            cleaned,
            SENSITIVE_KEYWORDS
        ),
        "action_keyword_count": count_keywords(
            cleaned,
            ACTION_KEYWORDS
        ),
        "exclamation_count": cleaned.count("!"),
        "question_count": cleaned.count("?"),
        "digit_count": sum(char.isdigit() for char in cleaned),
        "uppercase_count": sum(
            char.isupper() for char in text
        ),
    }