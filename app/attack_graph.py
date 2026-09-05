from collections import deque

# =========================================================
# RICH ATTACK GRAPHS & SCENARIOS
# =========================================================

SCENARIO_GRAPHS = {
    "phishing": {
        "title": "Phishing & Credential Compromise Chain",
        "start": "Phishing Bait",
        "target": "Account Takeover",
        "graph": {
            "Phishing Bait": ["Malicious Link", "Infected Attachment"],
            "Malicious Link": ["Spoofed Login Portal"],
            "Infected Attachment": ["Keylogger Dropper"],
            "Spoofed Login Portal": ["Credential Interception"],
            "Keylogger Dropper": ["Session Token Theft"],
            "Credential Interception": ["2FA Bypass Attempt"],
            "Session Token Theft": ["Account Takeover"],
            "2FA Bypass Attempt": ["Account Takeover"],
            "Account Takeover": []
        },
        "node_info": {
            "Phishing Bait": {"phase": "Initial Recon", "risk": "LOW", "detail": "Attacker sends an urgent lure email or SMS."},
            "Malicious Link": {"phase": "Weaponization", "risk": "MEDIUM", "detail": "Victim is directed to an unverified external domain."},
            "Infected Attachment": {"phase": "Delivery", "risk": "HIGH", "detail": "Victim opens weaponized macro document or APK."},
            "Spoofed Login Portal": {"phase": "Deception", "risk": "HIGH", "detail": "Victim encounters cloned login interface."},
            "Keylogger Dropper": {"phase": "Exploitation", "risk": "CRITICAL", "detail": "Malware installs quietly in background."},
            "Credential Interception": {"phase": "Harvesting", "risk": "CRITICAL", "detail": "User enters username, password, and OTP."},
            "Session Token Theft": {"phase": "Privilege Hijack", "risk": "CRITICAL", "detail": "Attacker captures active browser authentication cookies."},
            "2FA Bypass Attempt": {"phase": "Defense Evasion", "risk": "CRITICAL", "detail": "Attacker triggers OTP fatigue or SIM swap."},
            "Account Takeover": {"phase": "Objective Achieved", "risk": "CRITICAL", "detail": "Full unauthorized control of target assets."}
        }
    },
    "ransomware": {
        "title": "Ransomware Kill Chain",
        "start": "Exploit Vector",
        "target": "Extortion & Data Loss",
        "graph": {
            "Exploit Vector": ["Phishing Payload", "RDP Brute-Force"],
            "Phishing Payload": ["Script Execution"],
            "RDP Brute-Force": ["Credential Escalation"],
            "Script Execution": ["Lateral Movement"],
            "Credential Escalation": ["Lateral Movement"],
            "Lateral Movement": ["Shadow Copy Deletion"],
            "Shadow Copy Deletion": ["AES File Encryption"],
            "AES File Encryption": ["Extortion & Data Loss"],
            "Extortion & Data Loss": []
        },
        "node_info": {
            "Exploit Vector": {"phase": "Initial Access", "risk": "MEDIUM", "detail": "Attacker exploits exposed port or user action."},
            "Phishing Payload": {"phase": "Delivery", "risk": "HIGH", "detail": "Victim clicks download on malicious executable."},
            "RDP Brute-Force": {"phase": "Access Attempt", "risk": "HIGH", "detail": "Attacker automates credential guessing on port 3389."},
            "Script Execution": {"phase": "Execution", "risk": "HIGH", "detail": "PowerShell script initiates stealth payload download."},
            "Credential Escalation": {"phase": "Privilege Escalation", "risk": "CRITICAL", "detail": "Attacker dumps local SAM hashes to gain Admin."},
            "Lateral Movement": {"phase": "Internal Spread", "risk": "CRITICAL", "detail": "Ransomware discovers network shares and adjacent PCs."},
            "Shadow Copy Deletion": {"phase": "Defense Neutralization", "risk": "CRITICAL", "detail": "Attacker runs 'vssadmin delete shadows' to prevent easy restore."},
            "AES File Encryption": {"phase": "Impact", "risk": "CRITICAL", "detail": "Files encrypted with 256-bit key; ransom notes dropped."},
            "Extortion & Data Loss": {"phase": "Impact", "risk": "CRITICAL", "detail": "Cryptocurrency ransom demanded under threat of data leak."}
        }
    },
    "upi": {
        "title": "UPI Digital Payment Trap",
        "start": "Marketplace Social Engineering",
        "target": "Financial Debit",
        "graph": {
            "Marketplace Social Engineering": ["Fake Advance Payment Promise"],
            "Fake Advance Payment Promise": ["Spoofed Collect Request", "Fraudulent QR Code"],
            "Spoofed Collect Request": ["Prompt to Enter UPI PIN"],
            "Fraudulent QR Code": ["Prompt to Enter UPI PIN"],
            "Prompt to Enter UPI PIN": ["Victim Authorizes Transaction"],
            "Victim Authorizes Transaction": ["Financial Debit"],
            "Financial Debit": []
        },
        "node_info": {
            "Marketplace Social Engineering": {"phase": "Lure", "risk": "LOW", "detail": "Scammer poses as eager buyer on OLX/marketplace."},
            "Fake Advance Payment Promise": {"phase": "Trust Building", "risk": "MEDIUM", "detail": "Fraudster claims money is ready to be credited."},
            "Spoofed Collect Request": {"phase": "Interface Abuse", "risk": "HIGH", "detail": "Sends a 'Pay' request labeled 'Refund' or 'Receive'."},
            "Fraudulent QR Code": {"phase": "Trickery", "risk": "HIGH", "detail": "Sends merchant QR code claiming scanning it deposits cash."},
            "Prompt to Enter UPI PIN": {"phase": "Deception Trap", "risk": "CRITICAL", "detail": "Victim believes PIN confirms receipt rather than payment."},
            "Victim Authorizes Transaction": {"phase": "Human Error", "risk": "CRITICAL", "detail": "Victim enters secret PIN into banking app."},
            "Financial Debit": {"phase": "Impact", "risk": "CRITICAL", "detail": "Funds instantly transferred to untraceable mule accounts."}
        }
    }
}


