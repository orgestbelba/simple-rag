from fastapi import FastAPI

app = FastAPI(title="Simple RAG (bootstrap)")

@app.get("/health")
def health():
    return {"status": "ok"}
