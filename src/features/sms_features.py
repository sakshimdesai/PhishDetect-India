import re


URGENCY_KEYWORDS = [
    "urgent",
    "immediately",
    "now",
    "today",
    "asap",
    "expire",
    "expired",
    "blocked",
    "suspended",
    "disconnected",
    "तुरंत",
    "अभी",
    "जल्दी",
    "बंद",
    "निलंबित",
    "समाप्त",
    "ತಕ್ಷಣ",
    "ಈಗ",
    "ಮುಚ್ಚಲಾಗಿದೆ",
    "ಅಮಾನತು"
]

SENSITIVE_KEYWORDS = [
    "otp",
    "kyc",
    "upi",
    "pin",
    "password",
    "cvv",
    "aadhaar",
    "aadhar",
    "pan",
    "account",
    "verification",
    "verify",
    "पासवर्ड",
    "ओटीपी",
    "केवाईसी",
    "आधार",
    "खाता",
    "सत्यापन",
    "otp",
    "ಕೆವೈಸಿ",
    "ಯುಪಿಐ",
    "ಆಧಾರ್",
    "ಖಾತೆ",
    "ಪರಿಶೀಲನೆ"
]

ACTION_KEYWORDS = [
    "click",
    "click here",
    "verify",
    "confirm",
    "activate",
    "update",
    "pay",
    "register",
    "apply",
    "login",
    "open",
    "submit",
    "क्लिक",
    "जांचें",
    "सत्यापित",
    "पुष्टि",
    "भुगतान",
    "आवेदन",
    "लॉगिन",
    "खोलें",
    "ಪರಿಶೀಲಿಸಿ",
    "ದೃಢೀಕರಿಸಿ",
    "ಪಾವತಿಸಿ",
    "ನೋಂದಣಿ"
]

REWARD_LURE_KEYWORDS = [
    "reward",
    "cashback",
    "cash back",
    "bonus",
    "prize",
    "winner",
    "won",
    "win",
    "gift",
    "claim",
    "collect",
    "redeem",
    "jeeta",
    "jeeti",
    "jeete",
    "sigide",
    "sigitu",
    "padeyiri"
]
def count_keyword_matches(text, keywords):
    text_lower = text.lower()

    return sum(
        text_lower.count(keyword.lower())
        for keyword in keywords
    )


def extract_sms_features(sms_text, sender=None):
    """
    Extract handcrafted phishing-related SMS features.
    """

    if not isinstance(sms_text, str):
        sms_text = str(sms_text)

    text = sms_text.strip()

    url_matches = re.findall(
        r"https?://\S+|www\.\S+",
        text,
        flags=re.IGNORECASE
    )

    shortened_url_patterns = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "ow.ly",
        "is.gd",
        "cutt.ly",
        "rb.gy"
    ]

    shortened_url_count = sum(
        url.lower().count(domain)
        for url in url_matches
        for domain in shortened_url_patterns
    )

    digit_count = sum(
        character.isdigit()
        for character in text
    )

    uppercase_count = sum(
        character.isupper()
        for character in text
    )

    alphabetic_count = sum(
        character.isalpha()
        for character in text
    )

    uppercase_ratio = (
        uppercase_count / alphabetic_count
        if alphabetic_count > 0
        else 0
    )

    features = {
        "text_length": len(text),
        "word_count": len(text.split()),

        "urgency_keyword_count":
            count_keyword_matches(
                text,
                URGENCY_KEYWORDS
            ),

        "sensitive_keyword_count":
            count_keyword_matches(
                text,
                SENSITIVE_KEYWORDS
            ),

        "action_keyword_count":
            count_keyword_matches(
                text,
                ACTION_KEYWORDS
            ),

        "reward_lure_keyword_count":
            count_keyword_matches(
                text,
                REWARD_LURE_KEYWORDS
            ),

        "url_count": len(url_matches),

        "contains_url": int(
            len(url_matches) > 0
        ),

        "shortened_url_count":
            shortened_url_count,

        "exclamation_count":
            text.count("!"),

        "question_count":
            text.count("?"),

        "digit_count":
            digit_count,

        "uppercase_count":
            uppercase_count,

        "uppercase_ratio":
            uppercase_ratio,

        "currency_symbol_count":
            text.count("₹") +
            text.count("$"),

        "phone_number_count":
            len(
                re.findall(
                    r"(?:\+91[\s-]?)?[6-9]\d{9}",
                    text
                )
            ),

        "has_sender":
            int(
                sender is not None
                and str(sender).strip() != ""
            )
    }

    return features