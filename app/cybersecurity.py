# =========================================================
# COMPREHENSIVE CYBERSECURITY KNOWLEDGE VAULT
# =========================================================

CYBERSECURITY_TOPICS = {
    "phishing": {
        "title": "Phishing Attacks",
        "badge": "Email & Web Fraud",
        "description": "Phishing is a deceptive cyber attack where bad actors impersonate legitimate entities (banks, employers, tech companies) to trick you into disclosing confidential data such as passwords, OTPs, or credit card numbers.",
        "example": "An email claiming 'Your Netflix payment failed! Update billing details within 24 hours to avoid account cancellation' leading to a cloned credential-harvesting page.",
        "signs": [
            "Urgent demands threatening account closure or legal penalties",
            "Mismatched sender domain (e.g. support@paypa1-security.xyz)",
            "Generic greetings like 'Dear Customer' instead of your name",
            "Requests to click links and enter login credentials or OTP"
        ],
        "protection": [
            "Never click verification links in unverified emails or SMS",
            "Bookmark official banking and login portals directly",
            "Verify sender address carefully before responding",
            "Enforce hardware or authenticator-based Multi-Factor Authentication"
        ]
    },

    "smishing": {
        "title": "Smishing (SMS Phishing)",
        "badge": "Mobile Message Fraud",
        "description": "Smishing uses fraudulent SMS text messages to lure victims into tapping malicious links or contacting fake support helplines, often claiming parcel holds, electricity bill cut-offs, or bank account blocks.",
        "example": "'Dear Customer, your SBI YONO account will be blocked today. Please update your PAN Card immediately by clicking: http://tinyurl.com/sbi-update'",
        "signs": [
            "SMS sent from random 10-digit mobile numbers rather than registered corporate shortcodes",
            "Shortened URLs (bit.ly, tinyurl) or raw IP addresses",
            "Extreme urgency regarding utilities, courier deliveries, or bank accounts",
            "Demands to download APK files directly from SMS links"
        ],
        "protection": [
            "Never install APK files sent via SMS or WhatsApp",
            "Banks and utility providers will never ask for PAN/Aadhaar updates over random SMS",
            "Forward suspicious spam SMS to carrier reporting (e.g. 1909)",
            "Cross-verify claims by visiting the official app or portal independently"
        ]
    },

    "vishing": {
        "title": "Vishing (Voice Call Scams)",
        "badge": "Phone Impersonation",
        "description": "Vishing involves phone calls where fraudsters pose as bank managers, police officers, customs officials, or IT support to psychologically pressure you into transferring money or sharing OTPs.",
        "example": "A caller claiming 'I am Officer Sharma from Cyber Crime Cell. A parcel with narcotics in your name is seized. Transfer money to this RBI clearance account to avoid immediate arrest.'",
        "signs": [
            "Caller claims to be from law enforcement, customs, or bank headquarters",
            "Aggressive tone, threats of arrest, or refusal to let you disconnect",
            "Demands for screen sharing via AnyDesk, TeamViewer, or QuickSupport",
            "Insistence on secret transfers or revealing OTPs"
        ],
        "protection": [
            "Law enforcement and banks will NEVER demand funds transfer or OTP over a phone call",
            "Immediately hang up and call the official department number",
            "Never install remote desktop apps (AnyDesk, QuickSupport) at a caller's request",
            "Report vishing calls to the National Cyber Crime Helpline (1930 in India)"
        ]
    },

    "upi fraud": {
        "title": "UPI & Digital Payment Scams",
        "badge": "Financial Security",
        "description": "Scammers exploit misunderstandings of UPI interfaces by sending 'Collect Money' requests disguised as payments, or sending QR codes claiming you must scan them to 'receive money'.",
        "example": "On OLX/marketplace: 'I will buy your sofa. Scanning this QR code will deposit ₹15,000 into your account. Enter your UPI PIN to accept credit.'",
        "signs": [
            "Someone asking you to enter your UPI PIN to 'receive' money",
            "QR codes sent for receiving payments (QR codes are strictly for SENDING)",
            "Collect requests sent on PhonePe/GPay/Paytm from unknown parties",
            "Fake screenshot of payment transfer accompanied by demands for refund"
        ],
        "protection": [
            "GOLDEN RULE: You NEVER need to enter your UPI PIN or scan a QR code to receive money",
            "Decline unknown collect requests on payment apps immediately",
            "Verify money credited directly inside your banking app, not via screenshots",
            "Set daily transaction limits on your UPI applications"
        ]
    },

    "ransomware": {
        "title": "Ransomware",
        "badge": "Malicious Extortion",
        "description": "Ransomware is malicious software that encrypts your sensitive personal or enterprise files, rendering them inaccessible, and demands cryptocurrency ransom for decryption keys.",
        "example": "All your photos and documents suddenly show the '.locked' extension, with a desktop text file demanding 0.5 Bitcoin within 72 hours or files are destroyed.",
        "signs": [
            "Sudden CPU/disk spikes as files are encrypted in bulk",
            "Inaccessible files with strange extensions (.locked, .crypto)",
            "Ransom demand text notes appearing across directories",
            "Antivirus software disabled unexpectedly"
        ],
        "protection": [
            "Maintain the 3-2-1 backup rule: 3 copies, 2 media types, 1 immutable offline/cloud copy",
            "Keep operating systems and security patches strictly up-to-date",
            "Never pay ransoms: payment does not guarantee decryption and funds future crime",
            "Disable remote desktop protocols (RDP) on exposed internet ports"
        ]
    },

    "malware": {
        "title": "Malware & Spyware",
        "badge": "Endpoint Threats",
        "description": "Malware is any software intentionally designed to cause damage to a computer, server, client, or computer network, including trojans, keyloggers, worms, and spyware.",
        "example": "Downloading a pirated video editing program that secretly installs a keylogger logging all keystrokes and bank logins back to a command-and-control server.",
        "signs": [
            "Noticeable system slowdown, overheating, or unexpected data usage spikes",
            "Unprompted browser toolbars, redirections, or strange default search engines",
            "Antivirus notifications or disabled system defense tools",
            "Pop-ups appearing even when browsers are closed"
        ],
        "protection": [
            "Only download software from authorized app stores and official vendors",
            "Avoid pirated media, cracks, and modified APKs",
            "Run regular scans with reputable anti-malware software",
            "Review installed extensions and background startup programs periodically"
        ]
    },

    "social engineering": {
        "title": "Social Engineering",
        "badge": "Human Exploitation",
        "description": "Social engineering manipulates human psychology rather than technical flaws. Attackers exploit fear, trust, greed, or curiosity to deceive victims into handing over valuable data.",
        "example": "An attacker pretending to be a new employee who forgot their login card, asking you to hold the secure door or provide a guest Wi-Fi bypass password.",
        "signs": [
            "High-pressure appeals to authority, urgency, or extreme secrecy",
            "Offers that appear unnaturally generous (lottery prizes, free luxury trips)",
            "Unexpected requests for sensitive company or personal data",
            "Flattery or emotional manipulation to bypass safety protocols"
        ],
        "protection": [
            "Always follow verification procedures regardless of who claims to be asking",
            "Take a step back: emotional urgency is the number one sign of manipulation",
            "Establish secondary out-of-band verification for unusual financial requests",
            "Educate family members and colleagues about common impersonation scripts"
        ]
    },

    "password security": {
        "title": "Password Security & Credential Defense",
        "badge": "Access Control",
        "description": "Passwords are the primary gateway to your digital identity. Weak, reused, or compromised passwords allow automated brute-force attacks and credential stuffing across platforms.",
        "example": "Using the password 'Summer2023!' across 12 different websites; when one minor forum gets breached, attackers use the same password to compromise your primary email.",
        "signs": [
            "Using short passwords (<12 characters) or personal names/birthdays",
            "Reusing identical passwords across multiple online platforms",
            "Receiving password reset emails you did not initiate",
            "Storing passwords in plain text files or sticky notes"
        ],
        "protection": [
            "Use a dedicated Password Manager (e.g. Bitwarden, 1Password)",
            "Adopt passphrases with 14+ characters containing varied character types",
            "Enable Two-Factor Authentication (2FA) on every critical account",
            "Check breach monitoring services (e.g. haveibeenpwned.com) periodically"
        ]
    },

    "sim swapping": {
        "title": "SIM Swapping & Port Scams",
        "badge": "Telecom Threat",
        "description": "In a SIM swap attack, criminals convince your mobile carrier to transfer your phone number to a SIM card in their possession, hijacking all SMS-based OTPs and 2FA codes.",
        "example": "Your phone suddenly loses mobile network reception with 'No Service'. Minutes later, your bank account is drained using SMS OTPs intercepted on the attacker's SIM.",
        "signs": [
            "Sudden and unexplained loss of mobile cellular signal / 'No Service'",
            "SMS notifications from carrier regarding SIM change or porting requests",
            "Inability to make calls or receive SMS when bill is fully paid",
            "Unauthorized login alerts for banking or email accounts"
        ],
        "protection": [
            "Immediately contact your mobile carrier if your phone unexpectedly displays 'No Service'",
            "Set up a carrier PIN/passcode required for any SIM replacements",
            "Switch from SMS-based 2FA to app-based TOTP (Google Authenticator, YubiKey)",
            "Never publish your primary banking phone number openly on social media"
        ]
    },

    "deepfake scams": {
        "title": "Deepfake & AI Voice Cloning Scams",
        "badge": "AI Era Threats",
        "description": "Criminals use artificial intelligence to clone the voice or video likeness of family members, company executives, or celebrities to orchestrate convincing emergency extortion or investment fraud.",
        "example": "A grandparent receives a phone call with the exact voice of their grandson, crying and saying 'Grandma, I got into an accident in another city, please wire ₹50,000 for bail.'",
        "signs": [
            "Uncharacteristic emergency calls demanding instant wire transfers or crypto",
            "Slight robotic artifacts, pauses, or reluctance to answer personal questions",
            "Strict instructions not to contact other family members",
            "Video calls with glitching facial boundaries or unnatural blinking"
        ],
        "protection": [
            "Establish a private 'Family Safe Word' that AI voice clones cannot know",
            "Hang up and independently call the person back on their saved known number",
            "Be skeptical of urgent emotional financial emergencies requested via phone",
            "Limit public availability of high-quality voice audio clips on social networks"
        ]
    },

    "ddos": {
        "title": "DDoS (Distributed Denial-of-Service)",
        "badge": "Network Availability",
        "description": "DDoS attacks overwhelm a target server, service, or network with a flood of malicious internet traffic generated by botnets, causing outages and denying service to legitimate users.",
        "example": "An online store during Black Friday is targeted by 50,000 compromised IoT cameras sending fake HTTP requests, crashing the checkout servers.",
        "signs": [
            "Website or application becomes unresponsive or displays 502/504 gateway errors",
            "Unusual traffic spikes from specific geographic regions or IP ranges",
            "Specific endpoint degradation under sudden traffic spikes",
            "Severe internal network latency and timeout surges"
        ],
        "protection": [
            "Deploy Cloudflare, AWS Shield, or enterprise DDoS mitigation reverse-proxies",
            "Implement rate-limiting and Web Application Firewalls (WAF)",
            "Utilize Anycast DNS and distributed content delivery networks (CDNs)",
            "Maintain an incident response playbook with automated traffic shedding"
        ]
    }
}


