import re
from urllib.parse import urlparse

# =========================================================
# CATEGORIZED SUSPICIOUS PATTERNS
# =========================================================

PATTERNS = {
    "Urgency & Coercion": [
        r"\burgent\b",
        r"\bimmediate(ly)?\b",
        r"\bwithin\s+\d+\s*(hours?|mins?|minutes?)\b",
        r"\baccount\s+(has\s+been\s+)?blocked\b",
        r"\bsuspended\b",
        r"\bdeactivated\b",
        r"\bterminated\b",
        r"\blegal\s+action\b",
        r"\bpolice\b",
        r"\barrest\s+warrant\b",
        r"\bcourt\s+notice\b",
        r"\bfir\s+registered\b",
        r"\bpower\s+cut\b",
        r"\belectricity\s+(will\s+be\s+)?disconnected\b"
    ],
    "Credential & Identity Harvesting": [
        r"\botp\b",
        r"\bone\s*time\s*password\b",
        r"\bpin\b",
        r"\bcvv\b",
        r"\bpassword\b",
        r"\blogin\s+(here|now|to\s+verify)\b",
        r"\bverify\s+(your\s+)?(identity|account|details|kyc|pan|aadhaar)\b",
        r"\bkyc\s+(update|pending|expired|verification)\b",
        r"\bpan\s+card\b",
        r"\baadhaar\b",
        r"\bcredit\s+card\b",
        r"\bdebit\s+card\b",
        r"\bnet\s*banking\b"
    ],
    "Financial & Payment Demands": [
        r"\bpay\s+(\d+|fee|charges|registration|advance|delivery)\b",
        r"\bpayment\s+(required|pending|failed)\b",
        r"\bwire\s+transfer\b",
        r"\bupi\s*(pin|id|transfer)\b",
        r"\bgift\s*cards?\b",
        r"\bcrypto(currency)?\b",
        r"\bprocessing\s+fee\b",
        r"\bcustoms\s+(duty|charges|fee)\b"
    ],
    "Prize & Unrealistic Offers": [
        r"\blottery\b",
        r"\bwon\b",
        r"\bprize\b",
        r"\bclaim\s+(your|now|prize|reward)\b",
        r"\bcongratulations\b",
        r"\blucky\s+(winner|draw)\b",
        r"\bcashback\b",
        r"\bfree\s+gift\b",
        r"\bguaranteed\s+(return|profit|income)\b",
        r"\bdouble\s+your\s+money\b",
        r"\bearn\s+₹?\d+\s*(per|\/)\s*day\b",
        r"\bpart\s*time\s*job\b",
        r"\btelegram\s*task\b",
        r"\byoutube\s*like\b"
    ],
    "Impersonation & Phishing Traps": [
        r"\bclick\s+(here|this\s+link|on\s+link)\b",
        r"\bdownload\s+(apk|app|file|attachment)\b",
        r"\bapk\s+file\b",
        r"\bparcel\s+(on\s+hold|pending|stuck)\b",
        r"\bpackage\s+delivery\b",
        r"\bfedex\b",
        r"\bdhl\b",
        r"\bindia\s+post\b",
        r"\bincometax\b",
        r"\btax\s+refund\b",
        r"\bbank\s+(manager|officer|alert)\b"
    ]
}

SUSPICIOUS_TLDS = {
    "xyz", "top", "buzz", "club", "work", "cn", "ru", "click", "live", 
    "shop", "link", "online", "fit", "rest", "bar", "gq", "cf", "ml", "ga"
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "is.gd", "t.co", "cutt.ly", "rb.gy", "goo.gl", "ow.ly"
}

TRUSTED_BRANDS = [
    "sbi", "hdfc", "icici", "axis", "paytm", "phonepe", "gpay",
    "paypal", "amazon", "netflix", "apple", "microsoft", "google"
]


# =========================================================
# URL & LINK INSPECTION
# =========================================================

def analyze_urls(text):
    """
    Extracts and evaluates URLs, IPs, and suspicious domains in text.
    """
    findings = {
        "urls": [],
        "suspicious_indicators": [],
        "risk_boost": 0
    }

    url_pattern = r"(?:https?:\/\/|www\.)[^\s<>\"'()]+|\b[a-zA-Z0-9.-]+\.[a-z]{2,8}\b(?:\/[^\s<>\"']*)?"
    matches = re.findall(url_pattern, text)

    for raw_url in matches:
        full_url = raw_url
        if not full_url.startswith(("http://", "https://")):
            full_url = "http://" + full_url

        parsed = urlparse(full_url)
        hostname = parsed.hostname or ""
        hostname_lower = hostname.lower()

        if not hostname_lower or "." not in hostname_lower:
            continue

        findings["urls"].append(raw_url)

        # 1. IP Address as host
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname_lower):
            findings["suspicious_indicators"].append(f"Host uses raw IP address instead of domain ({hostname})")
            findings["risk_boost"] += 25

        # 2. Suspicious TLD
        tld = hostname_lower.split(".")[-1]
        if tld in SUSPICIOUS_TLDS:
            findings["suspicious_indicators"].append(f"Uses high-risk suspicious top-level domain (.{tld})")
            findings["risk_boost"] += 20

        # 3. URL shortener
        for shortener in SHORTENERS:
            if shortener in hostname_lower:
                findings["suspicious_indicators"].append(f"Uses URL masking shortener ({shortener})")
                findings["risk_boost"] += 15
                break

        # 4. Brand spoofing / lookalike subdomain (e.g. sbi.co.in.account-verify.xyz)
        for brand in TRUSTED_BRANDS:
            if brand in hostname_lower:
                parts = hostname_lower.split(".")
                main_domain = ".".join(parts[-2:]) if len(parts) >= 2 else hostname_lower
                if brand in hostname_lower and brand not in main_domain:
                    findings["suspicious_indicators"].append(f"Potential brand impersonation: '{brand}' placed in subdomain")
                    findings["risk_boost"] += 30
                    break

        # 5. Non-HTTPS link with login or verify keywords
        if raw_url.startswith("http://") and any(k in full_url.lower() for k in ["login", "verify", "secure", "bank", "pay"]):
            findings["suspicious_indicators"].append("Insecure HTTP protocol used on sensitive request link")
            findings["risk_boost"] += 15

    return findings


