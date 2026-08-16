import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)

import json
import joblib
import pandas as pd
import shap

from scipy.sparse import hstack, csr_matrix

from src.features.text_preprocessing import clean_sms_text
from src.features.sms_features import extract_sms_features


# ---------------------------------------------------------
# 1. Load model
# ---------------------------------------------------------

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "xgboost_sms_final.pkl"
)

model = joblib.load(
    MODEL_PATH
)


# ---------------------------------------------------------
# 2. Load TF-IDF vectorizer
# ---------------------------------------------------------

TFIDF_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "sms_tfidf_vectorizer_expanded.pkl"
)

tfidf_vectorizer = joblib.load(
    TFIDF_PATH
)


# ---------------------------------------------------------
# 3. Load feature metadata
# ---------------------------------------------------------

METADATA_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "sms_feature_metadata.json"
)

with open(
    METADATA_PATH,
    "r",
    encoding="utf-8"
) as file:

    metadata = json.load(file)


HANDCRAFTED_FEATURES = metadata[
    "handcrafted_features"
]


# ---------------------------------------------------------
# 4. Feature names
# ---------------------------------------------------------

TFIDF_FEATURES = list(
    tfidf_vectorizer.get_feature_names_out()
)

FEATURE_NAMES = (
    TFIDF_FEATURES
    + HANDCRAFTED_FEATURES
)


# ---------------------------------------------------------
# 5. SHAP explainer
# ---------------------------------------------------------

explainer = shap.TreeExplainer(
    model
)


# ---------------------------------------------------------
# 6. Create feature vector
# ---------------------------------------------------------

def create_sms_feature_vector(
    sms_text: str
):

    cleaned_text = clean_sms_text(
        sms_text
    )

    tfidf_features = (
        tfidf_vectorizer.transform(
            [cleaned_text]
        )
    )

    handcrafted = pd.DataFrame(
        [
            extract_sms_features(
                sms_text
            )
        ]
    )[HANDCRAFTED_FEATURES]

    handcrafted_matrix = csr_matrix(
        handcrafted.values
    )

    final_features = hstack(
        [
            tfidf_features,
            handcrafted_matrix
        ]
    ).tocsr()

    return final_features


# ---------------------------------------------------------
# 7. Generate SHAP explanation
# ---------------------------------------------------------

def explain_sms(
    sms_text: str,
    top_k: int = 3
) -> list:

    features = create_sms_feature_vector(
        sms_text
    )

    shap_values = explainer.shap_values(
        features
    )

    # XGBoost binary classifier returns
    # one SHAP value per feature.
    values = shap_values[0]

    # Find features with largest absolute
    # contribution.
    ranked_indices = sorted(
        range(len(values)),
        key=lambda index: abs(
            values[index]
        ),
        reverse=True
    )

    explanations = []

    for index in ranked_indices:

        contribution = float(
            values[index]
        )

        if contribution == 0:
            continue

        feature_name = FEATURE_NAMES[
            index
        ]

        direction = (
            "phishing"
            if contribution > 0
            else "legitimate"
        )

        explanations.append(
            {
                "feature": feature_name,
                "contribution": round(
                    contribution,
                    6
                ),
                "direction": direction
            }
        )

        if len(explanations) >= top_k:
            break

    return explanations