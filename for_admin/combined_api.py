from fastapi import FastAPI, Depends
import joblib
import pandas as pd
import sys
from pathlib import Path
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from recommender import Recommender
from database import get_db, engine, Base
from models import User, Organizer, Event

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Opportunity Hub ML API",
    description="Student Recommendation, Organizer Analytics and Admin Risk Detection",
    version="1.0"

    
)

# Student ML
student_model = Recommender(
    str(ROOT / "Opportunity_Hub_Master_Dataset_5000.csv")
)

# Organizer ML
organizer_model = joblib.load(HERE / "models" / "registration_model.pkl")
organizer_features = joblib.load(HERE / "models" / "registration_features.pkl")

# Admin ML
admin_model = joblib.load(HERE / "models" / "admin_event_anomaly_model.pkl")
admin_model_features = joblib.load(HERE / "models" / "admin_model_features.pkl")


@app.get("/")
def home():
    return {
        "message": "Opportunity Hub ML API is running",
        "services": {
            "student": "/student/recommend",
            "organizer_prediction": "/organizer/predict-registrations",
            "organizer_demand": "/organizer/event-demand",
            "organizer_analytics": "/organizer/analytics",
            "admin": "/admin/event-risk"
        }
    }


@app.post("/student/recommend")
def student_recommend(data: dict):

    result = student_model.recommend(
        domain=data.get("domain", ""),
        skills=data.get("skills", ""),
        year=data.get("year", ""),
        branch=data.get("branch", ""),
        mode=data.get("mode", "Any"),
        top_n=int(data.get("top_n", 5))
    )

    return {
        "recommendations": result.to_dict(orient="records")
    }


@app.post("/organizer/predict-registrations")
def predict_registrations(data: dict):

    input_data = pd.DataFrame([data])

    for column in ["certificate_available", "team_required"]:
        if column in input_data.columns:
            input_data[column] = input_data[column].astype(int)

    categorical_columns = [
        column
        for column in ["domain", "category", "mode"]
        if column in input_data.columns
    ]

    if categorical_columns:
        input_data = pd.get_dummies(
            input_data,
            columns=categorical_columns,
            dtype=int
        )

    input_data = input_data.reindex(
        columns=organizer_features,
        fill_value=0
    )

    prediction = organizer_model.predict(input_data)[0]

    return {
        "predicted_registrations": int(round(prediction))
    }


@app.get("/organizer/event-demand")
def event_demand(db: Session = Depends(get_db)):

    total_events = db.query(Event).count()

    pending_events = db.query(Event).filter(
        Event.status == "PENDING"
    ).count()

    approved_events = db.query(Event).filter(
        Event.status == "APPROVED"
    ).count()

    rejected_events = db.query(Event).filter(
        Event.status == "REJECTED"
    ).count()

    online_events = db.query(Event).filter(
        Event.mode == "Online"
    ).count()

    offline_events = db.query(Event).filter(
        Event.mode == "Offline"
    ).count()

    hybrid_events = db.query(Event).filter(
        Event.mode == "Hybrid"
    ).count()

    return {
        "total_events": total_events,
        "event_status": {
            "pending": pending_events,
            "approved": approved_events,
            "rejected": rejected_events
        },
        "mode_distribution": {
            "online": online_events,
            "offline": offline_events,
            "hybrid": hybrid_events
        }
    }


@app.get("/organizer/analytics")
def organizer_analytics(db: Session = Depends(get_db)):

    total_users = db.query(User).count()
    total_organizers = db.query(Organizer).count()
    total_events = db.query(Event).count()

    pending_organizers = db.query(Organizer).filter(
        Organizer.verification_status == "PENDING"
    ).count()

    verified_organizers = db.query(Organizer).filter(
        Organizer.verification_status == "VERIFIED"
    ).count()

    pending_events = db.query(Event).filter(
        Event.status == "PENDING"
    ).count()

    approved_events = db.query(Event).filter(
        Event.status == "APPROVED"
    ).count()

    rejected_events = db.query(Event).filter(
        Event.status == "REJECTED"
    ).count()

    return {
        "platform_statistics": {
            "total_users": total_users,
            "total_organizers": total_organizers,
            "total_events": total_events
        },
        "organizer_statistics": {
            "pending_verification": pending_organizers,
            "verified": verified_organizers
        },
        "event_statistics": {
            "pending": pending_events,
            "approved": approved_events,
            "rejected": rejected_events
        }
    }


@app.post("/admin/event-risk")
def check_event_risk(data: dict):

    input_data = pd.DataFrame([data])

    for feature in admin_model_features:
        if feature not in input_data.columns:
            input_data[feature] = 0

    input_data = input_data[admin_model_features]

    for column in input_data.columns:
        if input_data[column].dtype == bool:
            input_data[column] = input_data[column].astype(int)

    prediction = admin_model.predict(input_data)[0]

    anomaly_score = admin_model.decision_function(input_data)[0]

    risk_score = max(
        0,
        min(100, (0.5 - anomaly_score) * 100)
    )

    risk_score = round(float(risk_score), 2)

    status = "NEEDS REVIEW" if prediction == -1 else "NORMAL"

    if risk_score >= 75:
        priority = "HIGH"
    elif risk_score >= 50:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "admin_status": status,
        "risk_score": risk_score,
        "review_priority": priority,
        "anomaly_score": round(float(anomaly_score), 4)
    }
