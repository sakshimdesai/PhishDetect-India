import re
import ipaddress
from urllib.parse import urlparse


def extract_url_features(url: str) -> dict:
    """
    Extract URL-based features that can be calculated directly
    from the URL string.
    """

    if not isinstance(url, str):
        url = str(url)

    url = url.strip()

    # Add scheme temporarily if missing
    parsed_url = urlparse(
        url if "://" in url else "http://" + url
    )

    domain = parsed_url.netloc.split("@")[-1].split(":")[0]
    path = parsed_url.path
    query = parsed_url.query

    # Remove www. for subdomain calculation
    domain_without_www = re.sub(
        r"^www\.",
        "",
        domain,
        flags=re.IGNORECASE
    )

    domain_parts = [
        part for part in domain_without_www.split(".")
        if part
    ]

    # IP address detection
    is_ip = 0

    try:
        ipaddress.ip_address(domain)
        is_ip = 1
    except ValueError:
        pass

    # HTTPS
    has_https = int(
        parsed_url.scheme.lower() == "https"
    )

    # Special characters
    special_characters = re.findall(
        r"[^a-zA-Z0-9]",
        url
    )

    # Digits
    digit_count = sum(
        character.isdigit()
        for character in url
    )

    # Letters
    letter_count = sum(
        character.isalpha()
        for character in url
    )

    # Obfuscation indicators
    obfuscation_characters = [
        "@",
        "%",
        "\\",
        "//"
    ]

    obfuscation_count = sum(
        url.count(character)
        for character in obfuscation_characters
    )

    # URL structure
    features = {
        "url_length": len(url),
        "domain_length": len(domain),
        "subdomain_count": max(len(domain_parts) - 2, 0),
        "has_https": has_https,
        "is_ip": is_ip,
        "special_char_count": len(special_characters),
        "digit_count": digit_count,
        "letter_count": letter_count,
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "underscore_count": url.count("_"),
        "slash_count": url.count("/"),
        "question_mark_count": url.count("?"),
        "equals_count": url.count("="),
        "ampersand_count": url.count("&"),
        "at_symbol_count": url.count("@"),
        "percent_count": url.count("%"),
        "obfuscation_count": obfuscation_count,
        "path_length": len(path),
        "query_length": len(query),
    }

    return features