from flask import Flask, render_template, request, jsonify
from app.scam_detector import detect_scam
from app.cybersecurity import get_topic
from app.chatbot import chatbot_response
from app.quiz import get_random_quiz, evaluate_quiz

from pathlib import Path
from datetime import datetime
import csv


app = Flask(__name__)


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_FILE = BASE_DIR / "data" / "analysis_history.csv"


# =========================================================
# SAVE ANALYSIS FOR POWER BI / ANALYTICS
# =========================================================

def save_analysis(message, result):
    """
    Save scam analysis results into a CSV file for Power BI dashboard.
    """
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        file_exists = HISTORY_FILE.exists()

        with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Date",
                    "Message",
                    "Category",
                    "Risk",
                    "Risk Score",
                    "Confidence",
                    "Suspicious Words"
                ])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                message,
                result.get("category", "Unknown"),
                result.get("risk", "LOW"),
                result.get("risk_score", 0),
                result.get("confidence", 0.0),
                ", ".join(result.get("suspicious_words", []))
            ])
    except Exception as e:
        print(f"[Warning] Could not save analysis history: {e}")


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message to analyze."}), 400

    result = detect_scam(message)
    save_analysis(message, result)
    return jsonify(result)


@app.route("/cybersecurity", methods=["POST"])
def cybersecurity():
    data = request.get_json() or {}
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Please specify a cybersecurity topic."}), 400

    result = get_topic(topic)
    if not result:
        return jsonify({
            "error": "Topic not found. Try 'Phishing', 'Ransomware', 'UPI Fraud', 'Smishing', 'SIM Swapping', 'Malware', or 'Password Security'."
        }), 404

    return jsonify({
        "type": "cybersecurity",
        "data": result
    })


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        data = request.get_json() or {}
        quiz_id = data.get("quiz_id", "")
        option = data.get("option", "")
        result = evaluate_quiz(quiz_id, option)
        if not result:
            return jsonify({"error": "Invalid quiz submission."}), 400
        return jsonify(result)

    # GET random quiz
    return jsonify(get_random_quiz())


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    result = chatbot_response(message)

    # Save to history only if it's a scam analysis
    if result.get("type") == "scam_analysis":
        scam_result = result.get("data", {})
        save_analysis(message, scam_result)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)