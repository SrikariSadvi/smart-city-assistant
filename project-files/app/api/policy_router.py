from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import traceback
import os
from dotenv import load_dotenv

from langchain_ibm import WatsonxLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

# Verify environment variables
required_vars = ["WATSONX_APIKEY", "WATSONX_PROJECT_ID", "WATSONX_URL", "WATSONX_MODEL_ID"]
missing = [var for var in required_vars if os.getenv(var) is None]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# Initialize Watsonx LLM
watsonx_llm = WatsonxLLM(
    model_id=os.getenv("WATSONX_MODEL_ID"),
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    url=os.getenv("WATSONX_URL"),
    apikey=os.getenv("WATSONX_APIKEY"),
    params={"max_new_tokens": 1500, "temperature": 0.7, "decoding_method": "sample"}
)

# APIRouter instance
policy_router = APIRouter()

# Request schema
class SummaryRequest(BaseModel):
    text: str

# LLM summarization logic
def generate_summary(text: str):
    try:
        chain = LLMChain(
            llm=watsonx_llm,
            prompt=PromptTemplate.from_template(
                "Summarize the following policy document clearly and concisely:\n\n{text}"
            )
        )
        return chain.run(text=text)
    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}"

# Endpoint: POST /summarize-policy
@policy_router.post("/summarize-policy", tags=["Policy Summarization"])
def summarize_policy(request: SummaryRequest):
    summary = generate_summary(request.text)
    if summary.startswith("Error:"):
        raise HTTPException(status_code=500, detail=summary)
    return {"summary": summary}