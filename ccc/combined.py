from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from fastapi.middleware.cors import CORSMiddleware
from combined import app

load_dotenv()
client = genai.Client()

SYSTEM_INSTRUCTION = """
You are the official AI assistant of Opportunity Hub.
Opportunity Hub is a platform where students discover internships,
hackathons, competitions, courses and other career events.
Help students understand opportunities, eligibility, skills, deadlines
and application requirements. Be practical, concise and student-friendly.
Do not invent event names, deadlines, eligibility or links.
If information is not available, say so clearly.
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    previous_interaction_id: str | None = None


@app.post("/chat")
def chat(data: ChatRequest):
    params = {
        "model": "gemini-3.8-flash",
        "input": data.message,
        "system_instruction": SYSTEM_INSTRUCTION,
    }
    if data.previous_interaction_id:
        params["previous_interaction_id"] = data.previous_interaction_id

    interaction = client.interactions.create(**params)

    return {
        "reply": interaction.output_text,
        "interaction_id": interaction.id,
    }

print("MIDDLEWARE LIST:", app.user_middleware)