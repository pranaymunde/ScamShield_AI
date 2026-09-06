/* =========================================================
   SCAMSHIELD AI — CYBER DEFENSE CLIENT LOGIC & UI ENGINE
   ========================================================= */

// =========================================================
// AUDIO SYNTHESIZER
// =========================================================

class CyberAudioEngine {
    constructor() {
        this.ctx = null;
        this.enabled = localStorage.getItem("scamshield_audio") !== "false";
    }

    init() {
        if (!this.ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;

            if (AudioCtx) {
                this.ctx = new AudioCtx();
            }
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
                osc.frequency.exponentialRampToValueAtTime(
                    1400,
                    now + 0.05
                );

                gain.gain.setValueAtTime(0.08, now);
                gain.gain.exponentialRampToValueAtTime(
                    0.001,
                    now + 0.05
                );

                osc.start(now);
                osc.stop(now + 0.05);
            }

            else if (type === "scan") {
                osc.type = "triangle";
                osc.frequency.setValueAtTime(320, now);
                osc.frequency.exponentialRampToValueAtTime(
                    980,
                    now + 0.22
                );

                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(
                    0.001,
                    now + 0.22
                );

                osc.start(now);
                osc.stop(now + 0.22);
            }

            else if (type === "alert") {
                osc.type = "sawtooth";
                osc.frequency.setValueAtTime(350, now);
                osc.frequency.setValueAtTime(240, now + 0.1);

                gain.gain.setValueAtTime(0.12, now);
                gain.gain.exponentialRampToValueAtTime(
                    0.001,
                    now + 0.25
                );

                osc.start(now);
                osc.stop(now + 0.25);
            }

            else if (type === "success") {
                osc.type = "sine";

                osc.frequency.setValueAtTime(523.25, now);
                osc.frequency.setValueAtTime(659.25, now + 0.08);
                osc.frequency.setValueAtTime(783.99, now + 0.16);

                gain.gain.setValueAtTime(0.1, now);
                gain.gain.exponentialRampToValueAtTime(
                    0.001,
                    now + 0.35
                );

                osc.start(now);
                osc.stop(now + 0.35);
            }

        } catch (error) {
            console.warn("Audio error:", error);
        }
    }
}

const audioEngine = new CyberAudioEngine();


// =========================================================
// THEME & AUDIO CONTROLLERS
// =========================================================

function initTheme() {
    const savedTheme =
        localStorage.getItem("scamshield_theme") || "dark";

    document.documentElement.setAttribute(
        "data-theme",
        savedTheme
    );

    updateThemeButtonUI(savedTheme);
    updateAudioButtonUI();
}

function toggleTheme() {
    audioEngine.play("click");

    const current =
        document.documentElement.getAttribute("data-theme") ||
        "dark";

    const next =
        current === "dark" ? "light" : "dark";

    document.documentElement.setAttribute(
        "data-theme",
        next
    );

    localStorage.setItem(
        "scamshield_theme",
        next
    );

    updateThemeButtonUI(next);
}

function updateThemeButtonUI(theme) {
    const icon = document.getElementById("themeIcon");
    const text = document.getElementById("themeText");

    if (!icon || !text) return;

    if (theme === "dark") {
        icon.textContent = "☀️";
        text.textContent = "Light";
    } else {
        icon.textContent = "🌙";
        text.textContent = "Dark";
    }
}

function toggleSound() {
    audioEngine.enabled = !audioEngine.enabled;

    localStorage.setItem(
        "scamshield_audio",
        audioEngine.enabled
    );

    updateAudioButtonUI();

    if (audioEngine.enabled) {
        audioEngine.play("success");
    }
}

function updateAudioButtonUI() {
    const soundIcon =
        document.getElementById("soundIcon");

    if (soundIcon) {
        soundIcon.textContent =
            audioEngine.enabled ? "🔊" : "🔇";
    }
}

function toggleSidebar() {
    audioEngine.play("click");

    const sidebar =
        document.getElementById("sidebar");

    if (sidebar) {
        sidebar.classList.toggle("open");
    }
}


// =========================================================
// INPUT HANDLING
// =========================================================

function autoExpand(textarea) {
    if (!textarea) return;

    textarea.style.height = "auto";

    textarea.style.height =
        Math.min(textarea.scrollHeight, 140) + "px";
}

function handleKey(event) {
    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {
        event.preventDefault();
        analyzeMessage();
    }
}

function useSample(element) {
    audioEngine.play("click");

    if (!element) return;

    const snippetElement =
        element.querySelector(".vector-snippet");

    const input =
        document.getElementById("message");

    if (!snippetElement || !input) return;

    const snippet =
        snippetElement.innerText
            .replace(/^"|"$/g, "")
            .trim();

    input.value = snippet;

    autoExpand(input);
    input.focus();
}

function injectPrompt(promptText) {
    audioEngine.play("click");

    const input =
        document.getElementById("message");

    if (!input) return;

    input.value = promptText;

    autoExpand(input);

    analyzeMessage();
}

function triggerQuickAction(action) {
    audioEngine.play("click");

    const sidebar =
        document.getElementById("sidebar");

    if (
        sidebar &&
        sidebar.classList.contains("open")
    ) {
        sidebar.classList.remove("open");
    }

    if (action === "scan") {
        injectPrompt(
            "How does ScamShield analyze messages and detect phishing links?"
        );
    }

    else if (action === "password") {
        injectPrompt(
            "Check my password: CyberShield#2026!"
        );
    }

    else if (action === "quiz") {
        injectPrompt(
            "Start a scam quiz challenge"
        );
    }

    else if (action === "graph") {
        injectPrompt(
            "Simulate phishing attack progression with BFS"
        );
    }

    else if (action === "helpline") {
        injectPrompt(
            "What are the official cybercrime helpline numbers?"
        );
    }

    else if (action === "sql_stats") {
        injectPrompt(
            "Show live SQL database threat statistics"
        );
    }

    else if (action === "url") {
        injectPrompt(
            "Scan URL http://paypal-secure-login.xyz/verify?user=123"
        );
    }

    else if (action === "email") {
        injectPrompt(
            "How to analyze email headers for phishing?"
        );
    }
}


// =========================================================
// TELEMETRY
// =========================================================

async function fetchTelemetry() {
    try {
        const response =
            await fetch("/api/stats");

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data =
            await response.json();

        const scansEl =
            document.getElementById("teleTotalScans");

        const highEl =
            document.getElementById("teleHighThreats");

        const avgEl =
            document.getElementById("teleAvgScore");

        if (scansEl) {
            scansEl.textContent =
                data.total_scans ?? 0;
        }

        if (highEl) {
            highEl.textContent =
                data.high_threats ?? 0;
        }

        if (avgEl) {
            avgEl.textContent =
                `${data.avg_risk_score ?? 0}/100`;
        }

        return data;

    } catch (error) {
        console.warn(
            "Could not sync SQL telemetry:",
            error
        );

        return null;
    }
}

function fetchAndDisplayDbStats() {
    audioEngine.play("click");

    injectPrompt(
        "Show live SQL database threat statistics"
    );
}

function useCyberTopic(topic) {
    audioEngine.play("click");

    injectPrompt(
        "Explain " +
        topic +
        " and how to stay protected"
    );
}

function clearConversation() {
    audioEngine.play("click");
    location.reload();
}

function scrollBottom() {
    const chat =
        document.getElementById("chat");

    if (chat) {
        setTimeout(() => {
            chat.scrollTop =
                chat.scrollHeight;
        }, 50);
    }
}


// =========================================================
// MAIN CHAT REQUEST
// =========================================================

