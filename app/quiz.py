import random

QUIZ_SCENARIOS = [
    {
        "id": "quiz_1",
        "title": "Case 01: The Urgent Bank Alert",
        "message": "SMS: 'Dear Customer, your SBI account ending in 4102 has been temporarily suspended due to KYC non-compliance. Complete verification within 12 hours at http://sbi-kyc-update.xyz to prevent account permanent closure.'",
        "options": [
            {"id": "A", "text": "🚨 Phishing Scam (Do not click)"},
            {"id": "B", "text": "✅ Genuine Bank Notice (Update immediately)"}
        ],
        "correct": "A",
        "explanation": "This is a classic Phishing Scam. Banks never use third-party domains (.xyz) or send urgent KYC verification links over SMS. Genuine notices instruct you to visit your branch or log into the official banking application directly.",
        "difficulty": "Easy",
        "tags": ["Banking Scam", "Smishing", "Urgency Trap"]
    },
    {
        "id": "quiz_2",
        "title": "Case 02: Work From Home Job Offer",
        "message": "WhatsApp: 'Hi! I am Emma from Global Media HR. We are offering part-time freelance work: just like YouTube videos and earn ₹3,000 to ₹8,000 per day. No experience needed. Reply YES to join our Telegram group.'",
        "options": [
            {"id": "A", "text": "✅ Legitimate Remote Job"},
            {"id": "B", "text": "🚨 Task / Investment Scam"}
        ],
        "correct": "B",
        "explanation": "This is the prevalent 'Telegram Task Scam'. Victims are initially given small payouts (₹150) to build trust, then coerced into depositing tens of thousands for 'prepaid investment tasks' before the scammer vanishes.",
        "difficulty": "Medium",
        "tags": ["Job Scam", "Task Fraud", "Telegram"]
    },
    {
        "id": "quiz_3",
        "title": "Case 03: The Courier Customs Clearance",
        "message": "Email from 'tracking@fedex-express-delivery.club': 'Your international parcel #FX-88912 is on hold at customs. An outstanding customs clearance duty of ₹450 is required. Pay now via this payment link to release parcel.'",
        "options": [
            {"id": "A", "text": "🚨 Impersonation Scam (Phishing)"},
            {"id": "B", "text": "✅ Legitimate Courier Invoice"}
        ],
        "correct": "A",
        "explanation": "Notice the domain 'fedex-express-delivery.club' instead of official 'fedex.com'. Scammers send thousands of these hoping someone has an expected delivery. Paying gives them your debit/credit card details.",
        "difficulty": "Medium",
        "tags": ["Delivery Scam", "Spoofed Domain", "Credential Theft"]
    },
    {
        "id": "quiz_4",
        "title": "Case 04: The Genuine Transaction OTP",
        "message": "SMS from 'VK-HDFCBK': '829143 is your Secret OTP for online purchase of INR 1,299.00 at AMAZON INDIA on Card ending 9821. OTP valid for 5 mins. NEVER SHARE YOUR OTP WITH ANYONE.'",
        "options": [
            {"id": "A", "text": "✅ Genuine Bank Transaction OTP"},
            {"id": "B", "text": "🚨 Phishing Scam"}
        ],
        "correct": "A",
        "explanation": "This is a legitimate bank OTP notification sent from an authorized banking sender ID ('VK-HDFCBK'). It clearly states the exact merchant and amount, contains no suspicious links, and warns you never to share the code.",
        "difficulty": "Hard",
        "tags": ["Legitimate Traffic", "Authentic 2FA", "Cyber Literacy"]
    },
    {
        "id": "quiz_5",
        "title": "Case 05: Electricity Bill Disconnection Threat",
        "message": "SMS from '+91 98231 XXXXX': 'Dear consumer, your electricity power will be disconnected tonight at 9:30 PM because previous month bill was not updated. Please immediately contact our Electricity Officer at 98231XXXXX.'",
        "options": [
            {"id": "A", "text": "✅ Official Utility Notice"},
            {"id": "B", "text": "🚨 Electricity Bill Scam"}
        ],
        "correct": "B",
        "explanation": "Electricity boards never send disconnection notices from personal 10-digit mobile numbers or threaten cut-offs within hours. Calling the number connects you to a fraudster who instructs you to install QuickSupport or AnyDesk to steal bank funds.",
        "difficulty": "Easy",
        "tags": ["Utility Scam", "Social Engineering", "Remote Access"]
    },
    {
        "id": "quiz_6",
        "title": "Case 06: UPI QR Code to 'Receive' Money",
        "message": "Marketplace Chat: 'I want to purchase your laptop for ₹25,000. I am sending this QR code. Please open GooglePay, scan this QR code, and enter your UPI PIN so the money is deposited directly into your bank.'",
        "options": [
            {"id": "A", "text": "🚨 QR Code Reverse-Payment Scam"},
            {"id": "B", "text": "✅ Valid UPI Payment Method"}
        ],
        "correct": "A",
        "explanation": "CRITICAL RULE: You NEVER scan a QR code or enter your UPI PIN to RECEIVE money. Entering your UPI PIN always authorizes money leaving your account.",
        "difficulty": "Easy",
        "tags": ["UPI Fraud", "QR Scam", "Financial Literacy"]
    },
    {
        "id": "quiz_7",
        "title": "Case 07: OTP Requested by 'Bank Official'",
        "message": "Phone Call: 'Good morning, I am calling from SBI Credit Card Department. Your card benefits are expiring. To renew your reward points, I need to verify your identity. Please share the 6-digit OTP sent to your registered mobile number.'",
        "options": [
            {"id": "A", "text": "✅ Genuine Bank Customer Service"},
            {"id": "B", "text": "🚨 Vishing / OTP Phishing Attack"}
        ],
        "correct": "B",
        "explanation": "Banks NEVER call you to ask for OTPs. An OTP (One-Time Password) is a one-time authorization code for YOUR transactions. Sharing it with anyone — even a supposed bank official — transfers that authorization to the scammer who can instantly drain your account.",
        "difficulty": "Easy",
        "tags": ["Vishing", "OTP Fraud", "Banking Scam"]
    },
    {
        "id": "quiz_8",
        "title": "Case 08: The Stock Market Investment Group",
        "message": "WhatsApp Group: 'Join our SEBI-registered premium trading circle. Our AI algorithm guarantees 40% monthly returns. Invest ₹50,000 and watch it grow to ₹1,20,000 in 30 days. Limited slots! DM @InvestmentGuru_Official now.'",
        "options": [
            {"id": "A", "text": "✅ Legitimate SEBI Registered Investment"},
            {"id": "B", "text": "🚨 Investment Ponzi / Advance Fee Fraud"}
        ],
        "correct": "B",
        "explanation": "This is a classic Pig Butchering or Ponzi Scheme. No legitimate investment can guarantee 40% monthly returns. SEBI-registered advisors never recruit via WhatsApp groups. Early investors receive payouts from new investor money to build trust, then the operator vanishes with everyone's funds.",
        "difficulty": "Hard",
        "tags": ["Investment Fraud", "Ponzi Scheme", "SEBI Impersonation"]
    },
    {
        "id": "quiz_9",
        "title": "Case 09: Microsoft Technical Support Call",
        "message": "Pop-up on screen: '⚠️ WINDOWS SECURITY ALERT ⚠️ Your computer has been infected with a dangerous virus. Call Microsoft Support immediately: +1-800-xxx-xxxx. Do NOT shut down your computer. Data loss may occur.'",
        "options": [
            {"id": "A", "text": "🚨 Tech Support Scam (Fake Alert)"},
            {"id": "B", "text": "✅ Genuine Microsoft Security Warning"}
        ],
        "correct": "A",
        "explanation": "Microsoft NEVER shows pop-ups with phone numbers asking you to call. These browser-based scare-pop-ups are Tech Support Scams. Calling the number connects to scammers who request remote access (via AnyDesk/TeamViewer) to 'fix' the fake virus, while actually stealing banking credentials and charging hundreds for fake services.",
        "difficulty": "Medium",
        "tags": ["Tech Support Scam", "Social Engineering", "Remote Access Fraud"]
    },
    {
        "id": "quiz_10",
        "title": "Case 10: The Romance Scammer's Crisis",
        "message": "Dating App Chat (2 months): 'My love, I am stuck at customs in Dubai. They seized my engineering equipment worth $50,000. I need $3,000 for clearance fees. I promise to repay you 10x when I arrive. You are my only hope. Please send via Western Union.'",
        "options": [
            {"id": "A", "text": "🚨 Romance / Pig Butchering Scam"},
            {"id": "B", "text": "✅ Genuine Emergency from a Partner"}
        ],
        "correct": "A",
        "explanation": "This is a textbook Romance Scam. Scammers spend weeks or months building fake emotional bonds online, then fabricate emergencies requiring wire transfers via untraceable methods (Western Union, crypto, gift cards). The 'person' is entirely fake — often AI-generated or stock photos. Never send money to someone you have only met online.",
        "difficulty": "Medium",
        "tags": ["Romance Scam", "Pig Butchering", "Social Engineering"]
    }
]


def get_random_quiz(exclude_id=None):
    pool = [q for q in QUIZ_SCENARIOS if q["id"] != exclude_id]
    if not pool:
        pool = QUIZ_SCENARIOS
    return random.choice(pool)


def evaluate_quiz(quiz_id, selected_option):
    for q in QUIZ_SCENARIOS:
        if q["id"] == quiz_id:
            is_correct = (selected_option.upper().strip() == q["correct"].upper().strip())
            return {
                "quiz_id": q["id"],
                "title": q["title"],
                "is_correct": is_correct,
                "selected": selected_option,
                "correct_option": q["correct"],
                "explanation": q["explanation"],
                "difficulty": q["difficulty"],
                "tags": q["tags"]
            }
    return None
