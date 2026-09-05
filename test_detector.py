from app.scam_detector import detect_scam


print("=" * 50)
print("          SCAMSHIELD AI DEFENSE ENGINE")
print("=" * 50)

message = input("\nEnter a message to check: ")

result = detect_scam(message)

print("\n----- THREAT ANALYSIS -----")
print("Category:   ", result["category"])
print("Confidence: ", result["confidence"], "%")
print("Risk Level: ", result["risk"])
print("Risk Score: ", result["risk_score"], "/ 100")

if result["suspicious_words"]:
    print("Suspicious indicators:", ", ".join(result["suspicious_words"]))
else:
    print("Suspicious indicators: None")

if result.get("url_findings", {}).get("urls"):
    print("Detected URLs:        ", ", ".join(result["url_findings"]["urls"]))

if result.get("red_flags"):
    print("\nRed Flags Detected:")
    for rf in result["red_flags"]:
        print(f" • [{rf['severity']}] {rf['title']}: {rf['description']}")