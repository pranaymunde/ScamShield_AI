import re
import math

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678", "123456789", "qwerty",
    "admin", "welcome", "letmein", "iloveyou", "monkey", "dragon", "master",
    "sunshine", "princess", "football", "shadow", "superman", "trustno1"
}


def estimate_crack_time(seconds):
    """
    Translates crack time in seconds into human-readable duration.
    """
    if seconds < 0.001:
        return "Instant (< 1 millisecond)"
    elif seconds < 1:
        return f"{int(seconds * 1000)} milliseconds"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds / 86400)} days"
    elif seconds < 3153600000:
        return f"{int(seconds / 31536000)} years"
    elif seconds < 3153600000000:
        return f"{int(seconds / 3153600000)} centuries"
    else:
        return "Virtually uncrackable (billions of years)"


def check_password(password):
    password = str(password)
    length = len(password)
    suggestions = []
    checklist = []

    # 1. Diversity & Pool size
    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 33

    checklist.append({"label": "At least 12 characters", "passed": length >= 12})
    checklist.append({"label": "Uppercase letters (A-Z)", "passed": has_upper})
    checklist.append({"label": "Lowercase letters (a-z)", "passed": has_lower})
    checklist.append({"label": "Numbers (0-9)", "passed": has_digit})
    checklist.append({"label": "Special symbols (!@#$)", "passed": has_special})

    # Common dictionary check
    is_common = password.lower() in COMMON_PASSWORDS or bool(re.search(r"^(.)\1+$", password))
    checklist.append({"label": "Free of common dictionary patterns", "passed": not is_common})

    # Suggestions
    if length < 8:
        suggestions.append("Critically short: use at least 12-16 characters.")
    elif length < 12:
        suggestions.append("Lengthen to 12+ characters for quantum-safe resilience.")

    if not has_upper:
        suggestions.append("Add uppercase letters (e.g. A, B, C).")
    if not has_lower:
        suggestions.append("Add lowercase letters (e.g. a, b, c).")
    if not has_digit:
        suggestions.append("Add numbers (0-9).")
    if not has_special:
        suggestions.append("Add special characters (e.g. !@#$%^&*).")
    if is_common:
        suggestions.append("Avoid obvious words like 'password' or repeating characters.")

    # 2. Entropy calculation: H = L * log2(R)
    if pool_size > 0 and length > 0:
        entropy = round(length * math.log2(pool_size), 1)
    else:
        entropy = 0.0

    # 3. Crack time estimation (assumes high-end GPU cluster: 10^10 guesses/sec)
    if pool_size > 0 and length > 0 and not is_common:
        # Average combinations to check = (pool_size^length) / 2
        try:
            total_guesses = (pool_size ** length) / 2
            seconds = total_guesses / 10000000000.0  # 10 billion/sec
            crack_time = estimate_crack_time(seconds)
        except OverflowError:
            crack_time = "Virtually uncrackable (billions of years)"
    else:
        crack_time = "Instant (< 1 millisecond)"

    # 4. Strength Score (0 to 100)
    score_pct = min(int((entropy / 80.0) * 100), 100) if not is_common else 10
    if length < 6:
        score_pct = min(score_pct, 15)

    if score_pct < 30:
        strength = "Very Weak"
    elif score_pct < 55:
        strength = "Weak"
    elif score_pct < 75:
        strength = "Fair"
    elif score_pct < 90:
        strength = "Strong"
    else:
        strength = "Fortified"

    return {
        "strength": strength,
        "score": score_pct,
        "entropy": entropy,
        "crack_time": crack_time,
        "checklist": checklist,
        "suggestions": suggestions
    }