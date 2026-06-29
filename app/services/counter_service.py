import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent.parent / "db" / "counter.db"

def _get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY,
            count INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.execute("INSERT OR IGNORE INTO counter (id, count) VALUES (1, 0)")
    conn.commit()
    return conn

def increase_counter() -> int:
    with _get_connection() as conn:
        conn.execute("UPDATE counter SET count = count + 1 WHERE id = 1")
        count = conn.execute("SELECT count FROM counter WHERE id = 1").fetchone()[0]
    return count

def restart_counter() -> int:
    with _get_connection() as conn:
        conn.execute("UPDATE counter SET count = 0 WHERE id = 1")
    return 0

def get_counter() -> int:
    with _get_connection() as conn:
        return conn.execute("SELECT count FROM counter WHERE id = 1").fetchone()[0]