async function analyzeMessage() {
    const input =
        document.getElementById("message");

    if (!input) {
        console.error(
            "Message input not found."
        );
        return;
    }

    const message =
        input.value.trim();

    if (!message) return;

    audioEngine.play("scan");

    const welcome =
        document.getElementById("welcome");

    if (welcome) {
        welcome.remove();
    }

    addUserMessage(message);

    input.value = "";
    input.style.height = "auto";

    const typingId =
        addTypingIndicator();

    try {
        const response =
            await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    message: message
                })
            });

        let result;

        try {
            result =
                await response.json();
        } catch (jsonError) {
            result = {
                error:
                    `Server returned HTTP ${response.status}.`
            };
        }

        removeTypingIndicator(typingId);

        if (!response.ok || result.error) {
            audioEngine.play("alert");

            addAIMessage(
                result.error ||
                `Server error: HTTP ${response.status}`
            );

            return;
        }

        handleResponsePayload(result);

    } catch (error) {
        removeTypingIndicator(typingId);

        console.error(
            "Network / Server Error:",
            error
        );

        audioEngine.play("alert");

        addAIMessage(
            "⚠️ Unable to connect to ScamShield AI Defense Engine. Please verify that the Flask server is running."
        );
    }
}


// =========================================================
// RESPONSE ROUTER
// =========================================================

function handleResponsePayload(result) {
    if (!result) {
        addAIMessage(
            "⚠️ Empty response received from server."
        );
        return;
    }

    const type =
        result.type || "unknown";

    const data =
        result.data || {};

    if (type === "scam_analysis") {

        incrementSession("scan");

        if (data.risk === "HIGH") {
            audioEngine.play("alert");
            incrementSession("threat");
        } else {
            audioEngine.play("success");
        }

        renderScamResult(data);

        fetchTelemetry();
    }

    else if (type === "password_strength") {
        audioEngine.play("success");

        renderPasswordResult(
            data,
            result.password_tested
        );
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

        if (data.is_correct) {
            audioEngine.play("success");
            incrementSession(
                "quiz_correct"
            );
        } else {
            audioEngine.play("alert");
            incrementSession(
                "quiz_wrong"
            );
        }

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

    else if (type === "url_scan") {

        if (data.risk === "HIGH") {
            audioEngine.play("alert");
        } else {
            audioEngine.play("success");
        }

        renderUrlScanResult(data);
    }

    else if (
        type === "email_header_guide"
    ) {
        audioEngine.play("success");

        renderEmailHeaderGuide(data);
    }

    else if (type === "url_scan_prompt") {
        audioEngine.play("click");

        addAIMessage(
            result.message ||
            "Paste a URL to scan it."
        );
    }

    else {
        addAIMessage(
            result.message ||
            "Threat analysis completed."
        );
    }
}


// =========================================================
// MESSAGE BUILDERS
// =========================================================

function addUserMessage(text) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    row.innerHTML = `
        <div class="message-wrapper"
             style="justify-content:flex-end;">

            <div class="user-text-bubble">
                ${escapeHTML(text)}
            </div>

            <div class="message-avatar user">
                👤
            </div>

        </div>
    `;

    chat.appendChild(row);

    scrollBottom();
}

function addAIMessage(text) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                🛡️
            </div>

            <div class="message-content">

                <div class="message-sender">
                    SCAMSHIELD INTEL
                </div>

                <div class="ai-text-bubble">
                    ${escapeHTML(text)}
                </div>

            </div>

        </div>
    `;

    chat.appendChild(row);

    scrollBottom();
}

function addTypingIndicator() {
    const chat =
        document.getElementById("chat");

    if (!chat) return null;

    const id =
        "typing-" + Date.now();

    const row =
        document.createElement("div");

    row.id = id;
    row.className =
        "message-row";

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                🛡️
            </div>

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
    if (!id) return;

    const element =
        document.getElementById(id);

    if (element) {
        element.remove();
    }
}


// =========================================================
// 1. SCAM ANALYSIS RESULT
// =========================================================

function renderScamResult(data) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const riskClass =
        String(data.risk || "LOW")
            .toLowerCase();

    const score =
        Math.max(
            0,
            Math.min(
                100,
                Number(data.risk_score) || 0
            )
        );

    const confidence =
        Math.max(
            0,
            Math.min(
                100,
                Number(data.confidence) || 0
            )
        );

    const radius = 54;

    const circumference =
        2 * Math.PI * radius;

    const offset =
        circumference -
        (score / 100) *
        circumference;

    let strokeColor =
        "var(--emerald)";

    if (riskClass === "high") {
        strokeColor =
            "var(--rose)";
    }

    else if (riskClass === "medium") {
        strokeColor =
            "var(--amber)";
    }

    let redFlagsHtml = "";

    if (
        Array.isArray(data.red_flags) &&
        data.red_flags.length > 0
    ) {
        redFlagsHtml =
            data.red_flags.map(flag => `
                <div class="threat-tag ${flag.severity
                    ? String(flag.severity).toLowerCase()
                    : "medium"
                }">

                    <span>⚠️</span>

                    <strong>
                        ${escapeHTML(flag.title || "Warning")}:
                    </strong>

                    <span>
                        ${escapeHTML(
                    flag.description || ""
                )}
                    </span>

                </div>
            `).join("");
    }

    else {
        redFlagsHtml = `
            <div class="threat-tag safe">
                <span>✓</span>
                <span>
                    No high-severity linguistic threat patterns detected.
                </span>
            </div>
        `;
    }

    const urlFindings =
        data.url_findings || {};

    const urls =
        Array.isArray(urlFindings.urls)
            ? urlFindings.urls
            : [];

    const urlIssues =
        Array.isArray(
            urlFindings.suspicious_indicators
        )
            ? urlFindings.suspicious_indicators
            : [];

    let urlHtml = "";

    if (urls.length > 0) {

        urlHtml = `
            <div class="section-block">

                <div class="section-block-title">
                    <span>🔗</span>
                    EXTRACTED URL HEURISTICS
                    (${urls.length})
                </div>

                <div style="
                    font-family:var(--font-mono);
                    font-size:12px;
                    margin-bottom:8px;
                ">

                    ${urls.map(url => `
                        <div style="
                            color:var(--cyan);
                            word-break:break-all;
                        ">
                            • ${escapeHTML(url)}
                        </div>
                    `).join("")}

                </div>

                ${urlIssues.length > 0
                ? `
                            <div style="
                                display:flex;
                                flex-direction:column;
                                gap:5px;
                                margin-top:6px;
                            ">

                                ${urlIssues.map(issue => `
                                    <div class="threat-tag critical"
                                         style="display:flex;">
                                        <span>🚨</span>
                                        ${escapeHTML(issue)}
                                    </div>
                                `).join("")}

                            </div>
                        `
                : `
                            <div style="
                                font-size:11px;
                                color:var(--emerald);
                            ">
                                ✓ Domain syntax conforms to standard naming structures.
                            </div>
                        `
            }

            </div>
        `;
    }

    const steps =
        Array.isArray(data.safety_steps) &&
            data.safety_steps.length > 0
            ? data.safety_steps
            : [
                "Never share OTPs, passwords or bank account details.",
                "Verify sender identity through official verified sources."
            ];

    const checklistHtml =
        steps.map(step => `
            <div class="action-check-item"
                 onclick="toggleCheckItem(this)">

                <div class="action-check-box">
                    ✓
                </div>

                <span>
                    ${escapeHTML(step)}
                </span>

            </div>
        `).join("");

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                🛡️
            </div>

            <div class="message-content">

                <div class="message-sender">
                    SCAMSHIELD THREAT REPORT
                </div>

                <div class="card-scam">

                    <div class="card-top">

                        <div class="card-heading">

                            <div class="card-badge-icon">
                                🔍
                            </div>

                            <div>
                                <h4>
                                    Deep Threat Scan Result
                                </h4>

                                <span>
                                    Multi-Layer ML & Heuristics Breakdown
                                </span>
                            </div>

                        </div>

                        <div class="risk-pill ${riskClass}">
                            ${escapeHTML(
        data.risk || "LOW"
    )}
                            RISK
                        </div>

                    </div>

                    <div class="card-body">

                        <div class="scam-dashboard-grid">

                            <div class="gauge-box">

                                <div style="
                                    position:relative;
                                    display:grid;
                                    place-items:center;
                                ">

                                    <svg class="svg-gauge"
                                         viewBox="0 0 140 140">

                                        <circle
                                            class="gauge-bg"
                                            cx="70"
                                            cy="70"
                                            r="${radius}">
                                        </circle>

                                        <circle
                                            class="gauge-fill"
                                            cx="70"
                                            cy="70"
                                            r="${radius}"
                                            stroke="${strokeColor}"
                                            stroke-dasharray="${circumference}"
                                            stroke-dashoffset="${circumference}">
                                        </circle>

                                    </svg>

                                    <div class="gauge-text-wrap">

                                        <span
                                            class="gauge-score"
                                            style="color:${strokeColor};">
                                            ${score}
                                        </span>

                                        <span class="gauge-sub">
                                            RISK INDEX
                                        </span>

                                    </div>

                                </div>

                            </div>

                            <div>

                                <div class="stats-deck">

                                    <div class="stat-tile">

                                        <div class="stat-tile-label">
                                            Detected Category
                                        </div>

                                        <div class="stat-tile-val text-cyan">
                                            ${escapeHTML(
        data.category || "Unknown"
    )}
                                        </div>

                                    </div>

                                    <div class="stat-tile">

                                        <div class="stat-tile-label">
                                            Threat Severity
                                        </div>

                                        <div class="stat-tile-val"
                                             style="color:${strokeColor};">

                                            ${escapeHTML(
        data.risk || "LOW"
    )}

                                        </div>

                                    </div>

                                </div>

                                <div class="confidence-module">

                                    <div class="confidence-labels">

                                        <span>
                                            AI Model Confidence
                                        </span>

                                        <strong>
                                            ${confidence}%
                                        </strong>

                                    </div>

                                    <div class="confidence-bar-track">

                                        <div
                                            class="confidence-bar-fill"
                                            style="width:${confidence}%;">
                                        </div>

                                    </div>

                                </div>

                            </div>

                        </div>

                        ${urlHtml}

                        <div class="section-block">

                            <div class="section-block-title">
                                <span>⚡</span>
                                RED FLAGS & THREAT INDICATORS
                            </div>

                            <div class="tags-cluster">
                                ${redFlagsHtml}
                            </div>

                        </div>

                        <div class="section-block">

                            <div class="section-block-title">
                                <span>🛡️</span>
                                RECOMMENDED DEFENSIVE PROTOCOL
                            </div>

                            <div class="action-checklist">
                                ${checklistHtml}
                            </div>

                        </div>

                        <div class="card-action-bar">

                            <button
                                class="card-btn"
                                onclick="copyReport(this)">

                                <span>📋</span>
                                Copy Report

                            </button>

                        </div>

                    </div>

                </div>

            </div>

        </div>
    `;

    chat.appendChild(row);

    const gauge =
        row.querySelector(".gauge-fill");

    if (gauge) {
        setTimeout(() => {
            gauge.style.strokeDashoffset =
                offset;
        }, 100);
    }

    scrollBottom();
}

