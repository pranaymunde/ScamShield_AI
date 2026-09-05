from flask import Flask, render_template, request, jsonify
from app.scam_detector import detect_scam
from app.cybersecurity import get_topic
from app.chatbot import chatbot_response
from app.quiz import get_random_quiz, evaluate_quiz
from app.database import (
    init_db,
    save_analysis,
    save_quiz_attempt,
    get_recent_analyses,
    get_threat_stats
)

app = Flask(__name__)

# Initialize SQL Database on Startup
init_db()


# =========================================================
# WEB PAGES
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# CORE API ENDPOINTS
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message to analyze."}), 400

    result = detect_scam(message)
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    save_analysis(message, result, client_ip=client_ip)
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

        # Record quiz attempt in SQL database
        save_quiz_attempt(quiz_id, option, result["is_correct"])
        return jsonify(result)

    # GET returns random quiz challenge
    return jsonify(get_random_quiz())


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    result = chatbot_response(message)

    # Save to SQL database if it's a scam analysis
    if result.get("type") == "scam_analysis":
        scam_result = result.get("data", {})
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        save_analysis(message, scam_result, client_ip=client_ip)

    return jsonify(result)


# =========================================================
# SQL DATABASE TELEMETRY & HISTORY APIS
# =========================================================

@app.route("/api/stats", methods=["GET"])
def api_stats():
    """Returns real-time SQL threat statistics and telemetry."""
    stats = get_threat_stats()
    return jsonify(stats)


@app.route("/api/history", methods=["GET"])
def api_history():
    """Returns recent analysis events from SQL database."""
    limit = request.args.get("limit", 15, type=int)
    history = get_recent_analyses(limit=limit)
    return jsonify({"history": history})


if __name__ == "__main__":
    app.run(debug=True)