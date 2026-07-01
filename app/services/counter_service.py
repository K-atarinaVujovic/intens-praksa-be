import os
import psycopg2
from psycopg2 import pool

DATABASE_URL = os.environ["DATABASE_URL"]

_pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)

def _get_connection():
    conn = _pool.getconn()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS counter (
                id INTEGER PRIMARY KEY,
                count INTEGER NOT NULL DEFAULT 0
            )
        """)
        cur.execute("INSERT INTO counter (id, count) VALUES (1, 0) ON CONFLICT (id) DO NOTHING")
    conn.commit()
    return conn

def increase_counter() -> int:
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE counter SET count = count + 1 WHERE id = 1")
            cur.execute("SELECT count FROM counter WHERE id = 1")
            count = cur.fetchone()[0]
        conn.commit()
        return count
    finally:
        _pool.putconn(conn)

def restart_counter() -> int:
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE counter SET count = 0 WHERE id = 1")
        conn.commit()
        return 0
    finally:
        _pool.putconn(conn)

def get_counter() -> int:
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT count FROM counter WHERE id = 1")
            return cur.fetchone()[0]
    finally:
        _pool.putconn(conn)