function toggleCheckItem(element) {
    audioEngine.play("click");

    if (element) {
        element.classList.toggle("checked");
    }
}

async function copyReport(button) {
    audioEngine.play("success");

    if (!button) return;

    const card =
        button.closest(".card-scam");

    if (!card) return;

    const text =
        "ScamShield Threat Analysis:\n\n" +
        card.innerText;

    try {
        await navigator.clipboard.writeText(text);

        const original =
            button.innerHTML;

        button.innerHTML =
            "<span>✓</span> Copied!";

        setTimeout(() => {
            button.innerHTML =
                original;
        }, 2000);

    } catch (error) {
        showToast(
            "error",
            "Copy Failed",
            "Clipboard access was blocked by the browser."
        );
    }
}


// =========================================================
// 2. PASSWORD STRENGTH
// =========================================================

function renderPasswordResult(
    data,
    masked
) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const score =
        Math.max(
            0,
            Math.min(
                100,
                Number(data.score) || 0
            )
        );

    const strength =
        data.strength || "Weak";

    let segClass =
        "active-rose";

    if (score >= 90) {
        segClass =
            "active-emerald";
    }

    else if (score >= 70) {
        segClass =
            "active-cyan";
    }

    else if (score >= 45) {
        segClass =
            "active-amber";
    }

    const count =
        Math.min(
            5,
            Math.ceil(
                (score / 100) * 5
            )
        );

    const segments =
        Array.from(
            { length: 5 },
            (_, index) =>
                index < count
                    ? segClass
                    : ""
        );

    const checklistHtml =
        (data.checklist || [])
            .map(item => `
                <div class="pwd-check-item">

                    <span class="pwd-check-icon ${item.passed
                    ? "pass"
                    : "fail"
                }">

                        ${item.passed
                    ? "✓"
                    : "✗"
                }

                    </span>

                    <span>
                        ${escapeHTML(
                    item.label || ""
                )}
                    </span>

                </div>
            `)
            .join("");

    const suggestionsHtml =
        (data.suggestions || [])
            .map(suggestion => `
                <li style="
                    margin-bottom:6px;
                    color:var(--text-secondary);
                ">
                    ${escapeHTML(suggestion)}
                </li>
            `)
            .join("");

    const strengthClass =
        score >= 75
            ? "low"
            : score >= 45
                ? "medium"
                : "high";

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                🔐
            </div>

            <div class="message-content">

                <div class="message-sender">
                    PASSWORD ENTROPY LAB
                </div>

                <div class="card-scam">

                    <div class="card-top">

                        <div class="card-heading">

                            <div class="card-badge-icon">
                                🔑
                            </div>

                            <div>
                                <h4>
                                    Credential Resilience Analysis
                                </h4>

                                <span>
                                    GPU Offline Brute-Force Estimation
                                </span>
                            </div>

                        </div>

                        <div class="risk-pill ${strengthClass}">
                            ${escapeHTML(
        strength.toUpperCase()
    )}
                        </div>

                    </div>

                    <div class="card-body">

                        <div class="crack-time-hero">

                            <div>

                                <div class="crack-time-label">
                                    ESTIMATED TIME TO CRACK
                                </div>

                                <div class="crack-time-val">
                                    ${escapeHTML(
        data.crack_time || "Unknown"
    )}
                                </div>

                            </div>

                            <div style="text-align:right;">

                                <div class="crack-time-label">
                                    SHANNON ENTROPY
                                </div>

                                <div style="
                                    font-size:18px;
                                    font-weight:800;
                                    font-family:var(--font-mono);
                                ">
                                    ${escapeHTML(
        String(data.entropy ?? 0)
    )}
                                    BITS
                                </div>

                            </div>

                        </div>

                        <div class="password-meter-wrap">

                            ${segments.map(cls => `
                                <div class="meter-seg ${cls}">
                                </div>
                            `).join("")}

                        </div>

                        <div class="section-block">

                            <div class="section-block-title">
                                <span>🛡️</span>
                                COMPLEXITY & ENTROPY AUDIT
                            </div>

                            <div class="pwd-checklist-grid">
                                ${checklistHtml}
                            </div>

                        </div>

                        ${suggestionsHtml
            ? `
                                    <div class="section-block">

                                        <div class="section-block-title">
                                            <span>💡</span>
                                            HARDENING RECOMMENDATIONS
                                        </div>

                                        <ul style="
                                            padding-left:18px;
                                            font-size:13px;
                                            line-height:1.6;
                                        ">
                                            ${suggestionsHtml}
                                        </ul>

                                    </div>
                                `
            : ""
        }

                    </div>

                </div>

            </div>

        </div>
    `;

    chat.appendChild(row);

    scrollBottom();
}


// =========================================================
// 3. ATTACK GRAPH
// =========================================================

function renderAttackPathResult(data) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const steps =
        Array.isArray(data.steps)
            ? data.steps
            : [];

    const timelineHtml =
        steps.map((step, index) => {

            const isCritical =
                step.risk === "CRITICAL" ||
                index === steps.length - 1;

            return `
                <div class="timeline-step-node">

                    <div class="node-bullet ${isCritical
                    ? "critical"
                    : ""
                }">

                        ${String(
                    index + 1
                ).padStart(2, "0")}

                    </div>

                    <div class="node-card">

                        <div class="node-top">

                            <strong class="node-title">
                                ${escapeHTML(
                    step.name || "Attack Step"
                )}
                            </strong>

                            <span class="node-phase-tag">
                                ${escapeHTML(
                    step.phase || ""
                )}
                            </span>

                        </div>

                        <p class="node-desc">
                            ${escapeHTML(
                    step.detail || ""
                )}
                        </p>

                    </div>

                </div>
            `;
        })
            .join("");

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                🧭
            </div>

            <div class="message-content">

                <div class="message-sender">
                    CYBER GRAPH INTELLIGENCE
                </div>

                <div class="card-scam">

                    <div class="card-top">

                        <div class="card-heading">

                            <div class="card-badge-icon">
                                🕸️
                            </div>

                            <div>

                                <h4>
                                    ${escapeHTML(
        data.title ||
        "Cyber Attack Simulation"
    )}
                                </h4>

                                <span>
                                    ${escapeHTML(
        data.algorithm ||
        "Graph Algorithm"
    )}
                                </span>

                            </div>

                        </div>

                    </div>

                    <div class="card-body">

                        <p style="
                            font-size:13px;
                            color:var(--text-secondary);
                            line-height:1.6;
                            margin-bottom:20px;
                        ">
                            ${escapeHTML(
        data.explanation || ""
    )}
                        </p>

                        <div class="attack-timeline">
                            ${timelineHtml}
                        </div>

                        <div class="card-action-bar"
                             style="
                                justify-content:flex-start;
                                margin-top:20px;
                             ">

                            <button
                                class="card-btn"
                                onclick="injectPrompt('Simulate Phishing with BFS')">
                                BFS Phishing
                            </button>

                            <button
                                class="card-btn"
                                onclick="injectPrompt('Simulate Ransomware with DFS')">
                                DFS Ransomware
                            </button>

                            <button
                                class="card-btn"
                                onclick="injectPrompt('Find lowest cost mitigation with A*')">
                                A* Safe Path
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
// 4. QUIZ
// =========================================================

function renderQuizChallenge(quiz) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const options =
        Array.isArray(quiz.options)
            ? quiz.options
            : [];

    const optionsHtml =
        options.map(option => `
            <button
                class="quiz-opt-btn"
                onclick="submitQuizOption(
                    '${escapeJS(quiz.id)}',
                    '${escapeJS(option.id)}',
                    this
                )">

                <span class="quiz-opt-letter">
                    ${escapeHTML(option.id)}
                </span>

                <span>
                    ${escapeHTML(option.text)}
                </span>

            </button>
        `)
            .join("");

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                🎯
            </div>

            <div class="message-content">

                <div class="message-sender">
                    SCAMSHIELD DEFENSE QUIZ
                </div>

                <div class="quiz-card">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                    ">

                        <h4 style="
                            font-size:16px;
                            font-weight:800;
                        ">
                            ${escapeHTML(
        quiz.title ||
        "Cybersecurity Quiz"
    )}
                        </h4>

                        <span class="nav-badge hot">
                            ${escapeHTML(
        quiz.difficulty ||
        "Medium"
    )}
                        </span>

                    </div>

                    <div class="quiz-scenario-box">
                        ${escapeHTML(
        quiz.message || ""
    )}
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

async function submitQuizOption(
    quizId,
    optionId,
    button
) {
    audioEngine.play("click");

    if (!button) return;

    const parent =
        button.closest(".quiz-card");

    if (parent) {
        parent
            .querySelectorAll(".quiz-opt-btn")
            .forEach(btn => {
                btn.disabled = true;
                btn.style.opacity = "0.7";
            });
    }

    const typingId =
        addTypingIndicator();

    try {
        const response =
            await fetch("/quiz", {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    quiz_id: quizId,
                    option: optionId
                })
            });

        let result;

        try {
            result =
                await response.json();
        } catch (error) {
            result = {
                error:
                    `Server returned HTTP ${response.status}.`
            };
        }

        removeTypingIndicator(typingId);

        if (!response.ok || result.error) {
            addAIMessage(
                result.error ||
                "Quiz submission failed."
            );
            return;
        }

        renderQuizEvaluation(
            result,
            parent
        );

    } catch (error) {
        removeTypingIndicator(typingId);

        console.error(
            "Quiz submission error:",
            error
        );

        addAIMessage(
            "⚠️ Unable to submit quiz answer."
        );
    }
}

function renderQuizEvaluation(
    result,
    targetCard = null
) {
    const feedbackBox =
        document.createElement("div");

    feedbackBox.className =
        `quiz-feedback-box ${result.is_correct
            ? "correct"
            : "incorrect"
        }`;

    feedbackBox.innerHTML = `
        <div class="quiz-feedback-head">

            <span>
                ${result.is_correct
            ? "✅ SPOT ON! EXCELLENT INSTINCTS"
            : "🚨 CAUTION! YOU TOOK THE BAIT"
        }
            </span>

        </div>

        <div class="quiz-feedback-body">
            ${escapeHTML(
            result.explanation ||
            "No explanation provided."
        )}
        </div>

        <div style="
            margin-top:14px;
            display:flex;
            justify-content:flex-end;
        ">

            <button
                class="card-btn"
                onclick="injectPrompt('Next quiz challenge')">

                <span>➔</span>
                Next Question

            </button>

        </div>
    `;

    if (targetCard) {
        targetCard.appendChild(
            feedbackBox
        );
    }

    else {
        const chat =
            document.getElementById("chat");

        if (!chat) return;

        const row =
            document.createElement("div");

        row.className =
            "message-row";

        row.innerHTML = `
            <div class="message-wrapper">

                <div class="message-avatar ai">
                    🎯
                </div>

                <div class="message-content">

                    <div class="quiz-card">
                        ${feedbackBox.outerHTML}
                    </div>

                </div>

            </div>
        `;

        chat.appendChild(row);
    }

    if (result.is_correct) {
        audioEngine.play("success");
    } else {
        audioEngine.play("alert");
    }

    scrollBottom();
}


// =========================================================
// 5. CYBERSECURITY TOPIC
// =========================================================

function renderCybersecurityResult(data) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const signsHtml =
        (data.signs || [])
            .map(sign => `
                <li style="
                    margin-bottom:6px;
                    color:var(--text-secondary);
                ">
                    ${escapeHTML(sign)}
                </li>
            `)
            .join("");

    const protectionHtml =
        (data.protection || [])
            .map(item => `
                <li style="
                    margin-bottom:6px;
                    color:var(--text-secondary);
                ">
                    ${escapeHTML(item)}
                </li>
            `)
            .join("");

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                📚
            </div>

            <div class="message-content">

                <div class="message-sender">
                    CYBER KNOWLEDGE VAULT
                </div>

                <div class="card-scam">

                    <div class="card-top">

                        <div class="card-heading">

                            <div class="card-badge-icon">
                                📖
                            </div>

                            <div>

                                <h4>
                                    ${escapeHTML(
        data.topic ||
        "Cybersecurity Topic"
    )}
                                </h4>

                                <span>
                                    ${escapeHTML(
        data.badge ||
        "Cybersecurity Threat Overview"
    )}
                                </span>

                            </div>

                        </div>

                    </div>

                    <div class="card-body">

                        <p style="
                            font-size:14px;
                            line-height:1.7;
                            margin-bottom:18px;
                        ">
                            ${escapeHTML(
        data.description || ""
    )}
                        </p>

                        ${data.example
            ? `
                                    <div
                                        class="quiz-scenario-box"
                                        style="
                                            border-left-color:var(--cyan);
                                            margin-bottom:18px;
                                        ">

                                        <strong style="
                                            color:var(--cyan);
                                            display:block;
                                            margin-bottom:4px;
                                        ">
                                            REAL-WORLD ATTACK EXAMPLE:
                                        </strong>

                                        ${escapeHTML(
                data.example
            )}

                                    </div>
                                `
            : ""
        }

                        <div class="section-block">

                            <div class="section-block-title">
                                <span>⚠️</span>
                                TELLTALE WARNING SIGNS
                            </div>

                            <ul style="
                                padding-left:18px;
                                font-size:13px;
                                line-height:1.6;
                            ">
                                ${signsHtml}
                            </ul>

                        </div>

                        <div class="section-block">

                            <div class="section-block-title">
                                <span>🛡️</span>
                                HOW TO STAY PROTECTED
                            </div>

                            <ul style="
                                padding-left:18px;
                                font-size:13px;
                                line-height:1.6;
                            ">
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


// =========================================================
// 6. HELPLINE
// =========================================================

function renderHelplineResult(data) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const helplines =
        Array.isArray(data.helplines)
            ? data.helplines
            : [];

    const directoryHtml =
        helplines.map(item => `
            <div
                class="stat-tile"
                style="margin-bottom:8px;">

                <div style="
                    display:flex;
                    justify-content:space-between;
                ">

                    <strong>
                        ${escapeHTML(
            item.country || ""
        )}
                    </strong>

                    <span
                        class="risk-pill high"
                        style="
                            padding:3px 8px;
                            font-size:10px;
                        ">

                        ${escapeHTML(
            item.contact || ""
        )}

                    </span>

                </div>

                <div style="
                    font-size:12px;
                    color:var(--text-secondary);
                    margin:4px 0;
                ">
                    ${escapeHTML(
            item.service || ""
        )}
                </div>

                <div style="
                    font-size:11px;
                    font-family:var(--font-mono);
                    color:var(--cyan);
                ">
                    ${escapeHTML(
            item.portal || ""
        )}
                </div>

            </div>
        `)
            .join("");

    const actionsHtml =
        (data.immediate_actions || [])
            .map(action => `
                <li style="
                    margin-bottom:6px;
                    color:var(--text-secondary);
                ">
                    ${escapeHTML(action)}
                </li>
            `)
            .join("");

    row.innerHTML = `
        <div class="message-wrapper">

            <div
                class="message-avatar ai"
                style="
                    background:
                    linear-gradient(
                        135deg,
                        var(--rose),
                        var(--amber)
                    );
                ">
                🚨
            </div>

            <div class="message-content">

                <div class="message-sender">
                    EMERGENCY PROTOCOL
                </div>

                <div
                    class="card-scam"
                    style="
                        border-color:
                        rgba(244,63,94,0.35);
                    ">

                    <div
                        class="card-top"
                        style="
                            background:
                            rgba(244,63,94,0.12);
                        ">

                        <div class="card-heading">

                            <div
                                class="card-badge-icon"
                                style="
                                    background:
                                    rgba(244,63,94,0.2);
                                    border-color:
                                    var(--rose);
                                ">
                                🚨
                            </div>

                            <div>

                                <h4 style="
                                    color:var(--rose);
                                ">
                                    CRITICAL: Cyber Fraud Response
                                </h4>

                                <span>
                                    Immediate Damage Mitigation Guide
                                </span>

                            </div>

                        </div>

                    </div>

                    <div class="card-body">

                        <div style="
                            padding:14px 18px;
                            border-radius:12px;
                            background:
                            rgba(244,63,94,0.15);
                            border:
                            1px solid
                            rgba(244,63,94,0.3);
                            font-size:13px;
                            color:var(--rose);
                            font-weight:700;
                            margin-bottom:18px;
                        ">
                            ${escapeHTML(
        data.golden_hour_note || ""
    )}
                        </div>

                        <div
                            class="section-block"
                            style="
                                border-top:none;
                                padding-top:0;
                            ">

                            <div class="section-block-title">
                                <span>📞</span>
                                OFFICIAL CYBERCRIME HELPLINE DIRECTORY
                            </div>

                            ${directoryHtml}

                        </div>

                        <div class="section-block">

                            <div class="section-block-title">
                                <span>⚡</span>
                                IMMEDIATE CONTAINMENT PLAYBOOK
                            </div>

                            <ol style="
                                padding-left:20px;
                                font-size:13px;
                                line-height:1.7;
                            ">
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


