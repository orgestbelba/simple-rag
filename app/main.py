from fastapi import FastAPI
import app.models

app = FastAPI(title="Simple RAG (bootstrap)")

@app.get("/health")
def health():
    return {"status": "ok"}
