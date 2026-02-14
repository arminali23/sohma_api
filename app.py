from fastapi import FastAPI, HTTPException
from inference_core import predict

app = FastAPI(title="SOHMA Placeholder Model API", version="0.1")

# Minimal smoke test
@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/echo")
def echo(payload: dict):
    return {"ok": True, "session_id": payload.get("session_id")}

# Integration test endpoint
@app.post("/predict")
def predict_endpoint(payload: dict):
    try:
        return predict(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))