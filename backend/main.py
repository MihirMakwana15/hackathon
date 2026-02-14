from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from llm_service import extract_booking

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

sessions = {}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.post("/process")
async def process(data: dict):

    print("🔥 FULL INCOMING DATA:", data)

    message = None
    user_id = None

    # Case 1: Custom frontend format
    if "msg" in data:
        message = data.get("msg")
        user_id = data.get("id")

    # Case 2: Direct single message object
    elif "message" in data:
        msg_content = data.get("message", {})
        message = (
            msg_content.get("conversation")
            or msg_content.get("extendedTextMessage", {}).get("text")
            or msg_content.get("imageMessage", {}).get("caption")
        )
        user_id = data.get("key", {}).get("remoteJid")

    # Case 3: Baileys webhook format (MOST COMMON)
    elif "messages" in data:
        msg_obj = data["messages"][0]

        # Ignore system notifications
        if msg_obj.get("key", {}).get("fromMe"):
            return {"status": "ignored"}

        msg_content = msg_obj.get("message", {})

        message = (
            msg_content.get("conversation")
            or msg_content.get("extendedTextMessage", {}).get("text")
            or msg_content.get("imageMessage", {}).get("caption")
        )

        user_id = msg_obj.get("key", {}).get("remoteJid")

    # If still no message
    if not message:
        print("❌ No valid message found")
        return {"reply": "⚠ Please send a text message."}

    if not user_id:
        user_id = "unknown_user"

    # Session handling
    if user_id not in sessions:
        sessions[user_id] = {"history": []}

    sessions[user_id]["history"].append(f"User: {message}")

    conversation_text = "\n".join(sessions[user_id]["history"])

    try:
        bot_reply = extract_booking(conversation_text)
    except Exception as e:
        print("🔥 LLM ERROR:", str(e))
        return {"reply": "⚠ Server error. Try again later."}

    sessions[user_id]["history"].append(f"Bot: {bot_reply}")

    return {"reply": bot_reply}
