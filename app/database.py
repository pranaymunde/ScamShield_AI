import mysql.connector
import csv
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "analysis_history.csv"


def get_db_connection():
    """
    Creates and returns a MySQL database connection.
    Database credentials are read from environment variables.
    """

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "scamshield"),
        port=int(os.getenv("DB_PORT", "3306"))
    )


def init_db():
    """
    Initializes MySQL database tables and indexes.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Analyses Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            message TEXT NOT NULL,
            category VARCHAR(100),
            risk VARCHAR(20),
            risk_score INT DEFAULT 0,
            confidence FLOAT DEFAULT 0.0,
            suspicious_words TEXT,
            url_count INT DEFAULT 0,
            client_ip VARCHAR(64),

            INDEX idx_analyses_created (created_at),
            INDEX idx_analyses_risk (risk),
            INDEX idx_analyses_category (category)
        )
    """)

    # 2. Quiz Attempts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            quiz_id VARCHAR(50),
            selected_option VARCHAR(10),
            is_correct TINYINT DEFAULT 0
        )
    """)

    # 3. Scam Reports Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scam_reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scam_type VARCHAR(100),
            platform VARCHAR(100),
            amount_lost FLOAT DEFAULT 0.0,
            description TEXT,
            contact_shared TINYINT DEFAULT 0,
            reported_to_police TINYINT DEFAULT 0,
            reporter_email VARCHAR(200),
            status VARCHAR(20) DEFAULT 'pending',

            INDEX idx_reports_created (created_at)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def save_analysis(message, result, client_ip=None):
    """
    Saves scam analysis to MySQL.
    Also synchronizes the record to CSV for Power BI.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    suspicious_str = ", ".join(
        result.get("suspicious_words", [])
    )

    url_count = len(
        result.get("url_findings", {}).get("urls", [])
    )

    risk_score = int(
        result.get("risk_score", 0)
    )

    confidence = float(
        result.get("confidence", 0.0)
    )

    category = str(
        result.get("category", "Normal")
    )

    risk = str(
        result.get("risk", "LOW")
    )

    cursor.execute("""
        INSERT INTO analyses (
            message,
            category,
            risk,
            risk_score,
            confidence,
            suspicious_words,
            url_count,
            client_ip
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        message,
        category,
        risk,
        risk_score,
        confidence,
        suspicious_str,
        url_count,
        client_ip
    ))

    conn.commit()

    cursor.close()
    conn.close()

    # CSV sync for Power BI
    sync_csv(
        message,
        category,
        risk,
        risk_score,
        confidence,
        suspicious_str
    )


def save_quiz_attempt(quiz_id, option, is_correct):
    """
    Saves quiz attempt to MySQL.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_attempts (
            quiz_id,
            selected_option,
            is_correct
        )
        VALUES (%s, %s, %s)
    """, (
        quiz_id,
        option,
        1 if is_correct else 0
    ))

    conn.commit()

    cursor.close()
    conn.close()


def get_recent_analyses(limit=15):
    """
    Retrieves recent scam analyses.
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            created_at,
            message,
            category,
            risk,
            risk_score,
            confidence,
            suspicious_words
        FROM analyses
        ORDER BY id DESC
        LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def get_threat_stats():
    """
    Calculates live threat statistics using MySQL.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # Total scans
    cursor.execute("""
        SELECT COUNT(*)
        FROM analyses
    """)

    total_scans = cursor.fetchone()[0] or 0

    # High threats
    cursor.execute("""
        SELECT COUNT(*)
        FROM analyses
        WHERE risk = 'HIGH'
    """)

    high_threats = cursor.fetchone()[0] or 0

    # Medium threats
    cursor.execute("""
        SELECT COUNT(*)
        FROM analyses
        WHERE risk = 'MEDIUM'
    """)

    medium_threats = cursor.fetchone()[0] or 0

    # Low threats
    cursor.execute("""
        SELECT COUNT(*)
        FROM analyses
        WHERE risk = 'LOW'
    """)

    low_threats = cursor.fetchone()[0] or 0

    # Average risk score
    cursor.execute("""
        SELECT AVG(risk_score)
        FROM analyses
    """)

    avg_score = cursor.fetchone()[0]

    avg_score = (
        round(float(avg_score), 1)
        if avg_score is not None
        else 0.0
    )

    # Top threat category
    cursor.execute("""
        SELECT category, COUNT(*) AS cnt
        FROM analyses
        WHERE category != 'Normal'
        GROUP BY category
        ORDER BY cnt DESC
        LIMIT 1
    """)

    top_cat_row = cursor.fetchone()

    top_category = (
        top_cat_row[0]
        if top_cat_row
        else "None"
    )

    # Quiz statistics
    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(is_correct), 0)
        FROM quiz_attempts
    """)

    quiz_row = cursor.fetchone()

    quiz_total = quiz_row[0] or 0
    quiz_correct = quiz_row[1] or 0

    quiz_accuracy = (
        round((quiz_correct / quiz_total) * 100, 1)
        if quiz_total > 0
        else 100.0
    )

    cursor.close()
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


def save_scam_report(
    scam_type,
    platform,
    amount_lost,
    description,
    contact_shared,
    reported_to_police,
    reporter_email
):
    """
    Saves user scam report to MySQL.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scam_reports (
            scam_type,
            platform,
            amount_lost,
            description,
            contact_shared,
            reported_to_police,
            reporter_email
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        str(scam_type),
        str(platform),
        float(amount_lost) if amount_lost else 0.0,
        str(description),
        1 if contact_shared else 0,
        1 if reported_to_police else 0,
        str(reporter_email) if reporter_email else ""
    ))

    report_id = cursor.lastrowid

    conn.commit()

    cursor.close()
    conn.close()

    return report_id


def get_category_breakdown():
    """
    Returns category-wise threat statistics.
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            category,
            COUNT(*) AS count
        FROM analyses
        GROUP BY category
        ORDER BY count DESC
        LIMIT 8
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def get_recent_reports(limit=10):
    """
    Retrieves recent scam reports.
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            created_at,
            scam_type,
            platform,
            amount_lost,
            description,
            status
        FROM scam_reports
        ORDER BY id DESC
        LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def sync_csv(
    message,
    category,
    risk,
    risk_score,
    confidence,
    suspicious_words
):
    """
    Maintains CSV file for Power BI compatibility.
    """

    CSV_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    file_exists = CSV_PATH.exists()

    with open(
        CSV_PATH,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "created_at",
                "message",
                "category",
                "risk",
                "risk_score",
                "confidence",
                "suspicious_words"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            message,
            category,
            risk,
            risk_score,
            confidence,
            suspicious_words
        ])