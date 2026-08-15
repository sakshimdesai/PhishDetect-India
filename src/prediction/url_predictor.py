import os
import joblib
import pandas as pd

from src.features.url_features import extract_url_features


# Project root
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)


# Trained URL model
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "url_random_forest.pkl"
)


# Load trained model
model = joblib.load(MODEL_PATH)


# Feature order used by the trained Random Forest
if hasattr(model, "feature_names_in_"):
    FEATURE_COLUMNS = list(model.feature_names_in_)
else:
    FEATURE_COLUMNS = [
        "url_length",
        "domain_length",
        "subdomain_count",
        "has_https",
        "is_ip",
        "special_char_count",
        "digit_count",
        "letter_count",
        "dot_count",
        "hyphen_count",
        "underscore_count",
        "slash_count",
        "question_mark_count",
        "equals_count",
        "ampersand_count",
        "at_symbol_count",
        "percent_count",
        "obfuscation_count",
        "path_length",
        "query_length",
    ]


def predict_url(url: str) -> dict:
    """
    Predict whether a URL is phishing or legitimate.

    Returns:
        {
            "prediction": "Phishing" / "Legitimate",
            "confidence": float,
            "features": {...}
        }
    """

    # 1. Extract URL features
    features = extract_url_features(url)

    # 2. Create feature vector
    feature_vector = pd.DataFrame(
        [features]
    )[FEATURE_COLUMNS]

    # 3. Prediction
    prediction_value = model.predict(
        feature_vector
    )[0]

    # 4. Prediction probabilities
    probabilities = model.predict_proba(
        feature_vector
    )[0]

    # PhiUSIIL label mapping:
    # 0 = Phishing
    # 1 = Legitimate

    phishing_index = list(
        model.classes_
    ).index(0)

    phishing_probability = probabilities[
        phishing_index
    ]

    if prediction_value == 0:
        prediction = "Phishing"
        confidence = phishing_probability
    else:
        prediction = "Legitimate"
        confidence = 1 - phishing_probability

    return {
        "prediction": prediction,
        "confidence": round(
            float(confidence),
            4
        ),
        "features": features
    }