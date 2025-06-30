from fastapi import APIRouter, HTTPException
from datetime import datetime
import traceback

dashboard_router = APIRouter()

# Dummy dashboard data generator
def get_dashboard_metrics():
    try:
        now = datetime.now()
        return {
            "timestamp": now.isoformat(),
            "total_documents": 42,
            "active_users": 7,
            "eco_tips_generated": 128,
            "feedback_received": 19
        }
    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}"

# Route: GET /dashboard-data
@dashboard_router.get("/dashboard-data", tags=["Dashboard"])
def fetch_dashboard_data():
    data = get_dashboard_metrics()
    if isinstance(data, str) and data.startswith("Error:"):
        raise HTTPException(status_code=500, detail=data)
    return {"dashboard": data}