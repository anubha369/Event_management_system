cat > chatbot_api.py <<'PY'
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

SYSTEM_INSTRUCTION = """
You are the official AI assistant of Opportunity Hub.

Opportunity Hub is a platform where students can discover opportunities
such as internships, hackathons, competitions, courses, and other
career-related events.

Your responsibilities:
- Help students understand opportunities.
- Answer questions about internships, hackathons, competitions and events.
- Help students understand eligibility, skills, deadlines and application requirements.
- Give practical and concise guidance.
- If the user asks about a specific opportunity, explain it clearly.
- Do not invent event names, deadlines, eligibility criteria or application links.
- If information is not available, clearly say that the information is not available.
- Keep responses student-friendly and easy to understand.
"""




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
PY