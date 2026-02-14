import requests
import json

def extract_booking(text):
    """
    Sends conversation to Ollama and returns chatbot reply.
    """

    prompt = f"""
You are a professional and friendly appointment booking assistant.

Conversation so far:
{text}

Your behavior rules:

1. If this is the first message from the user, greet politely and ask how you can help.
2. Understand the user's intent.
3. If booking:
   - Identify service type.
   - Ask for missing details step-by-step.
4. Required booking info:
   - Full Name
   - Phone number
   - Address
   - Date
   - Time
   - Service type
5. If all info collected, confirm booking clearly.
6. Be natural and conversational.
7. Use proper line breaks.
8. Do NOT return JSON.
"""

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        data = res.json()

        if "response" not in data:
            return "⚠ AI model error."

        return data["response"].strip()

    except Exception as e:
        return f"⚠ LLM connection error: {str(e)}"
