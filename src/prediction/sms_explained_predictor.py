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

from src.prediction.sms_predictor import predict_sms
from src.explainability.shap_explainer import explain_sms
from src.explainability.reason_mapper import humanize_shap_reasons


def predict_sms_with_explanation(
    sms_text: str,
    sender=None
) -> dict:

    # -----------------------------------------------------
    # 1. Get normal prediction
    # -----------------------------------------------------

    prediction_result = predict_sms(
        sms_text,
        sender=sender
    )

    # -----------------------------------------------------
    # 2. Get SHAP explanation
    # -----------------------------------------------------

    explanations = explain_sms(
        sms_text,
        top_k=10
    )

    # -----------------------------------------------------
    # 3. Convert SHAP features into readable reasons
    # -----------------------------------------------------

    reasons = humanize_shap_reasons(
        explanations,
        max_reasons=3
    )

    # -----------------------------------------------------
    # 4. Return combined result
    # -----------------------------------------------------

    return {
        "prediction": prediction_result[
            "prediction"
        ],
        "confidence": prediction_result[
            "confidence"
        ],
        "reasons": reasons
    }