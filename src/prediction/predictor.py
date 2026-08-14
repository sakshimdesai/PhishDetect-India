import os
import joblib
import pandas as pd

from src.features.url_features import extract_url_features


# Project root
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "url_random_forest.pkl"
)

METADATA_PATH = os.path.join(
    BASE_DIR,
    "models",
    "url_feature_metadata.json"
)


# Load model
model = joblib.load(MODEL_PATH)

# Load feature metadata
import json

with open(METADATA_PATH, "r") as file:
    metadata = json.load(file)

FEATURE_COLUMNS = metadata["features"]


def predict_url(url: str) -> dict:
    """
    Predict whether a URL is phishing or legitimate.

    Returns:
        {
            "prediction": "Phishing" / "Legitimate",
            "confidence": float,
            "features": dict
        }
    """

    features = extract_url_features(url)

    feature_vector = pd.DataFrame(
        [features]
    )[FEATURE_COLUMNS]

    prediction_value = model.predict(
        feature_vector
    )[0]

    probabilities = model.predict_proba(
        feature_vector
    )[0]

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
        "confidence": round(float(confidence), 4),
        "features": features
    }