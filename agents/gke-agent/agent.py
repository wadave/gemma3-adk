
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import google.auth


import subprocess
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# --- Example Agent using a model hosted on a vLLM endpoint ---

# Endpoint URL provided by your vLLM deployment
api_base_url = "http://localhost:8000/v1"

# Model name as recognized by *your* vLLM endpoint configuration
model_name_at_endpoint = "hosted_vllm//gcs/gemma3-1b-vertex/full_merged_model" # Example from vllm_test.py


root_agent = Agent(
    model=LiteLlm(
        model=model_name_at_endpoint,
        api_base=api_base_url,
   
    ),
    name="vllm_agent",
    instruction="You are a helpful assistant running on a self-hosted vLLM endpoint.",
   
)