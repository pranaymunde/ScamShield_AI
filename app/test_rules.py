import sys
from pathlib import Path

# Ensure root workspace is in sys.path when executed directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rules import detect_rules, analyze_urls, calculate_risk

message = "Urgent! Your account is blocked. Click http://192.168.1.1/verify.php immediately."

found_words, categorized_matches = detect_rules(message)
url_findings = analyze_urls(message)

print("Message:", message)
print("Suspicious words:", found_words)
print("URL findings:", url_findings)

risk_data = calculate_risk(
    category="Banking Scam",
    confidence=90.0,
    found_words=found_words,
    categorized_matches=categorized_matches,
    url_findings=url_findings
)

print("Risk Level:", risk_data["level"])
print("Risk Score:", risk_data["score"])
print("Red Flags:", len(risk_data["red_flags"]))