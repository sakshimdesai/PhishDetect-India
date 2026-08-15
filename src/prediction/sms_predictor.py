import os
import json
import joblib

import pandas as pd
from scipy.sparse import hstack, csr_matrix

from src.features.text_preprocessing import clean_sms_text
from src.features.sms_features import extract_sms_features


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


# ============================================================
# MODEL ARTIFACT PATHS
# ============================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "sms_random_forest_expanded.pkl"
)

TFIDF_PATH = os.path.join(
    BASE_DIR,
    "models",
    "sms_tfidf_vectorizer_expanded.pkl"
)

METADATA_PATH = os.path.join(
    BASE_DIR,
    "models",
    "sms_feature_metadata.json"
)


# ============================================================
# LOAD TRAINED COMPONENTS
# ============================================================

model = joblib.load(
    MODEL_PATH
)

tfidf_vectorizer = joblib.load(
    TFIDF_PATH
)

with open(
    METADATA_PATH,
    "r",
    encoding="utf-8"
) as file:

    metadata = json.load(file)


# ============================================================
# HANDCRAFTED FEATURE NAMES
# ============================================================

HANDCRAFTED_FEATURES = metadata[
    "handcrafted_features"
]


# ============================================================
# SMS PREDICTION FUNCTION
# ============================================================

def predict_sms(
    sms_text: str,
    sender=None
) -> dict:

    """
    Predict whether an SMS is phishing or legitimate.

    Returns:
        {
            "prediction": "Phishing" / "Legitimate",
            "confidence": float,
            "features": {...}
        }
    """

    # --------------------------------------------------------
    # 1. Clean SMS text
    # --------------------------------------------------------

    cleaned_text = clean_sms_text(
        sms_text
    )


    # --------------------------------------------------------
    # 2. Extract TF-IDF features
    # --------------------------------------------------------

    tfidf_features = tfidf_vectorizer.transform(
        [cleaned_text]
    )


    # --------------------------------------------------------
    # 3. Extract handcrafted features
    # --------------------------------------------------------

    handcrafted = extract_sms_features(
        sms_text,
        sender=sender
    )

    handcrafted_df = pd.DataFrame(
        [handcrafted]
    )[HANDCRAFTED_FEATURES]

    handcrafted_matrix = csr_matrix(
        handcrafted_df.values
    )


    # --------------------------------------------------------
    # 4. Combine TF-IDF + handcrafted features
    # --------------------------------------------------------

    final_features = hstack([
        tfidf_features,
        handcrafted_matrix
    ]).tocsr()


    # --------------------------------------------------------
    # 5. Validate feature dimensions
    # --------------------------------------------------------

    expected_features = model.n_features_in_

    actual_features = final_features.shape[1]

    if actual_features != expected_features:

        raise ValueError(
            f"Feature dimension mismatch: "
            f"model expects {expected_features} features, "
            f"but predictor generated {actual_features}."
        )


    # --------------------------------------------------------
    # 6. Generate prediction
    # --------------------------------------------------------

    prediction_value = model.predict(
        final_features
    )[0]

    probabilities = model.predict_proba(
        final_features
    )[0]


    # --------------------------------------------------------
    # 7. Identify model classes
    # --------------------------------------------------------

    classes = list(
        model.classes_
    )


    # --------------------------------------------------------
    # 8. Support both label formats
    #
    #    String:
    #       ['Legitimate', 'Phishing']
    #
    #    Numeric:
    #       [0, 1]
    # --------------------------------------------------------

    if (
        "Phishing" in classes
        and "Legitimate" in classes
    ):

        phishing_index = classes.index(
            "Phishing"
        )

        legitimate_index = classes.index(
            "Legitimate"
        )

        prediction = str(
            prediction_value
        )

    else:

        phishing_index = classes.index(
            1
        )

        legitimate_index = classes.index(
            0
        )

        if prediction_value == 1:

            prediction = "Phishing"

        else:

            prediction = "Legitimate"


    # --------------------------------------------------------
    # 9. Extract class probabilities
    # --------------------------------------------------------

    phishing_probability = probabilities[
        phishing_index
    ]

    legitimate_probability = probabilities[
        legitimate_index
    ]


    # --------------------------------------------------------
    # 10. Confidence
    # --------------------------------------------------------

    if prediction == "Phishing":

        confidence = phishing_probability

    else:

        confidence = legitimate_probability


    # --------------------------------------------------------
    # 11. Return prediction result
    # --------------------------------------------------------

    return {
        "prediction": prediction,
        "confidence": round(
            float(confidence),
            4
        ),
        "features": handcrafted
    }