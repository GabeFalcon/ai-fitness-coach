from database.db import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        username TEXT,
        password TEXT
    )
    """)

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plans (
        user_id TEXT PRIMARY KEY,
        content TEXT,
        version INTEGER,
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checkins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        day INTEGER,
        date TEXT,
        exercises TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercise_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        exercise_name TEXT,
        avg_reps REAL,
        avg_weight REAL,
        sets_completed INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()