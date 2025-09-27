from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"]
)

# Sample telemetry data (replace with your real dataset or JSON)
sample_data = {
    "apac": [
        {"latency_ms": 150, "uptime": 0.99},
        {"latency_ms": 170, "uptime": 0.98},
        {"latency_ms": 200, "uptime": 0.97}
    ],
    "emea": [
        {"latency_ms": 120, "uptime": 0.995},
        {"latency_ms": 160, "uptime": 0.992},
        {"latency_ms": 190, "uptime": 0.99}
    ]
}

@app.post("/latency")
async def latency_metrics(request: Request):
    payload = await request.json()
    regions = payload.get("regions", [])
    threshold_ms = payload.get("threshold_ms", 180)

    result = {}
    for region in regions:
        data = sample_data.get(region, [])
        latencies = [d["latency_ms"] for d in data]
        uptimes = [d["uptime"] for d in data]
        breaches = sum(1 for l in latencies if l > threshold_ms)

        if latencies:
            result[region] = {
                "avg_latency": np.mean(latencies),
                "p95_latency": np.percentile(latencies, 95),
                "avg_uptime": np.mean(uptimes),
                "breaches": breaches
            }
        else:
            result[region] = {
                "avg_latency": None,
                "p95_latency": None,
                "avg_uptime": None,
                "breaches": 0
            }

    return result