// =========================================================
// 7. BOT INTRO
// =========================================================

function renderBotIntro(data) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const capabilitiesHtml =
        (data.capabilities || [])
            .map(capability => `
                <div
                    class="stat-tile"
                    style="
                        display:flex;
                        gap:12px;
                        align-items:flex-start;
                    ">

                    <span style="
                        font-size:22px;
                    ">
                        ${escapeHTML(
                capability.icon || "🛡️"
            )}
                    </span>

                    <div>

                        <strong style="
                            font-size:13px;
                            display:block;
                            margin-bottom:3px;
                        ">
                            ${escapeHTML(
                capability.title || ""
            )}
                        </strong>

                        <p style="
                            font-size:12px;
                            color:var(--text-secondary);
                            line-height:1.5;
                        ">
                            ${escapeHTML(
                capability.desc || ""
            )}
                        </p>

                    </div>

                </div>
            `)
            .join("");

    const promptsHtml =
        (data.quick_prompts || [])
            .map(prompt => `
                <button
                    class="chip-btn"
                    onclick="injectPrompt(
                        '${escapeJS(prompt)}'
                    )">

                    <span>➔</span>

                    ${escapeHTML(prompt)}

                </button>
            `)
            .join("");

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                🛡️
            </div>

            <div class="message-content">

                <div class="message-sender">
                    SCAMSHIELD AI DEFENSE AGENT
                </div>

                <div class="card-scam">

                    <div class="card-top">

                        <div class="card-heading">

                            <div class="card-badge-icon">
                                ⚡
                            </div>

                            <div>

                                <h4>
                                    ${escapeHTML(
        data.headline ||
        "AI Cyber Defense Assistant"
    )}
                                </h4>

                                <span>
                                    Next-Gen Multi-Vector Defense Hub
                                </span>

                            </div>

                        </div>

                    </div>

                    <div class="card-body">

                        <div style="
                            display:grid;
                            grid-template-columns:1fr;
                            gap:10px;
                            margin-bottom:20px;
                        ">
                            ${capabilitiesHtml}
                        </div>

                        <div class="section-block">

                            <div class="section-block-title">
                                <span>🚀</span>
                                SUGGESTED COMMANDS
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
// 8. SQL DATABASE TELEMETRY
// =========================================================

