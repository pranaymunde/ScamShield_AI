from app.app import detect_rules, calculate_risk


message = "Urgent! Your account is blocked. Click this link and verify."

found_words = detect_rules(message)

print("Message:", message)
print("Suspicious words:", found_words)

risk = calculate_risk(80, len(found_words))

print("Risk Level:", risk)