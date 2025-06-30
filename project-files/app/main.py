from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.api.kpi_upload_router import kpi_upload_router
from app.api.vector_router import vector_router
from app.api.eco_tips_router import eco_tips_router
from app.api.feedback_router import feedback_router
from app.api.kpi_forecasting_router import router as kpi_forecast_router
from app.api.policy_router import policy_router
from app.api.anomaly_router import router as anomaly_router
from app.api.chat_router import chat_router  # ✅ added
from app.api.report_router import report_router


# Load env vars
load_dotenv()
required_vars = ["WATSONX_APIKEY", "WATSONX_PROJECT_ID", "WATSONX_URL", "WATSONX_MODEL_ID"]
missing = [var for var in required_vars if os.getenv(var) is None]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(kpi_upload_router)
app.include_router(vector_router)
app.include_router(eco_tips_router)
app.include_router(feedback_router)
app.include_router(kpi_forecast_router)
app.include_router(policy_router)
app.include_router(anomaly_router)
app.include_router(chat_router)         # ✅ Now added
app.include_router(report_router)       # ✅ Now added

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart City Assistant API"}
