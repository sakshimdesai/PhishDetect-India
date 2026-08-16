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

import joblib
import pandas as pd
import shap

from src.features.url_features import extract_url_features


# ---------------------------------------------------------
# 1. Load URL model
# ---------------------------------------------------------

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "url_random_forest.pkl"
)

model = joblib.load(
    MODEL_PATH
)


# ---------------------------------------------------------
# 2. URL feature names
# ---------------------------------------------------------

FEATURE_NAMES = [
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
    "query_length"
]


# ---------------------------------------------------------
# 3. SHAP explainer
# ---------------------------------------------------------

explainer = shap.TreeExplainer(
    model
)


# ---------------------------------------------------------
# 4. Create URL feature vector
# ---------------------------------------------------------

def create_url_feature_vector(
    url: str
):

    features = extract_url_features(
        url
    )

    feature_vector = pd.DataFrame(
        [features]
    )[FEATURE_NAMES]

    return feature_vector


# ---------------------------------------------------------
# 5. Generate SHAP explanation
# ---------------------------------------------------------

def explain_url(
    url: str,
    top_k: int = 3
) -> list:

    features = create_url_feature_vector(
        url
    )

    shap_values = explainer.shap_values(
        features
    )

    # -----------------------------------------------------
    # SHAP 0.51.0 with this binary Random Forest returns:
    #
    # (samples, features, classes)
    #
    # Class 0 = Phishing
    # Class 1 = Legitimate
    # -----------------------------------------------------

    phishing_index = list(
        model.classes_
    ).index(0)

    values = shap_values[
        0,
        :,
        phishing_index
    ]

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