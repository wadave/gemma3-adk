

# Running the ADK Agents 🤖

Before proceeding, ensure you have already deployed your Gemma 3 model to either GKE or Vertex AI by following one of the primary notebooks.

The instructions below correspond to the deployment option you chose.

---

## Option 1: Agent for Gemma 3 on GKE

These steps will connect an ADK agent to the Gemma 3 model you deployed on a GKE cluster.

First, navigate to the correct agent directory:
```bash
cd agents/gke-agent

```
1. Set Up Environment Variables

Create a file named `.env` inside the gke-agent directory. This file will configure the agent to communicate with your local, port-forwarded model endpoint.

.env file content:

```

GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_API_KEY=YOUR_VALUE_HERE
GOOGLE_CLOUD_PROJECT= 
GOOGLE_CLOUD_LOCATION= 
MODEL_NAME = 
MODEL_VERSION= 
```

2. Connect to the GKE Service 

To allow your local machine to communicate with the model service running on GKE, you need to open a secure tunnel using kubectl port-forward.

➡️ Open a new, dedicated terminal window and run the following commands. You must keep this terminal open while you use the agent. 

Open a terminal
```
# Authenticate with your GKE cluster
# Exmaple: gcloud container clusters get-credentials gke-gemma-cluster-test --location us-central1
gcloud container clusters get-credentials <YOUR_CLUSTER_NAME> --location <YOUR_REGION>

# Forward the service port 8000 to your local machine
kubectl port-forward service/llm-service 8000:8000
```

You should see a message confirming the forwarding.

3. Run the ADK Agent 

➡️ Open another terminal window, navigate back to the `agents` directory, and start the ADK web server.

 ```
 uv run adk web --port 8001
```
You can now access your agent's UI or API, which is running on http://localhost:8001.



## Option 2: Agent for Gemma 3 on Vertex AI 

These steps will connect an ADK agent to the Gemma 3 model you deployed on a Vertex AI Endpoint.

First, navigate to the correct agent directory:

Bash
```
cd agents/vertexai-agent
```

1. Set Up Environment Variables
Create a file named `.env` inside the vertexai-agent directory. This file configures the agent with your Google Cloud project and Vertex AI endpoint details.

.env file with following keys:
```
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_API_KEY=YOUR_VALUE_HERE
GOOGLE_CLOUD_PROJECT= 
GOOGLE_CLOUD_LOCATION= 
VERTEX_AI_ENPOINT_ID = 
```
2. Run the ADK Agent 

In your terminal (back to `agents`directory), start the ADK web server.

 Under `agent` folder, run
 ```
 uv run adk web --port 8002
