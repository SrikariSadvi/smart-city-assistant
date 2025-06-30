from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import traceback

# Initialize APIRouter
feedback_router = APIRouter()

# Request schema
class FeedbackRequest(BaseModel):
    name: str
    email: str
    message: str

# Feedback processor
def process_feedback(name: str, email: str, message: str):
    try:
        print(f"[FEEDBACK RECEIVED]\nFrom: {name} <{email}>\nMessage: {message}")
        return "Feedback submitted successfully"
    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}"

# Route: POST /submit-feedback
@feedback_router.post("/submit-feedback", tags=["Feedback"])
def submit_feedback(request: FeedbackRequest):
    result = process_feedback(request.name, request.email, request.message)
    if result.startswith("Error:"):
        raise HTTPException(status_code=500, detail=result)
    return {"message": result}