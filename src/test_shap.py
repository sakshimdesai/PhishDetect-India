import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
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

model = joblib.load(
    "models/xgboost_sms_final.pkl"
)


# ---------------------------------------------------------
# 2. Load vectorizer
# ---------------------------------------------------------

tfidf_vectorizer = joblib.load(
    "models/sms_tfidf_vectorizer_expanded.pkl"
)


# ---------------------------------------------------------
# 3. Load metadata
# ---------------------------------------------------------

with open(
    "models/sms_feature_metadata.json",
    "r",
    encoding="utf-8"
) as file:
    metadata = json.load(file)

handcrafted_features = metadata[
    "handcrafted_features"
]


# ---------------------------------------------------------
# 4. Test SMS
# ---------------------------------------------------------

sms = (
    "Your SBI account will be blocked. "
    "Verify KYC immediately using this link "
    "https://fake-kyc.xyz"
)


# ---------------------------------------------------------
# 5. Create features
# ---------------------------------------------------------

cleaned_text = clean_sms_text(
    sms
)

tfidf_features = tfidf_vectorizer.transform(
    [cleaned_text]
)

handcrafted = pd.DataFrame(
    [
        extract_sms_features(sms)
    ]
)[handcrafted_features]

handcrafted_matrix = csr_matrix(
    handcrafted.values
)

X = hstack(
    [
        tfidf_features,
        handcrafted_matrix
    ]
).tocsr()


# ---------------------------------------------------------
# 6. Create SHAP explainer
# ---------------------------------------------------------

explainer = shap.TreeExplainer(
    model
)


# ---------------------------------------------------------
# 7. Calculate SHAP values
# ---------------------------------------------------------

shap_values = explainer.shap_values(
    X
)


# ---------------------------------------------------------
# 8. Print basic information
# ---------------------------------------------------------

print(
    "SHAP calculation successful."
)

print(
    "Input shape:",
    X.shape
)

print(
    "SHAP type:",
    type(shap_values)
)

print(
    "SHAP shape:",
    getattr(shap_values, "shape", "No shape")
)