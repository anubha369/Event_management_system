from fastapi import FastAPI
from pydantic import BaseModel
from recommender import Recommender

app = FastAPI()
rec = Recommender("Opportunity_Hub_Master_Dataset_5000.csv")


class StudentProfile(BaseModel):
    domain: str
    skills: str
    year: str
    branch: str
    mode: str = "Any"
    top_n: int = 10


@app.post("/recommend")
def recommend(profile: StudentProfile):
    result = rec.recommend(
        profile.domain, profile.skills, profile.year,
        profile.branch, profile.mode, profile.top_n
    )
    return result.to_dict(orient="records")
