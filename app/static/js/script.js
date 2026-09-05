/* =========================================================
   SCAMSHIELD AI — CYBER DEFENSE CLIENT LOGIC & UI ENGINE
   ========================================================= */

// --- AUDIO SYNTHESIZER (Native Web Audio API) ---
class CyberAudioEngine {
    constructor() {
        this.ctx = null;
        this.enabled = localStorage.getItem("scamshield_audio") !== "false";
    }

    init() {
        if (!this.ctx && typeof AudioContext !== "undefined") {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioCtx();
        }
        if (this.ctx && this.ctx.state === "suspended") {
            this.ctx.resume();
        }
    }

    play(type = "click") {
        if (!this.enabled) return;
        try {
            this.init();
            if (!this.ctx) return;

            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.connect(gain);
            gain.connect(this.ctx.destination);

            if (type === "click") {
                osc.type = "sine";
                osc.frequency.setValueAtTime(800, now);
                osc.frequency.exponentialRampToValueAtTime(1400, now + 0.05);
                gain.gain.setValueAtTime(0.08, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
                osc.start(now);
                osc.stop(now + 0.05);
            } 
            else if (type === "scan") {
                osc.type = "triangle";
                osc.frequency.setValueAtTime(320, now);
                osc.frequency.exponentialRampToValueAtTime(980, now + 0.22);
                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
                osc.start(now);
                osc.stop(now + 0.22);
            } 
            else if (type === "alert") {
                osc.type = "sawtooth";
                osc.frequency.setValueAtTime(350, now);
                osc.frequency.setValueAtTime(240, now + 0.1);
                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
                osc.start(now);
                osc.stop(now + 0.25);
            } 
            else if (type === "success") {
                osc.type = "sine";
                osc.frequency.setValueAtTime(523.25, now); // C5
                osc.frequency.setValueAtTime(659.25, now + 0.08); // E5
                osc.frequency.setValueAtTime(783.99, now + 0.16); // G5
                gain.gain.setValueAtTime(0.1, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
                osc.start(now);
                osc.stop(now + 0.35);
            }
        } catch (e) {
            // Audio context not allowed before gesture
        }
    }
}

const audioEngine = new CyberAudioEngine();


// =========================================================
// THEME & AUDIO TOGGLE CONTROLLERS
// =========================================================

function initTheme() {
    const savedTheme = localStorage.getItem("scamshield_theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);
    updateThemeButtonUI(savedTheme);
    updateAudioButtonUI();
}

function toggleTheme() {
    audioEngine.play("click");
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("scamshield_theme", next);
    updateThemeButtonUI(next);
}

function updateThemeButtonUI(theme) {
    const icon = document.getElementById("themeIcon");
    const text = document.getElementById("themeText");
    if (icon && text) {
        if (theme === "dark") {
            icon.textContent = "☀️";
            text.textContent = "Light";
        } else {
            icon.textContent = "🌙";
            text.textContent = "Dark";
        }
    }
}

function toggleSound() {
    audioEngine.enabled = !audioEngine.enabled;
    localStorage.setItem("scamshield_audio", audioEngine.enabled);
    updateAudioButtonUI();
    if (audioEngine.enabled) {
        audioEngine.play("success");
    }
}

function updateAudioButtonUI() {
    const soundIcon = document.getElementById("soundIcon");
    if (soundIcon) {
        soundIcon.textContent = audioEngine.enabled ? "🔊" : "🔇";
    }
}

function toggleSidebar() {
    audioEngine.play("click");
    const sidebar = document.getElementById("sidebar");
    if (sidebar) {
        sidebar.classList.toggle("open");
    }
}


// =========================================================
// INPUT HANDLING & QUICK ACTIONS
// =========================================================

function autoExpand(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = Math.min(textarea.scrollHeight, 140) + "px";
}

function handleKey(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        analyzeMessage();
    }
}

function useSample(element) {
    audioEngine.play("click");
    const snippet = element.querySelector(".vector-snippet").innerText.replace(/^"|"$/g, "").trim();
    const input = document.getElementById("message");
    input.value = snippet;
    autoExpand(input);
    input.focus();
}

function injectPrompt(promptText) {
    audioEngine.play("click");
    const input = document.getElementById("message");
    input.value = promptText;
    analyzeMessage();
}

function triggerQuickAction(action) {
    audioEngine.play("click");
    const sidebar = document.getElementById("sidebar");
    if (sidebar && sidebar.classList.contains("open")) {
        sidebar.classList.remove("open");
    }

    if (action === "scan") {
        injectPrompt("How does ScamShield analyze messages and detect phishing links?");
    } else if (action === "password") {
        injectPrompt("Check my password: CyberShield#2026!");
    } else if (action === "quiz") {
        injectPrompt("Start a scam quiz challenge");
    } else if (action === "graph") {
        injectPrompt("Simulate phishing attack progression with BFS");
    } else if (action === "helpline") {
        injectPrompt("What are the official cybercrime helpline numbers?");
    } else if (action === "sql_stats") {
        injectPrompt("Show live SQL database threat statistics");
    }
}

async function fetchTelemetry() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();
        const scansEl = document.getElementById("teleTotalScans");
        const highEl = document.getElementById("teleHighThreats");
        const avgEl = document.getElementById("teleAvgScore");
        if (scansEl) scansEl.textContent = data.total_scans;
        if (highEl) highEl.textContent = data.high_threats;
        if (avgEl) avgEl.textContent = data.avg_risk_score + "/100";
    } catch (e) {
        console.warn("Could not sync SQL telemetry:", e);
    }
}