async function renderDbStatsCard(data) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const stats =
        data.stats || {};

    const recent =
        Array.isArray(data.recent)
            ? data.recent
            : [];

    const breakdown =
        await fetchAndRenderChart();

    const maxCount =
        breakdown.reduce(
            (max, item) =>
                Math.max(
                    max,
                    Number(item.count) || 0
                ),
            1
        );

    const chartHtml =
        breakdown.length > 0
            ? `
                <div class="threat-chart-wrap">

                    <div class="threat-chart-title">
                        📊 THREAT CATEGORY DISTRIBUTION
                    </div>

                    <div class="chart-bars">

                        ${breakdown.map(item => {

                const count =
                    Number(item.count) || 0;

                const width =
                    Math.round(
                        (count / maxCount) *
                        100
                    );

                return `
                                <div class="chart-bar-row">

                                    <div class="chart-bar-label">
                                        ${escapeHTML(
                    item.category ||
                    "Unknown"
                )}
                                    </div>

                                    <div class="chart-bar-track">

                                        <div
                                            class="chart-bar-fill"
                                            style="
                                                width:${width}%;
                                            ">
                                        </div>

                                    </div>

                                    <div class="chart-bar-count">
                                        ${count}
                                    </div>

                                </div>
                            `;
            }).join("")}

                    </div>

                </div>
            `
            : "";

    // IMPORTANT:
    // This is the ONLY recentRows declaration.
    // The duplicate broken block from the old file has been removed.

    const recentRows =
        recent.map(item => `
            <tr style="
                border-bottom:
                1px solid
                var(--border-subtle);
                font-size:12px;
            ">

                <td style="
                    padding:10px 8px;
                    font-family:var(--font-mono);
                    color:var(--text-muted);
                    font-size:11px;
                    white-space:nowrap;
                ">
                    ${escapeHTML(
            item.created_at
                ? String(
                    item.created_at
                ).substring(5, 16)
                : ""
        )}
                </td>

                <td style="
                    padding:10px 8px;
                    font-weight:700;
                    color:var(--cyan);
                    white-space:nowrap;
                ">
                    ${escapeHTML(
            item.category ||
            "Unknown"
        )}
                </td>

                <td style="
                    padding:10px 8px;
                    white-space:nowrap;
                ">

                    <span
                        class="risk-pill ${String(
            item.risk || "LOW"
        ).toLowerCase()
            }"
                        style="
                            padding:2px 8px;
                            font-size:9px;
                        ">

                        ${escapeHTML(
                item.risk || "LOW"
            )}

                    </span>

                </td>

                <td style="
                    padding:10px 8px;
                    font-family:var(--font-mono);
                    font-weight:800;
                    color:var(--text-primary);
                    text-align:center;
                ">
                    ${Number(
                item.risk_score
            ) || 0}
                </td>

                <td style="
                    padding:10px 8px;
                    color:var(--text-secondary);
                    max-width:240px;
                    overflow:hidden;
                    text-overflow:ellipsis;
                    white-space:nowrap;
                ">
                    ${escapeHTML(
                item.message || ""
            )}
                </td>

            </tr>
        `)
            .join("");

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                📊
            </div>

            <div class="message-content">

                <div class="message-sender">
                    SQL THREAT TELEMETRY ENGINE
                </div>

                <div class="card-scam">

                    <div class="card-top">

                        <div class="card-heading">

                            <div class="card-badge-icon">
                                🗄️
                            </div>

                            <div>

                                <h4>
                                    SQLite Security Database
                                </h4>

                                <span>
                                    Real-Time Relational Threat Store &amp; Aggregation
                                </span>

                            </div>

                        </div>

                        <div
                            class="nav-badge"
                            style="
                                padding:6px 12px;
                                font-size:11px;
                            ">
                            SQL ARMED
                        </div>

                    </div>

                    <div class="card-body">

                        <div style="
                            display:grid;
                            grid-template-columns:
                            repeat(3, 1fr);
                            gap:12px;
                            margin-bottom:20px;
                        ">

                            <div class="stat-tile">

                                <div class="stat-tile-label">
                                    Total Scans
                                </div>

                                <div class="stat-tile-val text-cyan">
                                    ${stats.total_scans || 0}
                                </div>

                            </div>

                            <div class="stat-tile">

                                <div class="stat-tile-label">
                                    High Risk Blocked
                                </div>

                                <div class="stat-tile-val"
                                     style="color:var(--rose);">
                                    ${stats.high_threats || 0}
                                </div>

                            </div>

                            <div class="stat-tile">

                                <div class="stat-tile-label">
                                    Medium Risk
                                </div>

                                <div class="stat-tile-val"
                                     style="color:var(--amber);">
                                    ${stats.medium_threats || 0}
                                </div>

                            </div>

                            <div class="stat-tile">

                                <div class="stat-tile-label">
                                    Average Risk Score
                                </div>

                                <div class="stat-tile-val">
                                    ${stats.avg_risk_score || 0}/100
                                </div>

                            </div>

                            <div class="stat-tile">

                                <div class="stat-tile-label">
                                    Top Threat Type
                                </div>

                                <div
                                    class="stat-tile-val"
                                    style="
                                        color:var(--amber);
                                        font-size:13px;
                                        overflow:hidden;
                                        text-overflow:ellipsis;
                                        white-space:nowrap;
                                    ">

                                    ${escapeHTML(
        stats.top_threat_category ||
        "None"
    )}

                                </div>

                            </div>

                            <div class="stat-tile">

                                <div class="stat-tile-label">
                                    Quiz Accuracy
                                </div>

                                <div
                                    class="stat-tile-val"
                                    style="
                                        color:var(--emerald);
                                    ">
                                    ${stats.quiz_accuracy ?? 100}%
                                </div>

                            </div>

                        </div>

                        ${chartHtml}

                        <div
                            class="section-block"
                            style="
                                border-top:none;
                                padding-top:0;
                                margin-top:18px;
                            ">

                            <div class="section-block-title">
                                <span>📜</span>
                                RECENT VERIFIED SCANS
                                (STORED IN SQL)
                            </div>

                            ${recent.length > 0
            ? `
                                        <div style="
                                            overflow-x:auto;
                                            border-radius:12px;
                                            border:
                                            1px solid
                                            var(--border-subtle);
                                            background:
                                            rgba(0,0,0,0.15);
                                        ">

                                            <table style="
                                                width:100%;
                                                border-collapse:collapse;
                                                text-align:left;
                                            ">

                                                <thead>

                                                    <tr style="
                                                        border-bottom:
                                                        1px solid
                                                        var(--border-subtle);
                                                        font-size:10px;
                                                        font-family:
                                                        var(--font-mono);
                                                        color:
                                                        var(--text-muted);
                                                        text-transform:
                                                        uppercase;
                                                    ">

                                                        <th style="
                                                            padding:8px;
                                                        ">
                                                            Date
                                                        </th>

                                                        <th style="
                                                            padding:8px;
                                                        ">
                                                            Category
                                                        </th>

                                                        <th style="
                                                            padding:8px;
                                                        ">
                                                            Risk
                                                        </th>

                                                        <th style="
                                                            padding:8px;
                                                            text-align:center;
                                                        ">
                                                            Score
                                                        </th>

                                                        <th style="
                                                            padding:8px;
                                                        ">
                                                            Sample Text
                                                        </th>

                                                    </tr>

                                                </thead>

                                                <tbody>
                                                    ${recentRows}
                                                </tbody>

                                            </table>

                                        </div>
                                    `
            : `
                                        <p style="
                                            font-size:12px;
                                            color:var(--text-muted);
                                        ">
                                            No scan logs recorded yet.
                                            Analyze a sample message above
                                            to generate SQL records!
                                        </p>
                                    `
        }

                        </div>

                        <div class="card-action-bar">

                            <button
                                class="card-btn"
                                onclick="openReportModal()">

                                <span>📝</span>
                                Report a Scam

                            </button>

                            <button
                                class="card-btn"
                                onclick="
                                    fetchTelemetry();
                                    injectPrompt(
                                        'Show live SQL database threat statistics'
                                    );
                                ">

                                <span>🔄</span>
                                Refresh

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

