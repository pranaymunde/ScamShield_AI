import re
from app.scam_detector import detect_scam
from app.cybersecurity import get_topic
from app.attack_graph import bfs_attack_path, dfs_attack_path
from app.astar import astar_defense_path
from app.password_checker import check_password
from app.quiz import get_random_quiz, evaluate_quiz
from app.database import get_threat_stats, get_recent_analyses



def chatbot_response(message):
    original_message = str(message).strip()
    text = original_message.lower()

    # ---------------------------------------------------------
    # 1. QUIZ INTERACTIVE SUBMISSIONS (e.g. "QUIZ_ANSWER:quiz_1:A")
    # ---------------------------------------------------------
    if text.startswith("quiz_answer:"):
        parts = original_message.split(":")
        if len(parts) >= 3:
            quiz_id = parts[1].strip()
            chosen_opt = parts[2].strip()
            result = evaluate_quiz(quiz_id, chosen_opt)
            if result:
                return {
                    "type": "quiz_result",
                    "data": result
                }

    # ---------------------------------------------------------
    # 2. START / NEXT QUIZ CHALLENGE
    # ---------------------------------------------------------
    if any(k in text for k in ["quiz", "test me", "scam quiz", "spot the scam", "cyber challenge", "quiz me"]):
        quiz_data = get_random_quiz()
        return {
            "type": "quiz",
            "data": quiz_data
        }

    # ---------------------------------------------------------
    # 3. GREETINGS & INTRODUCTIONS
    # ---------------------------------------------------------
    greetings = ["hello", "hi", "hey", "greetings", "good morning", "good evening", "who are you", "what can you do", "help", "start"]
    if text in greetings or text.startswith(("hello ", "hi ", "hey ")):
        return {
            "type": "bot_intro",
            "message": "Welcome to ScamShield AI — Your Advanced Cybersecurity Co-Pilot",
            "data": {
                "headline": "I analyze digital threats, inspect malicious links, evaluate passwords, and run attack simulations.",
                "capabilities": [
                    {"icon": "⚡", "title": "Scam & Phishing Scanner", "desc": "Paste any SMS, WhatsApp text, email, or offer to assess fraud probability and red flags."},
                    {"icon": "🔗", "title": "Malicious Link Inspector", "desc": "Analyzes IP hosts, spoofed domains, and risky shorteners."},
                    {"icon": "🔐", "title": "Password Strength Lab", "desc": "Computes Shannon entropy and GPU offline crack time estimation."},
                    {"icon": "🧭", "title": "Attack Graph AI (BFS/DFS/A*)", "desc": "Visualizes cyber threat chains and shortest mitigation routes."},
                    {"icon": "🎯", "title": "Cyber Defense Quiz", "desc": "Test your scam detection reflexes with real-world scenarios."}
                ],
                "quick_prompts": [
                    "Check my password: Secret#2026",
                    "Simulate attack with BFS",
                    "Find safest path with A*",
                    "What is UPI fraud?",
                    "Start a scam quiz",
                    "Emergency helpline numbers"
                ]
            }
        }

    # ---------------------------------------------------------
    # 4. EMERGENCY REPORTING & HELPLINES
    # ---------------------------------------------------------
    helpline_triggers = ["helpline", "emergency", "complaint", "report scam", "report fraud", "scammed", "money stolen", "cyber crime number", "1930", "police"]
    if any(h in text for h in helpline_triggers):
        return {
            "type": "helpline",
            "title": "🚨 Emergency Cyber Crime Response Protocol",
            "data": {
                "golden_hour_note": "CRITICAL: Act within the 'Golden Hour' (first 2-3 hours) after fraudulent financial debits to maximize fund freeze success.",
                "helplines": [
                    {"country": "India", "service": "National Cyber Crime Reporting Helpline", "contact": "1930", "portal": "cybercrime.gov.in"},
                    {"country": "United States", "service": "Internet Crime Complaint Center (IC3 / FBI)", "contact": "ic3.gov", "portal": "www.ic3.gov"},
                    {"country": "United Kingdom", "service": "Action Fraud (National Fraud & Cyber Crime)", "contact": "0300 123 2040", "portal": "actionfraud.police.uk"},
                    {"country": "International", "service": "Local Law Enforcement / Interpol Cyber Desk", "contact": "112 / 911", "portal": "interpol.int"}
                ],
                "immediate_actions": [
                    "Call your bank customer support immediately to BLOCK credit/debit cards and freeze net banking.",
                    "Dial 1930 (India) or file a ticket on your national cybercrime portal with transaction reference (UTR) numbers.",
                    "Take clear screenshots of SMS, WhatsApp chats, sender phone numbers, and payment receipts as digital evidence.",
                    "Change passwords and enable 2FA on primary email and associated accounts from a clean device."
                ]
            }
        }

    # ---------------------------------------------------------
    # 5. PASSWORD STRENGTH LAB
    # ---------------------------------------------------------
    password_cmd_match = re.search(r"(?:check(?:\s+my)?\s+password|check\s+password[:\s]+|is\s+password[:\s]+)(.+)", original_message, re.IGNORECASE)
    if password_cmd_match:
        pwd = password_cmd_match.group(1).strip()
        if pwd:
            result = check_password(pwd)
            return {
                "type": "password_strength",
                "password_tested": "•" * min(len(pwd), 20),
                "data": result
            }

    if (
        "password strength" in text
        or "check password" in text
        or text == "password"
        or "strong password" in text
    ):
        return {
            "type": "password_strength",
            "data": {
                "strength": "Info",
                "score": 0,
                "entropy": 0,
                "crack_time": "N/A",
                "checklist": [
                    {"label": "14+ characters minimum length", "passed": True},
                    {"label": "Mix of uppercase, lowercase, numbers, and symbols", "passed": True},
                    {"label": "No dictionary words, birthdays, or keyboard walks", "passed": True},
                    {"label": "Unique to each account (backed by Password Manager)", "passed": True}
                ],
                "suggestions": [
                    "To test a specific password, type: 'check my password YourSecret123!'",
                    "We never store or log passwords submitted to the analyzer."
                ]
            }
        }

    # ---------------------------------------------------------
    # 6. ATTACK GRAPH SIMULATIONS (BFS / DFS / A*)
    # ---------------------------------------------------------
    scenario = "phishing"
    if "ransomware" in text:
        scenario = "ransomware"
    elif "upi" in text or "payment" in text or "qr" in text:
        scenario = "upi"

    if "bfs" in text or "breadth first" in text or "attack reach my account" in text:
        graph_result = bfs_attack_path(scenario)
        return {
            "type": "attack_path",
            "data": graph_result
        }

    if "dfs" in text or "depth first" in text or "possible phishing attack path" in text or "attack route" in text:
        graph_result = dfs_attack_path(scenario)
        return {
            "type": "attack_path",
            "data": graph_result
        }

    if any(k in text for k in ["a*", "astar", "safest", "safe action", "safety path", "mitigation path", "defense path"]):
        graph_result = astar_defense_path()
        return {
            "type": "attack_path",
            "data": graph_result
        }

    # ---------------------------------------------------------
    # 7. CYBERSECURITY KNOWLEDGE BASE
    # ---------------------------------------------------------
    cyber_result = get_topic(text)
    if cyber_result and len(text.split()) <= 12 and not any(k in text for k in ["http://", "https://", "won", "lottery", "otp", "blocked"]):
        return {
            "type": "cybersecurity",
            "data": cyber_result
        }

    # ---------------------------------------------------------
    # 8. SQL DATABASE TELEMETRY & STATS
    # ---------------------------------------------------------
    if any(k in text for k in ["database", "db stats", "telemetry", "how many scans", "threat statistics", "sql stats", "scan history"]):
        stats = get_threat_stats()
        recent = get_recent_analyses(5)
        return {
            "type": "db_stats",
            "title": "📊 SQL Database Threat Telemetry",
            "data": {
                "stats": stats,
                "recent": recent
            }
        }

    # ---------------------------------------------------------
    # 9. DEEP SCAM & PHISHING ANALYSIS (DEFAULT CORE ENGINE)
    # ---------------------------------------------------------
    scam_result = detect_scam(original_message)
    return {
        "type": "scam_analysis",
        "data": scam_result
    }