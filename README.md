# SOHMA Placeholder AI Model (Integration Test)

This is a minimal AI model API created for validating the end-to-end integration between:

Sokoban Game → SDK → AI Model → JSON Output

This version is **internal only** and intended for rapid integration testing.

---

## Purpose

- Validate JSON data flow from Unity SDK to AI model
- Return structured JSON output
- Derive at least one computed value from input (stress score)
- No production logic
- No real ML model (placeholder deterministic logic)

---

## Tech Stack

- FastAPI
- Uvicorn
- Python 3.10+

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/sohma-placeholder-api.git
cd sohma-placeholder-api
pip install -r requirements.txt
```

Run the API 

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Server runs on 

```bash
http://localhost:8000
```

# Endpoints

Health Check

```bash
GET /healthz
```

Returns: 

```bash
{"ok": true}
```

Predict Endpoint (Integration Test)

```bash
POST /predict
```

Example: 

```bash
curl -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d @sample_input.json
```

# What the Model Does

From Sokoban raw signals, it calculates:
- Interaction intensity
- Error rate
- Pause frequency
- Temporal instability
- Stress score (derived from intensity + error rate)

This allows us to test:
- SDK → API connection
- JSON schema compatibility
- Derived metric logic
- End-to-end data validation

  
