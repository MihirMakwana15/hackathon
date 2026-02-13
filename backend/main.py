from fastapi import FastAPI
from pydantic import BaseModel

from database import init_db
from llm_service import extract_booking
from booking_service import save_booking, get_bookings

app = FastAPI()
init_db()

class Message(BaseModel):
    text: str
    phone: str

@app.post("/process")
def process(msg: Message):

    booking = extract_booking(msg.text)

    if booking:
        save_booking(booking, msg.phone)
        return {"reply": f"""
✅ Booking Confirmed!

📅 {booking['date']}
⏰ {booking['time']}
💼 {booking['service']}
"""}

    return {"reply": "Please send booking details."}

@app.get("/bookings")
def list_bookings():
    return get_bookings()