function fetchAndDisplayDbStats() {
    audioEngine.play("click");
    injectPrompt("Show live SQL database threat statistics");
}

function useCyberTopic(topic) {
    audioEngine.play("click");
    injectPrompt("Explain " + topic + " and how to stay protected");
}

function clearConversation() {
    audioEngine.play("click");
    location.reload();
}

function scrollBottom() {
    const chat = document.getElementById("chat");
    if (chat) {
        setTimeout(() => {
            chat.scrollTop = chat.scrollHeight;
        }, 50);
    }
}


// =========================================================
// MESSAGE DISPATCH & API CONSUMPTION
// =========================================================

async function analyzeMessage() {
    const input = document.getElementById("message");
    const message = input.value.trim();
    if (!message) return;

    audioEngine.play("scan");

    // Hide initial welcome deck
    const welcome = document.getElementById("welcome");
    if (welcome) welcome.remove();

    // Append User Bubble
    addUserMessage(message);

    // Reset input
    input.value = "";
    input.style.height = "auto";

    // Append Typing Bubble
    const typingId = addTypingIndicator();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const result = await response.json();
        removeTypingIndicator(typingId);

        if (result.error) {
            audioEngine.play("alert");
            addAIMessage(result.error);
            return;
        }

        handleResponsePayload(result);

    } catch (error) {
        removeTypingIndicator(typingId);
        console.error("Network / Server Error:", error);
        audioEngine.play("alert");
        addAIMessage("⚠️ Unable to connect to ScamShield AI Defense Engine. Please verify server status.");
    }
}


// =========================================================
// RESPONSE PAYLOAD ROUTER
// =========================================================

function handleResponsePayload(result) {
    const type = result.type;
    const data = result.data || {};

    if (type === "scam_analysis") {
        if (data.risk === "HIGH") audioEngine.play("alert");
        else audioEngine.play("success");
        renderScamResult(data);
        fetchTelemetry();
    } 
    else if (type === "password_strength") {
        audioEngine.play("success");
        renderPasswordResult(data, result.password_tested);
    } 
    else if (type === "attack_path") {
        audioEngine.play("success");
        renderAttackPathResult(data);
    } 
    else if (type === "quiz") {
        audioEngine.play("click");
        renderQuizChallenge(data);
    } 
    else if (type === "quiz_result") {
        if (data.is_correct) audioEngine.play("success");
        else audioEngine.play("alert");
        renderQuizEvaluation(data);
        fetchTelemetry();
    } 
    else if (type === "cybersecurity") {
        audioEngine.play("success");
        renderCybersecurityResult(data);
    } 
    else if (type === "helpline") {
        audioEngine.play("alert");
        renderHelplineResult(data);
    } 
    else if (type === "db_stats") {
        audioEngine.play("success");
        renderDbStatsCard(data);
        fetchTelemetry();
    }
    else if (type === "bot_intro") {
        audioEngine.play("success");
        renderBotIntro(data);
    } 
    else {
        addAIMessage(result.message || "Threat analysis completed.");
    }
}


// =========================================================
// DOM BUILDERS: MESSAGES & CARDS
// =========================================================

function addUserMessage(text) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";
    row.innerHTML = `
        <div class="message-wrapper" style="justify-content: flex-end;">
            <div class="user-text-bubble">
                ${escapeHTML(text)}
            </div>
            <div class="message-avatar user">👤</div>
        </div>
    `;
    chat.appendChild(row);
    scrollBottom();
}