def get_topic(topic_query):
    """
    Finds matching cybersecurity topic data based on user inquiry.
    """
    topic_query = str(topic_query).lower().strip()

    # Direct match or partial keyword match
    for key, info in CYBERSECURITY_TOPICS.items():
        if key in topic_query or topic_query in key:
            return {
                "topic": info["title"],
                "badge": info["badge"],
                "description": info["description"],
                "example": info.get("example", ""),
                "signs": info["signs"],
                "protection": info["protection"]
            }

    # Keyword mappings
    synonyms = {
        "sms": "smishing",
        "text scam": "smishing",
        "call scam": "vishing",
        "fake call": "vishing",
        "phone scam": "vishing",
        "voice scam": "vishing",
        "upi": "upi fraud",
        "qr code": "upi fraud",
        "payment scam": "upi fraud",
        "trojan": "malware",
        "spyware": "malware",
        "virus": "malware",
        "passphrase": "password security",
        "credential": "password security",
        "sim card": "sim swapping",
        "sim swap": "sim swapping",
        "ai voice": "deepfake scams",
        "voice clone": "deepfake scams",
        "deepfake": "deepfake scams",
        "botnet": "ddos",
        "denial of service": "ddos"
    }

    for syn, mapped_key in synonyms.items():
        if syn in topic_query:
            info = CYBERSECURITY_TOPICS[mapped_key]
            return {
                "topic": info["title"],
                "badge": info["badge"],
                "description": info["description"],
                "example": info.get("example", ""),
                "signs": info["signs"],
                "protection": info["protection"]
            }

    return None