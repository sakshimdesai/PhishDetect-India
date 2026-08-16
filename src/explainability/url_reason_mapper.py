# ---------------------------------------------------------
# Human-readable explanations for URL features
# ---------------------------------------------------------

URL_REASON_MAP = {

    "url_length":
        "URL length influenced the prediction",

    "domain_length":
        "Domain length influenced the prediction",

    "subdomain_count":
        "Contains multiple subdomains",

    "has_https":
        "HTTPS usage influenced the prediction",

    "is_ip":
        "URL uses an IP address instead of a domain name",

    "special_char_count":
        "Contains a notable number of special characters",

    "digit_count":
        "Contains numerical characters",

    "letter_count":
        "Contains alphabetic characters",

    "dot_count":
        "Contains multiple dot characters",

    "hyphen_count":
        "Contains hyphen characters",

    "underscore_count":
        "Contains underscore characters",

    "slash_count":
        "Contains URL path separators",

    "question_mark_count":
        "Contains query parameters",

    "equals_count":
        "Contains parameter assignment characters",

    "ampersand_count":
        "Contains multiple query parameters",

    "at_symbol_count":
        "Contains an @ symbol",

    "percent_count":
        "Contains percent-encoded characters",

    "obfuscation_count":
        "Contains URL obfuscation patterns",

    "path_length":
        "URL path length influenced the prediction",

    "query_length":
        "URL query length influenced the prediction"
}


def humanize_url_shap_reasons(
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

        if feature not in URL_REASON_MAP:
            continue

        base_reason = URL_REASON_MAP[
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