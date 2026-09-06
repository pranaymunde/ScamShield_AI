from flask import Flask, render_template, request, jsonify
from app.scam_detector import detect_scam
from app.cybersecurity import get_topic
from app.chatbot import chatbot_response
from app.quiz import get_random_quiz, evaluate_quiz
from app.database import (
    init_db,
    save_analysis,
    save_quiz_attempt,
    save_scam_report,
    get_recent_analyses,
    get_threat_stats,
    get_category_breakdown,
    get_recent_reports
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


@app.route("/api/chart", methods=["GET"])
def api_chart():
    """Returns category breakdown data for threat chart visualization."""
    breakdown = get_category_breakdown()
    return jsonify({"breakdown": breakdown})


@app.route("/api/reports", methods=["GET"])
def api_reports():
    """Returns recent user-submitted scam reports."""
    limit = request.args.get("limit", 10, type=int)
    reports = get_recent_reports(limit=limit)
    return jsonify({"reports": reports})


@app.route("/api/report", methods=["POST"])
def submit_report():
    """Accepts a user-submitted scam incident report and stores it in SQL."""
    data = request.get_json() or {}

    scam_type = data.get("scam_type", "").strip()
    platform = data.get("platform", "").strip()
    amount_lost = data.get("amount_lost", 0)
    description = data.get("description", "").strip()
    contact_shared = data.get("contact_shared", False)
    reported_to_police = data.get("reported_to_police", False)
    reporter_email = data.get("reporter_email", "").strip()

    if not scam_type or not description:
        return jsonify({"error": "Scam type and description are required."}), 400

    report_id = save_scam_report(
        scam_type, platform, amount_lost, description,
        contact_shared, reported_to_police, reporter_email
    )
    return jsonify({
        "success": True,
        "report_id": report_id,
        "message": f"Your report #{report_id} has been submitted and logged to the ScamShield database. Thank you for helping protect the community!"
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)