# Instructions to run the agents

## Option 1: Run the agent use Gemma deployed on GKE cluster

- For gke-agent, create a .env file with following keys:

```

GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_API_KEY=YOUR_VALUE_HERE
GOOGLE_CLOUD_PROJECT= 
GOOGLE_CLOUD_LOCATION= 
MODEL_NAME = 
MODEL_VERSION= 
```
- Forward port
Open a terminal
```
gcloud container clusters get-credentials {CLUSTER_NAME} --location {REGION}
kubectl port-forward service/llm-service 8000:8000
```
Keep the above terminal open, open another terminal and go to `agents` folder
 - Run ADK web
 ```
 uv run adk web --port 8001
```

## Option 2: Run the agent use Gemma deployed on Vertex AI endpoint

- For vertexai-agent, create a .env file with following keys:
```
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_API_KEY=YOUR_VALUE_HERE
GOOGLE_CLOUD_PROJECT= 
GOOGLE_CLOUD_LOCATION= 
VERTEX_AI_ENPOINT_ID = 
```
 - Run ADK web
 Under `agent` folder, run
 ```
 uv run adk web --port 8001
