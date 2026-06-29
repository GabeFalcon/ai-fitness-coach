import sqlite3

DB_NAME = "coachai.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        username TEXT,
        password TEXT
    )
    """)

    # Profiles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        user_id TEXT PRIMARY KEY,
        age INTEGER,
        weight REAL,
        height INTEGER,
        days_per_week INTEGER,
        goal TEXT,
        experience TEXT
    )
    """)

    conn.commit()
    conn.close()