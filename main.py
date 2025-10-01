# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import generate_latest
from metrics import REQUEST_COUNT, ERROR_COUNT, TOKENS_GENERATED, VRAM_USAGE, LATENCY
from model_handler import generate_response
import subprocess
import random

app = FastAPI(title="Project11: Production-Ready LLM API")

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}

# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

# Generate endpoint
@app.post("/generate")
def generate(payload: dict):
    prompt = payload.get("prompt")
    max_tokens = payload.get("max_tokens", 50)

    if not prompt:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=400, detail="Prompt is required")

    REQUEST_COUNT.inc()

    try:
        with LATENCY.time():
            text, tokens_generated, latency_ms = generate_response(prompt, max_tokens)

        TOKENS_GENERATED.inc(tokens_generated)

        # Optional: mock VRAM usage for demo, can be replaced with GPU VRAM tracking
        VRAM_USAGE.set(random.randint(2_000_000_000, 5_000_000_000))  # bytes

        return {
            "text": text,
            "latency_ms": latency_ms
        }

    except Exception as e:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=500, detail=str(e))