# =========================================================
# RULE & PATTERN DETECTION
# =========================================================

def detect_rules(message):
    """
    Scans the message against categorized threat indicators.
    Returns matched keywords and categorized red flags.
    """
    message_lower = message.lower()
    found_words = []
    categorized_matches = {}

    for category, pattern_list in PATTERNS.items():
        cat_matches = []
        for pat in pattern_list:
            match = re.search(pat, message_lower)
            if match:
                matched_str = match.group(0).strip()
                cat_matches.append(matched_str)
                if matched_str not in found_words:
                    found_words.append(matched_str)
        if cat_matches:
            categorized_matches[category] = cat_matches

    return found_words, categorized_matches


# =========================================================
# ADVANCED RISK CALCULATION
# =========================================================

def calculate_risk(category, confidence, found_words, categorized_matches, url_findings):
    """
    Computes accurate risk score (0-100), risk level (LOW/MEDIUM/HIGH),
    red flags breakdown, and dynamic safety recommendations.
    """
    category_lower = str(category).lower()
    is_normal = (category_lower == "normal" or "safe" in category_lower)

    base_score = 0
    red_flags = []
    safety_steps = []

    # 1. ML Model Contribution
    if not is_normal:
        # Scam predicted by ML
        base_score = (confidence * 0.45)
    else:
        # Normal predicted by ML
        base_score = 10 - min((confidence * 0.1), 10)

    # 2. Rule Triggers Contribution
    rule_score = 0
    for cat_name, items in categorized_matches.items():
        weight = 10
        severity = "MEDIUM"
        if cat_name in ["Credential & Identity Harvesting", "Financial & Payment Demands"]:
            weight = 16
            severity = "CRITICAL"
        elif cat_name in ["Urgency & Coercion"]:
            weight = 12
            severity = "HIGH"

        cat_pts = len(items) * weight
        rule_score += min(cat_pts, 35)

        red_flags.append({
            "category": cat_name,
            "severity": severity,
            "title": f"{cat_name} detected",
            "description": f"Triggered by patterns: {', '.join(items[:3])}"
        })

    # 3. URL Findings Contribution
    url_score = min(url_findings.get("risk_boost", 0), 40)
    for indicator in url_findings.get("suspicious_indicators", []):
        red_flags.append({
            "category": "Malicious Link Analysis",
            "severity": "CRITICAL",
            "title": "Suspicious URL Heuristic",
            "description": indicator
        })

    # Total Score
    total_score = base_score + rule_score + url_score

    # Override: If predicted normal but strong red flags or URL risk exist
    if is_normal and (len(found_words) >= 3 or url_score >= 20):
        total_score = max(total_score, 55)

    # Normalize to 0-100 range
    final_score = int(round(min(max(total_score, 5 if not is_normal else 2), 99)))

    # Classification
    if final_score >= 68 or (not is_normal and len(found_words) >= 2):
        risk_level = "HIGH"
        safety_steps = [
            "DO NOT click any links, open attachments, or dial back the number.",
            "NEVER share OTP, UPI PIN, CVV, or passwords with anyone.",
            "Verify independently through the official company website or customer care app.",
            "Report this immediately to the National Cyber Crime Portal (helpline 1930 / cybercrime.gov.in)."
        ]
    elif final_score >= 38 or len(found_words) >= 1 or len(url_findings.get("urls", [])) > 0:
        risk_level = "MEDIUM"
        safety_steps = [
            "Exercise caution. Double-check the sender's phone number or email address.",
            "Do not execute payments or share personal details under time pressure.",
            "Check official status directly on the provider's verified portal."
        ]
    else:
        risk_level = "LOW"
        final_score = min(final_score, 25)
        safety_steps = [
            "The message does not display obvious scam indicators.",
            "Always follow general cyber hygiene: never disclose sensitive credentials."
        ]

    return {
        "score": final_score,
        "level": risk_level,
        "red_flags": red_flags,
        "safety_steps": safety_steps
    }