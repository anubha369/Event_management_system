from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

app = FastAPI(
    title="Opportunity Hub Chatbot",
    description="Gemini-powered chatbot for Opportunity Hub",
    version="1.0"
)


class ChatRequest(BaseModel):
    message: str
    previous_interaction_id: str | None = None


@app.get("/")
def home():
    return {
        "message": "Opportunity Hub Chatbot is running"
    }


@app.post("/chat")
def chat(data: ChatRequest):

    if data.previous_interaction_id:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=data.message,
            previous_interaction_id=data.previous_interaction_id
        )
    else:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=data.message
        )

    return {
        "reply": interaction.output_text,
        "interaction_id": interaction.id
    }