function escapeHTML(value) {
    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    const div =
        document.createElement("div");

    div.textContent =
        String(value);

    return div.innerHTML;
}

function escapeJS(value) {
    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replace(/\\/g, "\\\\")
        .replace(/'/g, "\\'")
        .replace(/"/g, '\\"')
        .replace(/\r?\n/g, "\\n");
}

function newChat() {
    audioEngine.play("click");
    location.reload();
}


// =========================================================
// SESSION STATS
// =========================================================

const sessionStats = {
    scans: 0,
    threats: 0,
    quizCorrect: 0,
    quizTotal: 0
};

function incrementSession(type) {

    if (type === "scan") {
        sessionStats.scans++;
    }

    if (type === "threat") {
        sessionStats.threats++;
    }

    if (type === "quiz_correct") {
        sessionStats.quizCorrect++;
        sessionStats.quizTotal++;
    }

    if (type === "quiz_wrong") {
        sessionStats.quizTotal++;
    }

    updateSessionUI();
}

function updateSessionUI() {
    const scansEl =
        document.getElementById(
            "sessionScansCount"
        );

    const threatsEl =
        document.getElementById(
            "sessionThreatsCount"
        );

    const quizEl =
        document.getElementById(
            "sessionQuizScore"
        );

    if (scansEl) {
        scansEl.textContent =
            sessionStats.scans;
    }

    if (threatsEl) {
        threatsEl.textContent =
            sessionStats.threats;
    }

    if (quizEl) {

        if (sessionStats.quizTotal > 0) {

            const percentage =
                Math.round(
                    (
                        sessionStats.quizCorrect /
                        sessionStats.quizTotal
                    ) * 100
                );

            quizEl.textContent =
                `${percentage}%`;
        }

        else {
            quizEl.textContent =
                "--";
        }
    }
}


// =========================================================
// SCAM REPORT MODAL
// =========================================================

function openReportModal() {
    audioEngine.play("click");

    const overlay =
        document.getElementById(
            "reportModalOverlay"
        );

    if (overlay) {
        overlay.classList.add("active");
    }

    document.body.style.overflow =
        "hidden";
}

function closeReportModal() {
    const overlay =
        document.getElementById(
            "reportModalOverlay"
        );

    if (overlay) {
        overlay.classList.remove("active");
    }

    document.body.style.overflow =
        "";
}

async function submitScamReport(event) {
    if (event) {
        event.preventDefault();
    }

    const button =
        document.getElementById(
            "reportSubmitBtn"
        );

    if (!button) return;

    const originalHTML =
        button.innerHTML;

    button.disabled = true;

    button.innerHTML = `
        <span class="btn-icon">⏳</span>
        <span>Submitting...</span>
    `;

    const getValue = id => {
        const element =
            document.getElementById(id);

        return element
            ? element.value
            : "";
    };

    const getChecked = id => {
        const element =
            document.getElementById(id);

        return element
            ? element.checked
            : false;
    };

    const payload = {
        scam_type:
            getValue("reportScamType"),

        platform:
            getValue("reportPlatform"),

        amount_lost:
            parseFloat(
                getValue("reportAmount")
            ) || 0,

        description:
            getValue("reportDescription"),

        contact_shared:
            getChecked(
                "reportContactShared"
            ),

        reported_to_police:
            getChecked(
                "reportReportedPolice"
            ),

        reporter_email:
            getValue("reportEmail")
    };

    try {

        const response =
            await fetch("/api/report", {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify(
                    payload
                )
            });

        const result =
            await response.json()
                .catch(() => ({
                    error:
                        `Server returned HTTP ${response.status}.`
                }));

        if (!response.ok) {
            throw new Error(
                result.error ||
                `HTTP ${response.status}`
            );
        }

        closeReportModal();

        const form =
            document.getElementById(
                "scamReportForm"
            );

        if (form) {
            form.reset();
        }

        if (result.success) {

            audioEngine.play("success");

            showToast(
                "success",
                "🚨 Report Submitted!",
                result.message ||
                "Your report was submitted successfully."
            );

            fetchTelemetry();
        }

        else {

            audioEngine.play("alert");

            showToast(
                "error",
                "⚠️ Submission Failed",
                result.error ||
                "Please try again."
            );
        }

    } catch (error) {

        console.error(
            "Report submission error:",
            error
        );

        audioEngine.play("alert");

        showToast(
            "error",
            "⚠️ Network Error",
            error.message ||
            "Could not submit report."
        );

    } finally {

        button.disabled = false;

        button.innerHTML =
            originalHTML;
    }
}

document.addEventListener(
    "keydown",
    event => {
        if (event.key === "Escape") {
            closeReportModal();
        }
    }
);


// =========================================================
// TOAST NOTIFICATIONS
// =========================================================

function showToast(
    type,
    title,
    message,
    duration = 5000
) {
    const toast =
        document.createElement("div");

    toast.className =
        `toast-notification ${type}`;

    toast.innerHTML = `
        <div class="toast-icon">
            ${type === "success"
            ? "✅"
            : "❌"
        }
        </div>

        <div>

            <div class="toast-title">
                ${escapeHTML(title)}
            </div>

            <div class="toast-msg">
                ${escapeHTML(message)}
            </div>

        </div>
    `;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.style.opacity =
            "0";

        toast.style.transform =
            "translateX(40px)";

        toast.style.transition =
            "all 0.4s ease";

        setTimeout(() => {
            toast.remove();
        }, 400);

    }, duration);
}


