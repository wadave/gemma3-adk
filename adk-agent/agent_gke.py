
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import google.auth


import subprocess
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# --- Example Agent using a model hosted on a vLLM endpoint ---

# Endpoint URL provided by your vLLM deployment
api_base_url = "http://127.0.0.1:8000"

# Model name as recognized by *your* vLLM endpoint configuration
model_name_at_endpoint = "google/gemma-3-1b-it" # Example from vllm_test.py

# Authentication (Example: using gcloud identity token for a Cloud Run deployment)
# Adapt this based on your endpoint's security
try:
    gcloud_token = subprocess.check_output(
        ["gcloud", "auth", "print-identity-token", "-q"]
    ).decode().strip()
    auth_headers = {"Authorization": f"Bearer {gcloud_token}"}
except Exception as e:
    print(f"Warning: Could not get gcloud token - {e}. Endpoint might be unsecured or require different auth.")
    auth_headers = None # Or handle error appropriately

agent_vllm = LlmAgent(
    model=LiteLlm(
        model=model_name_at_endpoint,
        api_base=api_base_url,
        # Pass authentication headers if needed
        #extra_headers=auth_headers
        # Alternatively, if endpoint uses an API key:
        # api_key="YOUR_ENDPOINT_API_KEY"
    ),
    name="vllm_agent",
    instruction="You are a helpful assistant running on a self-hosted vLLM endpoint.",
    # ... other agent parameters
)