from pathlib import Path
import sqlite3
from datetime import datetime


# ============================================================
# Database Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DB_DIR / "clipboard_guardian.db"


# ============================================================
# SQLite Logger
# ============================================================

class SQLiteLogger:

    def __init__(self):
        self.create_table()

    # ========================================================
    # Database Connection
    # ========================================================

    def get_connection(self):
        return sqlite3.connect(DB_FILE)

    # ========================================================
    # Create Database Table
    # ========================================================

    def create_table(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clipboard_history (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    timestamp TEXT NOT NULL,

                    category TEXT NOT NULL,

                    confidence REAL NOT NULL,

                    risk_score INTEGER NOT NULL,

                    risk_level TEXT NOT NULL,

                    action TEXT NOT NULL
                )
            """)

            conn.commit()

        finally:
            conn.close()

    # ========================================================
    # Log Detection
    # ========================================================

    def log_detection(self, risk):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO clipboard_history
                (
                    timestamp,
                    category,
                    confidence,
                    risk_score,
                    risk_level,
                    action
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                risk.category,
                risk.confidence,
                risk.risk_score,
                risk.risk_level,
                risk.action,
            ))

            conn.commit()

        finally:
            conn.close()

    # ========================================================
    # Fetch All History
    # ========================================================

    def fetch_all(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    timestamp,
                    category,
                    confidence,
                    risk_score,
                    risk_level,
                    action
                FROM clipboard_history
                ORDER BY id DESC
            """)

            return cursor.fetchall()

        finally:
            conn.close()

    # ========================================================
    # Compatibility Method
    # ========================================================
    # GUI currently expects:
    #
    #     logger.get_all_detections()
    #
    # Keep this method so the GUI and database layer work
    # together without changing the GUI code.

    def get_all_detections(self):

        return self.fetch_all()

    # ========================================================
    # Fetch Recent Detections
    # ========================================================

    def fetch_recent(self, limit=10):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    timestamp,
                    category,
                    confidence,
                    risk_score,
                    risk_level,
                    action
                FROM clipboard_history
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))

            return cursor.fetchall()

        finally:
            conn.close()

    # ========================================================
    # Get Detection By ID
    # ========================================================

    def get_detection_by_id(self, detection_id):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    timestamp,
                    category,
                    confidence,
                    risk_score,
                    risk_level,
                    action
                FROM clipboard_history
                WHERE id = ?
            """, (detection_id,))

            return cursor.fetchone()

        finally:
            conn.close()

    # ========================================================
    # Dashboard Statistics
    # ========================================================

    def get_total_count(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM clipboard_history
            """)

            result = cursor.fetchone()

            return result[0] if result else 0

        finally:
            conn.close()

    # ========================================================
    # Critical Count
    # ========================================================

    def get_critical_count(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM clipboard_history
                WHERE risk_level = ?
            """, ("Critical",))

            result = cursor.fetchone()

            return result[0] if result else 0

        finally:
            conn.close()

    # ========================================================
    # High Risk Count
    # ========================================================

    def get_high_count(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM clipboard_history
                WHERE risk_level = ?
            """, ("High",))

            result = cursor.fetchone()

            return result[0] if result else 0

        finally:
            conn.close()

    # ========================================================
    # Medium Risk Count
    # ========================================================

    def get_medium_count(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM clipboard_history
                WHERE risk_level = ?
            """, ("Medium",))

            result = cursor.fetchone()

            return result[0] if result else 0

        finally:
            conn.close()

    # ========================================================
    # Safe / Low Risk Count
    # ========================================================

    def get_safe_count(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM clipboard_history
                WHERE risk_level = ?
            """, ("Low",))

            result = cursor.fetchone()

            return result[0] if result else 0

        finally:
            conn.close()

    # ========================================================
    # Category Statistics
    # ========================================================

    def get_category_counts(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    category,
                    COUNT(*)
                FROM clipboard_history
                GROUP BY category
                ORDER BY COUNT(*) DESC
            """)

            return cursor.fetchall()

        finally:
            conn.close()

    # ========================================================
    # Risk Statistics
    # ========================================================

    def get_risk_counts(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    risk_level,
                    COUNT(*)
                FROM clipboard_history
                GROUP BY risk_level
                ORDER BY COUNT(*) DESC
            """)

            return cursor.fetchall()

        finally:
            conn.close()

    # ========================================================
    # Average Confidence
    # ========================================================

    def get_average_confidence(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT AVG(confidence)
                FROM clipboard_history
            """)

            result = cursor.fetchone()

            return float(result[0]) if result and result[0] is not None else 0.0

        finally:
            conn.close()

    # ========================================================
    # Average Risk Score
    # ========================================================

    def get_average_risk_score(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT AVG(risk_score)
                FROM clipboard_history
            """)

            result = cursor.fetchone()

            return float(result[0]) if result and result[0] is not None else 0.0

        finally:
            conn.close()

    # ========================================================
    # Clear History
    # ========================================================

    def clear_history(self):

        conn = self.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM clipboard_history
            """)

            conn.commit()

        finally:
            conn.close()

    # ========================================================
    # Database Information
    # ========================================================

    def get_database_path(self):

        return str(DB_FILE)

    # ========================================================
    # Database Size
    # ========================================================

    def get_database_size(self):

        try:
            return DB_FILE.stat().st_size
        except FileNotFoundError:
            return 0

    # ========================================================
    # Representation
    # ========================================================

    def __repr__(self):

        return (
            f"SQLiteLogger("
            f"database='{DB_FILE}')"
        )


# ============================================================
# Global Logger Instance
# ============================================================

logger = SQLiteLogger()