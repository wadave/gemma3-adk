# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import datetime
import os
from typing import Tuple

from google.cloud import aiplatform
from dotenv import load_dotenv
import vertexai


def get_job_name_with_datetime(prefix: str) -> str:
    """Gets a job name by adding current time to prefix.

    Args:
      prefix: A string of job name prefix.

    Returns:
      A job name.
    """
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    job_name = f"{prefix}-{now}".replace("_", "-")
    return job_name


def get_deploy_source() -> str:
    """Gets deploy_source string based on running environment."""
    vertex_product = os.environ.get("VERTEX_PRODUCT", "")
    match vertex_product:
        case "COLAB_ENTERPRISE":
            return "notebook_colab_enterprise"
        case "WORKBENCH_INSTANCE":
            return "notebook_workbench"
        case _:
            # Legacy workbench, legacy colab, or other custom environments.
            return "notebook_environment_unspecified"


accelerator_type = "NVIDIA_L4"
machine_type = "g2-standard-24"
accelerator_count = 2


def deploy_model_vllm(
    model_name: str,
    model_id: str,
    publisher: str,
    publisher_model_id: str,
    machine_type: str,
    accelerator_type: str,
    accelerator_count: int,
    gpu_memory_utilization: float,
    max_model_len: int,
    use_dedicated_endpoint: bool,
    base_model_id: str = None,
    dtype: str = "auto",
    enable_trust_remote_code: bool = False,
    enforce_eager: bool = False,
    enable_lora: bool = False,
    enable_chunked_prefill: bool = False,
    enable_prefix_cache: bool = False,
    host_prefix_kv_cache_utilization_target: float = 0.0,
    max_loras: int = 1,
    max_cpu_loras: int = 8,
    max_num_seqs: int = 256,
    model_type: str = None,
    enable_llama_tool_parser: bool = False,
) -> Tuple[aiplatform.Model, aiplatform.Endpoint]:
    """Deploys trained models with vLLM into Vertex AI."""
    endpoint = aiplatform.Endpoint.create(
        display_name=f"{model_name}-endpoint",
        dedicated_endpoint_enabled=use_dedicated_endpoint,
    )

    if not base_model_id:
        base_model_id = model_id

    vllm_args = [
        "python",
        "-m",
        "vllm.entrypoints.api_server",
        "--host=0.0.0.0",
        "--port=8080",
        f"--model={model_id}",
        f"--tensor-parallel-size={accelerator_count}",
        "--swap-space=16",
        f"--gpu-memory-utilization={gpu_memory_utilization}",
        f"--max-model-len={max_model_len}",
        f"--dtype={dtype}",
        f"--max-loras={max_loras}",
        f"--max-cpu-loras={max_cpu_loras}",
        f"--max-num-seqs={max_num_seqs}",
        "--disable-log-stats",
        "--enable-auto-tool-choice",
        "--tool-call-parser=pythonic",
    ]

    if enable_trust_remote_code:
        vllm_args.append("--trust-remote-code")
    if enforce_eager:
        vllm_args.append("--enforce-eager")
    if enable_lora:
        vllm_args.append("--enable-lora")
    if enable_chunked_prefill:
        vllm_args.append("--enable-chunked-prefill")
    if enable_prefix_cache:
        vllm_args.append("--enable-prefix-caching")
    if 0 < host_prefix_kv_cache_utilization_target < 1:
        vllm_args.append(
            f"--host-prefix-kv-cache-utilization-target={host_prefix_kv_cache_utilization_target}"
        )
    if model_type:
        vllm_args.append(f"--model-type={model_type}")
    if enable_llama_tool_parser:
        vllm_args.append("--enable-auto-tool-choice")
        vllm_args.append("--tool-call-parser=vertex-llama-3")

    env_vars = {
        "MODEL_ID": base_model_id,
        "DEPLOY_SOURCE": "notebook",
    }

    try:
        if HF_TOKEN:
            env_vars["HF_TOKEN"] = HF_TOKEN
    except NameError:
        pass

    VLLM_DOCKER_URI = "us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20250312_0916_RC01"
    model = aiplatform.Model.upload(
        display_name=model_name,
        serving_container_image_uri=VLLM_DOCKER_URI,
        serving_container_args=vllm_args,
        serving_container_ports=[8080],
        serving_container_predict_route="/generate",
        serving_container_health_route="/ping",
        serving_container_environment_variables=env_vars,
        serving_container_shared_memory_size_mb=(16 * 1024),
        serving_container_deployment_timeout=7200,
        model_garden_source_model_name=(
            f"publishers/{publisher}/models/{publisher_model_id}"
        ),
    )
    print(
        f"Deploying {model_name} on {machine_type} with {accelerator_count} {accelerator_type} GPU(s)."
    )
    model.deploy(
        endpoint=endpoint,
        machine_type=machine_type,
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
        deploy_request_timeout=3600,
        spot=False,
        system_labels={
            "NOTEBOOK_NAME": "model_garden_gemma3_deployment_on_vertex.ipynb",
            "NOTEBOOK_ENVIRONMENT": get_deploy_source(),
        },
    )
    print("endpoint_name:", endpoint.name)

    return model, endpoint


def main(args):
    """Deploys the Gemma 3 model to Vertex AI."""

    load_dotenv()

    PROJECT_ID = args.project_id or os.getenv("PROJECT_ID")
    REGION = args.region or os.getenv("REGION")
    MODEL_BUCKET = args.model_bucket or os.getenv("MODEL_BUCKET")
    MODEL_NAME = args.model_name or os.getenv("MODEL_NAME")
    MODEL_VERSION = args.model_version or os.getenv("MODEL_VERSION")

    GCS_MODEL_PATH = f"gs://{MODEL_BUCKET}/{MODEL_NAME}/{MODEL_VERSION}"

    aiplatform.init(project=PROJECT_ID, location=REGION)
    vertexai.init(project=PROJECT_ID, location=REGION)

    models, endpoints = {}, {}
    LABEL = "custom-deploy-1b"
    models[LABEL], endpoints[LABEL] = deploy_model_vllm(
        model_name=get_job_name_with_datetime(prefix="gemma3-serve"),
        model_id=GCS_MODEL_PATH,
        publisher="google",
        publisher_model_id="gemma3",
        machine_type=machine_type,
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
        gpu_memory_utilization=0.95,
        max_model_len=32768,
        use_dedicated_endpoint=False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", type=str, help="Google Cloud project ID.")
    parser.add_argument("--region", type=str, help="Google Cloud region.")
    parser.add_argument("--model-bucket", type=str, help="GCS bucket for the model.")
    parser.add_argument("--model-name", type=str, help="Name of the model.")
    parser.add_argument("--model-version", type=str, help="Version of the model.")
    args = parser.parse_args()
    main(args)
