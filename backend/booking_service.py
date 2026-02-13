import sqlite3

def save_booking(data, phone):
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bookings (name, phone, service, date, time, notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["customer_name"],
        phone,
        data["service"],
        data["date"],
        data["time"],
        data["notes"]
    ))

    conn.commit()
    conn.close()

def get_bookings():
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()
    conn.close()
    return rows
