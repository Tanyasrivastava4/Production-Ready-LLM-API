# metrics.py
from prometheus_client import Counter, Gauge, Histogram

# Total API requests
REQUEST_COUNT = Counter("requests_total", "Total API requests")

# Total errors
ERROR_COUNT = Counter("errors_total", "Total API errors")

# Tokens generated
TOKENS_GENERATED = Counter("tokens_total", "Total tokens generated")

# VRAM usage (GPU memory in bytes)
VRAM_USAGE = Gauge("vram_usage_bytes", "GPU VRAM usage")

# Latency in seconds
LATENCY = Histogram("latency_seconds", "API request latency")
