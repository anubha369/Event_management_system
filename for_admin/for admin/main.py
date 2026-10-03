from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI(
    title="Opportunity Hub Admin ML API",
    description="ML API for Admin Event Risk Detection",
    version="1.0"
)

admin_model = joblib.load(
    "models/admin_event_anomaly_model.pkl"
)

admin_model_features = joblib.load(
    "models/admin_model_features.pkl"
)


@app.get("/")
def home():
    return {
        "message": "Opportunity Hub Admin ML API is running"
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
        min(
            100,
            (0.5 - anomaly_score) * 100
        )
    )

    risk_score = round(float(risk_score), 2)

    if prediction == -1:
        status = "NEEDS REVIEW"
    else:
        status = "NORMAL"

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