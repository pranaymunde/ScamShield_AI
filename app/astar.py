import heapq

# =========================================================
# A* SAFETY & MITIGATION GRAPH
# =========================================================

SAFETY_GRAPH = {
    "Suspicious Message Received": {
        "Inspect Header & Sender": 2,
        "Click Embedded Link": 8,
        "Immediately Forward to Colleagues": 6,
        "Isolate & Quarantine Message": 1
    },

    "Inspect Header & Sender": {
        "Verify via Official Channel": 2,
        "Reply to Sender for Clarification": 7
    },

    "Click Embedded Link": {
        "Enter Credentials on Landing Page": 10,
        "Close Browser Immediately": 3
    },

    "Immediately Forward to Colleagues": {
        "Widespread Organization Contagion": 9,
        "Colleague Flags as Scam": 4
    },

    "Isolate & Quarantine Message": {
        "Report to Cyber Defense (1930 / SecOps)": 1,
        "Delete Message Completely": 2
    },

    "Verify via Official Channel": {
        "Confirmed Fraud - Block & Report": 1,
        "Confirmed Legitimate": 1
    },

    "Close Browser Immediately": {
        "Clear Cache & Run Antivirus Scan": 2
    },

    "Clear Cache & Run Antivirus Scan": {
        "System Verified Clean & Secure": 1
    },

    "Report to Cyber Defense (1930 / SecOps)": {
        "Threat Neutralized & Account Secured": 1
    },

    "Confirmed Fraud - Block & Report": {
        "Threat Neutralized & Account Secured": 1
    },

    "Confirmed Legitimate": {
        "Safe Normal Operation": 1
    },

    "Delete Message Completely": {
        "Threat Neutralized & Account Secured": 1
    }
}

# Heuristic: Estimated risk cost remaining to reach safe secure state
HEURISTICS = {
    "Suspicious Message Received": 3,
    "Inspect Header & Sender": 2,
    "Click Embedded Link": 9,
    "Immediately Forward to Colleagues": 8,
    "Isolate & Quarantine Message": 1,
    "Verify via Official Channel": 1,
    "Reply to Sender for Clarification": 7,
    "Enter Credentials on Landing Page": 15,
    "Close Browser Immediately": 3,
    "Widespread Organization Contagion": 12,
    "Colleague Flags as Scam": 4,
    "Report to Cyber Defense (1930 / SecOps)": 0,
    "Confirmed Fraud - Block & Report": 0,
    "Confirmed Legitimate": 0,
    "Delete Message Completely": 0,
    "Clear Cache & Run Antivirus Scan": 1,
    "System Verified Clean & Secure": 0,
    "Threat Neutralized & Account Secured": 0,
    "Safe Normal Operation": 0
}

TARGET_GOALS = {
    "Threat Neutralized & Account Secured",
    "System Verified Clean & Secure",
    "Safe Normal Operation"
}

NODE_METADATA = {
    "Suspicious Message Received": {
        "type": "Triage",
        "action": "Pause and do not interact immediately with any links or attachments."
    },
    "Isolate & Quarantine Message": {
        "type": "Defensive Action",
        "action": "Prevent accidental execution or propagation across devices."
    },
    "Inspect Header & Sender": {
        "type": "Investigation",
        "action": "Inspect true sender domain, DKIM/SPF signatures, and URL structures."
    },
    "Verify via Official Channel": {
        "type": "Verification",
        "action": "Contact the institution using public directory numbers, never contact details from the message."
    },
    "Confirmed Fraud - Block & Report": {
        "type": "Neutralization",
        "action": "Block caller/sender and report incident to cybercrime helpline (1930) or SecOps."
    },
    "Report to Cyber Defense (1930 / SecOps)": {
        "type": "Reporting",
        "action": "Submit full headers and URL artifacts to law enforcement or IT security teams."
    },
    "Threat Neutralized & Account Secured": {
        "type": "Secure State",
        "action": "Incident closed. Zero credential leakage or financial compromise."
    },
    "System Verified Clean & Secure": {
        "type": "Secure State",
        "action": "Endpoint sanitized; local files and credentials remain protected."
    },
    "Safe Normal Operation": {
        "type": "Secure State",
        "action": "Message verified genuine; standard workflow resumed."
    }
}


def astar_defense_path(start="Suspicious Message Received"):
    """
    Executes A* search to calculate the lowest-cost, most resilient safety mitigation path.
    """
    # Priority queue stores: (f_score, g_score, current_node, path)
    initial_h = HEURISTICS.get(start, 5)
    pq = [(initial_h, 0, start, [start])]
    visited = {}

    while pq:
        f, g, current, path = heapq.heappop(pq)

        if current in TARGET_GOALS:
            steps = []
            for node in path:
                meta = NODE_METADATA.get(node, {
                    "type": "Mitigation Step",
                    "action": "Execute standard cybersecurity countermeasure."
                })
                steps.append({
                    "name": node,
                    "phase": meta["type"],
                    "risk": "LOW" if node in TARGET_GOALS else "MEDIUM",
                    "detail": meta["action"]
                })
            return {
                "title": "A* Optimal Defense & Mitigation Path",
                "algorithm": "A* Pathfinding (Heuristic Defense)",
                "total_cost": g,
                "explanation": "A* evaluates step risk costs and forward safety heuristics to compute the lowest-risk remediation route.",
                "path_names": path,
                "steps": steps
            }

        if current in visited and visited[current] <= g:
            continue
        visited[current] = g

        for neighbour, edge_cost in SAFETY_GRAPH.get(current, {}).items():
            new_g = g + edge_cost
            h = HEURISTICS.get(neighbour, 5)
            new_f = new_g + h
            heapq.heappush(pq, (new_f, new_g, neighbour, path + [neighbour]))

    return None


# Backward compatibility
def astar(start="Suspicious Message", goal="Safe"):
    result = astar_defense_path()
    if result:
        return result["path_names"]
    return ["Suspicious Message", "Verify Sender", "Report Message", "Safe"]