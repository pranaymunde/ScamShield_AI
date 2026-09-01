import re


def detect_rules(message):

    message = message.lower()

    suspicious_words = [
        "urgent",
        "otp",
        "password",
        "click",
        "pay",
        "payment",
        "won",
        "prize",
        "verify",
        "blocked"
    ]

    found = []

    for word in suspicious_words:
        pattern = r"\b" + re.escape(word) + r"\b"

        if re.search(pattern, message):
            found.append(word)

    return found


def calculate_risk(confidence, rule_count):

    score = (confidence * 0.6) + (rule_count * 10)

    score = min(score, 100)

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"