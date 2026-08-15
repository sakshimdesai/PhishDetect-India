from src.prediction.sms_predictor import predict_sms
from src.prediction.url_predictor import predict_url


def predict(input_text: str, input_type: str) -> dict:
    """
    Unified prediction interface.

    input_type:
        - "sms"
        - "url"
    """

    input_type = input_type.lower().strip()

    if input_type == "sms":
        return predict_sms(input_text)

    if input_type == "url":
        return predict_url(input_text)

    raise ValueError(
        "input_type must be either 'sms' or 'url'"
    )