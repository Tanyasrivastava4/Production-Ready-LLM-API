# model_handler.py
#import time
#import requests
#import os

# Environment variables
# SALAD_PUBLIC_URL: vLLM API server URL (localhost if same container)
#SALAD_PUBLIC_URL = os.getenv("SALAD_PUBLIC_URL", "http://localhost:8000/v1/completions")

#def generate_response(prompt, max_tokens):
 #   """
  #  Calls the real vLLM API server and returns text, token count, and latency
   # """
    #start = time.time()
   # try:
    #    payload = {
     #       "prompt": prompt,
      #      "max_tokens": max_tokens
      #  }
       # response = requests.post(SALAD_PUBLIC_URL, json=payload)
       # response.raise_for_status()
      #  data = response.json()
      #  text = data.get("text", "")
      #  tokens_generated = len(text.split())
    #except Exception as e:
     #   text = f"Error: {str(e)}"
      #  tokens_generated = 0

    #latency_ms = (time.time() - start) * 1000
    #return text, tokens_generated, latency_ms


import time
import os
import requests

ENV = os.getenv("ENV", "GPU")
SALAD_PUBLIC_URL = os.getenv("SALAD_PUBLIC_URL", "https://feta-coriander-4fybgc189fwlr18m.salad.cloud:8000/v1/completions")

def generate_response(prompt, max_tokens):
    start = time.time()
    if ENV == "GPU":
        try:
            payload = {"prompt": prompt, "max_tokens": max_tokens}
            resp = requests.post(SALAD_PUBLIC_URL, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            text = data.get("text", "")
            tokens_generated = len(text.split())
        except Exception as e:
            text = f"Error: {str(e)}"
            tokens_generated = 0
    else:
        text = f"Mocked response: {prompt}"
        tokens_generated = min(len(prompt.split()), max_tokens)
        time.sleep(0.05)
    latency_ms = (time.time() - start) * 1000
    return text, tokens_generated, latency_ms
