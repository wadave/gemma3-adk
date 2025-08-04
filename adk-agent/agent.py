import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
import google.auth
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env into the environment

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
endpoint_id = os.getenv("VERTEX_AI_ENPOINT_ID")


def _get_auth_headers() -> dict[str, str]:
    """Gets the auth headers for the model garden endpoint."""
    creds, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {creds.token}",
    }


auth_headers = _get_auth_headers()
model = f"vertex_ai/openai/{endpoint_id}"  # fine tuned working with ADK


print("The current model is: {model}")

root_agent = LlmAgent(
    name="root_agent",
    model=LiteLlm(
        model=model,
    ),
    instruction=(
        """You are a helpful AI assistant designed to provide accurate and useful
        information."""
    ),
    description="Answers questions about math problems.",
)
