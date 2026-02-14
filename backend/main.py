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


@app.post("/chat")
async def chat(data: dict):
    user_id = data["user_id"]
    message = data["message"]

    if user_id not in sessions:
        sessions[user_id] = {"history": []}

    sessions[user_id]["history"].append(f"User: {message}")

    conversation_text = "\n".join(sessions[user_id]["history"])

    # Call LLM Service
    bot_reply = extract_booking(conversation_text)

    sessions[user_id]["history"].append(f"Bot: {bot_reply}")

    return {"response": bot_reply}
