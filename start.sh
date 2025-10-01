#!/bin/bash

# -----------------------------
# 1️⃣ Set environment variables
# -----------------------------
export ENV=GPU
export SALAD_PUBLIC_URL="http://[::1]:8000/v1/completions"  # IPv6 localhost format

# -----------------------------
# 2️⃣ Install dependencies
# -----------------------------
pip install --upgrade pip
pip install -r requirements.txt

# -----------------------------
# 3️⃣ Start vLLM API server in background
# -----------------------------
python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.2 \
    --tensor-parallel-size 1 \
    --host ::      \  # Bind to all IPv6 interfaces
    --port 8000 &

# Wait a few seconds for vLLM to initialize
sleep 10

# -----------------------------
# 4️⃣ Start FastAPI app
# -----------------------------
uvicorn main:app \
    --host ::      \  # Bind to all IPv6 interfaces
    --port 8001 \
    --reload \
    --workers 1
