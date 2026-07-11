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
        created_at TEXT,
        last_updated TEXT,
        change_reason TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checkins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        weight REAL,
        calories_avg INTEGER,
        protein_avg INTEGER,
        sleep_avg REAL,
        completed_workouts INTEGER,
        notes TEXT,
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercise_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        exercise_name TEXT,
        set_number INTEGER,
        reps INTEGER,
        weight REAL,
        completed INTEGER,
        workout_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        decision TEXT,
        confidence REAL,
        reasoning TEXT,
        applied INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()