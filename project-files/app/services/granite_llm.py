import os
from dotenv import load_dotenv
from langchain.llms import WatsonxLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pydantic import SecretStr
import traceback

load_dotenv()

required_env_vars = ["WATSONX_MODEL_ID", "WATSONX_PROJECT_ID", "WATSONX_URL", "WATSONX_API_KEY"]
missing = [var for var in required_env_vars if os.getenv(var) is None]
if missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

watsonx_llm = WatsonxLLM(
    model_id=os.getenv("WATSONX_MODEL_ID"),
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    url=os.getenv("WATSONX_URL"),
    api_key=SecretStr(os.getenv("WATSONX_API_KEY")),
    params={
        "max_tokens": 1500,
        "temperature": 0.7,
        "decoding_method": "sample"
    }
)