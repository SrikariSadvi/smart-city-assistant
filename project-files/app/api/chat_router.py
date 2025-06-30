from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import traceback

from langchain_ibm import WatsonxLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Validate Watsonx credentials
required_vars = ["WATSONX_APIKEY", "WATSONX_PROJECT_ID", "WATSONX_URL", "WATSONX_MODEL_ID"]
missing = [var for var in required_vars if os.getenv(var) is None]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# Init Watsonx
watsonx_llm = WatsonxLLM(
    model_id=os.getenv("WATSONX_MODEL_ID"),
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    url=os.getenv("WATSONX_URL"),
    apikey=os.getenv("WATSONX_APIKEY"),
    params={"max_new_tokens": 1500, "temperature": 0.7, "decoding_method": "sample"}
)

# Define router
chat_router = APIRouter()

# Input model
class PromptRequest(BaseModel):
    prompt: str

# LLM handler
def ask_granite(prompt: str):
    try:
        chain = LLMChain(
            llm=watsonx_llm,
            prompt=PromptTemplate.from_template("You are a helpful city assistant. Respond to: {prompt}")
        )
        return chain.run(prompt=prompt)
    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}"

# Route: POST /ask-assistant
@chat_router.post("/ask-assistant", tags=["Chat Assistant"])
def ask_city_assistant(request: PromptRequest):
    response = ask_granite(request.prompt)
    if response.startswith("Error:"):
        raise HTTPException(status_code=500, detail=response)
    return {"response": response}