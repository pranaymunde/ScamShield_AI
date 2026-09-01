from flask import Flask, render_template, request, jsonify
from app.scam_detector import detect_scam

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Please enter a message."
        }), 400

    result = detect_scam(message)

    return jsonify(result)


if __name__ == "__main__":
    app.run()
    
