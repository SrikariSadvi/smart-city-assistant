from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np

router = APIRouter()

# Request model
class AnomalyRequest(BaseModel):
    data: list[float]

# Anomaly detection logic using Z-score
def detect_anomalies(data, threshold=1.5):
    mean = np.mean(data)
    std = np.std(data)
    anomalies = [
        {"index": i, "value": x}
        for i, x in enumerate(data)
        if abs((x - mean) / std) > threshold
    ]
    return anomalies


# POST endpoint to detect anomalies
@router.post("/check-anomalies", tags=["Anomaly Checker"])
def check_anomalies(request: AnomalyRequest):
    try:
        anomalies = detect_anomalies(request.data)
        return {"anomalies": anomalies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
