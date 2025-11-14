from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.models import SessionLocal
from app.services.embeddings import embed_all_articles

app = FastAPI(
    title="Simple RAG Search",
    version="1.0.0",
    description="Search AI articles with semantic search"
)

@app.on_event("startup")
async def startup_event():
    """
    Enhancement: build in-memory Chroma index when the API starts.
    """
    db = SessionLocal()
    await embed_all_articles(db)

# Allow all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)