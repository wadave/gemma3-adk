
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env into the environment

MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_VERSION = os.getenv("MODEL_VERSION")



# --- Example Agent using a model hosted on a vLLM endpoint ---

# Endpoint URL provided by your vLLM deployment
api_base_url = "http://localhost:8000/v1"

# Model name as recognized by *your* vLLM endpoint configuration
model_name_at_endpoint = f"hosted_vllm//gcs/{MODEL_NAME}/{MODEL_VERSION}" # Example from vllm_test.py


root_agent = LlmAgent(
    model=LiteLlm(
        model=model_name_at_endpoint,
        api_base=api_base_url,
   
    ),
    name="root_agent",
    instruction=(
        """You are a helpful AI assistant designed to provide accurate and useful
        information."""
    ),
    description="Answers questions about math problems.",
   
)