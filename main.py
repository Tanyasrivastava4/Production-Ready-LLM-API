# main.py
#from fastapi import FastAPI, HTTPException, Request
#from fastapi.responses import Response
#from prometheus_client import generate_latest
#from metrics import REQUEST_COUNT, ERROR_COUNT, TOKENS_GENERATED, VRAM_USAGE, LATENCY
#from model_handler import generate_response  # your actual model call
#import torch  # optional, for real GPU VRAM tracking
#import time
#import random

#app = FastAPI(title="Project11: Production-Ready LLM API")

# -----------------------------
# 1️⃣ Health check endpoint
# -----------------------------
#@app.get("/health")
#def health():
 #   return {"status": "healthy"}

# -----------------------------
# 2️⃣ Prometheus metrics endpoint
# -----------------------------
#@app.get("/metrics")
#def metrics():
 #   return Response(generate_latest(), media_type="text/plain")

# -----------------------------
# 3️⃣ Helper: Get GPU VRAM usage
# -----------------------------
#def get_vram_usage():
 #   try:
  #      return torch.cuda.memory_allocated()
   # except:
        # fallback if GPU not available
  #      return random.randint(2_000_000_000, 5_000_000_000)

# -----------------------------
# 4️⃣ Generate endpoint
# -----------------------------
#@app.post("/generate")
#def generate(payload: dict, request: Request):
 #   prompt = payload.get("prompt")
  #  max_tokens = payload.get("max_tokens", 50)

  #  if not prompt:
   #     ERROR_COUNT.inc()
    #    raise HTTPException(status_code=400, detail="Prompt is required")

    #REQUEST_COUNT.inc()  # increment total requests

    #start_time = time.time()
    #try:
        # Call your model and measure latency
     #   text, tokens_generated, _ = generate_response(prompt, max_tokens)

        # Update metrics
      #  TOKENS_GENERATED.inc(tokens_generated)
       # VRAM_USAGE.set(get_vram_usage())

       # return {
        #    "text": text,
         #   "latency_ms": round((time.time() - start_time) * 1000, 2),
         #   "tokens_generated": tokens_generated
        #}

    #except Exception as e:
     #   ERROR_COUNT.inc()
      #  raise HTTPException(status_code=500, detail=str(e))
   # finally:
    #    LATENCY.observe(time.time() - start_time)  # record latency








from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from prometheus_client import generate_latest
from metrics import REQUEST_COUNT, ERROR_COUNT, TOKENS_GENERATED, VRAM_USAGE, LATENCY
from model_handler import generate_response
import torch
import time
import random

app = FastAPI(title="Project11: Production-Ready LLM API")

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

def get_vram_usage():
    try:
        return torch.cuda.memory_allocated()
    except:
        return random.randint(2_000_000_000, 5_000_000_000)

@app.post("/generate")
def generate(payload: dict, request: Request):
    prompt = payload.get("prompt")
    max_tokens = payload.get("max_tokens", 50)

    if not prompt:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=400, detail="Prompt is required")

    REQUEST_COUNT.inc()

    start_time = time.time()
    try:
        text, tokens_generated, _ = generate_response(prompt, max_tokens)
        TOKENS_GENERATED.inc(tokens_generated)
        VRAM_USAGE.set(get_vram_usage())

        return {
            "text": text,
            "latency_ms": round((time.time() - start_time) * 1000, 2),
            "tokens_generated": tokens_generated
        }
    except Exception as e:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        LATENCY.observe(time.time() - start_time)