function addAIMessage(text) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";
    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai">🛡️</div>
            <div class="message-content">
                <div class="message-sender">SCAMSHIELD INTEL</div>
                <div class="ai-text-bubble">${escapeHTML(text)}</div>
            </div>
        </div>
    `;
    chat.appendChild(row);
    scrollBottom();
}

function addTypingIndicator() {
    const chat = document.getElementById("chat");
    const id = "typing-" + Date.now();
    const row = document.createElement("div");
    row.id = id;
    row.className = "message-row";
    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai">🛡️</div>
            <div class="message-content">
                <div class="typing-cluster">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>
        </div>
    `;
    chat.appendChild(row);
    scrollBottom();
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}


// =========================================================
// 1. RENDER SCAM ANALYSIS
// =========================================================

function renderScamResult(data) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";

    const riskClass = (data.risk || "low").toLowerCase();
    const score = Math.max(0, Math.min(100, data.risk_score || 0));

    // Calculate SVG circular stroke
    const radius = 54;
    const circumference = 2 * Math.PI * radius; // ~339.29
    const offset = circumference - (score / 100) * circumference;

    let strokeColor = "var(--emerald)";
    if (riskClass === "high") strokeColor = "var(--rose)";
    else if (riskClass === "medium") strokeColor = "var(--amber)";

    // Suspicious words / Red Flags
    let redFlagsHtml = "";
    if (data.red_flags && data.red_flags.length > 0) {
        redFlagsHtml = data.red_flags.map(rf => `
            <div class="threat-tag ${rf.severity ? rf.severity.toLowerCase() : 'medium'}">
                <span>⚠️</span>
                <strong>${escapeHTML(rf.title)}:</strong>
                <span>${escapeHTML(rf.description)}</span>
            </div>
        `).join("");
    } else {
        redFlagsHtml = `
            <div class="threat-tag safe">
                <span>✓</span>
                <span>No high-severity linguistic threat patterns detected.</span>
            </div>
        `;
    }

    // URL & Link Inspection
    let urlHtml = "";
    const urls = (data.url_findings && data.url_findings.urls) || [];
    const urlIssues = (data.url_findings && data.url_findings.suspicious_indicators) || [];
    if (urls.length > 0) {
        urlHtml = `
            <div class="section-block">
                <div class="section-block-title">
                    <span>🔗</span> EXTRACTED URL HEURISTICS (${urls.length})
                </div>
                <div style="font-family:var(--font-mono);font-size:12px;margin-bottom:8px;">
                    ${urls.map(u => `<div style="color:var(--cyan);word-break:break-all;">• ${escapeHTML(u)}</div>`).join("")}
                </div>
                ${urlIssues.length > 0 ? `
                    <div style="display:flex;flex-direction:column;gap:5px;margin-top:6px;">
                        ${urlIssues.map(iss => `<div class="threat-tag critical" style="display:flex;"><span>🚨</span> ${escapeHTML(iss)}</div>`).join("")}
                    </div>
                ` : `<div style="font-size:11px;color:var(--emerald);">✓ Domain syntax conforms to standard naming structures.</div>`}
            </div>
        `;
    }

    // Checklist of actions
    const steps = data.safety_steps || [
        "Never share OTPs, passwords or bank account details.",
        "Verify sender identity through official verified sources."
    ];

    const checklistHtml = steps.map((step, idx) => `
        <div class="action-check-item" onclick="toggleCheckItem(this)">
            <div class="action-check-box">✓</div>
            <span>${escapeHTML(step)}</span>
        </div>
    `).join("");

    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai">🛡️</div>
            <div class="message-content">
                <div class="message-sender">SCAMSHIELD THREAT REPORT</div>
                <div class="card-scam">
                    <div class="card-top">
                        <div class="card-heading">
                            <div class="card-badge-icon">🔍</div>
                            <div>
                                <h4>Deep Threat Scan Result</h4>
                                <span>Multi-Layer ML & Heuristics Breakdown</span>
                            </div>
                        </div>
                        <div class="risk-pill ${riskClass}">
                            ${escapeHTML(data.risk)} RISK
                        </div>
                    </div>

                    <div class="card-body">
                        <div class="scam-dashboard-grid">
                            <!-- Circular Gauge -->
                            <div class="gauge-box">
                                <div style="position:relative; display:grid; place-items:center;">
                                    <svg class="svg-gauge" viewBox="0 0 140 140">
                                        <circle class="gauge-bg" cx="70" cy="70" r="${radius}"></circle>
                                        <circle class="gauge-fill" cx="70" cy="70" r="${radius}" 
                                            stroke="${strokeColor}"
                                            stroke-dasharray="${circumference}"
                                            stroke-dashoffset="${circumference}"
                                            id="gauge-fill-${row.id || Math.random().toString(36).substring(7)}"
                                        ></circle>
                                    </svg>
                                    <div class="gauge-text-wrap">
                                        <span class="gauge-score" style="color:${strokeColor}">${score}</span>
                                        <span class="gauge-sub">RISK INDEX</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Stat Tiles -->
                            <div>
                                <div class="stats-deck">
                                    <div class="stat-tile">
                                        <div class="stat-tile-label">Detected Category</div>
                                        <div class="stat-tile-val text-cyan">${escapeHTML(data.category)}</div>
                                    </div>
                                    <div class="stat-tile">
                                        <div class="stat-tile-label">Threat Severity</div>
                                        <div class="stat-tile-val" style="color:${strokeColor}">${escapeHTML(data.risk)}</div>
                                    </div>
                                </div>

                                <div class="confidence-module">
                                    <div class="confidence-labels">
                                        <span>AI Model Confidence</span>
                                        <strong>${data.confidence}%</strong>
                                    </div>
                                    <div class="confidence-bar-track">
                                        <div class="confidence-bar-fill" style="width:${data.confidence}%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        ${urlHtml}

                        <div class="section-block">
                            <div class="section-block-title">
                                <span>⚡</span> RED FLAGS & THREAT INDICATORS
                            </div>
                            <div class="tags-cluster">
                                ${redFlagsHtml}
                            </div>
                        </div>

                        <div class="section-block">
                            <div class="section-block-title">
                                <span>🛡️</span> RECOMMENDED DEFENSIVE PROTOCOL
                            </div>
                            <div class="action-checklist">
                                ${checklistHtml}
                            </div>
                        </div>

                        <div class="card-action-bar">
                            <button class="card-btn" onclick="copyReport(this)">
                                <span>📋</span> Copy Report
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    chat.appendChild(row);

    // Animate Gauge filling
    const gaugeEl = row.querySelector(".gauge-fill");
    if (gaugeEl) {
        setTimeout(() => {
            gaugeEl.style.strokeDashoffset = offset;
        }, 100);
    }

    scrollBottom();
}

