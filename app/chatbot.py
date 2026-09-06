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
    # 6a. EMAIL HEADER ANALYZER
    # ---------------------------------------------------------
    email_triggers = ["email header", "analyze email", "check email header", "inspect email", "spf", "dkim", "dmarc", "received from"]
    if any(k in text for k in email_triggers):
        return {
            "type": "email_header_guide",
            "title": "📧 Email Header Forensics Guide",
            "data": {
                "description": "Email headers are hidden metadata attached to every email that reveal the true origin and routing of a message. Analyzing them exposes spoofed senders and phishing infrastructure.",
                "fields": [
                    {
                        "field": "Return-Path",
                        "icon": "📬",
                        "risk": "HIGH",
                        "explanation": "The actual reply address. If different from the 'From' address, the email is likely spoofed.",
                        "what_to_look": "Mismatch between From: and Return-Path: domains is a critical red flag."
                    },
                    {
                        "field": "Received: from",
                        "icon": "🌐",
                        "risk": "HIGH",
                        "explanation": "Shows the chain of mail servers the email passed through. Read from bottom to top — the bottom entry is the true origin.",
                        "what_to_look": "IP addresses in private ranges (192.168.x.x, 10.x.x.x) or known malicious hosting countries."
                    },
                    {
                        "field": "Authentication-Results (SPF)",
                        "icon": "🛡️",
                        "risk": "MEDIUM",
                        "explanation": "Sender Policy Framework verifies the sending server is authorized to send email on behalf of the domain.",
                        "what_to_look": "Look for 'spf=fail' or 'spf=softfail' — these indicate the email domain does NOT authorize the sending server."
                    },
                    {
                        "field": "DKIM-Signature",
                        "icon": "🔐",
                        "risk": "MEDIUM",
                        "explanation": "DomainKeys Identified Mail is a cryptographic signature proving the email content was not altered in transit.",
                        "what_to_look": "A missing or failing DKIM signature means the message may have been tampered with or is fraudulent."
                    },
                    {
                        "field": "X-Mailer / User-Agent",
                        "icon": "⚙️",
                        "risk": "LOW",
                        "explanation": "Reveals the email client or server software used. Spammers often use bulk mailers (Sendgrid, Mailchimp misuse, phpmailer scripts).",
                        "what_to_look": "Generic script-based mailers (PHPMailer, Python smtplib) sending 'official bank notices' are suspicious."
                    },
                    {
                        "field": "Message-ID",
                        "icon": "🆔",
                        "risk": "LOW",
                        "explanation": "A unique identifier for the message. Legitimate emails have Message-IDs matching their sending domain.",
                        "what_to_look": "Message-ID with random gibberish domains (e.g. <abc@fkjd23.ru>) on a supposed Google or HDFC email."
                    }
                ],
                "how_to_access": [
                    "Gmail: Open email → 3-dot menu → Show Original",
                    "Outlook: File → Properties → Internet Headers",
                    "Yahoo Mail: More → View Raw Message",
                    "Paste raw headers into: mxtoolbox.com/EmailHeaders.aspx"
                ]
            }
        }

    # ---------------------------------------------------------
    # 6b. URL / DOMAIN DEEP SCANNER
    # ---------------------------------------------------------
    url_scan_triggers = ["scan url", "check url", "analyze url", "is this url safe", "scan domain", "check domain", "url scanner", "domain scanner"]
    url_in_message = re.search(r'https?://[\S]+', original_message, re.IGNORECASE)
    if any(k in text for k in url_scan_triggers) or (url_in_message and len(text.split()) <= 5):
        if url_in_message:
            url = url_in_message.group(0)
            from app.rules import analyze_urls
            url_result = analyze_urls(original_message)
            indicators = url_result.get('suspicious_indicators', [])
            urls = url_result.get('urls', [])
            risk = 'HIGH' if len(indicators) >= 3 else ('MEDIUM' if len(indicators) >= 1 else 'LOW')
            return {
                "type": "url_scan",
                "title": "🔗 URL Deep Threat Analysis",
                "data": {
                    "url": url,
                    "urls": urls,
                    "indicators": indicators,
                    "risk": risk,
                    "checks": url_result,
                    "advice": "Never visit this URL on a primary device. Use an isolated sandbox or VirusTotal (virustotal.com) for additional verification." if risk == 'HIGH' else "Exercise caution. Verify this URL against the official website of the organization."
                }
            }
        return {
            "type": "url_scan_prompt",
            "message": "🔗 To scan a URL, paste it directly into the chat (e.g. 'http://suspicious-site.xyz/login') or type 'scan url http://example.com'. I will analyze domain structure, IP exposure, path heuristics, and suspicious indicators."
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