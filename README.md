# Gemma 3 on Vertex AI & GKE with ADK 🚀

This repository provides a comprehensive guide and all the necessary code to deploy a fine-tuned **Gemma 3** model on Google Cloud. You have two deployment options:
1.  **Google Kubernetes Engine (GKE)** using the high-performance **vLLM** inference server.
2.  **Vertex AI Model Garden & Endpoints** for a fully managed, serverless experience.

Once deployed, you can integrate your Gemma 3 model with intelligent agents built using the **Agent Development Kit (ADK)**.


### 📂 Folder Structure

```bash
├── agents
│   ├── Dockerfile
│   ├── gke-agent
│   │   ├── agent.py
│   │   ├── __init__.py
│   │   └── requirements.txt
│   ├── pyproject.toml
│   ├── README.md
│   ├── uv.lock
│   └── vertexai-agent
│       ├── agent.py
│       ├── __init__.py
│       └── requirements.txt
├── deployment
│   ├── common_util.py
│   ├── deploy_gemma3_vllm_on_gke.ipynb
│   ├── deploy_gemma3_vllm_on_gke.sh
│   ├── deploy_gemma3_vllm_on_vertex.ipynb
│   ├── deploy_gemma3_vllm_on_vertex.py
│   └── deploy_gemma3_vllm_on_vertex.sh
├── pyproject.toml
├── README.md
├── requirements.txt
└── uv.lock
```


### 🔧 Prerequisites

Before you begin, ensure you have the following tools installed and configured on your system (Please note Cloud Shell have these pre-installed):

* **Google Cloud SDK:** [Install gcloud CLI](https://cloud.google.com/sdk/docs/install)
    * *Make sure to authenticate by running `gcloud auth login` and `gcloud auth application-default login`.*
* **kubectl:** [Install kubectl](https://kubernetes.io/docs/tasks/tools/)
* **uv:** [Install uv](https://docs.astral.sh/uv/getting-started/installation/) (an extremely fast Python package installer)


### ⚙️ Setup

 **Clone the repository:**
```bash
    git clone <your-repo-url> 

    cd <your-repo-name>
```
--

### 🚀 Deployment Options

Follow one of the notebooks below to deploy your Gemma 3 model.

### Option 1: Deploy to Google Kubernetes Engine (GKE)

This approach uses **vLLM** to serve the Gemma 3 model on a GKE cluster, giving you full control over the serving environment and hardware.

➡️ **Follow the notebook:** [`deployment/deploy_gemma3_vllm_on_gke.ipynb`](./deployment/deploy_gemma3_vllm_on_gke.ipynb)

Alternatively, you can also deploy your model using the following command:
➡️ **Use the shell command:** [`deployment/deploy_gemma3_vllm_on_gke.sh`](./deployment/deploy_gemma3_vllm_on_gke.sh)

Under `deployment` directory:

Please create a .env file with your PROJECT_ID, REGION, MODEL_BUCKET, MODEL_NAME, MODEL_VERSION, CLUSTER_NAME, PROJECT_NUMBER, and KSA_NAME

Your model is saved in Google Cloud Storage bucket like this: 
```gs://{MODEL_BUCKET}/{MODEL_NAME}/{MODEL_VERSION}```
```bash
chmod u+x deploy_gemma3_vllm_on_gke.sh
uv run bash deploy_gemma3_vllm_on_gke.sh
```

### Option 2: Deploy to Vertex AI

This approach uses the **Vertex AI Model Garden** to deploy Gemma 3 to a **Vertex AI Endpoint**. This is a fully managed, auto-scaling solution that simplifies deployment and maintenance.

➡️ **Follow the notebook:** [`deployment/deploy_gemma3_vllm_on_vertex.ipynb`](./deployment/deploy_gemma3_vllm_on_vertex.ipynb)

Alternatively, you can also deploy your model using the following command:
➡️ **Use the shell command:** [`deployment/deploy_gemma3_vllm_on_vertex.sh`](./deployment/deploy_gemma3_vllm_on_vertex.sh)

Under `deployment` directory:
Please create a .env file with your PROJECT_ID, REGION, MODEL_BUCKET, MODEL_NAME, and

Your model is saved in Google Cloud Storage bucket like this: 
```gs://{MODEL_BUCKET}/{MODEL_NAME}/{MODEL_VERSION}```
```bash
chmod u+x deploy_gemma3_vllm_on_vertex.sh
uv run bash deploy_gemma3_vllm_on_vertex.sh
```


---

### 🤖 Run the ADK Agents

After successfully deploying your model using either GKE or Vertex AI, you can run the corresponding ADK agent to interact with it.

Navigate to the `agents` directory and follow the instructions in the README file there to start your agent.

```bash
cd agents
```
Inside the agents folder, you will find specific instructions for running the gke-agent or the vertexai-agent, depending on which deployment path you chose.