function toggleCheckItem(el) {
    audioEngine.play("click");
    el.classList.toggle("checked");
}

function copyReport(btn) {
    audioEngine.play("success");
    const original = btn.innerHTML;
    navigator.clipboard.writeText("ScamShield Threat Analysis:\n" + btn.closest(".card-scam").innerText);
    btn.innerHTML = "<span>✓</span> Copied!";
    setTimeout(() => { btn.innerHTML = original; }, 2000);
}


// =========================================================
// 2. RENDER PASSWORD STRENGTH LAB
// =========================================================

function renderPasswordResult(data, masked) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";

    const score = data.score || 0;
    const strength = data.strength || "Weak";

    // 5 segments
    let segs = ["", "", "", "", ""];
    let segClass = "active-rose";
    if (score >= 90) segClass = "active-emerald";
    else if (score >= 70) segClass = "active-cyan";
    else if (score >= 45) segClass = "active-amber";

    const count = Math.min(5, Math.ceil((score / 100) * 5));
    for (let i = 0; i < count; i++) {
        segs[i] = segClass;
    }

    const checklistHtml = (data.checklist || []).map(item => `
        <div class="pwd-check-item">
            <span class="pwd-check-icon ${item.passed ? 'pass' : 'fail'}">
                ${item.passed ? '✓' : '✗'}
            </span>
            <span>${escapeHTML(item.label)}</span>
        </div>
    `).join("");

    const suggestionsHtml = (data.suggestions || []).map(sug => `
        <li style="margin-bottom:6px; color:var(--text-secondary);">${escapeHTML(sug)}</li>
    `).join("");

    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai">🔐</div>
            <div class="message-content">
                <div class="message-sender">PASSWORD ENTROPY LAB</div>
                <div class="card-scam">
                    <div class="card-top">
                        <div class="card-heading">
                            <div class="card-badge-icon">🔑</div>
                            <div>
                                <h4>Credential Resilience Analysis</h4>
                                <span>GPU Offline Brute-Force Estimation</span>
                            </div>
                        </div>
                        <div class="risk-pill ${score >= 75 ? 'low' : score >= 45 ? 'medium' : 'high'}">
                            ${escapeHTML(strength.toUpperCase())}
                        </div>
                    </div>

                    <div class="card-body">
                        <!-- Crack time banner -->
                        <div class="crack-time-hero">
                            <div>
                                <div class="crack-time-label">ESTIMATED TIME TO CRACK</div>
                                <div class="crack-time-val">${escapeHTML(data.crack_time)}</div>
                            </div>
                            <div style="text-align:right;">
                                <div class="crack-time-label">SHANNON ENTROPY</div>
                                <div style="font-size:18px;font-weight:800;font-family:var(--font-mono);">${data.entropy} BITS</div>
                            </div>
                        </div>

                        <!-- Segmented meter -->
                        <div class="password-meter-wrap">
                            ${segs.map(cls => `<div class="meter-seg ${cls}"></div>`).join("")}
                        </div>

                        <div class="section-block">
                            <div class="section-block-title">
                                <span>🛡️</span> COMPLEXITY & ENTROPY AUDIT
                            </div>
                            <div class="pwd-checklist-grid">
                                ${checklistHtml}
                            </div>
                        </div>

                        ${data.suggestions && data.suggestions.length > 0 ? `
                            <div class="section-block">
                                <div class="section-block-title">
                                    <span>💡</span> HARDENING RECOMMENDATIONS
                                </div>
                                <ul style="padding-left:18px; font-size:13px; line-height:1.6;">
                                    ${suggestionsHtml}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        </div>
    `;

    chat.appendChild(row);
    scrollBottom();
}