// =========================================================
// SECURITY TIPS
// =========================================================

const SECURITY_TIPS = [

    "🔐 Never share OTPs or UPI PINs — not even with 'bank officials'. Legitimate banks never ask for these over calls.",

    "🔗 Before clicking any link, hover over it to see the actual URL. Mismatched domains = phishing.",

    "💡 Use a password manager like Bitwarden or 1Password. One strong master password protects everything.",

    "📱 Enable 2FA on all critical accounts — email, banking, and social media. Prefer TOTP apps over SMS.",

    "🚨 If you receive a suspicious call from 'police' or 'customs' demanding money transfer — it is a scam.",

    "💳 You NEVER need to enter your UPI PIN to receive money. QR codes only send money FROM you.",

    "🤖 Deepfake voice calls can clone family members' voices. Establish a family safe word.",

    "📧 Check SPF/DKIM failures in email headers — spoofed emails often fail authentication.",

    "🛡️ Keep all software updated to reduce exposure to known vulnerabilities.",

    "📊 Check haveibeenpwned.com regularly to know if your email has appeared in a data breach.",

    "🔍 When in doubt, don't click. Visit the official website directly by typing the URL.",

    "💰 Guaranteed high returns in investments are a major scam warning sign.",

    "📡 SIM Swap: If your phone loses signal suddenly, immediately contact your carrier.",

    "🏦 Verify bank messages through official banking apps or websites.",

    "⚡ Never install remote-access software because an unknown caller tells you to."
];

let currentTipIndex =
    Math.floor(
        Math.random() *
        SECURITY_TIPS.length
    );

function rotateTip() {
    audioEngine.play("click");

    currentTipIndex =
        (
            currentTipIndex + 1
        ) %
        SECURITY_TIPS.length;

    displayTip();
}

function displayTip() {
    const element =
        document.getElementById(
            "tipText"
        );

    if (!element) return;

    element.style.opacity =
        "0";

    setTimeout(() => {

        element.textContent =
            SECURITY_TIPS[
            currentTipIndex
            ];

        element.style.opacity =
            "1";

        element.style.transition =
            "opacity 0.3s ease";

    }, 150);
}


// =========================================================
// ACTIVE NAVIGATION
// =========================================================

function setActiveNav(element) {

    document
        .querySelectorAll(".nav-item")
        .forEach(item => {
            item.classList.remove(
                "active"
            );
        });

    if (element) {
        element.classList.add(
            "active"
        );
    }
}


// =========================================================
// URL SCANNER RESULT
// =========================================================

