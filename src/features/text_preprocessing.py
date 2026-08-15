import re


def clean_sms_text(text: str) -> str:
    """
    Basic language-preserving SMS preprocessing.

    Keeps Hindi, Kannada, English and Hinglish characters.
    """

    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Lowercase only Latin characters.
    # Hindi/Kannada characters are unaffected.
    text = text.lower()

    return text