// =========================================================
// 3. RENDER ATTACK GRAPH & A* SIMULATION
// =========================================================

function renderAttackPathResult(data) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";

    const steps = data.steps || [];
    const timelineHtml = steps.map((st, idx) => {
        const isCritical = st.risk === "CRITICAL" || idx === steps.length - 1;
        return `
            <div class="timeline-step-node">
                <div class="node-bullet ${isCritical ? 'critical' : ''}">
                    0${idx + 1}
                </div>
                <div class="node-card">
                    <div class="node-top">
                        <strong class="node-title">${escapeHTML(st.name)}</strong>
                        <span class="node-phase-tag">${escapeHTML(st.phase)}</span>
                    </div>
                    <p class="node-desc">${escapeHTML(st.detail)}</p>
                </div>
            </div>
        `;
    }).join("");

    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai">🧭</div>
            <div class="message-content">
                <div class="message-sender">CYBER GRAPH INTELLIGENCE</div>
                <div class="card-scam">
                    <div class="card-top">
                        <div class="card-heading">
                            <div class="card-badge-icon">🕸️</div>
                            <div>
                                <h4>${escapeHTML(data.title)}</h4>
                                <span>${escapeHTML(data.algorithm)}</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-body">
                        <p style="font-size:13px;color:var(--text-secondary);line-height:1.6;margin-bottom:20px;">
                            ${escapeHTML(data.explanation)}
                        </p>

                        <div class="attack-timeline">
                            ${timelineHtml}
                        </div>

                        <div class="card-action-bar" style="justify-content:flex-start; margin-top:20px;">
                            <button class="card-btn" onclick="injectPrompt('Simulate Phishing with BFS')">BFS Phishing</button>
                            <button class="card-btn" onclick="injectPrompt('Simulate Ransomware with DFS')">DFS Ransomware</button>
                            <button class="card-btn" onclick="injectPrompt('Find lowest cost mitigation with A*')">A* Safe Path</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    chat.appendChild(row);
    scrollBottom();
}


// =========================================================
// 4. RENDER CYBER DEFENSE QUIZ
// =========================================================

