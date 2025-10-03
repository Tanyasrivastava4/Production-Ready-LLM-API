
#!/bin/bash

# -----------------------------
# 1  ^o ^c  Set environment variables
# -----------------------------

# 1  ^o ^c  Set environment variables
# -----------------------------
export ENV=GPU
export SALAD_PUBLIC_URL="http://[::1]:8000/v1/completions"  # Use IPv6 localhost

# -----------------------------
# 2  ^o ^c  Install dependencies
# -----------------------------
pip install --upgrade pip
pip install -r requirements.txt

# -----------------------------
# 3  ^o ^c  Start vLLM API server in background
# -----------------------------
echo "Starting vLLM API server..."
python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.2 \
    --tensor-parallel-size 1 \
    --host :: \   # Bind to all IPv6 interfaces
    --port 8000 &

VLLM_PID=$!
echo "vLLM PID: $VLLM_PID"
sleep 10  # wait for vLLM to be ready

# -----------------------------
# 4  ^o ^c  Start FastAPI app in background
# -----------------------------
echo "Starting FastAPI server..."
uvicorn main:app --host :: --port 8001 &
FASTAPI_PID=$!
echo "FastAPI PID: $FASTAPI_PID"

# -----------------------------
# 5  ^o ^c  Wait for both processes
# -----------------------------
wait $VLLM_PID $FASTAPI_PID
