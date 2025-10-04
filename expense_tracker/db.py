import sqlite3, os, pathlib, datetime as dt

DB_PATH = os.getenv("DB_PATH", str(pathlib.Path("data/expenses.db")))

def get_conn():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL CHECK(amount >= 0),
        method TEXT,
        created_at TEXT NOT NULL
    );
    """)
    return conn
