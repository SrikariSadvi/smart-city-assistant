from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import traceback
import os
from dotenv import load_dotenv

from langchain_ibm import WatsonxLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

# Validate environment
required_vars = ["WATSONX_APIKEY", "WATSONX_PROJECT_ID", "WATSONX_URL", "WATSONX_MODEL_ID"]
missing = [var for var in required_vars if os.getenv(var) is None]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# Initialize LLM
watsonx_llm = WatsonxLLM(
    model_id=os.getenv("WATSONX_MODEL_ID"),
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    url=os.getenv("WATSONX_URL"),
    apikey=os.getenv("WATSONX_APIKEY"),
    params={"max_new_tokens": 1500, "temperature": 0.7, "decoding_method": "sample"}
)

# APIRouter instance
eco_tips_router = APIRouter()

# Request schema
class EcoTipRequest(BaseModel):
    topic: str

# LLM function
def generate_eco_tip(topic: str):
    try:
        chain = LLMChain(
            llm=watsonx_llm,
            prompt=PromptTemplate.from_template(
                "Provide a practical and creative eco-friendly tip on: {topic}"
            )
        )
        return chain.run(topic=topic)
    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}"

# Endpoint
@eco_tips_router.get("/get-eco-tips", tags=["Eco Tips"])
def get_eco_tip(topic: str):
    tip = generate_eco_tip(topic)
    if tip.startswith("Error:"):
        raise HTTPException(status_code=500, detail=tip)
    return {"tip": tip}