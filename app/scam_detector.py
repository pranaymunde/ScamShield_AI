import re
import joblib
from pathlib import Path

from app.rules import detect_rules, analyze_urls, calculate_risk

# -----------------------------
# Model Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model" / "scam_model.pkl"
VECTORIZER_PATH = BASE_DIR / "model" / "tfidf_vectorizer.pkl"


# -----------------------------
# Load Trained Model
# -----------------------------

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# -----------------------------
# Text Cleaning
# -----------------------------

def clean_text(text):
    text = str(text).lower()
    # Keep letters, numbers and spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# -----------------------------
# Scam Detection
# -----------------------------

def detect_scam(message):
    original_message = str(message).strip()

    # Clean message for ML model
    cleaned = clean_text(original_message)

    # Convert message into TF-IDF
    message_tfidf = vectorizer.transform([cleaned])

    # ML prediction
    prediction = str(model.predict(message_tfidf)[0])

    # Prediction confidence
    probabilities = model.predict_proba(message_tfidf)
    confidence = float(round(float(probabilities.max()) * 100, 2))

    # Rule-based & heuristic detection
    found_words, categorized_matches = detect_rules(original_message)

    # URL & domain inspection
    url_findings = analyze_urls(original_message)

    # Advanced risk calculation
    risk_data = calculate_risk(
        category=prediction,
        confidence=confidence,
        found_words=found_words,
        categorized_matches=categorized_matches,
        url_findings=url_findings
    )

    return {
        "category": prediction,
        "confidence": confidence,
        "risk": risk_data["level"],
        "risk_score": risk_data["score"],
        "suspicious_words": found_words,
        "red_flags": risk_data["red_flags"],
        "url_findings": url_findings,
        "safety_steps": risk_data["safety_steps"]
    }