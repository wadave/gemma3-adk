#!/bin/bash
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

# Fail on any error.
set -e

# Display commands being run.
set -x

# Set your project and environment variables
if [ -f "./.env" ]; then
  source ./.env
else
  echo "Please create a .env file with your PROJECT_ID, REGION, MODEL_BUCKET, MODEL_NAME, and MODEL_VERSION"
  exit 1
fi

# Execute the python script
python3 deploy_gemma3_vllm_on_vertex.py \
  --project-id="${PROJECT_ID}" \
  --region="${REGION}" \
  --model-bucket="${MODEL_BUCKET}" \
  --model-name="${MODEL_NAME}" \
  --model-version="${MODEL_VERSION}"

echo "Deployment script finished."