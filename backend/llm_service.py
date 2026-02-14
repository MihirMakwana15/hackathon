import requests
import json

def extract_booking(text):

    prompt = f"""
You are a professional appointment booking assistant.

Conversation so far:
{text}

Your task:
1. Understand the user's intent.
2. Identify service type.
3. Ask for missing required information.
4. If all information is collected, confirm the booking.

Required information for booking:
- Full Name
- Phone number
- Address
- Date
- Time
- Service type

Respond naturally like a real assistant.
"""


    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = res.json()

    print("LLM RAW RESPONSE:", data)  # Debug print

    if "response" not in data:
        raise Exception(f"LLM Error: {data}")

    output = data["response"]


    try:
        return json.loads(output)
    except:
        return None
