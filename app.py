from flask import Flask, request, jsonify
from flask_cors import CORS

import json

from src.prediction.sms_explained_predictor import (
    predict_sms_with_explanation
)

from src.prediction.url_predictor import predict_url

from src.explainability.url_shap_explainer import (
    explain_url
)

from src.explainability.url_reason_mapper import (
    humanize_url_shap_reasons
)

from database.db import (
    initialize_database,
    save_prediction,
    get_prediction_history
)


# ---------------------------------------------------------
# Create Flask application
# ---------------------------------------------------------

app = Flask(__name__)

CORS(app)


# ---------------------------------------------------------
# Initialize SQLite database
# ---------------------------------------------------------

initialize_database()


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "running",
        "message": "PhishDetect India API is running"
    })


# ---------------------------------------------------------
# Prediction endpoint
# ---------------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    input_text = data.get("input")
    input_type = data.get("input_type")

    if not input_text:

        return jsonify({
            "error": "Missing input"
        }), 400

    if not input_type:

        return jsonify({
            "error": "Missing input_type"
        }), 400

    input_type = input_type.lower().strip()


    # -----------------------------------------------------
    # SMS
    # -----------------------------------------------------

    if input_type == "sms":

        result = predict_sms_with_explanation(
            input_text
        )

        prediction = result["prediction"]
        confidence = result["confidence"]
        reasons = result["reasons"]

        save_prediction(
            input_type="sms",
            input_text=input_text,
            prediction=prediction,
            confidence=confidence,
            reasons=json.dumps(reasons)
        )

        return jsonify({
            "input_type": "sms",
            "prediction": prediction,
            "confidence": confidence,
            "reasons": reasons
        })


    # -----------------------------------------------------
    # URL
    # -----------------------------------------------------

    if input_type == "url":

        prediction_result = predict_url(
            input_text
        )

        shap_explanations = explain_url(
            input_text,
            top_k=10
        )

        reasons = humanize_url_shap_reasons(
            shap_explanations,
            max_reasons=3
        )

        prediction = prediction_result[
            "prediction"
        ]

        confidence = prediction_result[
            "confidence"
        ]

        save_prediction(
            input_type="url",
            input_text=input_text,
            prediction=prediction,
            confidence=confidence,
            reasons=json.dumps(reasons)
        )

        return jsonify({
            "input_type": "url",
            "prediction": prediction,
            "confidence": confidence,
            "reasons": reasons
        })


    # -----------------------------------------------------
    # Invalid input type
    # -----------------------------------------------------

    return jsonify({
        "error": "input_type must be either 'sms' or 'url'"
    }), 400


# ---------------------------------------------------------
# Prediction history endpoint
# ---------------------------------------------------------

@app.route("/history", methods=["GET"])
def history():

    try:

        limit = request.args.get(
            "limit",
            default=50,
            type=int
        )

        # Keep the requested limit within a safe range
        limit = max(
            1,
            min(limit, 100)
        )

        history_data = get_prediction_history(
            limit
        )

        return jsonify({
            "count": len(history_data),
            "history": history_data
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ---------------------------------------------------------
# Run application
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )