from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import traceback
import os
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

# Validate environment variables
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
report_router = APIRouter()

# Request schema (now includes 'city')
class ReportRequest(BaseModel):
    city: str
    kpi_data: str

# LLM function
def generate_city_report(city: str, kpi_data: str):
    try:
        prompt = PromptTemplate.from_template(
    "You are an expert sustainability analyst. Generate a detailed Smart City Sustainability Report for the city of {city}, using the following KPIs:\n\n{kpi_data}\n\n"
    "Structure the report professionally, including sections for each KPI and a conclusion. Directly use the city name \"{city}\" throughout the report — do NOT use placeholders like [City Name] or [Smart City Name]."
)

        
        chain = LLMChain(llm=watsonx_llm, prompt=prompt)
        return chain.run(city=city, kpi_data=kpi_data)

    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}"

# Endpoint
@report_router.post("/generate-report", tags=["City Report"])
def city_report(request: ReportRequest):
    report = generate_city_report(request.city, request.kpi_data)
    if report.startswith("Error:"):
        raise HTTPException(status_code=500, detail=report)
    return {"report": report}
