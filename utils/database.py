import sqlite3
from datetime import datetime

from config import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Create screening_history table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS screening_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            ats_score REAL NOT NULL,
            skills TEXT,
            missing_skills TEXT,
            word_count INTEGER,
            char_count INTEGER,
            resume_length TEXT,
            ats_rating TEXT,
            improvement_tips TEXT,
            user_id INTEGER,
            created_at TEXT NOT NULL
        )
        """
    )

    # 2. Create users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'candidate',
            created_at TEXT NOT NULL
        )
        """
    )
    
    # 3. Migration check for user_id column in screening_history
    cursor.execute("PRAGMA table_info(screening_history)")
    columns = [row[1] for row in cursor.fetchall()]
    if "user_id" not in columns:
        cursor.execute("ALTER TABLE screening_history ADD COLUMN user_id INTEGER")
        
    conn.commit()
    conn.close()


def create_user(username, email, password_hash, role="candidate"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, email, password_hash, role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def save_screening_result(data, user_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO screening_history
        (filename, prediction, confidence, ats_score, skills, missing_skills,
         word_count, char_count, resume_length, ats_rating, improvement_tips, user_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["filename"],
            data["prediction"],
            data["confidence"],
            data["ats_score"],
            data.get("skills", ""),
            data.get("missing_skills", ""),
            data.get("word_count", 0),
            data.get("char_count", 0),
            data.get("resume_length", ""),
            data.get("ats_rating", ""),
            data.get("improvement_tips", ""),
            user_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id


def get_all_history(user_id=None, role=None):
    conn = get_connection()
    cursor = conn.cursor()
    if role == "recruiter" or user_id is None:
        cursor.execute(
            """
            SELECT * FROM screening_history
            ORDER BY datetime(created_at) DESC
            """
        )
    else:
        cursor.execute(
            """
            SELECT * FROM screening_history
            WHERE user_id = ?
            ORDER BY datetime(created_at) DESC
            """,
            (user_id,),
        )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_history_by_id(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM screening_history WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def delete_history_record(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM screening_history WHERE id = ?", (record_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_dashboard_stats(user_id=None, role=None):
    conn = get_connection()
    cursor = conn.cursor()

    is_recruiter = (role == "recruiter" or user_id is None)

    # 1. Total Uploads
    if is_recruiter:
        cursor.execute("SELECT COUNT(*) AS total FROM screening_history")
    else:
        cursor.execute("SELECT COUNT(*) AS total FROM screening_history WHERE user_id = ?", (user_id,))
    total_uploads = cursor.fetchone()["total"]

    # 2. Top Category
    if is_recruiter:
        cursor.execute(
            """
            SELECT prediction, COUNT(*) AS count
            FROM screening_history
            GROUP BY prediction
            ORDER BY count DESC
            LIMIT 1
            """
        )
    else:
        cursor.execute(
            """
            SELECT prediction, COUNT(*) AS count
            FROM screening_history
            WHERE user_id = ?
            GROUP BY prediction
            ORDER BY count DESC
            LIMIT 1
            """,
            (user_id,)
        )
    top_category_row = cursor.fetchone()
    most_common_category = top_category_row["prediction"] if top_category_row else "N/A"

    # 3. Avg ATS Score
    if is_recruiter:
        cursor.execute("SELECT AVG(ats_score) AS avg_ats FROM screening_history")
    else:
        cursor.execute("SELECT AVG(ats_score) AS avg_ats FROM screening_history WHERE user_id = ?", (user_id,))
    avg_ats = cursor.fetchone()["avg_ats"] or 0

    # 4. Avg Confidence
    if is_recruiter:
        cursor.execute("SELECT AVG(confidence) AS avg_conf FROM screening_history")
    else:
        cursor.execute("SELECT AVG(confidence) AS avg_conf FROM screening_history WHERE user_id = ?", (user_id,))
    avg_confidence = cursor.fetchone()["avg_conf"] or 0

    # 5. Latest Upload
    if is_recruiter:
        cursor.execute(
            """
            SELECT filename, prediction, created_at
            FROM screening_history
            ORDER BY datetime(created_at) DESC
            LIMIT 1
            """
        )
    else:
        cursor.execute(
            """
            SELECT filename, prediction, created_at
            FROM screening_history
            WHERE user_id = ?
            ORDER BY datetime(created_at) DESC
            LIMIT 1
            """,
            (user_id,)
        )
    latest_upload = cursor.fetchone()

    # 6. Category Distribution
    if is_recruiter:
        cursor.execute(
            """
            SELECT prediction, COUNT(*) AS count
            FROM screening_history
            GROUP BY prediction
            ORDER BY count DESC
            """
        )
    else:
        cursor.execute(
            """
            SELECT prediction, COUNT(*) AS count
            FROM screening_history
            WHERE user_id = ?
            GROUP BY prediction
            ORDER BY count DESC
            """,
            (user_id,)
        )
    category_distribution = [dict(row) for row in cursor.fetchall()]

    # 7. Upload Trends
    if is_recruiter:
        cursor.execute(
            """
            SELECT DATE(created_at) AS upload_date, COUNT(*) AS count
            FROM screening_history
            GROUP BY DATE(created_at)
            ORDER BY upload_date ASC
            """
        )
    else:
        cursor.execute(
            """
            SELECT DATE(created_at) AS upload_date, COUNT(*) AS count
            FROM screening_history
            WHERE user_id = ?
            GROUP BY DATE(created_at)
            ORDER BY upload_date ASC
            """,
            (user_id,)
        )
    upload_trends = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "total_uploads": total_uploads,
        "most_common_category": most_common_category,
        "avg_ats_score": round(avg_ats, 1),
        "avg_confidence": round(avg_confidence, 1),
        "latest_upload": dict(latest_upload) if latest_upload else None,
        "category_distribution": category_distribution,
        "upload_trends": upload_trends,
    }


