# 🛡️ ScamShield AI

> An AI-powered cybersecurity assistant that detects, analyzes, and explains potentially fraudulent or scam messages in real time.

ScamShield AI is a web-based cybersecurity application designed to help users identify suspicious messages such as phishing, banking scams, job scams, investment scams, prize scams, delivery scams, and impersonation scams.

The system combines **Machine Learning, NLP, rule-based detection, risk scoring, and cybersecurity awareness features** to provide users with an understandable security analysis.

---

## 🚀 Live Demo

🌐 **ScamShield AI:**  
https://scamshield-ai-bnp4.onrender.com/

---

## ✨ Features

### 🤖 AI Scam Detection
- Detects potentially fraudulent messages using Machine Learning.
- Uses **TF-IDF** for text feature extraction.
- Uses **Logistic Regression** for classification.
- Provides the predicted scam category and confidence score.

### 🔍 Rule-Based Detection
The system also checks messages for suspicious indicators such as:

- OTP
- Password
- Urgent
- Payment
- Prize
- Verify
- Blocked
- Click
- Pay

This provides an additional layer of cybersecurity analysis along with the ML model.

### ⚠️ Risk Assessment

ScamShield AI calculates an overall risk score based on:

- Machine Learning confidence
- Number of suspicious indicators
- Rule-based analysis

Risk levels:

| Risk Level | Meaning |
|------------|---------|
| 🟢 LOW | Message appears relatively safe |
| 🟡 MEDIUM | Message contains suspicious indicators |
| 🔴 HIGH | Message has strong scam/fraud indicators |

### 💬 AI Cybersecurity Chatbot
The project includes a conversational chatbot designed to answer cybersecurity-related questions and help users understand suspicious messages.

### 🔐 Cybersecurity Tools
The application includes additional security-focused features such as:

- Password strength checking
- Cybersecurity awareness
- Scam reporting
- Security quiz
- Attack visualization
- Cybersecurity analysis

### 📊 Analysis History
Scam analysis results can be stored in a database for future reference and analysis.

### 📝 Scam Reporting
Users can report suspected scams and provide information such as:

- Scam type
- Platform
- Amount lost
- Description
- Contact information shared
- Whether the incident was reported to police

---

# 🧠 How ScamShield AI Works

The system follows a multi-stage process:

```text
User Message
     │
     ▼
Text Preprocessing
     │
     ▼
TF-IDF Feature Extraction
     │
     ▼
Machine Learning Model
(Logistic Regression)
     │
     ├───────────────┐
     ▼               ▼
Scam Category    Rule-Based Detection
     │               │
     └───────┬───────┘
             ▼
       Risk Calculation
             │
             ▼
      Final Analysis
             │
             ▼
     Result to the User