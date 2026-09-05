import sqlite3
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "scamshield.db"
CSV_PATH = BASE_DIR / "data" / "analysis_history.csv"


def get_db_connection():
    """
    Creates and returns a SQLite database connection with Row factory.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initializes SQL database schema with tables and indexes.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Analyses Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            message TEXT NOT NULL,
            category VARCHAR(100),
            risk VARCHAR(20),
            risk_score INTEGER DEFAULT 0,
            confidence REAL DEFAULT 0.0,
            suspicious_words TEXT,
            url_count INTEGER DEFAULT 0,
            client_ip VARCHAR(64)
        );
    """)

    # 2. Quiz Attempts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            quiz_id VARCHAR(50),
            selected_option VARCHAR(10),
            is_correct INTEGER
        );
    """)

    # 3. Performance Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyses_created ON analyses(created_at DESC);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyses_risk ON analyses(risk);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyses_category ON analyses(category);")

    conn.commit()
    conn.close()


def save_analysis(message, result, client_ip=None):
    """
    Inserts a scam analysis record into SQL database using parameterized queries.
    Also syncs to CSV for Power BI compatibility.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    suspicious_str = ", ".join(result.get("suspicious_words", []))
    url_count = len(result.get("url_findings", {}).get("urls", []))
    risk_score = int(result.get("risk_score", 0))
    confidence = float(result.get("confidence", 0.0))
    category = str(result.get("category", "Normal"))
    risk = str(result.get("risk", "LOW"))

    cursor.execute("""
        INSERT INTO analyses (
            message, category, risk, risk_score, confidence, suspicious_words, url_count, client_ip
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        message, category, risk, risk_score, confidence, suspicious_str, url_count, client_ip
    ))

    conn.commit()
    conn.close()

    # Maintain CSV sync for Power BI
    sync_csv(message, category, risk, risk_score, confidence, suspicious_str)


def save_quiz_attempt(quiz_id, option, is_correct):
    """
    Logs an interactive quiz submission in the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_attempts (quiz_id, selected_option, is_correct)
        VALUES (?, ?, ?);
    """, (quiz_id, option, 1 if is_correct else 0))
    conn.commit()
    conn.close()


def get_recent_analyses(limit=15):
    """
    Retrieves the most recent analysis events from SQL database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, created_at, message, category, risk, risk_score, confidence, suspicious_words
        FROM analyses
        ORDER BY id DESC
        LIMIT ?;
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_threat_stats():
    """
    Runs SQL aggregate queries to compute live telemetry and statistics.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total Scans
    cursor.execute("SELECT COUNT(*) FROM analyses;")
    total_scans = cursor.fetchone()[0] or 0

    # Risk breakdown
    cursor.execute("SELECT COUNT(*) FROM analyses WHERE risk = 'HIGH';")
    high_threats = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM analyses WHERE risk = 'MEDIUM';")
    medium_threats = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM analyses WHERE risk = 'LOW';")
    low_threats = cursor.fetchone()[0] or 0

    # Average Risk Score
    cursor.execute("SELECT AVG(risk_score) FROM analyses;")
    avg_score = cursor.fetchone()[0]
    avg_score = round(avg_score, 1) if avg_score is not None else 0.0

    # Top Threat Category
    cursor.execute("""
        SELECT category, COUNT(*) as cnt
        FROM analyses
        WHERE category != 'Normal'
        GROUP BY category
        ORDER BY cnt DESC
        LIMIT 1;
    """)
    top_cat_row = cursor.fetchone()
    top_category = top_cat_row[0] if top_cat_row else "None"

    # Quiz stats
    cursor.execute("SELECT COUNT(*), SUM(is_correct) FROM quiz_attempts;")
    quiz_row = cursor.fetchone()
    quiz_total = quiz_row[0] or 0
    quiz_correct = quiz_row[1] or 0
    quiz_accuracy = round((quiz_correct / quiz_total) * 100, 1) if quiz_total > 0 else 100.0

    conn.close()

    return {
        "total_scans": total_scans,
        "high_threats": high_threats,
        "medium_threats": medium_threats,
        "low_threats": low_threats,
        "avg_risk_score": avg_score,
        "top_threat_category": top_category,
        "quiz_total": quiz_total,
        "quiz_accuracy": quiz_accuracy
    }


def sync_csv(message, category, risk, risk_score, confidence, suspicious_str):
    """
    Appends analysis record to CSV file for Power BI dashboard support.
    """
    try:
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        file_exists = CSV_PATH.exists()

        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    "Date",
                    "Message",
                    "Category",
                    "Risk",
                    "Risk Score",
                    "Confidence",
                    "Suspicious Words"
                ])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                message,
                category,
                risk,
                risk_score,
                confidence,
                suspicious_str
            ])
    except Exception as e:
        print(f"[Warning] Could not sync CSV: {e}")
