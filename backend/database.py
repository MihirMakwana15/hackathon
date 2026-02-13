import sqlite3

def init_db():
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        service TEXT,
        date TEXT,
        time TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()
