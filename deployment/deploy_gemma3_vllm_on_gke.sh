#!/bin/bash

# Copyright 2025 Google LLC
# https://github.com/GoogleCloudPlatform/accelerated-platforms/tree/main/use-cases/inferencing/serving/vllm/gcsfuse
# https://github.com/kenthua/gke/blob/main/inf-gw-lab/gemma-3-1b-ft.yaml.tmpl
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

# This script is converted from the notebook notebooks/deploy_gemma3_vllm_on_gke copy.ipynb.

# --- Prequisites ---
# 1. Install Google Cloud CLI: https://cloud.google.com/sdk/docs/install-sdk
# 2. Install kubectl.
# 3. Create a .env file in the same directory as this script with the following variables:
#
#    PROJECT_ID=<your-gcp-project-id>
#    REGION=<your-gcp-region>
#    KSA_NAME=<your-kubernetes-service-account-name> # In this example, we use "vllm-ksa" or any name you prefer
#    PROJECT_NUMBER=<your-gcp-project-number>
#    CLUSTER_NAME=<your-gke-cluster-name>
#    MODEL_BUCKET=<your-gcs-bucket-name>
#    MODEL_NAME=<your-model-name>
#    MODEL_VERSION=<your-model-version>
#
# --- Usage ---
#
# Make the script executable:
# chmod +x notebooks/deploy_gemma3_vllm_on_gke.sh
#
# Run the script:
# ./notebooks/deploy_gemma3_vllm_on_gke.sh

# It's recommended to run this script in a clean environment.
# If you have a .env file, source it before running the script.
# For example:
# set -a; source .env; set +a

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

# Set up gcloud
gcloud config set project ${PROJECT_ID}
gcloud services enable container.googleapis.com

echo "Creating cluster: ${CLUSTER_NAME}"

gcloud container clusters create ${CLUSTER_NAME} \
    --project=${PROJECT_ID} \
    --region=${REGION} \
    --subnetwork="default" \
    --workload-pool=${PROJECT_ID}.svc.id.goog \
    --release-channel=rapid \
    --num-nodes=4 \
    --enable-shielded-nodes \
    --shielded-secure-boot \
    --shielded-integrity-monitoring \
    --addons=GcsFuseCsiDriver

gcloud container node-pools create gpupool \
    --accelerator=type=nvidia-l4,count=2,gpu-driver-version=latest \
    --project=${PROJECT_ID} \
    --location=${REGION} \
    --node-locations=${REGION}-a \
    --cluster=${CLUSTER_NAME} \
    --machine-type=g2-standard-24 \
    --num-nodes=1 \
    --shielded-secure-boot \
    --shielded-integrity-monitoring

gcloud container clusters get-credentials ${CLUSTER_NAME} --location ${REGION}

kubectl create serviceaccount ${KSA_NAME}

gcloud projects add-iam-policy-binding projects/${PROJECT_ID} \
    --role=roles/container.clusterViewer \
    --member=principal://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${PROJECT_ID}.svc.id.goog/subject/ns/default/sa/${KSA_NAME} \
    --condition=None

gcloud storage buckets add-iam-policy-binding gs://${MODEL_BUCKET} \
    --role=roles/storage.objectViewer \
    --member=principal://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${PROJECT_ID}.svc.id.goog/subject/ns/default/sa/${KSA_NAME} \
    --condition=None

V_MODEL_BUCKET=${MODEL_BUCKET}
V_MODEL_NAME=${MODEL_NAME}
V_MODEL_VERSION=${MODEL_VERSION}
V_KSA=${KSA_NAME}

cat << EOF > vllm-3-1b-it-ft.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-gemma3-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gemma-server
  template:
    metadata:
      labels:
        app: gemma-server
      annotations:
        gke-gcsfuse/volumes: "true"
    spec:
      containers:
      - name: inference-server
        args:
        - --model=/gcs/${V_MODEL_NAME}/${V_MODEL_VERSION}
        - --tensor-parallel-size=1
        - --host=0.0.0.0
        - --port=8000
        env:
        - name: VLLM_ATTENTION_BACKEND
          value: FLASHINFER
        image: vllm/vllm-openai:v0.8.5.post1
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /health
            port: 8000
            scheme: HTTP
          initialDelaySeconds: 240
          periodSeconds: 5
          successThreshold: 1
          timeoutSeconds: 1
        resources:
          requests:
            cpu: "2"
            memory: "25Gi"
            nvidia.com/gpu: "1"
          limits:
            cpu: "2"
            memory: "25Gi"
            nvidia.com/gpu: "1"
        volumeMounts:
        - mountPath: /dev/shm
          name: dshm
        - name: gcs-fuse-csi-ephemeral
          mountPath: /gcs
          readOnly: true
      nodeSelector:
        cloud.google.com/gke-accelerator: nvidia-l4
        cloud.google.com/gke-gpu-driver-version: latest
      serviceAccountName: ${V_KSA}
      tolerations:
      - key: "nvidia.com/gpu"
        operator: "Exists"
        effect: "NoSchedule"
      - key: "on-demand"
        value: "true"
        operator: "Equal"
        effect: "NoSchedule"
      volumes:
      - name: dshm
        emptyDir:
            medium: Memory
      - name: gcs-fuse-csi-ephemeral
        csi:
          driver: gcsfuse.csi.storage.gke.io
          volumeAttributes:
            bucketName: ${V_MODEL_BUCKET}
            mountOptions: "implicit-dirs,file-cache:enable-parallel-downloads:true,file-cache:max-parallel-downloads:-1"
            fileCacheCapacity: "20Gi"
            fileCacheForRangeRead: "true"
            metadataStatCacheCapacity: "-1"
            metadataTypeCacheCapacity: "-1"
            metadataCacheTTLSeconds: "-1"
---
apiVersion: v1
kind: Service
metadata:
  name: llm-service
spec:
  selector:
    app: gemma-server
  type: ClusterIP
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000

EOF

kubectl apply -f vllm-3-1b-it-ft.yaml
