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

from scipy.sparse import hstack, csr_matrix

from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier

from src.features.text_preprocessing import clean_sms_text
from src.features.sms_features import extract_sms_features


# ---------------------------------------------------------
# 1. Load final dataset
# ---------------------------------------------------------

df = pd.read_csv(
    "data/processed/india_sms_dataset_final.csv"
)


# ---------------------------------------------------------
# 2. Load final TF-IDF vectorizer
# ---------------------------------------------------------

tfidf_vectorizer = joblib.load(
    "models/sms_tfidf_vectorizer_expanded.pkl"
)


# ---------------------------------------------------------
# 3. Load feature metadata
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
# 4. Create TF-IDF features
# ---------------------------------------------------------

cleaned_text = (
    df["SMS_Text"]
    .astype(str)
    .apply(clean_sms_text)
)

tfidf_features = tfidf_vectorizer.transform(
    cleaned_text
)


# ---------------------------------------------------------
# 5. Create handcrafted features
# ---------------------------------------------------------

handcrafted = pd.DataFrame(
    [
        extract_sms_features(text)
        for text in df["SMS_Text"].astype(str)
    ]
)[handcrafted_features]

handcrafted_matrix = csr_matrix(
    handcrafted.values
)


# ---------------------------------------------------------
# 6. Combine features
# ---------------------------------------------------------

X = hstack(
    [
        tfidf_features,
        handcrafted_matrix
    ]
).tocsr()


# ---------------------------------------------------------
# 7. Labels
# ---------------------------------------------------------

y = (
    df["Label"] == "Phishing"
).astype(int)


# ---------------------------------------------------------
# 8. Same train/test split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ---------------------------------------------------------
# 9. Train selected XGBoost model
# ---------------------------------------------------------

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=1.0,
    random_state=42,
    eval_metric="logloss"
)

model.fit(
    X_train,
    y_train
)


# ---------------------------------------------------------
# 10. Save final XGBoost model
# ---------------------------------------------------------

output_path = (
    "models/xgboost_sms_final.pkl"
)

joblib.dump(
    model,
    output_path
)


# ---------------------------------------------------------
# 11. Confirmation
# ---------------------------------------------------------

print("Final XGBoost model trained successfully.")
print("Model features:", model.n_features_in_)
print("Model trees:", model.n_estimators)
print("Saved to:", output_path)