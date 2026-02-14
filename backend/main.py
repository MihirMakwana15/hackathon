from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

sessions = {}

class RequestModel(BaseModel):
    text: str
    phone: str

@app.post("/process")
async def process(data: RequestModel):
    user = data.phone
    message = data.text.lower()

    # Initialize user session
    if user not in sessions:
        sessions[user] = {
            "step": "greet",
            "booking": {}
        }

    session = sessions[user]

    # STEP 1: Greeting
    if session["step"] == "greet":
        session["step"] = "ask_service"
        return {"reply": "Hi 👋 Welcome! What service would you like to book?"}

    # STEP 2: Ask Service
    if session["step"] == "ask_service":
        session["booking"]["service"] = message
        session["step"] = "ask_date"
        return {"reply": "Great 👍 What date would you like?"}

    # STEP 3: Ask Date
    if session["step"] == "ask_date":
        session["booking"]["date"] = message
        session["step"] = "ask_time"
        return {"reply": "Perfect. What time?"}

    # STEP 4: Ask Time
    if session["step"] == "ask_time":
        session["booking"]["time"] = message

        booking = session["booking"]

        # Reset session after booking
        sessions.pop(user)

        return {
            "reply": f"✅ Booking Confirmed!\n\nService: {booking['service']}\nDate: {booking['date']}\nTime: {booking['time']}"
        }
