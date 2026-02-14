from fastapi import FastAPI
import ollama
app = FastAPI()

sessions = {}

@app.post("/chat")
async def chat(data: dict):
    user_id = data["user_id"]
    message = data["message"]

    if user_id not in sessions:
        sessions[user_id] = {"history": []}

    sessions[user_id]["history"].append(f"User: {message}")

    prompt = f"""
    You are a smart appointment booking chatbot.

    Conversation:
    {sessions[user_id]["history"]}

    If booking info is missing, ask only for the missing info.
    If complete, confirm booking clearly.
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    bot_reply = response["message"]["content"]

    sessions[user_id]["history"].append(f"Bot: {bot_reply}")

    return {"response": bot_reply}