function renderQuizChallenge(quiz) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";

    const optionsHtml = (quiz.options || []).map(opt => `
        <button class="quiz-opt-btn" onclick="submitQuizOption('${quiz.id}', '${opt.id}', this)">
            <span class="quiz-opt-letter">${opt.id}</span>
            <span>${escapeHTML(opt.text)}</span>
        </button>
    `).join("");

    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai">🎯</div>
            <div class="message-content">
                <div class="message-sender">SCAMSHIELD DEFENSE QUIZ</div>
                <div class="quiz-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <h4 style="font-size:16px;font-weight:800;">${escapeHTML(quiz.title)}</h4>
                        <span class="nav-badge hot">${escapeHTML(quiz.difficulty || "Medium")}</span>
                    </div>

                    <div class="quiz-scenario-box">
                        ${escapeHTML(quiz.message)}
                    </div>

                    <div class="quiz-options-deck">
                        ${optionsHtml}
                    </div>
                </div>
            </div>
        </div>
    `;

    chat.appendChild(row);
    scrollBottom();
}

async function submitQuizOption(quizId, optionId, btn) {
    audioEngine.play("click");
    const parent = btn.closest(".quiz-card");

    // Disable all option buttons in this card
    parent.querySelectorAll(".quiz-opt-btn").forEach(b => {
        b.disabled = true;
        b.style.opacity = "0.7";
    });

    const typingId = addTypingIndicator();

    try {
        const response = await fetch("/quiz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ quiz_id: quizId, option: optionId })
        });

        const result = await response.json();
        removeTypingIndicator(typingId);
        renderQuizEvaluation(result, parent);

    } catch (e) {
        removeTypingIndicator(typingId);
        console.error("Quiz submission error:", e);
    }
}

function renderQuizEvaluation(result, targetCard = null) {
    const feedbackBox = document.createElement("div");
    feedbackBox.className = `quiz-feedback-box ${result.is_correct ? 'correct' : 'incorrect'}`;

    feedbackBox.innerHTML = `
        <div class="quiz-feedback-head">
            <span>${result.is_correct ? '✅ SPOT ON! EXCELLENT INSTINCTS' : '🚨 CAUTION! YOU TOOK THE BAIT'}</span>
        </div>
        <div class="quiz-feedback-body">
            ${escapeHTML(result.explanation)}
        </div>
        <div style="margin-top:14px; display:flex; justify-content:flex-end;">
            <button class="card-btn" onclick="injectPrompt('Next quiz challenge')">
                <span>➔</span> Next Question
            </button>
        </div>
    `;

    if (targetCard) {
        targetCard.appendChild(feedbackBox);
    } else {
        const chat = document.getElementById("chat");
        const row = document.createElement("div");
        row.className = "message-row";
        row.innerHTML = `
            <div class="message-wrapper">
                <div class="message-avatar ai">🎯</div>
                <div class="message-content">
                    <div class="quiz-card">
                        ${feedbackBox.outerHTML}
                    </div>
                </div>
            </div>
        `;
        chat.appendChild(row);
    }

    if (result.is_correct) audioEngine.play("success");
    else audioEngine.play("alert");

    scrollBottom();
}


// =========================================================
// 5. RENDER CYBERSECURITY TOPIC & HELPLINE
// =========================================================

function renderCybersecurityResult(data) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";

    const signsHtml = (data.signs || []).map(s => `
        <li style="margin-bottom:6px; color:var(--text-secondary);">${escapeHTML(s)}</li>
    `).join("");

    const protectionHtml = (data.protection || []).map(p => `
        <li style="margin-bottom:6px; color:var(--text-secondary);">${escapeHTML(p)}</li>
    `).join("");

    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai">📚</div>
            <div class="message-content">
                <div class="message-sender">CYBER KNOWLEDGE VAULT</div>
                <div class="card-scam">
                    <div class="card-top">
                        <div class="card-heading">
                            <div class="card-badge-icon">📖</div>
                            <div>
                                <h4>${escapeHTML(data.topic)}</h4>
                                <span>${escapeHTML(data.badge || "Cybersecurity Threat Overview")}</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-body">
                        <p style="font-size:14px; line-height:1.7; margin-bottom:18px;">
                            ${escapeHTML(data.description)}
                        </p>

                        ${data.example ? `
                            <div class="quiz-scenario-box" style="border-left-color:var(--cyan); margin-bottom:18px;">
                                <strong style="color:var(--cyan); display:block; margin-bottom:4px;">REAL-WORLD ATTACK EXAMPLE:</strong>
                                ${escapeHTML(data.example)}
                            </div>
                        ` : ''}

                        <div class="section-block">
                            <div class="section-block-title">
                                <span>⚠️</span> TELLTALE WARNING SIGNS
                            </div>
                            <ul style="padding-left:18px; font-size:13px; line-height:1.6;">
                                ${signsHtml}
                            </ul>
                        </div>

                        <div class="section-block">
                            <div class="section-block-title">
                                <span>🛡️</span> HOW TO STAY IMMUNIZED
                            </div>
                            <ul style="padding-left:18px; font-size:13px; line-height:1.6;">
                                ${protectionHtml}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    chat.appendChild(row);
    scrollBottom();
}

function renderHelplineResult(data) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";

    const helplines = data.helplines || [];
    const directoryHtml = helplines.map(h => `
        <div class="stat-tile" style="margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between;">
                <strong>${escapeHTML(h.country)}</strong>
                <span class="risk-pill high" style="padding:3px 8px; font-size:10px;">${escapeHTML(h.contact)}</span>
            </div>
            <div style="font-size:12px; color:var(--text-secondary); margin:4px 0;">${escapeHTML(h.service)}</div>
            <div style="font-size:11px; font-family:var(--font-mono); color:var(--cyan);">${escapeHTML(h.portal)}</div>
        </div>
    `).join("");

    const actionsHtml = (data.immediate_actions || []).map(a => `
        <li style="margin-bottom:6px; color:var(--text-secondary);">${escapeHTML(a)}</li>
    `).join("");

    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai" style="background:linear-gradient(135deg,var(--rose),var(--amber));">🚨</div>
            <div class="message-content">
                <div class="message-sender">EMERGENCY PROTOCOL</div>
                <div class="card-scam" style="border-color:rgba(244,63,94,0.35);">
                    <div class="card-top" style="background:rgba(244,63,94,0.12);">
                        <div class="card-heading">
                            <div class="card-badge-icon" style="background:rgba(244,63,94,0.2); border-color:var(--rose);">🚨</div>
                            <div>
                                <h4 style="color:var(--rose);">CRITICAL: Cyber Fraud Response</h4>
                                <span>Immediate Damage Mitigation Guide</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-body">
                        <div style="padding:14px 18px; border-radius:12px; background:rgba(244,63,94,0.15); border:1px solid rgba(244,63,94,0.3); font-size:13px; color:var(--rose); font-weight:700; margin-bottom:18px;">
                            ${escapeHTML(data.golden_hour_note)}
                        </div>

                        <div class="section-block" style="border-top:none; padding-top:0;">
                            <div class="section-block-title">
                                <span>📞</span> OFFICIAL CYBERCRIME HELPLINE DIRECTORY
                            </div>
                            ${directoryHtml}
                        </div>

                        <div class="section-block">
                            <div class="section-block-title">
                                <span>⚡</span> IMMEDIATE CONTAINMENT PLAYBOOK
                            </div>
                            <ol style="padding-left:20px; font-size:13px; line-height:1.7;">
                                ${actionsHtml}
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    chat.appendChild(row);
    scrollBottom();
}

function renderBotIntro(data) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";

    const capabilitiesHtml = (data.capabilities || []).map(cap => `
        <div class="stat-tile" style="display:flex;gap:12px;align-items:flex-start;">
            <span style="font-size:22px;">${cap.icon}</span>
            <div>
                <strong style="font-size:13px;display:block;margin-bottom:3px;">${escapeHTML(cap.title)}</strong>
                <p style="font-size:12px;color:var(--text-secondary);line-height:1.5;">${escapeHTML(cap.desc)}</p>
            </div>
        </div>
    `).join("");

    const promptsHtml = (data.quick_prompts || []).map(p => `
        <button class="chip-btn" onclick="injectPrompt('${escapeHTML(p)}')">
            <span>➔</span> ${escapeHTML(p)}
        </button>
    `).join("");

    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai">🛡️</div>
            <div class="message-content">
                <div class="message-sender">SCAMSHIELD AI DEFENSE AGENT</div>
                <div class="card-scam">
                    <div class="card-top">
                        <div class="card-heading">
                            <div class="card-badge-icon">⚡</div>
                            <div>
                                <h4>${escapeHTML(data.headline)}</h4>
                                <span>Next-Gen Multi-Vector Defense Hub</span>
                            </div>
                        </div>
                    </div>

                    <div class="card-body">
                        <div style="display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:20px;">
                            ${capabilitiesHtml}
                        </div>

                        <div class="section-block">
                            <div class="section-block-title">
                                <span>🚀</span> SUGGESTED COMMANDS
                            </div>
                            <div class="tags-cluster">
                                ${promptsHtml}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    chat.appendChild(row);
    scrollBottom();
}


// =========================================================
// 6. RENDER SQL DATABASE THREAT TELEMETRY
// =========================================================

function renderDbStatsCard(data) {
    const chat = document.getElementById("chat");
    const row = document.createElement("div");
    row.className = "message-row";

    const s = data.stats || {};
    const recent = data.recent || [];

    const recentRows = recent.map((r) => `
        <tr style="border-bottom: 1px solid var(--border-subtle); font-size:12px;">
            <td style="padding:10px 8px; font-family:var(--font-mono); color:var(--text-muted); font-size:11px; white-space:nowrap;">
                ${escapeHTML(r.created_at ? r.created_at.substring(5, 16) : '')}
            </td>
            <td style="padding:10px 8px; font-weight:700; color:var(--cyan); white-space:nowrap;">
                ${escapeHTML(r.category || 'Unknown')}
            </td>
            <td style="padding:10px 8px; white-space:nowrap;">
                <span class="risk-pill ${(r.risk || 'low').toLowerCase()}" style="padding:2px 8px; font-size:9px;">
                    ${escapeHTML(r.risk || 'LOW')}
                </span>
            </td>
            <td style="padding:10px 8px; font-family:var(--font-mono); font-weight:800; color:var(--text-primary); text-align:center;">
                ${r.risk_score || 0}
            </td>
            <td style="padding:10px 8px; color:var(--text-secondary); max-width:240px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                ${escapeHTML(r.message || '')}
            </td>
        </tr>
    `).join("");

    row.innerHTML = `
        <div class="message-wrapper">
            <div class="message-avatar ai">📊</div>
            <div class="message-content">
                <div class="message-sender">SQL THREAT TELEMETRY ENGINE</div>
                <div class="card-scam">
                    <div class="card-top">
                        <div class="card-heading">
                            <div class="card-badge-icon">🗄️</div>
                            <div>
                                <h4>SQLite Security Database</h4>
                                <span>Real-Time Relational Threat Store & Aggregation</span>
                            </div>
                        </div>
                        <div class="nav-badge" style="padding:6px 12px; font-size:11px;">SQL ARMED</div>
                    </div>

                    <div class="card-body">
                        <!-- Stats Grid -->
                        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:12px; margin-bottom:20px;">
                            <div class="stat-tile">
                                <div class="stat-tile-label">Total Scans</div>
                                <div class="stat-tile-val text-cyan">${s.total_scans || 0}</div>
                            </div>
                            <div class="stat-tile">
                                <div class="stat-tile-label">High Risk Blocked</div>
                                <div class="stat-tile-val" style="color:var(--rose);">${s.high_threats || 0}</div>
                            </div>
                            <div class="stat-tile">
                                <div class="stat-tile-label">Average Risk</div>
                                <div class="stat-tile-val">${s.avg_risk_score || 0}/100</div>
                            </div>
                            <div class="stat-tile">
                                <div class="stat-tile-label">Top Threat Type</div>
                                <div class="stat-tile-val" style="color:var(--amber); font-size:13px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;">
                                    ${escapeHTML(s.top_threat_category || 'None')}
                                </div>
                            </div>
                        </div>

                        <!-- Recent SQL Log Table -->
                        <div class="section-block" style="border-top:none; padding-top:0;">
                            <div class="section-block-title">
                                <span>📜</span> RECENT VERIFIED SCANS (STORED IN SQL)
                            </div>
                            ${recent.length > 0 ? `
                                <div style="overflow-x:auto; border-radius:12px; border:1px solid var(--border-subtle); background:rgba(0,0,0,0.15);">
                                    <table style="width:100%; border-collapse:collapse; text-align:left;">
                                        <thead>
                                            <tr style="border-bottom:1px solid var(--border-subtle); font-size:10px; font-family:var(--font-mono); color:var(--text-muted); text-transform:uppercase;">
                                                <th style="padding:8px;">Date</th>
                                                <th style="padding:8px;">Category</th>
                                                <th style="padding:8px;">Risk</th>
                                                <th style="padding:8px; text-align:center;">Score</th>
                                                <th style="padding:8px;">Sample Text</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${recentRows}
                                        </tbody>
                                    </table>
                                </div>
                            ` : `<p style="font-size:12px; color:var(--text-muted);">No scan logs recorded yet. Analyze a sample message above to generate SQL records!</p>`}
                        </div>

                        <div class="card-action-bar">
                            <button class="card-btn" onclick="fetchTelemetry(); injectPrompt('Show live SQL database threat statistics');">
                                <span>🔄</span> Refresh Database Telemetry
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    chat.appendChild(row);
    scrollBottom();
}


// =========================================================
// UTILITIES
// =========================================================

function escapeHTML(str) {
    if (!str) return "";
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    fetchTelemetry();
});

