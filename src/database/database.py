import sqlite3
import threading
from pathlib import Path
from datetime import datetime

DB_DIR = Path("database")
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "clipboard_guardian.db"


class ClipboardDatabase:

    def __init__(self):
        # Allow access from multiple threads
        self.conn = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )

        self.lock = threading.Lock()

        self.create_table()

    def create_table(self):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS clipboard_history(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT NOT NULL,

                category TEXT NOT NULL,

                confidence REAL NOT NULL,

                risk_score INTEGER NOT NULL,

                risk_level TEXT NOT NULL

            )
            """)

            self.conn.commit()

    def insert_detection(
        self,
        category,
        confidence,
        risk_score,
        risk_level
    ):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                """
                INSERT INTO clipboard_history(

                    timestamp,
                    category,
                    confidence,
                    risk_score,
                    risk_level

                )

                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    category,
                    confidence,
                    risk_score,
                    risk_level,
                ),
            )

            self.conn.commit()

    def fetch_history(self):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute("""
                SELECT *

                FROM clipboard_history

                ORDER BY id DESC
            """)

            return cursor.fetchall()

    def clear_history(self):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute("DELETE FROM clipboard_history")

            self.conn.commit()

    def close(self):

        with self.lock:
            self.conn.close()


if __name__ == "__main__":

    db = ClipboardDatabase()

    db.insert_detection(
        "api_key",
        0.9987,
        95,
        "Critical"
    )

    print("\nHistory\n")

    for row in db.fetch_history():
        print(row)

    db.close()