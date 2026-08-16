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
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

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
# 9. XGBoost tuning experiments
# ---------------------------------------------------------

experiments = [

    {
        "name": "Baseline",
        "n_estimators": 100,
        "max_depth": 6,
        "learning_rate": 0.3,
        "subsample": 1.0
    },

    {
        "name": "Experiment 1",
        "n_estimators": 200,
        "max_depth": 6,
        "learning_rate": 0.1,
        "subsample": 1.0
    },

    {
        "name": "Experiment 2",
        "n_estimators": 300,
        "max_depth": 6,
        "learning_rate": 0.1,
        "subsample": 0.8
    },

    {
        "name": "Experiment 3",
        "n_estimators": 300,
        "max_depth": 4,
        "learning_rate": 0.1,
        "subsample": 0.8
    },

    {
        "name": "Experiment 4",
        "n_estimators": 500,
        "max_depth": 4,
        "learning_rate": 0.05,
        "subsample": 0.8
    }
]


results = []


# ---------------------------------------------------------
# 10. Run experiments
# ---------------------------------------------------------

for experiment in experiments:

    print(
        f"\nRunning {experiment['name']}..."
    )

    model = XGBClassifier(
        n_estimators=experiment["n_estimators"],
        max_depth=experiment["max_depth"],
        learning_rate=experiment["learning_rate"],
        subsample=experiment["subsample"],
        random_state=42,
        eval_metric="logloss"
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions
    )

    recall = recall_score(
        y_test,
        predictions
    )

    f1 = f1_score(
        y_test,
        predictions
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1       : {f1:.4f}"
    )

    print(
        f"ROC-AUC  : {roc_auc:.4f}"
    )

    results.append(
        {
            "Model": "XGBoost",
            "Experiment": experiment["name"],
            "n_estimators": experiment["n_estimators"],
            "max_depth": experiment["max_depth"],
            "learning_rate": experiment["learning_rate"],
            "subsample": experiment["subsample"],
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1": f1,
            "ROC-AUC": roc_auc
        }
    )


# ---------------------------------------------------------
# 11. Save tuning results
# ---------------------------------------------------------

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    "models/xgboost_tuning_results.csv",
    index=False
)

print(
    "\nTuning results saved to:"
)

print(
    "models/xgboost_tuning_results.csv"
)