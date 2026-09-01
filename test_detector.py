from app.scam_detector import detect_scam


print("=" * 50)
print("          SCAMSHIELD AI")
print("=" * 50)

message = input("\nEnter a message to check: ")

result = detect_scam(message)

print("\n----- ANALYSIS -----")

print("Category:", result["category"])
print("Confidence:", result["confidence"], "%")
print("Risk Level:", result["risk"])

if result["suspicious_words"]:
    print(
        "Suspicious indicators:",
        ", ".join(result["suspicious_words"])
    )
else:
    print("Suspicious indicators: None")