def bfs_attack_path(scenario="phishing"):
    scenario_data = SCENARIO_GRAPHS.get(scenario, SCENARIO_GRAPHS["phishing"])
    graph = scenario_data["graph"]
    start = scenario_data["start"]
    target = scenario_data["target"]
    node_info = scenario_data["node_info"]

    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == target:
            steps = []
            for n in path:
                info = node_info.get(n, {})
                steps.append({
                    "name": n,
                    "phase": info.get("phase", "Attack Phase"),
                    "risk": info.get("risk", "MEDIUM"),
                    "detail": info.get("detail", "")
                })
            return {
                "title": scenario_data["title"],
                "algorithm": "Breadth-First Search (BFS)",
                "explanation": "BFS explores the attack space layer-by-layer to discover the shortest path from initial compromise to target impact.",
                "path_names": path,
                "steps": steps
            }

        if node not in visited:
            visited.add(node)
            for neighbour in graph.get(node, []):
                queue.append(path + [neighbour])

    return None


def dfs_attack_path(scenario="phishing"):
    scenario_data = SCENARIO_GRAPHS.get(scenario, SCENARIO_GRAPHS["phishing"])
    graph = scenario_data["graph"]
    start = scenario_data["start"]
    target = scenario_data["target"]
    node_info = scenario_data["node_info"]

    stack = [[start]]
    visited = set()

    while stack:
        path = stack.pop()
        node = path[-1]

        if node == target:
            steps = []
            for n in path:
                info = node_info.get(n, {})
                steps.append({
                    "name": n,
                    "phase": info.get("phase", "Attack Phase"),
                    "risk": info.get("risk", "MEDIUM"),
                    "detail": info.get("detail", "")
                })
            return {
                "title": scenario_data["title"],
                "algorithm": "Depth-First Search (DFS)",
                "explanation": "DFS explores a single attack vector deeply to its ultimate impact before backtracking to alternative exploitation vectors.",
                "path_names": path,
                "steps": steps
            }

        if node not in visited:
            visited.add(node)
            for neighbour in graph.get(node, []):
                stack.append(path + [neighbour])

    return None