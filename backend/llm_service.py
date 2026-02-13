import requests
import json

def extract_booking(text):

    prompt = f"""
Extract booking details.
Return JSON only.

{{
 "customer_name": "",
 "service": "",
 "date": "",
 "time": "",
 "notes": ""
}}

Message:
{text}
"""

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    output = res.json()["response"]

    try:
        return json.loads(output)
    except:
        return None
