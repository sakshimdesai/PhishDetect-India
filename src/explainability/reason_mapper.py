# ---------------------------------------------------------
# Human-readable explanations for handcrafted features
# ---------------------------------------------------------

HANDCRAFTED_REASON_MAP = {

    "urgency_keyword_count":
        "Uses urgent or time-sensitive language",

    "sensitive_keyword_count":
        "Contains sensitive information-related terms",

    "action_keyword_count":
        "Uses action-oriented language such as verify, click or update",

    "reward_lure_keyword_count":
        "Contains reward, prize or cashback-related language",

    "url_count":
        "Contains a URL",

    "contains_url":
        "Contains a URL",

    "shortened_url_count":
        "Contains a shortened URL",

    "exclamation_count":
        "Uses exclamation marks",

    "question_count":
        "Uses question-based language",

    "digit_count":
        "Contains numerical information",

    "uppercase_count":
        "Contains uppercase characters",

    "uppercase_ratio":
        "Contains a notable amount of uppercase text",

    "currency_symbol_count":
        "Contains currency-related information",

    "phone_number_count":
        "Contains a phone number",

    "text_length":
        "Message length influenced the prediction",

    "word_count":
        "Word count influenced the prediction",

    "has_sender":
        "Sender information was present"
}


def humanize_shap_reasons(
    explanations,
    max_reasons=3
):

    reasons = []

    for explanation in explanations:

        feature = explanation[
            "feature"
        ]

        direction = explanation[
            "direction"
        ]

        if feature not in HANDCRAFTED_REASON_MAP:
            continue

        base_reason = HANDCRAFTED_REASON_MAP[
            feature
        ]

        if direction == "phishing":

            reason = (
                base_reason
                + " contributing to the phishing prediction"
            )

        else:

            reason = (
                base_reason
                + " contributing to the legitimate prediction"
            )

        reasons.append(
            {
                "feature": feature,
                "reason": reason,
                "contribution": explanation[
                    "contribution"
                ],
                "direction": direction
            }
        )

        if len(reasons) >= max_reasons:
            break

    return reasons