# Use Gemma3 on Vertex AI or GKE with ADK
This repo shows how to set up fine-tuned Gemma3 on Vertex AI or GKE, and use with ADK agents.

### Folder structure

```
├── agents
│   ├── gke-agent
│   │   ├── agent.py
│   │   └── __init__.py
│   └── vertexai-agent
│       ├── agent.py
│       └── __init__.py
├── notebooks
│   ├── deploy_gemma3_vllm_on_gke.ipynb
│   └── deploy_gemma3_vllm_on_vertex.ipynb
├── pyproject.toml
├── README.md
└── uv.lock
```

### Pre-requisites:

- [gcloud installed](https://cloud.google.com/sdk/docs/install)
- [kubectl installed](https://kubernetes.io/docs/tasks/tools/)
- [uv package installed](https://docs.astral.sh/uv/getting-started/installation/)      

### Deploy Gemma3 on GKE. 

Following the this notebook to deploy Gemma3 on GKE.
```
├── notebooks
   ├── deploy_gemma3_vllm_on_gke.ipynb
    
```


### Deploy Gemma3 on Vertex AI  

Following the this notebook to deploy Gemma3 on Vertex AI.
```
├── notebooks
    └── deploy_gemma3_vllm_on_vertex.ipynb
```

### Run ADK agents  

Go to `agents` folder, and follow the readme to run ADK agents.