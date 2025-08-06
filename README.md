# Use Gemma3 on Vertex AI or GKE with ADK
This repo shows how to set up fine-tuned Gemma3 on Vertex AI or GKE, and use with ADK agents.

Folder structure

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

