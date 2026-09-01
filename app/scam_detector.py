import re
import joblib
from pathlib import Path

from app.rules import detect_rules, calculate_risk

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

    # Clean message
    cleaned = clean_text(message)

    # Convert message into TF-IDF
    message_tfidf = vectorizer.transform([cleaned])

    # ML prediction
    prediction = model.predict(message_tfidf)[0]

    # Prediction confidence
    probabilities = model.predict_proba(message_tfidf)

    confidence = probabilities.max() * 100

    # Rule-based detection
    suspicious_words = detect_rules(message)

    # Risk calculation
    risk = calculate_risk(
        confidence,
        len(suspicious_words)
    )

    return {
        "category": prediction,
        "confidence": round(confidence, 2),
        "risk": risk,
        "suspicious_words": suspicious_words
    }