function renderUrlScanResult(data) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const risk =
        data.risk || "LOW";

    const riskClass =
        String(risk).toLowerCase();

    const indicators =
        Array.isArray(data.indicators)
            ? data.indicators
            : [];

    const urls =
        Array.isArray(data.urls)
            ? data.urls
            : [];

    const indicatorsHtml =
        indicators.length > 0
            ? indicators.map(indicator => `
                <div class="threat-tag critical">

                    <span>🚨</span>

                    ${escapeHTML(
                indicator
            )}

                </div>
            `).join("")

            : `
                <div class="threat-tag safe">

                    <span>✓</span>

                    No suspicious URL indicators detected.

                </div>
            `;

    const urlsHtml =
        urls.map(url => `
            <div style="
                margin-bottom:4px;
                font-family:var(--font-mono);
                font-size:11px;
                color:var(--cyan);
                word-break:break-all;
            ">
                • ${escapeHTML(url)}
            </div>
        `)
            .join("");

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                🔗
            </div>

            <div class="message-content">

                <div class="message-sender">
                    URL DOMAIN THREAT SCANNER
                </div>

                <div class="card-scam">

                    <div class="card-top">

                        <div class="card-heading">

                            <div class="card-badge-icon">
                                🔍
                            </div>

                            <div>

                                <h4>
                                    URL Deep Threat Analysis
                                </h4>

                                <span>
                                    Heuristic Domain Inspection Engine
                                </span>

                            </div>

                        </div>

                        <div class="risk-pill ${riskClass}">
                            ${escapeHTML(risk)}
                            RISK
                        </div>

                    </div>

                    <div class="card-body">

                        <div class="url-display-box">
                            ${escapeHTML(
        data.url || ""
    )}
                        </div>

                        <div
                            class="section-block"
                            style="
                                border-top:none;
                                padding-top:0;
                            ">

                            <div class="section-block-title">

                                <span>🔗</span>

                                EXTRACTED URLS
                                (${urls.length})

                            </div>

                            ${urlsHtml ||
        `
                                    <span style="
                                        font-size:12px;
                                        color:var(--text-muted);
                                    ">
                                        No URLs extracted.
                                    </span>
                                `
        }

                        </div>

                        <div class="section-block">

                            <div class="section-block-title">

                                <span>⚡</span>

                                THREAT INDICATORS
                                (${indicators.length})

                            </div>

                            <div class="tags-cluster">
                                ${indicatorsHtml}
                            </div>

                        </div>

                        <div class="section-block">

                            <div class="section-block-title">

                                <span>🛡️</span>

                                SECURITY ADVICE

                            </div>

                            <div class="action-check-item">

                                <div class="action-check-box">
                                    ✓
                                </div>

                                <span>
                                    ${escapeHTML(
            data.advice ||
            "Verify the domain before entering sensitive information."
        )}
                                </span>

                            </div>

                            <div
                                class="action-check-item"
                                style="margin-top:8px;">

                                <div class="action-check-box">
                                    ✓
                                </div>

                                <span>
                                    Cross-check suspicious URLs using trusted security tools.
                                </span>

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
// EMAIL HEADER FORENSICS
// =========================================================

function renderEmailHeaderGuide(data) {
    const chat =
        document.getElementById("chat");

    if (!chat) return;

    const row =
        document.createElement("div");

    row.className =
        "message-row";

    const fieldsHtml =
        (data.fields || [])
            .map(field => `
                <div class="email-field-item">

                    <div class="email-field-icon">
                        ${escapeHTML(
                field.icon || "📧"
            )}
                    </div>

                    <div class="email-field-content">

                        <div class="email-field-name">

                            <span class="email-field-header">
                                ${escapeHTML(
                field.field || ""
            )}
                            </span>

                            <span
                                class="email-risk-badge ${String(
                field.risk ||
                "medium"
            ).toLowerCase()
                }">

                                ${escapeHTML(
                    field.risk ||
                    "MEDIUM"
                )}

                            </span>

                        </div>

                        <p class="email-field-desc">
                            ${escapeHTML(
                    field.explanation || ""
                )}
                        </p>

                        <div class="email-field-tip">
                            ⚑
                            ${escapeHTML(
                    field.what_to_look || ""
                )}
                        </div>

                    </div>

                </div>
            `)
            .join("");

    const accessHtml =
        (data.how_to_access || [])
            .map(item => `
                <li style="
                    margin-bottom:6px;
                    color:var(--text-secondary);
                ">
                    ${escapeHTML(item)}
                </li>
            `)
            .join("");

    row.innerHTML = `
        <div class="message-wrapper">

            <div class="message-avatar ai">
                📧
            </div>

            <div class="message-content">

                <div class="message-sender">
                    EMAIL FORENSICS LAB
                </div>

                <div class="card-scam">

                    <div class="card-top">

                        <div class="card-heading">

                            <div class="card-badge-icon">
                                📬
                            </div>

                            <div>

                                <h4>
                                    Email Header Analysis Guide
                                </h4>

                                <span>
                                    SPF · DKIM · DMARC · Routing Forensics
                                </span>

                            </div>

                        </div>

                    </div>

                    <div class="card-body">

                        <p style="
                            font-size:13px;
                            color:var(--text-secondary);
                            line-height:1.65;
                            margin-bottom:20px;
                        ">
                            ${escapeHTML(
        data.description || ""
    )}
                        </p>

                        <div
                            class="section-block"
                            style="
                                border-top:none;
                                padding-top:0;
                            ">

                            <div class="section-block-title">

                                <span>🔍</span>

                                CRITICAL HEADER FIELDS TO INSPECT

                            </div>

                            ${fieldsHtml}

                        </div>

                        <div class="section-block">

                            <div class="section-block-title">

                                <span>📂</span>

                                HOW TO ACCESS EMAIL HEADERS

                            </div>

                            <ol style="
                                padding-left:20px;
                                font-size:13px;
                                line-height:1.7;
                            ">
                                ${accessHtml}
                            </ol>

                        </div>

                        <div class="card-action-bar">

                            <button
                                class="card-btn"
                                onclick="
                                    injectPrompt(
                                        'What is phishing?'
                                    )
                                ">

                                <span>📖</span>
                                Phishing Guide

                            </button>

                            <button
                                class="card-btn"
                                onclick="
                                    window.open(
                                        'https://mxtoolbox.com/EmailHeaders.aspx',
                                        '_blank'
                                    )
                                ">

                                <span>🔗</span>
                                MXToolbox Analyzer

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
// CHART & COMMUNITY DATA
// =========================================================

async function fetchAndRenderChart() {
    try {

        const response =
            await fetch("/api/chart");

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data =
            await response.json();

        return data.breakdown || [];

    } catch (error) {

        console.warn(
            "Chart fetch failed:",
            error
        );

        return [];
    }
}

async function fetchCommunityReports() {
    try {

        const response =
            await fetch(
                "/api/reports?limit=1"
            );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data =
            await response.json();

        return data.reports || [];

    } catch (error) {

        console.warn(
            "Community reports fetch failed:",
            error
        );

        return [];
    }
}


// =========================================================
// INITIALIZATION
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        console.log(
            "🛡️ ScamShield AI frontend initialized."
        );

        initTheme();

        displayTip();

        setInterval(() => {

            currentTipIndex =
                (
                    currentTipIndex + 1
                ) %
                SECURITY_TIPS.length;

            displayTip();

        }, 45000);

        const stats =
            await fetchTelemetry();

        const heroTotal =
            document.getElementById(
                "heroTotalScans"
            );

        const heroHigh =
            document.getElementById(
                "heroHighThreats"
            );

        const heroCommunity =
            document.getElementById(
                "heroCommunityReports"
            );

        if (stats) {

            if (heroTotal) {
                heroTotal.textContent =
                    stats.total_scans || "0";
            }

            if (heroHigh) {
                heroHigh.textContent =
                    stats.high_threats || "0";
            }
        }

        try {

            const response =
                await fetch(
                    "/api/reports"
                );

            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}`
                );
            }

            const data =
                await response.json();

            const count =
                Array.isArray(data.reports)
                    ? data.reports.length
                    : 0;

            if (heroCommunity) {
                heroCommunity.textContent =
                    count;
            }

            const telemetryCommunity =
                document.getElementById(
                    "teleCommunityReports"
                );

            if (telemetryCommunity) {
                telemetryCommunity.textContent =
                    count;
            }

        } catch (error) {

            console.warn(
                "Community reports fetch failed:",
                error
            );
        }

        updateSessionUI();
    }
);