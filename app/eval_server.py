# eval_server.py
from fastapi import FastAPI

app = FastAPI(title="Fake Evaluation Server")

@app.post("/evaluation")
def evaluation(payload: dict):
    print("✅ Received evaluation POST:", payload)
    return {"status": "ok"}
